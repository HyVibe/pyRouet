"""
┌──────────────────────────────────────┐
│ Various errors the maestro can throw │
└──────────────────────────────────────┘

 Florian Dupeyron
 February 2022

 Copyright (C) 2022, the Pyrouet project core team.
 
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License along
 with this program; if not, write to the Free Software Foundation, Inc.,
 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

# ┌────────────────────────────────────────┐
# │ Procedure errors                       │
# └────────────────────────────────────────┘

class Procedure_Error(Exception):
    def __init__(self, msg, path_stack = None):
        super().__init__(msg)

        self.path_stack = None
        if path_stack:
            # Ensure tuple type to break mutable
            # path stack if path_stack is a list
            self.path_stack = tuple(path_stack)

class Procedure_Abort_Error(Procedure_Error):
    def __init__(self, path_stack=None):
        super().__init__("Procedure aborted", path_stack)

class Procedure_Stop_Error(Procedure_Error):
    def __init__(self, path_stack=None):
        super().__init__("Procedure stopped", path_stack)

class Procedure_ChildFailed_Error(Procedure_Error):
    def __init__(self, path_stack=None):
        super().__init__("One of child item failed", path_stack)
