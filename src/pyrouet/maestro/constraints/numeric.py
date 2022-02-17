"""
┌──────────────────────────────────┐
│ Numeric constraints for measures │
└──────────────────────────────────┘

 Florian Dupeyron
 August 2020
 Revised February 2022
"""

from pyrouet.maestro.objects.constraints import Constraint_Object
from dataclasses                         import dataclass,field,asdict

@dataclass
class Constraint_Below(Constraint_Object):
    constraint_class = "below"
    ref_value: float

    def _validate(self,v):
        return v <= self.ref_value


@dataclass
class Constraint_Above(Constraint_Object):
    constraint_class = "above"
    ref_value: float

    def _validate(self,v):
        return v >= self.ref_value


@dataclass
class Constraint_Tolerance(Constraint_Object):
    constraint_class = "tolerance"

    ref_value:       float
    tolerance_pcent: float

    def _validate(self,v):
        return abs(v-self.ref_value)/(self.ref_value) < (self.tolerance_pcent/100.0)


@dataclass
class Constraint_Range(Constraint_Object):
    constraint_class = "range"

    ref_min: float
    ref_max: float

    def _validate(self,v):
        return (v >= self.ref_min) and (v <= self.ref_max)
