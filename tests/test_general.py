import ast
import os
import platform
import pytest
import subprocess
import sys
import distro

MODULE_DISTRO = distro._distro

skip_py26 = pytest.mark.skipif(sys.version_info <= (2, 7), reason='Python 2.6 does not support __main__.py')


class TestGeneral:
    def test_repr(self):
        # We test that the class name and the names of all instance attributes
        # show up in the repr() string.
        repr_str = repr(distro._distro)
        assert "Distribution" in repr_str
        for attr in MODULE_DISTRO.__dict__.keys():
            assert attr + '=' in repr_str

    @pytest.mark.skipif(platform.system() != 'Linux', reason='Only run this test on Linux.')
    def test_linux_distribution(self):
        assert distro.linux_distribution() == distro.distribution()
        assert distro.linux_distribution(True) == distro.distribution(True)


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

    @skip_py26
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

    @skip_py26
    def test_cli_json(self):
        command = [sys.executable, '-m', 'distro', '-j']
        assert ast.literal_eval(self._run(command)) == distro.info()


class TestGlobal:
    """Test the global module-level functions, and default values of their
    arguments.
    """

    def setup_method(self, test_method):
        pass

    def test_global(self):
        # Because the module-level functions use the module-global
        # Distribution instance, it would influence the tested
        # code too much if we mocked that in order to use the distro
        # specific release files. Instead, we let the functions use
        # the release files of the distro this test runs on, and
        # compare the result of the global functions with the result
        # of the methods on the global LinuxDistribution object.

        def _test_consistency(function, kwargs=None):
            kwargs = kwargs or {}
            method_result = getattr(MODULE_DISTRO, function)(**kwargs)
            function_result = getattr(distro, function)(**kwargs)
            assert method_result == function_result

        if platform.system() == 'Linux':
            kwargs = {'full_distribution_name': True}
            _test_consistency('linux_distribution', kwargs)
            kwargs = {'full_distribution_name': False}
            _test_consistency('linux_distribution', kwargs)

        kwargs = {'pretty': False}
        _test_consistency('name', kwargs)
        _test_consistency('version', kwargs)
        _test_consistency('info', kwargs)

        kwargs = {'pretty': True}
        _test_consistency('name', kwargs)
        _test_consistency('version', kwargs)
        _test_consistency('info', kwargs)

        kwargs = {'best': False}
        _test_consistency('version', kwargs)
        _test_consistency('version_parts', kwargs)
        _test_consistency('major_version', kwargs)
        _test_consistency('minor_version', kwargs)
        _test_consistency('build_number', kwargs)
        _test_consistency('info', kwargs)

        kwargs = {'best': True}
        _test_consistency('version', kwargs)
        _test_consistency('version_parts', kwargs)
        _test_consistency('major_version', kwargs)
        _test_consistency('minor_version', kwargs)
        _test_consistency('build_number', kwargs)
        _test_consistency('info', kwargs)

        _test_consistency('id')
        _test_consistency('like')
        _test_consistency('codename')
        _test_consistency('info')
