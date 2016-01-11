import os

import testtools

import ld
from ld import constants as const


RESOURCES = os.path.join('tests', 'resources')
DISTROS = os.path.join(RESOURCES, 'distros')
SPECIAL = os.path.join(RESOURCES, 'special')

RELATIVE_UNIXCONFDIR = const._UNIXCONFDIR.lstrip('/')
RELATIVE_OS_RELEASE = const._OS_RELEASE.lstrip('/')


class TestOSRelease(testtools.TestCase):

    def setUp(self):
        super(TestOSRelease, self).setUp()

    def test_rhel7_os_release(self):
        os_release = os.path.join(DISTROS, 'rhel7', 'etc', 'os-release')

        ldi = ld.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(ldi.id(), 'rhel')
        self.assertEqual(ldi.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            ldi.name(pretty=True),
            'Red Hat Enterprise Linux Server 7.0 (Maipo)')
        self.assertEqual(ldi.version(), '7.0')
        self.assertEqual(ldi.version(pretty=True), '7.0 (Maipo)')
        self.assertEqual(ldi.like(), 'fedora')
        self.assertEqual(ldi.codename(), 'Maipo')
        self.assertEqual(ldi.base(), 'fedora')

    def test_centos7_os_release(self):
        os_release = os.path.join(DISTROS, 'centos7', 'etc', 'os-release')

        ldi = ld.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(ldi.id(), 'centos')
        self.assertEqual(ldi.name(), 'CentOS Linux')
        self.assertEqual(ldi.name(pretty=True), 'CentOS Linux 7 (Core)')
        self.assertEqual(ldi.version(), '7')
        self.assertEqual(ldi.version(pretty=True), '7 (Core)')
        self.assertEqual(ldi.like(), 'rhel fedora')
        self.assertEqual(ldi.codename(), 'Core')
        self.assertEqual(ldi.base(), 'rhel')

    def test_opensuse42_os_release(self):
        os_release = os.path.join(DISTROS, 'opensuse42', 'etc', 'os-release')

        ldi = ld.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(ldi.id(), 'opensuse')
        self.assertEqual(ldi.name(), 'openSUSE Leap')
        self.assertEqual(ldi.name(pretty=True), 'openSUSE Leap 42.1 (x86_64)')
        self.assertEqual(ldi.version(), '42.1')
        self.assertEqual(ldi.version(pretty=True), '42.1')
        self.assertEqual(ldi.like(), 'suse')
        self.assertEqual(ldi.codename(), '')
        self.assertEqual(ldi.base(), 'suse')

    def test_fedora23_os_release(self):
        os_release = os.path.join(DISTROS, 'fedora23', 'etc', 'os-release')

        ldi = ld.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(ldi.id(), 'fedora')
        self.assertEqual(ldi.name(), 'Fedora')
        self.assertEqual(ldi.name(pretty=True), 'Fedora 23 (Twenty Three)')
        self.assertEqual(ldi.version(), '23')
        self.assertEqual(ldi.version(pretty=True), '23 (Twenty Three)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Twenty Three')
        self.assertEqual(ldi.base(), 'fedora')

    def test_ubuntu14_os_release(self):
        os_release = os.path.join(DISTROS, 'ubuntu14', 'etc', 'os-release')

        ldi = ld.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(ldi.id(), 'ubuntu')
        self.assertEqual(ldi.name(), 'Ubuntu')
        self.assertEqual(ldi.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(ldi.version(), '14.04')
        self.assertEqual(ldi.version(pretty=True), '14.04 (Trusty Tahr)')
        self.assertEqual(ldi.like(), 'debian')
        self.assertEqual(ldi.codename(), 'Trusty Tahr')
        self.assertEqual(ldi.base(), 'debian')

    def test_arch_os_release(self):
        os_release = os.path.join(DISTROS, 'arch', 'etc', 'os-release')

        ldi = ld.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(ldi.id(), 'arch')
        self.assertEqual(ldi.name(), 'Arch Linux')
        self.assertEqual(ldi.name(pretty=True), 'Arch Linux')
        self.assertEqual(ldi.version(), '')
        self.assertEqual(ldi.version(pretty=True), '')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), '')
        self.assertEqual(ldi.base(), 'arch')

    def test_debian8_os_release(self):
        os_release = os.path.join(DISTROS, 'debian8', 'etc', 'os-release')

        ldi = ld.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(ldi.id(), 'debian')
        self.assertEqual(ldi.name(), 'Debian GNU/Linux')
        self.assertEqual(ldi.name(pretty=True), 'Debian GNU/Linux 8 (jessie)')
        self.assertEqual(ldi.version(), '8')
        self.assertEqual(ldi.version(pretty=True), '8 (jessie)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'jessie')
        self.assertEqual(ldi.base(), 'debian')

    def test_slackware14_os_release(self):
        os_release = os.path.join(DISTROS, 'slackware14', 'etc', 'os-release')

        ldi = ld.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(ldi.id(), 'slackware')
        self.assertEqual(ldi.name(), 'Slackware')
        self.assertEqual(ldi.name(pretty=True), 'Slackware 14.1')
        self.assertEqual(ldi.version(), '14.1')
        self.assertEqual(ldi.version(pretty=True), '14.1')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), '')
        self.assertEqual(ldi.base(), 'slackware')


