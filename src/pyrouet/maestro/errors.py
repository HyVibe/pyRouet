"""
┌──────────────────────────────────────┐
│ Various errors the maestro can throw │
└──────────────────────────────────────┘

 Florian Dupeyron
 February 2022
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

class Procedure_MissingUI_Error(Procedure_Error):
    def __init__(self, path_stack=None):
        super().__init__("Missing UI item")
