# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import benchexec.tools.template
import benchexec.result as result

import re

class Tool(benchexec.tools.template.BaseTool2):
    """
    Tool info for BTOR2C-Val: An SV-COMP Witness Validator for BTOR2C programs
    URL: https://gitlab.com/sosy-lab/software/btor2c-val
    """

    def executable(self, tool_locator):
        return tool_locator.find_executable("main.py")

    def name(self):
        return "btor2c-val"

    def cmdline(self, executable, options, task, rlimits):
        return [executable] + options + ["--program"] + [task.single_input_file]

    def get_value_from_output(self, output, identifier):
        status = result.RESULT_UNKNOWN
        for line in output:
            if "Validation result:" in line:
                # correctness cases
                if "unknown(invariant parse failed)" in line:
                    status = result.RESULT_UNKNOWN + "(invariant parse failed)"
                elif "unknown(no invariant)" in line:
                    status = result.RESULT_UNKNOWN + "(no invariant)"
                elif "true(valid invariant)" in line:
                    status = result.RESULT_TRUE_PROP
                elif "true(safe invariant)" in line:
                    status = result.RESULT_TRUE_PROP
                elif "true(inductive invariant)" in line:
                    status = result.RESULT_TRUE_PROP
                elif "unknown(invalid invariant)" in line:
                    status = result.RESULT_UNKNOWN + "(invalid invariant)"
                elif "unknown(unsafe invariant)" in line:
                    status = result.RESULT_UNKNOWN + "(unsafe invariant)"
                elif "unknown(not inductive invariant)" in line:
                    status = result.RESULT_UNKNOWN + "(not inductive invariant)"
                # violation cases
                elif "false" in line:
                    status = result.RESULT_FALSE_PROP
                elif "unknown(violation not reached)" in line:
                    status = result.RESULT_UNKNOWN + "(violation not reached)"
                # common cases
                elif "error" in line:
                    pattern = r"error(\([^)]+\))"
                    cause = str(re.search(pattern, line).group(1))
                    status = result.RESULT_ERROR + cause
                break
        return status
