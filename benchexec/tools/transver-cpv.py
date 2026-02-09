# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import benchexec.tools.cpv
import benchexec.result as result


class Tool(benchexec.tools.cpv.Tool):
    """
    Tool info for TransVer-CPV
    """

    REQUIRED_PATHS = [
        "bin/",
        "cpv/",
        "transver/",
    ]

    def executable(self, tool_locator):
        return tool_locator.find_executable("transver-cpv", subdir="bin")

    def name(self):
        return "TransVer-CPV"

    def project_url(self):
        return "https://gitlab.com/sosy-lab/software/transver-cpv"

    def determine_result(self, run):
        if any(line.startswith("ERROR: TransVer failed") for line in run.output[::-1]):
            return result.RESULT_ERROR + "(TransVer failed)"
        return super().determine_result(run)
