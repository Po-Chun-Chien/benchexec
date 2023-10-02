# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import benchexec.tools.template
import benchexec.result as result


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
        return [executable] + options + [task.single_input_file]

    def get_value_from_output(self, output, identifier):
        status = result.RESULT_UNKNOWN
        for line in output:
            if "Result:" in line:
                if "invalid-invariant" in line:
                    status = result.WITNESS_CATEGORY_WRONG + "(invalid invariant)"
                elif "no-invariant" in line:
                    status = result.WITNESS_CATEGORY_WRONG + "(no invariant)"
                elif "ok" in line:
                    status = result.WITNESS_CATEGORY_CORRECT
                elif "prop-bad" in line:
                    status = result.WITNESS_CATEGORY_WRONG + "(prop-bad)"
                elif "init-t-bad" in line:
                    status = result.WITNESS_CATEGORY_WRONG + "(init-t-bad)"
                elif "t-bad" in line:
                    status = result.WITNESS_CATEGORY_WRONG + "(t-bad)"
                elif "init-bad" in line:
                    status = result.WITNESS_CATEGORY_WRONG + "(init-bad)"
                elif "bad" in line:
                    status = result.WITNESS_CATEGORY_WRONG + "(bad)"
                elif "verifier-err" in line:
                    status = result.WITNESS_CATEGORY_ERROR + "(verifier-err)"
                elif "conflict" in line:
                    status = result.WITNESS_CATEGORY_ERROR + "(conflict)"
                break
        return status
