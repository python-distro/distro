import os

import testtools

import ld
from ld import constants as const


RESOURCES = os.path.join('tests', 'resources')
DISTROS = os.path.join(RESOURCES, 'distros')
TESTDISTROS = os.path.join(RESOURCES, 'testdistros')
SPECIAL = os.path.join(RESOURCES, 'special')

RELATIVE_UNIXCONFDIR = const._UNIXCONFDIR.lstrip('/')

MODULE_LDI = ld._ldi

class DistroTestCase(testtools.TestCase):
    """A base class for any testcase classes that test the distributions
    represented in the `DISTROS` subtree."""

    def setUp(self):
        super(DistroTestCase, self).setUp()
        # The environment stays the same across all testcases, so we
        # save and restore the PATH env var in each test case that
        # changes it:
        self._saved_path = os.environ["PATH"]

    def tearDown(self):
        super(DistroTestCase, self).tearDown()
        os.environ["PATH"] = self._saved_path

    def _setup_for_distro(self, distro_root):
        distro_bin = os.path.join(os.getcwd(), distro_root, 'bin')
        # We don't want to pick up a possibly present lsb_release in the
        # distro that runs this test, so we use a PATH with only one entry:
        os.environ["PATH"] = distro_bin
        const._UNIXCONFDIR = os.path.join(distro_root, RELATIVE_UNIXCONFDIR)


class TestOSRelease(testtools.TestCase):

    def setUp(self):
        super(TestOSRelease, self).setUp()

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

    def test_mageia5_os_release(self):
        os_release = os.path.join(DISTROS, 'mageia5', 'etc', 'os-release')

        ldi = ld.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(ldi.id(), 'mageia')
        self.assertEqual(ldi.name(), 'Mageia')
        self.assertEqual(ldi.name(pretty=True), 'Mageia 5')
        self.assertEqual(ldi.version(), '5')
        self.assertEqual(ldi.version(pretty=True), '5')
        self.assertEqual(ldi.like(), 'mandriva fedora')
        self.assertEqual(ldi.codename(), '')

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


