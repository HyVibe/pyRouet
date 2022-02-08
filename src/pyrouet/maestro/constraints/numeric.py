"""
┌──────────────────────────────────┐
│ Numeric constraints for measures │
└──────────────────────────────────┘

 Florian Dupeyron
 August 2020
 Revised February 2022
"""

from pyrouet.maestro.objects.constraints import Constraint_Object


class Constraint_Below(Constraint_Object):
    def __init__(self, ref_value ):
        super().__init__("below")
        self.ref_value = ref_value

    def __str__(self):
        return f"<{self.ref_value}"

    def _validate(self,v):
        return v <= self.ref_value

    def data(self):
        d = super().data()
        d.update({
            "ref_value": float(self.ref_value)
        })
        return d

class Constraint_Above(Constraint_Object):
    def __init__(self, ref_value):
        super().__init__("above")
        self.ref_value = ref_value
    def __str__(self):
        return f">{self.ref_value}"

    def _validate(self,v):
        return v >= self.ref_value

    def data(self):
        d = super().data()
        d.update({
            "ref_value": float(self.ref_value)
        })
        return d

class Constraint_Tolerance(Constraint_Object):
    def __init__( self, ref_value, tolerance_pcent ):
        super().__init__("tolerance")
        self.ref_value       = ref_value
        self.tolerance_pcent = tolerance_pcent
    def __str__(self):
        return f"{self.ref_value} +-{self.tolerance_pcent}%"
    def _validate(self,v):
        return abs(v-self.ref_value)/(self.ref_value) < (self.tolerance_pcent/100)

    def data(self):
        d = super().data()
        d.update({
            "ref_value"       : float(self.ref_value),
            "tolerance_pcent" : float(self.tolerance_pcent)
        })
        return d

class Constraint_Range(Constraint_Object):
    def __init__( self, ref_min, ref_max ):
        super().__init__("range")
        self.ref_min = ref_min
        self.ref_max = ref_max
    def __str__(self):
        return f"min : {self.ref_min} max : {self.ref_max}"
    def _validate(self,v):
        return (v >= self.ref_min) and (v <= self.ref_max)

    def data(self):
        d = super().data()
        d.update({
            "ref_min" : float(self.ref_min),
            "ref_max" : float(self.ref_max)
        })

        return d

