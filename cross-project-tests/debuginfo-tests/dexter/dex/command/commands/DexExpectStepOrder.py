# DExTer : Debugging Experience Tester
# ~~~~~~   ~         ~~         ~   ~~
#
# Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from dex.command.CommandBase import CommandBase
from dex.dextIR import LocIR
from dex.dextIR import ValueIR


class DexExpectStepOrder(CommandBase):
    """Expect the line every `DexExpectStepOrder` is found on to be stepped on
    in `order`. Each instance must have a set of unique ascending indices.

    DexExpectStepOrder(*order)

    See Commands.md for more info.
    """

    def __init__(self, *args, **kwargs):
        if not args:
            raise TypeError("Need at least one order number")

        if "on_line" in kwargs:
            try:
                on_line = kwargs.pop("on_line")
                self.on_line = int(on_line)
            except ValueError:
                raise ValueError(
                    "on_line value '{0}' cannot be parsed to an integer".format(on_line)
                )
        self.sequence = [int(x) for x in args]
        super(DexExpectStepOrder, self).__init__()

    @staticmethod
    def get_name():
        return __class__.__name__

    def get_line(self):
        return self.on_line if hasattr(self, "on_line") else self.lineno

    def eval(self, step_info):
        return {
            "DexExpectStepOrder": ValueIR(
                expression=str(step_info.current_location.lineno),
                value=str(step_info.step_index),
                type_name=None,
                error_string=None,
                could_evaluate=True,
                is_optimized_away=True,
                is_irretrievable=False,
            )
        }
