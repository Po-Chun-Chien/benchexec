# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import logging
import benchexec.tools.template
import benchexec.result as result


class Tool(benchexec.tools.template.BaseTool2):
    """
    Tool info for Btor2-Val: A portfolio-based validator for Btor2
    URL: https://gitlab.com/sosy-lab/software/btor2-val
    """

    def executable(self, tool_locator):
        return tool_locator.find_executable("btor2-val", subdir="bin")

    def name(self):
        return "btor2-val"

    def cmdline(self, executable, options, task, rlimits):
        return [
            executable,
            *options,
            "--program",
            task.input_files[0],
            "--btor2",
            task.input_files[1],
        ]

    def determine_result(self, run):
        if run.was_timeout:
            return result.RESULT_TIMEOUT
        pattern = "Validation result:"
        for line in run.output:
            if pattern in line:
                line = line.split(pattern)
                if len(line) != 2:
                    continue
                status = line[1].strip()
                if status.startswith(result.RESULT_TRUE_PROP):
                    return result.RESULT_CLASS_TRUE
                if (
                    status.startswith(result.RESULT_FALSE_PROP)
                    or status.startswith(result.RESULT_UNKNOWN)
                    or status.startswith(result.RESULT_ERROR)
                ):
                    return status
                # correctness cases
        return result.RESULT_ERROR

    def get_value_from_output(self, output, identifier):
        match = None
        for line in output:
            if identifier in line:
                startPosition = line.find(f"{identifier}") + len(identifier)
                if match is None:
                    match = (
                        identifier
                        if startPosition == len(line)
                        else line[startPosition:].strip()
                    )
                else:
                    logging.warning(
                        "skipping repeated match for identifier '%s': '%s'",
                        identifier,
                        line,
                    )
        return match
