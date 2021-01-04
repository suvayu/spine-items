######################################################################################################################
# Copyright (C) 2017-2020 Spine project consortium
# This file is part of Spine Items.
# Spine Items is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
The ExporterFactory class.

:author: M. Marin (KTH)
:date:   15.4.2020
"""

from spinetoolbox.project_item.project_item_factory import ProjectItemFactory
from .gdx_exporter import GdxExporter
from .gdx_exporter_icon import GdxExporterIcon
from .widgets.add_gdx_exporter_widget import AddGdxExporterWidget
from .widgets.gdx_exporter_properties import GdxExporterProperties


class GdxExporterFactory(ProjectItemFactory):
    @staticmethod
    def item_class():
        return GdxExporter

    @staticmethod
    def icon():
        return ":/icons/item_icons/database-export.svg"

    @staticmethod
    def make_add_item_widget(toolbox, x, y, specification):
        return AddGdxExporterWidget(toolbox, x, y, specification)

    @staticmethod
    def make_icon(toolbox):
        return GdxExporterIcon(toolbox, GdxExporterFactory.icon())

    @staticmethod
    def make_item(name, item_dict, toolbox, project):
        return GdxExporter.from_dict(name, item_dict, toolbox, project)

    @staticmethod
    def make_properties_widget(toolbox):
        """See base class."""
        return GdxExporterProperties(toolbox)

    @staticmethod
    def make_specification_menu(parent, index):
        raise NotImplementedError()

    @staticmethod
    def show_specification_widget(toolbox, specification=None):
        """See base class."""
        raise NotImplementedError()
