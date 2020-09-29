######################################################################################################################
# Copyright (C) 2017-2020 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
Contains Combiner's executable item as well as support utilities.

:authors: A. Soininen (VTT)
:date:   2.4.2020
"""

import os
import pathlib
from PySide2.QtCore import QObject, QEventLoop, Slot, QThread
from ..executable_item_base import ExecutableItemBase
from ..helpers import shorten
from .item_info import ItemInfo
from .combiner_worker import CombinerWorker


class ExecutableItem(ExecutableItemBase, QObject):
    def __init__(self, name, logs_dir, cancel_on_error, logger):
        """
        Args:
            name (str): item's name
            logs_dir (str): path to the directory where logs should be stored
            cancel_on_error (bool): if True, revert changes on error and move on
            logger (LoggerInterface): a logger
        """
        ExecutableItemBase.__init__(self, name, logger)
        QObject.__init__(self)
        self._resources_from_downstream = list()
        self._logs_dir = logs_dir
        self._cancel_on_error = cancel_on_error
        self._worker = None
        self._worker_thread = None
        self._loop = None
        self._merge_succeeded = False

    @staticmethod
    def item_type():
        """Returns Combiner's type identifier string."""
        return ItemInfo.item_type()

    @classmethod
    def from_dict(cls, item_dict, name, project_dir, app_settings, specifications, logger):
        """See base class."""
        data_dir = pathlib.Path(project_dir, ".spinetoolbox", "items", shorten(name))
        logs_dir = os.path.join(data_dir, "logs")
        cancel_on_error = item_dict["cancel_on_error"]
        return cls(name, logs_dir, cancel_on_error, logger)

    def stop_execution(self):
        """Stops execution."""
        super().stop_execution()
        if self._loop:
            if self._loop.isRunning():
                self._loop.exit(-1)
            self._loop = None
        if self._worker:
            self._worker.deleteLater()
            self._worker = None
        if self._worker_thread:
            self._worker_thread.quit()
            self._worker_thread.wait()
            self._worker_thread = None

    def _execute_backward(self, resources):
        """See base class."""
        self._resources_from_downstream = resources.copy()
        return True

    @staticmethod
    def _urls_from_resources(resources):
        return [r.url for r in resources if r.type_ == "database"]

    def _execute_forward(self, resources):
        """See base class."""
        from_urls = self._urls_from_resources(resources)
        to_urls = self._urls_from_resources(self._resources_from_downstream)
        if not from_urls:
            self._logger.msg_warning.emit("No input database(s) available. Moving on...")
            return True
        elif not to_urls:
            self._logger.msg_warning.emit("No output database available. Moving on...")
            return True
        self._destroy_current_worker()
        self._loop = QEventLoop()
        self._worker = CombinerWorker(from_urls, to_urls, self._logs_dir, self._cancel_on_error, self._logger)
        self._worker_thread = QThread()
        self._worker.moveToThread(self._worker_thread)
        self._worker.finished.connect(self._handle_worker_finished)
        self._worker.finished.connect(self._loop.quit)
        self._worker_thread.started.connect(self._worker.do_work)
        self._worker_thread.start()
        loop_retval = self._loop.exec_()
        if loop_retval:
            # If retval is not 0, loop exited with nonzero return value. Should happen when
            # user stops execution
            self._logger.msg_error.emit(f"Combiner {self.name} stopped")
            return False
        else:
            self._logger.msg_success.emit(f"Executing Combiner {self.name} finished")
        return self._merge_succeeded

    def _handle_worker_finished(self):
        """Runs when Combiner worker has finished."""
        self._destroy_current_worker()
        self._merge_succeeded = True

    @Slot()
    def _destroy_current_worker(self):
        """Runs when starting execution and after worker has finished.
        Destroys current loop, worker and quits thread, if any.
        """
        if self._loop:
            self._loop.deleteLater()
            self._loop = None
        if self._worker:
            self._worker.deleteLater()
            self._worker = None
        if self._worker_thread:
            self._worker_thread.quit()
            self._worker_thread.wait()
            self._worker_thread = None
