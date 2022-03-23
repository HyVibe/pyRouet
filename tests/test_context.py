"""
┌────────────────────────────────────────┐
│ Various tests around procedure context │
└────────────────────────────────────────┘

 Florian Dupeyron
 March 2022
"""

from pyrouet.maestro.procedure.ctx import Procedure_Context
from pyrouet.maestro.errors import ( Procedure_Error,
    Procedure_Abort_Error,
    Procedure_Stop_Error,
    Procedure_Constraint_Error
)

from pyrouet.maestro.procedure.step import (
    Step_Base,
    Step_Action,
    Step_Measure,
    Step_Measure_Transform
)

from pyrouet.maestro.constraints import (
    Constraint_Boolean
)

import logging
from threading import Event

from pprint import pprint

# ┌────────────────────────────────────────┐
# │ Tests around context values            │
# └────────────────────────────────────────┘

def test_values_clear():
    class Test_Measure(Step_Measure):
        """
        Generates a dumb value. Add the 'save_value' option to save
        into procedure context values.
        """
        def __init__(self, value, constraint, unit="", **kwargs):
            super().__init__(constraint, unit, **kwargs)
            self.value = value

        def _measure(self, ctx, path_stack, values):
            return self.value

    class Test_Values_Clear(Step_Measure):
        """
        Empties values from context. Returns wether the
        context values are empty or not

        Please note that this step is some hack for the sake
        of testing. Please **do not** use the clear() function
        otherwise. This may be removed in the future.
        """
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def _measure(self, ctx, path_stack, values):
            values.clear()
            return (not values.values)


    class Test_Values_IsEmpty(Step_Measure):
        """
        Checks wether the procedure values is empty or not
        """

        def __init__(self, constraint, **kwargs):
            super().__init__(
                constraint = constraint,
                unit       = ""
            )

        def _measure(self, ctx, path_stack, values):
            return (not values.values)
        
    proc = (
        ("test_values_empty", Test_Values_IsEmpty, {"constraint": Constraint_Boolean(True)}),
        ("save_value"       , Test_Measure       , {"value": 1.0, "save_value": True, "constraint": None}),
        ("test_non_empty"   , Test_Values_IsEmpty, {"constraint": Constraint_Boolean(False)}),
        ("clear_stuff"      , Test_Values_Clear  , {"constraint": Constraint_Boolean(True) }),
    )
    
    ctx          = Procedure_Context()
    res, errlist = ctx.procedure_run(proc)

    pprint(res)

    assert res.result == True

# ┌────────────────────────────────────────┐
# │ Tests around callbacks                 │
# └────────────────────────────────────────┘

def test_step_enter_leave_callbacks():
    class Dummy_Action(Step_Action):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def _impl(self, ctx, path_stack):
            pass # Some lazy action, heh!

    enter_callback_ok            = Event()
    enter_callback_ok            = Event()
    second_enter_callback_ok     = Event()
    leave_callback_ok            = Event()
    second_leave_callback_ok     = Event()

    def first_enter(pstack):
        print("first_enter()")
        enter_callback_ok.set()

    def second_enter(pstack):
        print("second_enter()")
        second_enter_callback_ok.set()

    def first_leave(pstack, result):
        print("first_leave()")

        assert result.step_id == "dummy1"
        assert result.result  == True

        leave_callback_ok.set()

    def second_leave(pstack, result):
        print("second_leave()")

        assert result.step_id == "dummy1"
        assert result.result  == True

        second_leave_callback_ok.set()

    ctx = Procedure_Context()
    ctx.register_step_enter_callback(first_enter )
    ctx.register_step_enter_callback(second_enter)
    ctx.register_step_leave_callback(first_leave )
    ctx.register_step_leave_callback(second_leave)


    proc = (
        ("dummy1", Dummy_Action, {},),
    )

    res,errlist = ctx.procedure_run(proc)
    assert res.result == True

    assert enter_callback_ok.is_set()
    assert second_enter_callback_ok.is_set() 
    assert leave_callback_ok.is_set()        
    assert second_leave_callback_ok.is_set() 

def test_procedure_enter_leave_callbacks():
    class Dummy_Action(Step_Action):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def _impl(self, ctx, path_stack):
            pass # Some lazy action, heh!

    enter_callback_ok            = Event()
    enter_callback_ok            = Event()
    second_enter_callback_ok     = Event()
    leave_callback_ok            = Event()
    second_leave_callback_ok     = Event()

    def first_enter(pstack):
        print("first_enter()")
        enter_callback_ok.set()

    def second_enter(pstack):
        print("second_enter()")
        second_enter_callback_ok.set()

    def first_leave(pstack, result):
        print("first_leave()")

        assert result.tests[0].step_id == "dummy1"
        assert result.result  == True

        leave_callback_ok.set()

    def second_leave(pstack, result):
        print("second_leave()")

        assert result.tests[0].step_id == "dummy1"
        assert result.result  == True

        second_leave_callback_ok.set()

    ctx = Procedure_Context()
    ctx.register_procedure_enter_callback(first_enter )
    ctx.register_procedure_enter_callback(second_enter)
    ctx.register_procedure_leave_callback(first_leave )
    ctx.register_procedure_leave_callback(second_leave)


    proc = (
        ("dummy1", Dummy_Action, {},),
        ("dummy2", Dummy_Action, {},),
    )

    res,errlist = ctx.procedure_run(proc)
    assert res.result == True

    assert enter_callback_ok.is_set()
    assert second_enter_callback_ok.is_set() 
    assert leave_callback_ok.is_set()        
    assert second_leave_callback_ok.is_set() 
