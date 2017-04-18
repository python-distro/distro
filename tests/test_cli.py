import ast
import pytest
import subprocess
import sys
import distro


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
        command = [sys.executable, '-m', 'distro']
        desired_output = 'Name: ' + distro.name(pretty=True)
        distro_version = distro.version(pretty=True)
        distro_codename = distro.codename()
        desired_output += '\n' + 'Version: ' + distro_version
        desired_output += '\n' + 'Codename: ' + distro_codename
        desired_output += '\n'
        assert self._run(command) == desired_output

    def test_cli_json(self):
        command = [sys.executable, '-m', 'distro', '-j']
        assert ast.literal_eval(self._run(command)) == distro.info()
