"""
┌──────────────────────────────────────────────┐
│ Base class for measure constraint definition │
└──────────────────────────────────────────────┘

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

from abc         import ABC,abstractmethod
from dataclasses import dataclass, field, asdict
from typing      import Dict


# ┌────────────────────────────────────────┐
# │ Default constraints                    │
# └────────────────────────────────────────┘

@dataclass
class Constraint_Object:
    constraint_class: str = field(init=None)

    def validate(self,v):
        if v is None: return False
        else        : return bool(self._validate(v))

    @abstractmethod
    def _validate(self,v): pass


# ┌────────────────────────────────────────┐
# │ Constraint description                 │
# └────────────────────────────────────────┘

# constraint description object: Read/write from results
# file

@dataclass
class Constraint_Description:
    constraint_class: str
    options: Dict[str, any]

    @classmethod
    def from_constraint(cls, c: Constraint_Object):
        cnst_dict  = asdict(c)
        cnst_class = cnst_dict["constraint_class"]

        del cnst_dict["constraint_class"]

        return cls(
            constraint_class=cnst_class,
            options         = cnst_dict
        )
