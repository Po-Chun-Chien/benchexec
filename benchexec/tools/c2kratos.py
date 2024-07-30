# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import benchexec.tools.template
from benchexec.tools.sv_benchmarks_util import get_data_model_from_task, ILP32, LP64


class Tool(benchexec.tools.template.BaseTool2):
    """
    Tool info for c2kratos: A translator from C to K2 programs
    """

    def executable(self, tool_locator):
        return tool_locator.find_executable("c2kratos.py", subdir="tools")

    def name(self):
        return "C2Kratos"

    def project_url(self):
        return "https://kratos.fbk.eu/"

    def cmdline(self, executable, options, task, rlimits):
        assert task.options.get("language") == "C"
        options += ["--svcomp-spec", task.property_file]
        data_model = get_data_model_from_task(task, {ILP32: "32", LP64: "64"})
        if data_model and "--bitvectors" not in options:
            options += ["--bitvectors", data_model]
        return [executable, task.single_input_file, *options]
