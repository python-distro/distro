import os

import testtools

import ld


RESOURCES = os.path.join('ld', 'tests', 'resources')


class TestOSRelease(testtools.TestCase):

    def setUp(self):
        super(TestOSRelease, self).setUp()
        self.redhat_os_release = os.path.join(RESOURCES, 'redhat-os-release')
        self.suse_os_release = os.path.join(RESOURCES, 'suse-os-release')
        self.fedora_os_release = os.path.join(RESOURCES, 'fedora-os-release')
        self.ubuntu_os_release = os.path.join(RESOURCES, 'ubuntu-os-release')

    def test_redhat_os_release(self):
        ldi = ld.LinuxDistribution(
            self.redhat_os_release, 'non', 'non')

        # raise Exception(self.os_release_file)
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
        ldi = ld.LinuxDistribution(
            self.suse_os_release, 'non', 'non')

        self.assertEqual(ldi.id(), 'opensuse')
        self.assertEqual(ldi.name(), 'openSUSE Leap')
        self.assertEqual(ldi.name(pretty=True), 'openSUSE Leap 42.1 (x86_64)')
        self.assertEqual(ldi.version(), '42.1')
        self.assertEqual(ldi.version(pretty=True), '42.1')
        self.assertEqual(ldi.like(), 'suse')
        self.assertEqual(ldi.codename(), '')
        self.assertEqual(ldi.base(), 'suse')

    def test_fedora_os_release(self):
        ldi = ld.LinuxDistribution(
            self.fedora_os_release, 'non', 'non')

        self.assertEqual(ldi.id(), 'fedora')
        self.assertEqual(ldi.name(), 'Fedora')
        self.assertEqual(ldi.name(pretty=True), 'Fedora 23 (Twenty Three)')
        self.assertEqual(ldi.version(), '23')
        self.assertEqual(ldi.version(pretty=True), '23 (Twenty Three)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Twenty Three')
        self.assertEqual(ldi.base(), 'fedora')

    def test_ubuntu_os_release(self):
        ldi = ld.LinuxDistribution(
            self.ubuntu_os_release, 'non', 'non')

        self.assertEqual(ldi.id(), 'ubuntu')
        self.assertEqual(ldi.name(), 'Ubuntu')
        self.assertEqual(ldi.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(ldi.version(), '14.04')
        self.assertEqual(ldi.version(pretty=True), '14.04.3 LTS, Trusty Tahr')
        self.assertEqual(ldi.like(), 'debian')
        self.assertEqual(ldi.codename(), 'Trusty Tahr')
        self.assertEqual(ldi.base(), 'debian')


class TestLSBRelease(testtools.TestCase):

    def setUp(self):
        super(TestLSBRelease, self).setUp()
        self.lsb_release = os.path.join(RESOURCES, 'lsb-release')

    def test_lsb_release(self):
        ldi = ld.LinuxDistribution(
            'non', self.lsb_release, 'non')

        self.assertEqual(ldi.id(), 'ubuntu')
        self.assertEqual(ldi.name(), 'Ubuntu')
        self.assertEqual(ldi.name(pretty=True), 'Ubuntu 14.04 (trusty)')
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

    def test_redhat_release(self):
        ldi = ld.LinuxDistribution(
            'non', 'non', self.redhat_release)

        self.assertEqual(ldi.id(), 'redhat')
        self.assertEqual(ldi.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            ldi.name(pretty=True),
            'Red Hat Enterprise Linux Server 7.0 (Maipo)')
        self.assertEqual(ldi.version(), '7.0')
        self.assertEqual(ldi.version(pretty=True), '7.0 (Maipo)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Maipo')
        self.assertEqual(ldi.base(), '')
        self.assertEqual(ldi.version_parts(), ('7', '0', ''))

    def test_suse_release(self):
        ldi = ld.LinuxDistribution(
            'non', 'non', self.suse_release)

        self.assertEqual(ldi.id(), 'openSUSE')
        self.assertEqual(ldi.name(), 'openSUSE')
        self.assertEqual(ldi.name(pretty=True), 'openSUSE 42.1')
        self.assertEqual(ldi.version(), '42.1')
        self.assertEqual(ldi.version(pretty=True), '42.1')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), '')
        self.assertEqual(ldi.base(), '')
        self.assertEqual(ldi.major_version(), '42')
        self.assertEqual(ldi.minor_version(), '1')
        self.assertEqual(ldi.build_number(), '')

    def test_centos_release(self):
        ldi = ld.LinuxDistribution(
            'non', 'non', self.centos_release)

        self.assertEqual(ldi.id(), 'centos')
        self.assertEqual(ldi.name(), 'CentOS Linux')
        self.assertEqual(ldi.name(pretty=True), 'CentOS Linux 7.1.1503 (Core)')
        self.assertEqual(ldi.version(), '7.1.1503')
        self.assertEqual(ldi.version(pretty=True), '7.1.1503 (Core)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Core')
        self.assertEqual(ldi.base(), '')
        self.assertEqual(ldi.major_version(), '7')
        self.assertEqual(ldi.minor_version(), '1')
        self.assertEqual(ldi.build_number(), '1503')
