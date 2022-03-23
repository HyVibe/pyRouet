"""
┌───────────────────────────────────────┐
│ Procedure execution context managment │
└───────────────────────────────────────┘

 Florian Dupeyron
 September 2020
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

import traceback
import time
import logging

from typing      import List, Dict
from collections import OrderedDict
from dataclasses import dataclass, field

from pyrouet.maestro.procedure.step import (
    Step_Base,
    Step_Action
)

from pyrouet.maestro.objects.results import (
    Result_Procedure,
    Result_Container,
    Result_Action,
    Result_Measure
)

from pyrouet.maestro.errors import (
    Procedure_Error,
    Procedure_Abort_Error,
    Procedure_Stop_Error
)

# ┌────────────────────────────────────────┐
# │ Procedure context values               │
# └────────────────────────────────────────┘

class Procedure_Context_Values:
    def __init__(self):
        self.values = dict()

    def clear(self):
        """
        Clear the stored values
        """
        self.values = dict()

    def set(self, path_stack, v):
        """
        Sets a stored value.
        """
        key = ".".join(path_stack)
        self.values[key] = v

    def get(self, key, path_stack):
        """
        Returns a stored value, returns KeyError if
        not found.

        A ^ in the key string is replaced by the 
        current subprocedure path, suffixed with a separator.
        For example, if the current step has a path corresponding
        to audio.test_actuatorL.measure_rms,
        a ^ in the key string will be replaced
        by "audio.test_actuatorL." (WITH A DOT!!!).
        So the initialization options for the measure could look like:

        ("measure_rms", Signal_RMS_Measure, {"from": "^record"})

        That will be expanded to:

        ("measure_rms", Signal_RMS_Measure, {"from": "audio.test_actuatorL.record"})

        if at the root procedure, no dot is put.
        """
        path_subproc = ".".join(path_stack[:-1])
        return self.values[key.replace("^", path_subproc + ("." if path_subproc else ""))]


@dataclass
class Procedure_Context_Errors:
    errors: List[Exception] = field(default_factory = list)
    
    def register(self, path_stack: List[str], err: Exception):
        self.errors.append( (tuple(path_stack), err,) )


# ┌────────────────────────────────────────┐
# │ Procedure context                      │
# └────────────────────────────────────────┘

class Procedure_Context:
    def __init__(self):
        self.log                              = logging.getLogger(__file__)

        # ───────────── Callback sets ──────────── #

        self.on_step_enter_callbacks          = set()
        self.on_step_leave_callbacks          = set()

        self.on_procedure_enter_callbacks     = set()
        self.on_procedure_leave_callbacks     = set()


    # ┌────────────────────────────────────────┐
    # │ Callback managment                     │
    # └────────────────────────────────────────┘

    def register_step_enter_callback(self,clbk):
        self.on_step_enter_callbacks.add(clbk)

    def register_step_leave_callback(self,clbk):
        self.on_step_leave_callbacks.add(clbk)
    
    def register_procedure_enter_callback(self,clbk):
        self.on_procedure_enter_callbacks.add(clbk)

    def register_procedure_leave_callback(self,clbk):
        self.on_procedure_leave_callbacks.add(clbk)


    # ┌────────────────────────────────────────┐
    # │ Run functions                          │
    # └────────────────────────────────────────┘
    
    # ────────── Procedure execution ───────── #

    def procedure_run(self, proc: List[Step_Base],
                      id_: str=None,
                      path_stack: List[str] = None,
                      errlist: Procedure_Context_Errors=None,
                      values: Procedure_Context_Values=None):

        # Init context objects
        path_stack = path_stack or list()
        errlist    = errlist    or Procedure_Context_Errors()
        values     = values     or Procedure_Context_Values()

        # Init result object
        proc_res = Result_Container(step_id=id_) if id_ else Result_Procedure()

        # Add id to path_stack if any
        if id_:
            path_stack.append(id_)
        
        # Some log stuff
        if id_:
            self.log.info(f"Entering subprocedure {'.'.join(path_stack)}")
        else:
            self.log.info(f"Starting root procedure")

        # Get checklist item
        # TODO #

        # Callback
        for clbk in self.on_procedure_enter_callbacks:
            clbk(path_stack)

        try:
            for step in proc:
                # Get step info
                step_id  = step[0]
                step_def = step[1]
                res      = None

                self.log.debug(repr(step))

                # Run subprocedure
                if isinstance(step_def, tuple):
                    # Run procedure, should not throw any exception
                    res,_ = self.procedure_run( proc       = step_def,
                                                id_        = step_id,
                                                path_stack = path_stack,
                                                errlist    = errlist,
                                                values     = values )

                    # Store result for subprocedure
                    proc_res.tests.append(res)

                    if (not res.result) or (res.err is not None):
                        proc_res.result = False

                        if isinstance(res.err, Procedure_Abort_Error) or \
                            isinstance(res.err, Procedure_Stop_Error):
                                proc_res.err = res.err
                                break # Critical error

                # Run step
                elif issubclass(step_def, Step_Base):
                    step_args     = step[2]
                    step_instance = step_def(**step_args)

                    res,_ = self.step_run(
                        id_        = step_id,
                        step       = step_instance,
                        path_stack = path_stack,
                        errlist    = errlist,
                        values     = values
                    )

                    proc_res.tests.append(res)
                    if (not res.result) or (res.err is not None):
                        proc_res.result = False # Procedure is failed

                        if isinstance(res.err, Procedure_Abort_Error) or \
                            isinstance(res.err, Procedure_Stop_Error):
                                proc_res.err = res.err
                                break # Critical error
                        # For other exceptions
                        else:
                            if step_instance.critical: # Must. stop. procedure.
                                proc_res.err = Procedure_Stop_Error() # Request to stop procedure
                                break                                 # Break from loop

                            elif step_instance.break_if_error:
                                break # Just break from loop without storing error
                else:
                    raise TypeError(f"Uknown step type for step {step_id}: {step_def}:{type(step_def)}, step={step}")

            # All steps where executed without error!
            if proc_res.result is None:
                proc_res.result = True

        except Exception as exc:
            proc_res.result = False # Execution error

            proc_res.err    = exc
            errlist.register(path_stack, exc)
            proc_res.tests  = list() # Empty tests result list
            self.log.debug(traceback.format_exc())

        finally:
            # Procedure leave callback
            for clbk in self.on_procedure_leave_callbacks:
                clbk(path_stack, proc_res)

            # Some log
            if id_:
                self.log.info(f"Leaving subprocedure {'.'.join(path_stack)}")
            else:
                self.log.info(f"Leaving root procedure")

            # Remove id from path_stack if any
            if id_:
                path_stack.pop()

        return proc_res, errlist.errors


    # ──────────── Step execution ──────────── #

    def step_run(self, id_, step, path_stack=None, errlist=None, values=None):
        # Init context objects
        path_stack = path_stack or list()
        errlist    = errlist    or Procedure_Context_Errors()
        values     = values     or Procedure_Context_Values()

        # Append id to current path stack
        path_stack.append(id_)

        t_start = time.time()

        for clbk in self.on_step_enter_callbacks:
            clbk(path_stack)

        res = None
        try:
            # Should not throw any exception: caught in step.run!
            # If any exception is thrown by step.run, there will be caught
            # by the parent procedure_run() function or directly by the caller.
            res = step.run(self, path_stack, errlist, values)

            # Add step flags to result
            if res is not None:
                res.step_id = id_
                res.options.update(step.options_get())

            # TODO # Move in finally section with none result if error?
            for clbk in self.on_step_leave_callbacks:
                clbk(path_stack,res)

        finally:
            path_stack.pop() # Remove name from queue
            step.clean()     # Clean step data

        return res, errlist.errors
