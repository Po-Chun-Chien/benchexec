# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import logging

import benchexec.result
from benchexec.tools.sv_benchmarks_util import ILP32, LP64, get_data_model_from_task
from benchexec.tools.template import BaseTool2


class Tool(BaseTool2):
    """
    Tool info for liv.
    """

    REQUIRED_PATHS = ["liv", "lib", "bin", "actors"]

    def executable(self, tool_locator: BaseTool2.ToolLocator):
        return tool_locator.find_executable("liv", subdir="bin")

    def program_files(self, executable):
        return [executable] + self._program_files_from_executable(
            executable, self.REQUIRED_PATHS, parent_dir=True
        )

    def version(self, executable):
        return self._version_from_tool(executable)

    def name(self):
        return "liv"

    def cmdline(self, executable, options, task, rlimits):
        if task.property_file:
            options = options + ["--property", task.property_file]

        data_model_param = get_data_model_from_task(
            task, {ILP32: "ILP32", LP64: "LP64"}
        )

        if data_model_param and "--data-model" not in options:
            options += ["--data-model", data_model_param]

        self.options = options
        return [executable] + options + list(task.input_files_or_identifier)

    def determine_result(self, run):
        if run.was_timeout:
            return benchexec.result.RESULT_TIMEOUT
        if not run.output:
            return benchexec.result.RESULT_ERROR
        lastline = run.output[-1]
        if "true" in lastline:
            return benchexec.result.RESULT_TRUE_PROP
        elif "false" in lastline:
            return benchexec.result.RESULT_FALSE_PROP
        elif "unknown" in lastline:
            return benchexec.result.RESULT_UNKNOWN
        else:
            return benchexec.result.RESULT_ERROR

    def get_value_from_output(self, output, identifier):
        # search for the text in output and get its value,
        # search the first line, that starts with the searched text
        # warn if there are more lines (multiple statistics from sequential analysis?)
        match = None
        for line in output:
            if line.lstrip().startswith(identifier):
                startPosition = line.find(":") + 1
                endPosition = line.find("(", startPosition)
                if endPosition == -1:
                    endPosition = len(line)
                if match is None:
                    match = line[startPosition:endPosition].strip()
                else:
                    logging.warning(
                        "skipping repeated match for identifier '%s': '%s'",
                        identifier,
                        line,
                    )
        return match
