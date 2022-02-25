"""
┌──────────────────────────────────┐
│ Numeric constraints for measures │
└──────────────────────────────────┘

 Florian Dupeyron
 August 2020
 Revised February 2022

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
