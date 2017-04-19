import distro._mac_os
import platform


class TestMacOSOverall(object):
    """Test a MacOSDistribution object created with default arguments."""

    def setup_method(self, test_method):
        self.mac_ver = ('', '', '', '')
        self.old_mac_ver = platform.win32_ver
        platform.mac_ver = lambda *_: self.mac_ver

        self.distro = distro._mac_os.get_distribution()

    def teardown_method(self, test_method):
        platform.win32_ver = self.old_mac_ver

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

    def test_mac_osx_10_0(self):
        self.mac_ver = ('10.0.4', ('', '', ''), 'x86_64')

        desired_outcome = {
            'id': 'macos',
            'name': 'Mac OS',
            'pretty_name': 'Mac OS 10.0.4 (Cheetah)',
            'version': '10.0.4',
            'pretty_version': '10.0.4 (Cheetah)',
            'major_version': '10',
            'minor_version': '0',
            'build_number': '4',
            'best_version': '10.0.4',
            'codename': 'Cheetah'
        }
        self._test_outcome(desired_outcome)

    def test_mac_osx_10_1(self):
        self.mac_ver = ('10.1.5', ('', '', ''), 'x86_64')

        desired_outcome = {
            'id': 'macos',
            'name': 'Mac OS',
            'pretty_name': 'Mac OS 10.1.5 (Puma)',
            'version': '10.1.5',
            'pretty_version': '10.1.5 (Puma)',
            'major_version': '10',
            'minor_version': '1',
            'build_number': '5',
            'best_version': '10.1.5',
            'codename': 'Puma'
        }
        self._test_outcome(desired_outcome)

    def test_mac_osx_10_2(self):
        self.mac_ver = ('10.2.8', ('', '', ''), 'x86_64')

        desired_outcome = {
            'id': 'macos',
            'name': 'Mac OS',
            'pretty_name': 'Mac OS 10.2.8 (Jaguar)',
            'version': '10.2.8',
            'pretty_version': '10.2.8 (Jaguar)',
            'major_version': '10',
            'minor_version': '2',
            'build_number': '8',
            'best_version': '10.2.8',
            'codename': 'Jaguar'
        }
        self._test_outcome(desired_outcome)

    def test_mac_osx_10_3(self):
        self.mac_ver = ('10.3.9', ('', '', ''), 'x86_64')

        desired_outcome = {
            'id': 'macos',
            'name': 'Mac OS',
            'pretty_name': 'Mac OS 10.3.9 (Panther)',
            'version': '10.3.9',
            'pretty_version': '10.3.9 (Panther)',
            'major_version': '10',
            'minor_version': '3',
            'build_number': '9',
            'best_version': '10.3.9',
            'codename': 'Panther'
        }
        self._test_outcome(desired_outcome)