class TestLSBRelease(testtools.TestCase):

    @staticmethod
    def _mock_lsb_release_info():
        lsb_release_file = os.path.join(SPECIAL, 'lsb_release.ubuntu14.out')
        with open(lsb_release_file, 'r') as data:
            return ld.LinuxDistribution()._parse_lsb_release(data) or {}

    def test_lsb_release(self):
        ldi = ld.LinuxDistribution(True, 'non', 'non')
        ldi._lsb_release_info = self._mock_lsb_release_info()

        self.assertEqual(ldi.id(), 'ubuntu')
        self.assertEqual(ldi.name(), 'Ubuntu')
        self.assertEqual(ldi.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(ldi.version(), '14.04')
        self.assertEqual(ldi.version(pretty=True), '14.04 (trusty)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'trusty')
        self.assertEqual(ldi.base(), 'debian')


class TestDistRelease(testtools.TestCase):

    def setUp(self):
        super(TestDistRelease, self).setUp()

    def test_rhel7_release(self):
        distro_release = os.path.join(DISTROS, 'rhel7', 'etc',
                                      'redhat-release')

        ldi = ld.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(ldi.id(), 'redhat')
        self.assertEqual(ldi.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            ldi.name(pretty=True),
            'Red Hat Enterprise Linux Server 7.0 (Maipo)')
        self.assertEqual(ldi.version(), '7.0')
        self.assertEqual(ldi.version(pretty=True), '7.0 (Maipo)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Maipo')
        self.assertEqual(ldi.base(), 'rhel')
        self.assertEqual(ldi.version_parts(), ('7', '0', ''))

    def test_rhel6_release(self):
        distro_release = os.path.join(DISTROS, 'rhel6', 'etc',
                                      'redhat-release')

        ldi = ld.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(ldi.id(), 'redhat')
        self.assertEqual(ldi.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            ldi.name(pretty=True),
            'Red Hat Enterprise Linux Server 6.5 (Santiago)')
        self.assertEqual(ldi.version(), '6.5')
        self.assertEqual(ldi.version(pretty=True), '6.5 (Santiago)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Santiago')
        self.assertEqual(ldi.base(), 'rhel')
        self.assertEqual(ldi.version_parts(), ('6', '5', ''))

    def test_opensuse42_release(self):
        distro_release = os.path.join(DISTROS, 'opensuse42', 'etc',
                                      'SuSE-release')

        ldi = ld.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(ldi.id(), '')
        self.assertEqual(ldi.name(), 'openSUSE')
        self.assertEqual(ldi.name(pretty=True), 'openSUSE 42.1 (x86_64)')
        self.assertEqual(ldi.version(), '42.1')
        self.assertEqual(ldi.version(pretty=True), '42.1 (x86_64)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'x86_64')
        self.assertEqual(ldi.base(), '')
        self.assertEqual(ldi.major_version(), '42')
        self.assertEqual(ldi.minor_version(), '1')
        self.assertEqual(ldi.build_number(), '')

    def test_centos5_release(self):
        distro_release = os.path.join(DISTROS, 'centos5', 'etc',
                                      'centos-release')
        ldi = ld.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(ldi.id(), 'centos')
        self.assertEqual(ldi.name(), 'CentOS')
        self.assertEqual(ldi.name(pretty=True), 'CentOS 5.11 (Final)')
        self.assertEqual(ldi.version(), '5.11')
        self.assertEqual(ldi.version(pretty=True), '5.11 (Final)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Final')
        self.assertEqual(ldi.base(), 'rhel')
        self.assertEqual(ldi.major_version(), '5')
        self.assertEqual(ldi.minor_version(), '11')
        self.assertEqual(ldi.build_number(), '')

    def test_centos7_release(self):
        distro_release = os.path.join(DISTROS, 'centos7', 'etc',
                                      'centos-release')

        ldi = ld.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(ldi.id(), 'centos')
        self.assertEqual(ldi.name(), 'CentOS Linux')
        self.assertEqual(ldi.name(pretty=True), 'CentOS Linux 7.1.1503 (Core)')
        self.assertEqual(ldi.version(), '7.1.1503')
        self.assertEqual(ldi.version(pretty=True), '7.1.1503 (Core)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Core')
        self.assertEqual(ldi.base(), 'rhel')
        self.assertEqual(ldi.major_version(), '7')
        self.assertEqual(ldi.minor_version(), '1')
        self.assertEqual(ldi.build_number(), '1503')

    def test_fedora23_release(self):
        distro_release = os.path.join(DISTROS, 'fedora23', 'etc',
                                      'fedora-release')

        ldi = ld.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(ldi.id(), 'fedora')
        self.assertEqual(ldi.name(), 'Fedora')
        self.assertEqual(ldi.name(pretty=True), 'Fedora 23 (Twenty Three)')
        self.assertEqual(ldi.version(), '23')
        self.assertEqual(ldi.version(pretty=True), '23 (Twenty Three)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Twenty Three')
        self.assertEqual(ldi.base(), 'fedora')

    def test_oracle7_release(self):
        distro_release = os.path.join(DISTROS, 'oracle7', 'etc',
                                      'oracle-release')

        ldi = ld.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(ldi.id(), 'oracle')
        self.assertEqual(ldi.name(), 'Oracle Linux Server')
        self.assertEqual(ldi.name(pretty=True), 'Oracle Linux Server 7.1')
        self.assertEqual(ldi.version(), '7.1')
        self.assertEqual(ldi.version(pretty=True), '7.1')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), '')
        self.assertEqual(ldi.base(), 'rhel')

    def test_empty_release(self):
        distro_release = os.path.join(SPECIAL, 'empty-release')

        ldi = ld.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(ldi.id(), '')
        self.assertEqual(ldi.name(), '')
        self.assertEqual(ldi.name(pretty=True), '')
        self.assertEqual(ldi.version(), '')
        self.assertEqual(ldi.version(pretty=True), '')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), '')
        self.assertEqual(ldi.base(), '')

    def test_arch_release(self):
        distro_release = os.path.join(DISTROS, 'arch', 'etc', 'arch-release')

        ldi = ld.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(ldi.id(), 'arch')
        self.assertEqual(ldi.name(), '')
        self.assertEqual(ldi.name(pretty=True), '')
        self.assertEqual(ldi.version(), '')
        self.assertEqual(ldi.version(pretty=True), '')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), '')
        self.assertEqual(ldi.base(), 'arch')

    def test_exherbo_release(self):
        distro_release = os.path.join(DISTROS, 'exherbo', 'etc',
                                      'exherbo-release')
        # TODO: This release file is currently empty and should be completed.

        ldi = ld.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(ldi.id(), 'exherbo')
        self.assertEqual(ldi.name(), '')
        self.assertEqual(ldi.name(pretty=True), '')
        self.assertEqual(ldi.version(), '')
        self.assertEqual(ldi.version(pretty=True), '')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), '')
        self.assertEqual(ldi.base(), 'exherbo')

    def test_slackware14_release(self):
        distro_release = os.path.join(DISTROS, 'slackware14', 'etc',
                                      'slackware-version')

        ldi = ld.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(ldi.id(), 'slackware')
        self.assertEqual(ldi.name(), 'Slackware')
        self.assertEqual(ldi.name(pretty=True), 'Slackware 14.1')
        self.assertEqual(ldi.version(), '14.1')
        self.assertEqual(ldi.version(pretty=True), '14.1')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), '')
        self.assertEqual(ldi.base(), 'slackware')