class TestLSBRelease(DistroTestCase):

    def test_lsb_release_normal(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb',
                                            'ubuntu14_normal'))

        #import pdb; pdb.set_trace()

        ldi = ld.LinuxDistribution(True, 'non', 'non')

        self.assertEqual(ldi.id(), 'ubuntu')
        self.assertEqual(ldi.name(), 'Ubuntu')
        self.assertEqual(ldi.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(ldi.version(), '14.04')
        self.assertEqual(ldi.version(pretty=True), '14.04 (trusty)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'trusty')

    def test_lsb_release_nomodules(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb',
                                            'ubuntu14_nomodules'))

        ldi = ld.LinuxDistribution(True, 'non', 'non')

        self.assertEqual(ldi.id(), 'ubuntu')
        self.assertEqual(ldi.name(), 'Ubuntu')
        self.assertEqual(ldi.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(ldi.version(), '14.04')
        self.assertEqual(ldi.version(pretty=True), '14.04 (trusty)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'trusty')

    def test_lsb_release_trailingblanks(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb',
                                            'ubuntu14_trailingblanks'))

        ldi = ld.LinuxDistribution(True, 'non', 'non')

        self.assertEqual(ldi.id(), 'ubuntu')
        self.assertEqual(ldi.name(), 'Ubuntu')
        self.assertEqual(ldi.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(ldi.version(), '14.04')
        self.assertEqual(ldi.version(pretty=True), '14.04 (trusty)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'trusty')


class TestDistRelease(testtools.TestCase):

    def setUp(self):
        super(TestDistRelease, self).setUp()

    def test_arch_dist_release(self):
        distro_release = os.path.join(DISTROS, 'arch', 'etc', 'arch-release')

        ldi = ld.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(ldi.id(), 'arch')
        self.assertEqual(ldi.name(), '')
        self.assertEqual(ldi.name(pretty=True), '')
        self.assertEqual(ldi.version(), '')
        self.assertEqual(ldi.version(pretty=True), '')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), '')

    def test_centos5_dist_release(self):
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
        self.assertEqual(ldi.major_version(), '5')
        self.assertEqual(ldi.minor_version(), '11')
        self.assertEqual(ldi.build_number(), '')

    def test_centos7_dist_release(self):
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
        self.assertEqual(ldi.major_version(), '7')
        self.assertEqual(ldi.minor_version(), '1')
        self.assertEqual(ldi.build_number(), '1503')

    def test_empty_dist_release(self):
        distro_release = os.path.join(SPECIAL, 'empty-release')

        ldi = ld.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(ldi.id(), 'empty')
        self.assertEqual(ldi.name(), '')
        self.assertEqual(ldi.name(pretty=True), '')
        self.assertEqual(ldi.version(), '')
        self.assertEqual(ldi.version(pretty=True), '')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), '')

    def test_exherbo_dist_release(self):
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

    def test_fedora23_dist_release(self):
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

    def test_mageia5_dist_release(self):
        distro_release = os.path.join(DISTROS, 'mageia5', 'etc',
                                      'mageia-release')

        ldi = ld.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(ldi.id(), 'mageia')
        self.assertEqual(ldi.name(), 'Mageia')
        self.assertEqual(ldi.name(pretty=True), 'Mageia 5 (Official)')
        self.assertEqual(ldi.version(), '5')
        self.assertEqual(ldi.version(pretty=True), '5 (Official)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Official')

    def test_opensuse42_dist_release(self):
        distro_release = os.path.join(DISTROS, 'opensuse42', 'etc',
                                      'SuSE-release')

        ldi = ld.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(ldi.id(), 'opensuse')
        self.assertEqual(ldi.name(), 'openSUSE')
        self.assertEqual(ldi.name(pretty=True), 'openSUSE 42.1 (x86_64)')
        self.assertEqual(ldi.version(), '42.1')
        self.assertEqual(ldi.version(pretty=True), '42.1 (x86_64)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'x86_64')
        self.assertEqual(ldi.major_version(), '42')
        self.assertEqual(ldi.minor_version(), '1')
        self.assertEqual(ldi.build_number(), '')

    def test_oracle7_dist_release(self):
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

    def test_rhel6_dist_release(self):
        distro_release = os.path.join(DISTROS, 'rhel6', 'etc',
                                      'redhat-release')

        ldi = ld.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(ldi.id(), 'rhel')
        self.assertEqual(ldi.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            ldi.name(pretty=True),
            'Red Hat Enterprise Linux Server 6.5 (Santiago)')
        self.assertEqual(ldi.version(), '6.5')
        self.assertEqual(ldi.version(pretty=True), '6.5 (Santiago)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Santiago')
        self.assertEqual(ldi.version_parts(), ('6', '5', ''))

    def test_rhel7_dist_release(self):
        distro_release = os.path.join(DISTROS, 'rhel7', 'etc',
                                      'redhat-release')

        ldi = ld.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(ldi.id(), 'rhel')
        self.assertEqual(ldi.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            ldi.name(pretty=True),
            'Red Hat Enterprise Linux Server 7.0 (Maipo)')
        self.assertEqual(ldi.version(), '7.0')
        self.assertEqual(ldi.version(pretty=True), '7.0 (Maipo)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Maipo')
        self.assertEqual(ldi.version_parts(), ('7', '0', ''))

    def test_slackware14_dist_release(self):
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


class TestOverall(DistroTestCase):
    """Test a LinuxDistribution object created with default arguments.

    The direct accessor functions on that object are tested (e.g. `id()`); they
    implement the precedence between the different sources of information.

    In addition, because the distro release file is searched when not
    specified, the information resulting from the distro release file is also
    tested. The LSB and os-release sources are not tested again, because their
    test is already done in TestLSBRelease and TestOSRelease, and their
    algorithm does not depend on whether or not the file is specified.

    TODO: This class should have testcases for all distros that are claimed
    to be reliably maintained w.r.t. to their ID (see `id()`). Testcases for
    the following distros are still missing:
      * `sles` - SUSE Linux Enterprise Server
      * `amazon` - Amazon Linux
      * `cloudlinux` - CloudLinux OS
      * `exherbo` - Exherbo Linux
      * `gentoo` - GenToo Linux
      * `ibm_powerkvm` - IBM PowerKVM
      * `linuxmint` - Linux Mint
      * `mandriva` - Mandriva Linux
      * `nexus_centos` - TODO: Clarify
      * `parallels` - Parallels
      * `pidora` - Pidora (Fedora remix for Raspberry Pi)
      * `raspbian` - Raspbian
      * `scientific` - Scientific Linux
      * `xenserver` - XenServer
    """

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

        # Test the info from the searched distro release file
        # Does not have one; The empty /etc/arch-release file is not
        # considered a valid distro release file:
        self.assertEqual(ldi.distro_release_file, '')
        self.assertEqual(len(ldi.distro_release_info()), 0)

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
        self.assertEqual(ldi.major_version(), '5')
        self.assertEqual(ldi.minor_version(), '11')
        self.assertEqual(ldi.build_number(), '')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(ldi.distro_release_file),
                         'centos-release')
        distro_info = ldi.distro_release_info()
        self.assertEqual(distro_info['id'], 'centos')
        self.assertEqual(distro_info['name'], 'CentOS')
        self.assertEqual(distro_info['version_id'], '5.11')
        self.assertEqual(distro_info['codename'], 'Final')

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
        self.assertEqual(ldi.major_version(), '7')
        self.assertEqual(ldi.minor_version(), '')
        self.assertEqual(ldi.build_number(), '')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(ldi.distro_release_file),
                         'centos-release')
        distro_info = ldi.distro_release_info()
        self.assertEqual(distro_info['id'], 'centos')
        self.assertEqual(distro_info['name'], 'CentOS Linux')
        self.assertEqual(distro_info['version_id'], '7.1.1503')
        self.assertEqual(distro_info['codename'], 'Core')

    def test_debian8_release(self):
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

        # Test the info from the searched distro release file
        # Does not have one:
        self.assertEqual(ldi.distro_release_file, '')
        self.assertEqual(len(ldi.distro_release_info()), 0)

    def test_exherbo_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'exherbo'))

        ldi = ld.LinuxDistribution()

        # TODO: This release file is currently empty and should be completed.
        self.assertEqual(ldi.id(), '')
        self.assertEqual(ldi.name(), '')
        self.assertEqual(ldi.name(pretty=True), '')
        self.assertEqual(ldi.version(), '')
        self.assertEqual(ldi.version(pretty=True), '')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), '')

        # Test the info from the searched distro release file
        # TODO: Add tests for searched Exherbo distro release file

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

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(ldi.distro_release_file),
                         'fedora-release')
        distro_info = ldi.distro_release_info()
        self.assertEqual(distro_info['id'], 'fedora')
        self.assertEqual(distro_info['name'], 'Fedora')
        self.assertEqual(distro_info['version_id'], '23')
        self.assertEqual(distro_info['codename'], 'Twenty Three')

    def test_mageia5_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'mageia5'))

        ldi = ld.LinuxDistribution()

        self.assertEqual(ldi.id(), 'mageia')
        self.assertEqual(ldi.name(), 'Mageia')
        self.assertEqual(ldi.name(pretty=True), 'Mageia 5')
        self.assertEqual(ldi.version(), '5')
        self.assertEqual(ldi.version(pretty=True), '5 (thornicroft)')
        self.assertEqual(ldi.like(), 'mandriva fedora')
        # TODO: Codename differs between distro release file and lsb_release.
        self.assertEqual(ldi.codename(), 'thornicroft')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(ldi.distro_release_file),
                         'mageia-release')
        distro_info = ldi.distro_release_info()
        self.assertEqual(distro_info['id'], 'mageia')
        self.assertEqual(distro_info['name'], 'Mageia')
        self.assertEqual(distro_info['version_id'], '5')
        self.assertEqual(distro_info['codename'], 'Official')

    def test_opensuse42_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'opensuse42'))

        ldi = ld.LinuxDistribution()

        self.assertEqual(ldi.id(), 'opensuse')
        self.assertEqual(ldi.name(), 'openSUSE Leap')
        self.assertEqual(ldi.name(pretty=True), 'openSUSE Leap 42.1 (x86_64)')
        self.assertEqual(ldi.version(), '42.1')
        self.assertEqual(ldi.version(pretty=True), '42.1 (x86_64)')
        self.assertEqual(ldi.like(), 'suse')
        self.assertEqual(ldi.codename(), 'x86_64')
        self.assertEqual(ldi.major_version(), '42')
        self.assertEqual(ldi.minor_version(), '1')
        self.assertEqual(ldi.build_number(), '')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(ldi.distro_release_file),
                         'SuSE-release')
        distro_info = ldi.distro_release_info()
        self.assertEqual(distro_info['id'], 'SuSE')
        self.assertEqual(distro_info['name'], 'openSUSE')
        self.assertEqual(distro_info['version_id'], '42.1')
        self.assertEqual(distro_info['codename'], 'x86_64')

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

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(ldi.distro_release_file),
                         'oracle-release')
        distro_info = ldi.distro_release_info()
        self.assertEqual(distro_info['id'], 'oracle')
        self.assertEqual(distro_info['name'], 'Oracle Linux Server')
        self.assertEqual(distro_info['version_id'], '7.1')
        self.assertTrue('codename' not in distro_info)

    def test_rhel6_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'rhel6'))

        ldi = ld.LinuxDistribution()

        self.assertEqual(ldi.id(), 'rhel')
        self.assertEqual(ldi.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            ldi.name(pretty=True),
            'Red Hat Enterprise Linux Server 6.5 (Santiago)')
        self.assertEqual(ldi.version(), '6.5')
        self.assertEqual(ldi.version(pretty=True), '6.5 (Santiago)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Santiago')
        self.assertEqual(ldi.version_parts(), ('6', '5', ''))

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(ldi.distro_release_file),
                         'redhat-release')
        distro_info = ldi.distro_release_info()
        self.assertEqual(distro_info['id'], 'redhat')
        self.assertEqual(distro_info['name'],
                         'Red Hat Enterprise Linux Server')
        self.assertEqual(distro_info['version_id'], '6.5')
        self.assertEqual(distro_info['codename'], 'Santiago')

    def test_rhel7_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'rhel7'))

        ldi = ld.LinuxDistribution()

        self.assertEqual(ldi.id(), 'rhel')
        self.assertEqual(ldi.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            ldi.name(pretty=True),
            'Red Hat Enterprise Linux Server 7.0 (Maipo)')
        self.assertEqual(ldi.version(), '7.0')
        self.assertEqual(ldi.version(pretty=True), '7.0 (Maipo)')
        self.assertEqual(ldi.like(), 'fedora')
        self.assertEqual(ldi.codename(), 'Maipo')
        self.assertEqual(ldi.version_parts(), ('7', '0', ''))

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(ldi.distro_release_file),
                         'redhat-release')
        distro_info = ldi.distro_release_info()
        self.assertEqual(distro_info['id'], 'redhat')
        self.assertEqual(distro_info['name'],
                         'Red Hat Enterprise Linux Server')
        self.assertEqual(distro_info['version_id'], '7.0')
        self.assertEqual(distro_info['codename'], 'Maipo')

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

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(ldi.distro_release_file),
                         'slackware-version')
        distro_info = ldi.distro_release_info()
        self.assertEqual(distro_info['id'], 'slackware')
        self.assertEqual(distro_info['name'], 'Slackware')
        self.assertEqual(distro_info['version_id'], '14.1')
        self.assertTrue('codename' not in distro_info)

    def test_ubuntu14_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'ubuntu14'))

        ldi = ld.LinuxDistribution()

        self.assertEqual(ldi.id(), 'ubuntu')
        self.assertEqual(ldi.name(), 'Ubuntu')
        self.assertEqual(ldi.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(ldi.version(), '14.04')
        self.assertEqual(ldi.version(pretty=True), '14.04 (Trusty Tahr)')
        self.assertEqual(ldi.like(), 'debian')
        self.assertEqual(ldi.codename(), 'Trusty Tahr')

        # Test the info from the searched distro release file
        # Does not have one; /etc/debian_version is not considered a distro
        # release file:
        self.assertEqual(ldi.distro_release_file, '')
        self.assertEqual(len(ldi.distro_release_info()), 0)

    def test_unknowndistro_release(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'distro',
                                            'unknowndistro'))

        ldi = ld.LinuxDistribution()

        self.assertEqual(ldi.id(), 'unknowndistro')
        self.assertEqual(ldi.name(), 'Unknown Distro')
        self.assertEqual(ldi.name(pretty=True),
                         'Unknown Distro 1.0 (Unknown Codename)')
        self.assertEqual(ldi.version(), '1.0')
        self.assertEqual(ldi.version(pretty=True), '1.0 (Unknown Codename)')
        self.assertEqual(ldi.like(), '')
        self.assertEqual(ldi.codename(), 'Unknown Codename')


