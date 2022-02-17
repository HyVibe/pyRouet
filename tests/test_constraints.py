"""
┌──────────────────────────┐
│ Measure constraint tests │
└──────────────────────────┘

 Florian Dupeyron
 March 2021
"""

from pyrouet.maestro.constraints import (
    Constraint_Boolean,
    Constraint_Below,
    Constraint_Above,
    Constraint_Tolerance,
    Constraint_Range
)

def test_constraint_boolean():
    cnstr_bool_true = Constraint_Boolean(ref_value = True)
    assert     cnstr_bool_true.validate(True)
    assert not cnstr_bool_true.validate(False)

    cnstr_bool_false = Constraint_Boolean(ref_value = False)
    assert not cnstr_bool_false.validate(True)
    assert     cnstr_bool_false.validate(False)


def test_constraint_below():
    cnstr_below = Constraint_Below(ref_value = 1.0)

    assert     cnstr_below.validate(0.999999)
    assert not cnstr_below.validate(1.2)


def test_constraint_above():
    cnstr_above = Constraint_Above(ref_value = 1.0)

    assert not cnstr_above.validate(0.999999)
    assert     cnstr_above.validate(1.2)


def test_constraint_tolerance():
    cnstr_tolerance = Constraint_Tolerance(ref_value = 1.0, tolerance_pcent = 10.0)

    assert     cnstr_tolerance.validate(1.0 )
    assert     cnstr_tolerance.validate(1.09)
    assert     cnstr_tolerance.validate(1.09)
    assert not cnstr_tolerance.validate(1.2 )
