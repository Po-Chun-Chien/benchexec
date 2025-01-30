# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import benchexec.result as result
import benchexec.tools.template


class Tool(benchexec.tools.template.BaseTool2):
    def executable(self, tool_locator):
        return tool_locator.find_executable("btor2-select", subdir="bin")

    def name(self):
        return "Btor2-Select"

    def project_url(self):
        return "https://gitlab.com/sosy-lab/software/btor2-select"

    def cmdline(self, executable, options, task, rlimits):
        return [executable] + [task.single_input_file] + options

    def determine_result(self, run):
        RES_PREFIX = "[INFO] Verification result: "
        for line in run.output[::-1]:
            if line.startswith(RES_PREFIX):
                res_str = line[len(RES_PREFIX) :]
                if res_str.startswith("true"):
                    return result.RESULT_TRUE_PROP
                if res_str.startswith("false"):
                    return result.RESULT_FALSE_PROP
                if res_str.startswith("unknown"):
                    return result.RESULT_UNKNOWN
        return result.RESULT_ERROR
