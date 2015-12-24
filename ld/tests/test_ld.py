import os

import testtools

import ld


RESOURCES = os.path.join('ld', 'tests', 'resources')
LSB_RELEASE_FILE = os.path.join(RESOURCES, 'lsb_release')


class TestOSRelease(testtools.TestCase):

    def setUp(self):
        super(TestOSRelease, self).setUp()
        self.redhat_os_release = os.path.join(RESOURCES, 'redhat-os-release')
        self.suse_os_release = os.path.join(RESOURCES, 'suse-os-release')
        self.fedora_os_release = os.path.join(RESOURCES, 'fedora-os-release')
        self.ubuntu_os_release = os.path.join(RESOURCES, 'ubuntu-os-release')

    def test_redhat_os_release(self):
        ldi = ld.LinuxDistribution(self.redhat_os_release, 'non')

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

    def test_suse_os_release(self):
        ldi = ld.LinuxDistribution(self.suse_os_release, 'non')

        self.assertEqual(ldi.id(), 'opensuse')
        self.assertEqual(ldi.name(), 'openSUSE Leap')
        self.assertEqual(ldi.name(pretty=True), 'openSUSE Leap 42.1 (x86_64)')
        self.assertEqual(ldi.version(), '42.1')
        self.assertEqual(ldi.version(pretty=True), '42.1')
        self.assertEqual(ldi.like(), 'suse')
        self.assertEqual(ldi.codename(), '')
        self.assertEqual(ldi.base(), 'suse')

    def test_fedora_os_release(self):
        ldi = ld.LinuxDistribution(self.fedora_os_release, 'non')

        self.assertEqual(ldi.id(), 'fedora')
        self.assertEqual(ldi.name(), 'Fedora')
        self.assertEqual(ldi.name(pretty=True), 'Fedora 23 (Twenty Three)')
        self.assertEqual(ldi.version(), '23')
        self.assertEqual(ldi.version(pretty=True), '23 (Twenty Three)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Twenty Three')
        self.assertEqual(ldi.base(), 'fedora')

    def test_ubuntu_os_release(self):
        ldi = ld.LinuxDistribution(self.ubuntu_os_release, 'non')

        self.assertEqual(ldi.id(), 'ubuntu')
        self.assertEqual(ldi.name(), 'Ubuntu')
        self.assertEqual(ldi.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(ldi.version(), '14.04')
        self.assertEqual(ldi.version(pretty=True), '14.04 (Trusty Tahr)')
        self.assertEqual(ldi.like(), 'debian')
        self.assertEqual(ldi.codename(), 'Trusty Tahr')
        self.assertEqual(ldi.base(), 'debian')


class TestLSBRelease(testtools.TestCase):

    @staticmethod
    def _mock_lsb_release_info():
        with open(LSB_RELEASE_FILE) as data:
            return ld.LinuxDistribution()._parse_lsb_release(data) or {}

    def test_lsb_release(self):
        ldi = ld.LinuxDistribution('non', 'non')
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
        self.redhat_release = os.path.join(RESOURCES, 'redhat-release')
        self.suse_release = os.path.join(RESOURCES, 'SuSE-release')
        self.centos_release = os.path.join(RESOURCES, 'centos-release')
        self.fedora_release = os.path.join(RESOURCES, 'fedora-release')
        self.oracle_release = os.path.join(RESOURCES, 'oracle-release')
        self.empty_release = os.path.join(RESOURCES, 'empty-release')

    def test_redhat_release(self):
        ldi = ld.LinuxDistribution(
            'non', self.redhat_release)

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

    def test_suse_release(self):
        ldi = ld.LinuxDistribution(
            'non', self.suse_release)

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

    def test_centos_release(self):
        ldi = ld.LinuxDistribution(
            'non', self.centos_release)

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

    def test_fedora_release(self):
        ldi = ld.LinuxDistribution(
            'non', self.fedora_release)

        self.assertEqual(ldi.id(), 'fedora')
        self.assertEqual(ldi.name(), 'Fedora')
        self.assertEqual(ldi.name(pretty=True), 'Fedora 23 (Twenty Three)')
        self.assertEqual(ldi.version(), '23')
        self.assertEqual(ldi.version(pretty=True), '23 (Twenty Three)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Twenty Three')
        self.assertEqual(ldi.base(), 'fedora')

    def test_oracle_release(self):
        ldi = ld.LinuxDistribution(
            'non', self.oracle_release)

        self.assertEqual(ldi.id(), 'oracle')
        self.assertEqual(ldi.name(), 'Oracle Linux Server')
        self.assertEqual(ldi.name(pretty=True), 'Oracle Linux Server 7.1')
        self.assertEqual(ldi.version(), '7.1')
        self.assertEqual(ldi.version(pretty=True), '7.1')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), '')
        self.assertEqual(ldi.base(), 'rhel')

    def test_empty_release(self):
        ldi = ld.LinuxDistribution(
            'non', self.empty_release)

        self.assertEqual(ldi.id(), '')
        self.assertEqual(ldi.name(), '')
        self.assertEqual(ldi.name(pretty=True), '')
        self.assertEqual(ldi.version(), '')
        self.assertEqual(ldi.version(pretty=True), '')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), '')
        self.assertEqual(ldi.base(), '')


class TestInfo(testtools.TestCase):

    def setUp(self):
        super(TestInfo, self).setUp()
        self.redhat_os_release = os.path.join(RESOURCES, 'redhat-os-release')

    def test_info(self):
        ldi = ld.LinuxDistribution(
            self.redhat_os_release, 'non')

        info = ldi.info()
        self.assertEqual(info['id'], 'rhel')
        self.assertEqual(info['version'], '7.0')
        self.assertEqual(info['like'], 'fedora')
        self.assertEqual(info['base'], 'fedora')
        self.assertEqual(info['version_parts']['major'], '7')
        self.assertEqual(info['version_parts']['minor'], '0')
        self.assertEqual(info['version_parts']['build_number'], '')

    def test_none(self):
        ldi = ld.LinuxDistribution(
            'non', 'non')

        info = ldi.info()
        self.assertEqual(info['id'], '')
        self.assertEqual(info['version'], '')
        self.assertEqual(info['like'], '')
        self.assertEqual(info['base'], '')
        self.assertEqual(info['version_parts']['major'], '')
        self.assertEqual(info['version_parts']['minor'], '')
        self.assertEqual(info['version_parts']['build_number'], '')

    def test_linux_disribution(self):
        ldi = ld.LinuxDistribution(self.redhat_os_release)
        i = ldi.linux_distribution()
        self.assertEqual(
            i, ('Red Hat Enterprise Linux Server', '7.0', 'Maipo'))

    def test_linux_disribution_full_false(self):
        ldi = ld.LinuxDistribution(self.redhat_os_release)
        i = ldi.linux_distribution(full_distribution_name=False)
        self.assertEqual(i, ('rhel', '7.0', 'Maipo'))
