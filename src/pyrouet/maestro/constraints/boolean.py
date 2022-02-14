"""
┌──────────────────────────────────┐
│ Boolean constraints for measures │
└──────────────────────────────────┘

 Florian Dupeyron
 August 2020
 Revised February 2022
"""

from pyrouet.maestro.objects.constraints import Constraint_Object
from dataclasses                         import dataclass, field


@datalcass
class Constraint_Boolean(Constraint_Object):
    name = "boolean"
    ref_value: any

    def _validate(self,v):
        return v == self.ref_value

#class Constraint_Boolean(Constraint_Object):
#    def __init__( self, ref_value ):
#        super().__init__("boolean")
#        self.ref_value = ref_value
#
#    def _validate(self,v):
#        return v == self.ref_value
#    def __str__(self):
#        return f"{self.ref_value}"
#        
#    def data(self):
#        d = super().data()
#        d.update({
#            "ref_value" : bool(self.ref_value)
#        })
#        return d
#
#
