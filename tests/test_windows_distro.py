import distro._windows
import platform


class TestWindowsOverall(object):
    """Test a WindowsDistribution object created with default arguments."""

    def setup_method(self, test_method):
        self.win32_ver = ('', '', '', '')
        self.old_win32_ver = platform.win32_ver
        platform.win32_ver = lambda *_: self.win32_ver

        self.distro = distro._windows.get_distribution()

    def teardown_method(self, test_method):
        platform.win32_ver = self.old_win32_ver

    def _test_outcome(self, outcome):
        assert self.distro.id() == outcome.get('id', '')
        assert self.distro.name() == outcome.get('name', '')
        assert self.distro.name(pretty=True) == outcome.get('pretty_name', '')
        assert self.distro.version() == outcome.get('version', '')
        assert self.distro.version(pretty=True) == \
               outcome.get('pretty_version', '')
        assert self.distro.version(best=True) == \
               outcome.get('best_version', '')
        assert self.distro.like() == outcome.get('like', '')
        assert self.distro.codename() == outcome.get('codename', '')
        assert self.distro.major_version() == outcome.get('major_version', '')
        assert self.distro.minor_version() == outcome.get('minor_version', '')
        assert self.distro.build_number() == outcome.get('build_number', '')

    def test_windows_10(self):
        self.win32_ver = ('10', '10.0.14393', '', 'Multiprocessor Free')

        desired_outcome = {
            'id': 'windows',
            'name': 'Windows',
            'pretty_name': 'Windows 10.0.14393 (10)',
            'version': '10.0.14393',
            'pretty_version': '10.0.14393 (10)',
            'major_version': '10',
            'minor_version': '0',
            'build_number': '14393',
            'best_version': '10.0.14393',
            'codename': '10'
        }
        self._test_outcome(desired_outcome)

    def test_windows_8_1(self):
        self.win32_ver = ('8.1', '6.2.9600', '', 'Multiprocessor Free')

        desired_outcome = {
            'id': 'windows',
            'name': 'Windows',
            'pretty_name': 'Windows 6.2.9600 (8.1)',
            'version': '6.2.9600',
            'pretty_version': '6.2.9600 (8.1)',
            'major_version': '6',
            'minor_version': '2',
            'build_number': '9600',
            'best_version': '6.2.9600',
            'codename': '8.1'
        }
        self._test_outcome(desired_outcome)

    def test_windows_8(self):
        self.win32_ver = ('8', '6.2.9200', '', 'Multiprocessor Free')

        desired_outcome = {
            'id': 'windows',
            'name': 'Windows',
            'pretty_name': 'Windows 6.2.9200 (8)',
            'version': '6.2.9200',
            'pretty_version': '6.2.9200 (8)',
            'major_version': '6',
            'minor_version': '2',
            'build_number': '9200',
            'best_version': '6.2.9200',
            'codename': '8'
        }
        self._test_outcome(desired_outcome)

    def test_windows_7(self):
        self.win32_ver = ('7', '6.1.7601', 'SP1', 'Multiprocessor Free')

        desired_outcome = {
            'id': 'windows',
            'name': 'Windows',
            'pretty_name': 'Windows 6.1.7601 (7)',
            'version': '6.1.7601',
            'pretty_version': '6.1.7601 (7)',
            'major_version': '6',
            'minor_version': '1',
            'build_number': '7601',
            'best_version': '6.1.7601',
            'codename': '7'
        }
        self._test_outcome(desired_outcome)

    def test_windows_vista(self):
        self.win32_ver = ('Vista', '6.0.6002', 'SP2', 'Multiprocessor Free')

        desired_outcome = {
            'id': 'windows',
            'name': 'Windows',
            'pretty_name': 'Windows 6.0.6002 (Vista)',
            'version': '6.0.6002',
            'pretty_version': '6.0.6002 (Vista)',
            'major_version': '6',
            'minor_version': '0',
            'build_number': '6002',
            'best_version': '6.0.6002',
            'codename': 'Vista'
        }
        self._test_outcome(desired_outcome)

    def test_windows_xp(self):
        self.win32_ver = ('XP', '5.1.2600', 'SP2', 'Multiprocessor Free')

        desired_outcome = {
            'id': 'windows',
            'name': 'Windows',
            'pretty_name': 'Windows 5.1.2600 (XP)',
            'version': '5.1.2600',
            'pretty_version': '5.1.2600 (XP)',
            'major_version': '5',
            'minor_version': '1',
            'build_number': '2600',
            'best_version': '5.1.2600',
            'codename': 'XP'
        }
        self._test_outcome(desired_outcome)