class TestGetAttr(DistroTestCase):
    """Test the consistency between the results of
    `get_{source}_release_attr()` and `{source}_release_info()` for all
    distros in `DISTROS`."""

    def test_os_release_attr(self):
        distros = os.listdir(DISTROS)
        for distro in distros:
            self._setup_for_distro(os.path.join(DISTROS, distro))

            ldi = ld.LinuxDistribution()

            info = ldi.os_release_info()
            for key in info.keys():
                self.assertEqual(info[key],
                                 ldi.get_os_release_attr(key),
                                 "distro: %s, key: %s" % (distro, key))

    def test_lsb_release_attr(self):
        distros = os.listdir(DISTROS)
        for distro in distros:
            self._setup_for_distro(os.path.join(DISTROS, distro))

            ldi = ld.LinuxDistribution()

            info = ldi.lsb_release_info()
            for key in info.keys():
                self.assertEqual(info[key],
                                 ldi.get_lsb_release_attr(key),
                                 "distro: %s, key: %s" % (distro, key))

    def test_distro_release_attr(self):
        distros = os.listdir(DISTROS)
        for distro in distros:
            self._setup_for_distro(os.path.join(DISTROS, distro))

            ldi = ld.LinuxDistribution()

            info = ldi.distro_release_info()
            for key in info.keys():
                self.assertEqual(info[key],
                                 ldi.get_distro_release_attr(key),
                                 "distro: %s, key: %s" % (distro, key))


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
        self.assertEqual(info['version_parts']['major'], '7')
        self.assertEqual(info['version_parts']['minor'], '0')
        self.assertEqual(info['version_parts']['build_number'], '')

    def test_none(self):
        ldi = ld.LinuxDistribution(False, 'non', 'non')

        info = ldi.info()
        self.assertEqual(info['id'], '')
        self.assertEqual(info['version'], '')
        self.assertEqual(info['like'], '')
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


