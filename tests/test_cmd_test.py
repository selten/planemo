"""Module contains :class:`CmdTestTestCase` - integration tests for the ``test`` command."""
import os

from .test_utils import (
    assert_exists,
    CliTestCase,
    PROJECT_TEMPLATES_DIR,
    skip_unless_python_2_7,
    skip_if_environ,
    TEST_DATA_DIR,
)


class CmdTestTestCase(CliTestCase):
    """Integration tests for the ``test`` command."""

    @skip_if_environ("PLANEMO_SKIP_GALAXY_TESTS")
    def test_workflow_test_simple(self):
        """Test testing a simple workflow with Galaxy."""
        with self._isolate():
            random_lines = os.path.join(PROJECT_TEMPLATES_DIR, "demo", "randomlines.xml")
            cat = os.path.join(PROJECT_TEMPLATES_DIR, "demo", "cat.xml")
            test_artifact = os.path.join(TEST_DATA_DIR, "wf1.gxwf.yml")
            test_command = [
                "--verbose",
                "test",
                "--extra_tools", random_lines,
                "--extra_tools", cat,
                test_artifact,
            ]
            self._check_exit_code(test_command, exit_code=0)

    @skip_unless_python_2_7()
    def test_cwltool_tool_test(self):
        """Test testing a CWL tool with cwltool."""
        with self._isolate() as f:
            test_artifact = os.path.join(TEST_DATA_DIR, "int_tool.cwl")
            test_command = [
                "test",
                "--engine", "cwltool",
                test_artifact,
            ]
            self._check_exit_code(test_command, exit_code=0)
            assert_exists(os.path.join(f, "tool_test_output.json"))
