"""
┌─────────────────────────────────────┐
│ Module defining measure constraints │
└─────────────────────────────────────┘

 Florian Dupeyron
 August 2020
 Revised February 2022
"""

class Constraint_None(Constraint_Object):
    def __init__(self):
        super().__init__("none")

    def __str__(self):
        return f"None"

    def _validate(self,v):
        return True

# ┌────────────────────────────────────────┐
# │ Boolean constraints                    │
# └────────────────────────────────────────┘

from .boolean import Constraint_Boolean


# ┌────────────────────────────────────────┐
# │ Numeric constraints                    │
# └────────────────────────────────────────┘

from .numeric import (
    Constraint_Below,
    Constraint_Above,
    Constraint_Tolerance,
    Constraint_Range
)