class TestGlobal(testtools.TestCase):
    """Test the global module-level functions, and default values of their
    arguments."""

    def test_global(self):
        # Because the module-level functions use the module-global
        # LinuxDistribution instance, it would influence the tested
        # code too much if we mocked that in order to use the distro
        # specific release files. Instead, we let the functions use
        # the release files of the distro this test runs on, and
        # compare the result of the global functions with the result
        # of the methods on the global LinuxDistribution object.
        self.assertEqual(ld.id(),
            MODULE_LDI.id())
        self.assertEqual(ld.name(),
            MODULE_LDI.name(pretty=False))
        self.assertEqual(ld.name(pretty=False),
            MODULE_LDI.name())
        self.assertEqual(ld.name(pretty=True),
            MODULE_LDI.name(pretty=True))
        self.assertEqual(ld.version(),
            MODULE_LDI.version(pretty=False))
        self.assertEqual(ld.version(pretty=False),
            MODULE_LDI.version())
        self.assertEqual(ld.version(pretty=True),
            MODULE_LDI.version(pretty=True))
        self.assertEqual(ld.major_version(),
            MODULE_LDI.major_version())
        self.assertEqual(ld.minor_version(),
            MODULE_LDI.minor_version())
        self.assertEqual(ld.build_number(),
            MODULE_LDI.build_number())
        self.assertEqual(ld.like(),
            MODULE_LDI.like())
        self.assertEqual(ld.codename(),
            MODULE_LDI.codename())
        self.assertEqual(ld.linux_distribution(),
            MODULE_LDI.linux_distribution(full_distribution_name=True))
        self.assertEqual(ld.linux_distribution(full_distribution_name=True),
            MODULE_LDI.linux_distribution())
        self.assertEqual(ld.linux_distribution(full_distribution_name=False),
            MODULE_LDI.linux_distribution(full_distribution_name=False))
        self.assertEqual(ld.os_release_info(),
            MODULE_LDI.os_release_info())
        self.assertEqual(ld.lsb_release_info(),
            MODULE_LDI.lsb_release_info())
        self.assertEqual(ld.distro_release_info(),
            MODULE_LDI.distro_release_info())
        self.assertEqual(ld.info(),
            MODULE_LDI.info())


class TestRepr(testtools.TestCase):
    """Test the __repr__() method."""

    def test_repr(self):
        # We test that the class name and the names of all instance attributes
        # show up in the repr() string.
        repr_str = repr(ld._ldi)
        self.assertIn("LinuxDistribution", repr_str)
        for attr in MODULE_LDI.__dict__.keys():
            self.assertIn(attr+'=', repr_str)

