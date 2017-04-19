import ast
import os
import pytest
import subprocess
import sys
import distro

MODULE_DISTRO = distro._distro


@pytest.mark.skipif(sys.version_info <= (2, 7), reason='Python 2.6 does not support __main__.py')
class TestCli:
    def _parse(self, command):
        sys.argv = command.split()
        distro.main()

    def _run(self, command):
        stdout, _ = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).communicate()
        # Need to decode or we get bytes in Python 3.x
        return stdout.decode('utf-8')

    def test_cli_for_coverage_yuch(self):
        self._parse('distro')
        self._parse('distro -j')

    def test_cli(self):
        sep = os.linesep
        command = [sys.executable, '-m', 'distro']
        desired_output = 'Name: ' + distro.name(pretty=True)
        distro_version = distro.version(pretty=True)
        distro_codename = distro.codename()
        desired_output += sep + 'Version: ' + distro_version
        desired_output += sep + 'Codename: ' + distro_codename
        desired_output += sep
        assert self._run(command) == desired_output

    def test_cli_json(self):
        command = [sys.executable, '-m', 'distro', '-j']
        assert ast.literal_eval(self._run(command)) == distro.info()


class TestRepr:
    """Test the __repr__() method."""

    def test_repr(self):
        # We test that the class name and the names of all instance attributes
        # show up in the repr() string.
        repr_str = repr(distro._distro)
        assert "Distribution" in repr_str
        for attr in MODULE_DISTRO.__dict__.keys():
            assert attr + '=' in repr_str