class TestOverall(testtools.TestCase):

    def setUp(self):
        super(TestOverall, self).setUp()

    def _setup_for_distro(self, distro_root):
        distro_bin = os.path.join(os.getcwd(), distro_root, 'bin')
        # We don't want to pick up a possibly present lsb_release in the
        # distro that runs this test, so we use a PATH with only one entry:
        os.environ["PATH"] = distro_bin
        const._UNIXCONFDIR = os.path.join(distro_root, RELATIVE_UNIXCONFDIR)
        const._OS_RELEASE = os.path.join(distro_root, RELATIVE_OS_RELEASE)

    def test_arch_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'arch'))

        ldi = ld.LinuxDistribution()

        self.assertEqual(ldi.id(), 'arch')
        self.assertEqual(ldi.name(), 'Arch Linux')
        self.assertEqual(ldi.name(pretty=True), 'Arch Linux')
        # Arch Linux has a continuous release concept:
        self.assertEqual(ldi.version(), '')
        self.assertEqual(ldi.version(pretty=True), '')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), '')
        self.assertEqual(ldi.base(), 'arch')

    def test_centos5_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'centos5'))

        ldi = ld.LinuxDistribution()

        self.assertEqual(ldi.id(), 'centos')
        self.assertEqual(ldi.name(), 'CentOS')
        self.assertEqual(ldi.name(pretty=True), 'CentOS 5.11 (Final)')
        self.assertEqual(ldi.version(), '5.11')
        self.assertEqual(ldi.version(pretty=True), '5.11 (Final)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Final')
        self.assertEqual(ldi.base(), 'rhel')
        self.assertEqual(ldi.major_version(), '5')
        self.assertEqual(ldi.minor_version(), '11')
        self.assertEqual(ldi.build_number(), '')

    def test_centos7_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'centos7'))

        ldi = ld.LinuxDistribution()

        self.assertEqual(ldi.id(), 'centos')
        self.assertEqual(ldi.name(), 'CentOS Linux')
        self.assertEqual(ldi.name(pretty=True), 'CentOS Linux 7 (Core)')
        # TODO: Fix issue that version() looses precision.
        self.assertEqual(ldi.version(), '7')
        self.assertEqual(ldi.version(pretty=True), '7 (Core)')
        self.assertEqual(ldi.like(), 'rhel fedora')
        self.assertEqual(ldi.codename(), 'Core')
        self.assertEqual(ldi.base(), 'rhel')
        self.assertEqual(ldi.major_version(), '7')
        self.assertEqual(ldi.minor_version(), '')
        self.assertEqual(ldi.build_number(), '')

    def test_debian8_os_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'debian8'))

        ldi = ld.LinuxDistribution()

        self.assertEqual(ldi.id(), 'debian')
        self.assertEqual(ldi.name(), 'Debian GNU/Linux')
        self.assertEqual(ldi.name(pretty=True), 'Debian GNU/Linux 8 (jessie)')
        # TODO: Fix issue that version() looses precision.
        self.assertEqual(ldi.version(), '8')
        self.assertEqual(ldi.version(pretty=True), '8 (jessie)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'jessie')
        self.assertEqual(ldi.base(), 'debian')

    def test_exherbo_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'exherbo'))

        ldi = ld.LinuxDistribution()

        # TODO: This release file is currently empty and should be completed.
        self.assertEqual(ldi.id(), 'exherbo')
        self.assertEqual(ldi.name(), '')
        self.assertEqual(ldi.name(pretty=True), '')
        self.assertEqual(ldi.version(), '')
        self.assertEqual(ldi.version(pretty=True), '')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), '')
        self.assertEqual(ldi.base(), 'exherbo')

    def test_fedora23_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'fedora23'))

        ldi = ld.LinuxDistribution()

        self.assertEqual(ldi.id(), 'fedora')
        self.assertEqual(ldi.name(), 'Fedora')
        self.assertEqual(ldi.name(pretty=True), 'Fedora 23 (Twenty Three)')
        self.assertEqual(ldi.version(), '23')
        self.assertEqual(ldi.version(pretty=True), '23 (Twenty Three)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Twenty Three')
        self.assertEqual(ldi.base(), 'fedora')

    def test_opensuse42_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'opensuse42'))

        ldi = ld.LinuxDistribution()

        self.assertEqual(ldi.id(), 'opensuse')
        self.assertEqual(ldi.name(), 'openSUSE Leap')
        self.assertEqual(ldi.name(pretty=True), 'openSUSE Leap 42.1 (x86_64)')
        self.assertEqual(ldi.version(), '42.1')
        self.assertEqual(ldi.version(pretty=True), '42.1')
        self.assertEqual(ldi.like(), 'suse')
        self.assertEqual(ldi.codename(), '')
        self.assertEqual(ldi.base(), 'suse')
        self.assertEqual(ldi.major_version(), '42')
        self.assertEqual(ldi.minor_version(), '1')
        self.assertEqual(ldi.build_number(), '')

    def test_oracle7_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'oracle7'))

        ldi = ld.LinuxDistribution()

        self.assertEqual(ldi.id(), 'oracle')
        self.assertEqual(ldi.name(), 'Oracle Linux Server')
        self.assertEqual(ldi.name(pretty=True), 'Oracle Linux Server 7.1')
        self.assertEqual(ldi.version(), '7.1')
        self.assertEqual(ldi.version(pretty=True), '7.1')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), '')
        self.assertEqual(ldi.base(), 'rhel')

    def test_rhel6_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'rhel6'))

        ldi = ld.LinuxDistribution()

        self.assertEqual(ldi.id(), 'redhat')
        self.assertEqual(ldi.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            ldi.name(pretty=True),
            'Red Hat Enterprise Linux Server 6.5 (Santiago)')
        self.assertEqual(ldi.version(), '6.5')
        self.assertEqual(ldi.version(pretty=True), '6.5 (Santiago)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Santiago')
        self.assertEqual(ldi.base(), 'rhel')
        self.assertEqual(ldi.version_parts(), ('6', '5', ''))

    def test_rhel7_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'rhel7'))

        ldi = ld.LinuxDistribution()

        # TODO: Resolve issue that the id() has changed compared to rhel6
        self.assertEqual(ldi.id(), 'rhel')
        self.assertEqual(ldi.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            ldi.name(pretty=True),
            'Red Hat Enterprise Linux Server 7.0 (Maipo)')
        self.assertEqual(ldi.version(), '7.0')
        self.assertEqual(ldi.version(pretty=True), '7.0 (Maipo)')
        self.assertEqual(ldi.like(), 'fedora')
        self.assertEqual(ldi.codename(), 'Maipo')
        self.assertEqual(ldi.base(), 'fedora')
        self.assertEqual(ldi.version_parts(), ('7', '0', ''))

    def test_slackware14_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'slackware14'))

        ldi = ld.LinuxDistribution()

        self.assertEqual(ldi.id(), 'slackware')
        self.assertEqual(ldi.name(), 'Slackware')
        self.assertEqual(ldi.name(pretty=True), 'Slackware 14.1')
        self.assertEqual(ldi.version(), '14.1')
        self.assertEqual(ldi.version(pretty=True), '14.1')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), '')
        self.assertEqual(ldi.base(), 'slackware')

    def test_ubuntu14_os_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'ubuntu14'))

        ldi = ld.LinuxDistribution()

        self.assertEqual(ldi.id(), 'ubuntu')
        self.assertEqual(ldi.name(), 'Ubuntu')
        self.assertEqual(ldi.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(ldi.version(), '14.04')
        self.assertEqual(ldi.version(pretty=True), '14.04 (Trusty Tahr)')
        self.assertEqual(ldi.like(), 'debian')
        self.assertEqual(ldi.codename(), 'Trusty Tahr')
        self.assertEqual(ldi.base(), 'debian')


class TestInfo(testtools.TestCase):

    def setUp(self):
        super(TestInfo, self).setUp()
        self.rhel7_os_release = os.path.join(DISTROS, 'rhel7', 'etc',
                                             'os-release')

    def test_info(self):
        ldi = ld.LinuxDistribution(False, self.rhel7_os_release, 'non')

        info = ldi.info()
        self.assertEqual(info['id'], 'rhel')
        self.assertEqual(info['version'], '7.0')
        self.assertEqual(info['like'], 'fedora')
        self.assertEqual(info['base'], 'fedora')
        self.assertEqual(info['version_parts']['major'], '7')
        self.assertEqual(info['version_parts']['minor'], '0')
        self.assertEqual(info['version_parts']['build_number'], '')

    def test_none(self):
        ldi = ld.LinuxDistribution(False, 'non', 'non')

        info = ldi.info()
        self.assertEqual(info['id'], '')
        self.assertEqual(info['version'], '')
        self.assertEqual(info['like'], '')
        self.assertEqual(info['base'], '')
        self.assertEqual(info['version_parts']['major'], '')
        self.assertEqual(info['version_parts']['minor'], '')
        self.assertEqual(info['version_parts']['build_number'], '')

    def test_linux_disribution(self):
        ldi = ld.LinuxDistribution(False, self.rhel7_os_release)
        i = ldi.linux_distribution()
        self.assertEqual(
            i, ('Red Hat Enterprise Linux Server', '7.0', 'Maipo'))

    def test_linux_disribution_full_false(self):
        ldi = ld.LinuxDistribution(False, self.rhel7_os_release)
        i = ldi.linux_distribution(full_distribution_name=False)
        self.assertEqual(i, ('rhel', '7.0', 'Maipo'))
