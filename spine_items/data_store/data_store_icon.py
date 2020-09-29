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
Module for data store icon class.

:authors: M. Marin (KTH), P. Savolainen (VTT)
:date:   4.4.2018
"""

from PySide2.QtGui import QColor
from spine_items.graphics_items import ProjectItemIcon


class DataStoreIcon(ProjectItemIcon):
    def __init__(self, toolbox, x, y, project_item, icon):
        """Data Store icon for the Design View.

        Args:
            toolbox (ToolBoxUI): QMainWindow instance
            x (float): Icon x coordinate
            y (float): Icon y coordinate
            project_item (ProjectItem): Item
            icon (str): icon resource path
        """
        super().__init__(
            toolbox, x, y, project_item, icon, icon_color=QColor("#cc33ff"), background_color=QColor("#f9e6ff")
        )

    def mouseDoubleClickEvent(self, e):
        """Opens Spine database editor when this Data Store icon is double-clicked.

        Args:
            e (QGraphicsSceneMouseEvent): Event
        """
        super().mouseDoubleClickEvent(e)
        self._project_item.open_ds_form()
