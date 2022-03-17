"""
┌──────────────────────────┐
│ Measure constraint tests │
└──────────────────────────┘

 Florian Dupeyron
 March 2021
"""

from pyrouet.maestro.objects.constraints import (
    Constraint_Description
)

from pyrouet.maestro.constraints import (
    Constraint_None,

    Constraint_Boolean,
    Constraint_Below,
    Constraint_Above,
    Constraint_Tolerance,
    Constraint_Range
)

def test_constraint_none():
    cnstr_none = Constraint_None()

    assert cnstr_none.validate("Coucou")
    assert cnstr_none.validate(-2.42424242)

    assert not cnstr_none.validate(None)


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


def test_constraint_range():
    cnstr_range = Constraint_Range(ref_min = 2.0, ref_max = 3.0)
    assert     cnstr_range.validate(2.2     )
    assert     cnstr_range.validate(2.596839)
    assert not cnstr_range.validate(4.0     )
    assert not cnstr_range.validate(1.9999  )


def test_constraint_description():
    cnstr_range = Constraint_Range(ref_min=2.0, ref_max=3.0)
    cnstr_desc  = Constraint_Description.from_constraint(cnstr_range)

    assert cnstr_desc.constraint_class   == "range"
    assert cnstr_desc.options["ref_min"] == 2.0
    assert cnstr_desc.options["ref_max"] == 3.0


