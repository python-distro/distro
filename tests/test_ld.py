# Copyright 2015,2016 Nir Cohen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# flake8: NOQA

import os
import testtools
import subprocess
try:
    from StringIO import StringIO  # Python 2.x
except ImportError:
    from io import StringIO  # Python 3.x


import distro


RESOURCES = os.path.join('tests', 'resources')
DISTROS = os.path.join(RESOURCES, 'distros')
TESTDISTROS = os.path.join(RESOURCES, 'testdistros')
SPECIAL = os.path.join(RESOURCES, 'special')

RELATIVE_UNIXCONFDIR = distro._UNIXCONFDIR.lstrip('/')

MODULE_DISTROI = distro._distroi


class DistroTestCase(testtools.TestCase):
    """A base class for any testcase classes that test the distributions
    represented in the `DISTROS` subtree."""

    def setUp(self):
        super(DistroTestCase, self).setUp()
        # The environment stays the same across all testcases, so we
        # save and restore the PATH env var in each test case that
        # changes it:
        self._saved_path = os.environ["PATH"]
        self._saved_UNIXCONFDIR = distro._UNIXCONFDIR

    def tearDown(self):
        super(DistroTestCase, self).tearDown()
        os.environ["PATH"] = self._saved_path
        distro._UNIXCONFDIR = self._saved_UNIXCONFDIR

    def _setup_for_distro(self, distro_root):
        distro_bin = os.path.join(os.getcwd(), distro_root, 'bin')
        # We don't want to pick up a possibly present lsb_release in the
        # distro that runs this test, so we use a PATH with only one entry:
        os.environ["PATH"] = distro_bin
        distro._UNIXCONFDIR = os.path.join(distro_root, RELATIVE_UNIXCONFDIR)


class TestOSRelease(testtools.TestCase):

    def setUp(self):
        super(TestOSRelease, self).setUp()

    def test_arch_os_release(self):
        os_release = os.path.join(DISTROS, 'arch', 'etc', 'os-release')

        distroi = distro.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(distroi.id(), 'arch')
        self.assertEqual(distroi.name(), 'Arch Linux')
        self.assertEqual(distroi.name(pretty=True), 'Arch Linux')
        self.assertEqual(distroi.version(), '')
        self.assertEqual(distroi.version(pretty=True), '')
        self.assertEqual(distroi.version(best=True), '')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), '')

    def test_centos7_os_release(self):
        os_release = os.path.join(DISTROS, 'centos7', 'etc', 'os-release')

        distroi = distro.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(distroi.id(), 'centos')
        self.assertEqual(distroi.name(), 'CentOS Linux')
        self.assertEqual(distroi.name(pretty=True), 'CentOS Linux 7 (Core)')
        self.assertEqual(distroi.version(), '7')
        self.assertEqual(distroi.version(pretty=True), '7 (Core)')
        self.assertEqual(distroi.version(best=True), '7')
        self.assertEqual(distroi.like(), 'rhel fedora')
        self.assertEqual(distroi.codename(), 'Core')

    def test_debian8_os_release(self):
        os_release = os.path.join(DISTROS, 'debian8', 'etc', 'os-release')

        distroi = distro.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(distroi.id(), 'debian')
        self.assertEqual(distroi.name(), 'Debian GNU/Linux')
        self.assertEqual(distroi.name(pretty=True), 'Debian GNU/Linux 8 (jessie)')
        self.assertEqual(distroi.version(), '8')
        self.assertEqual(distroi.version(pretty=True), '8 (jessie)')
        self.assertEqual(distroi.version(best=True), '8')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'jessie')

    def test_fedora19_os_release(self):
        os_release = os.path.join(DISTROS, 'fedora19', 'etc', 'os-release')

        distroi = distro.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(distroi.id(), 'fedora')
        self.assertEqual(distroi.name(), 'Fedora')
        self.assertEqual(distroi.name(pretty=True), u'Fedora 19 (Schr\u00F6dinger\u2019s Cat)')
        self.assertEqual(distroi.version(), '19')
        self.assertEqual(distroi.version(pretty=True), u'19 (Schr\u00F6dinger\u2019s Cat)')
        self.assertEqual(distroi.version(best=True), '19')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), u'Schr\u00F6dinger\u2019s Cat')

    def test_fedora23_os_release(self):
        os_release = os.path.join(DISTROS, 'fedora23', 'etc', 'os-release')

        distroi = distro.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(distroi.id(), 'fedora')
        self.assertEqual(distroi.name(), 'Fedora')
        self.assertEqual(distroi.name(pretty=True), 'Fedora 23 (Twenty Three)')
        self.assertEqual(distroi.version(), '23')
        self.assertEqual(distroi.version(pretty=True), '23 (Twenty Three)')
        self.assertEqual(distroi.version(best=True), '23')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'Twenty Three')

    def test_kvmibm1_os_release(self):
        os_release = os.path.join(DISTROS, 'kvmibm1', 'etc', 'os-release')

        distroi = distro.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(distroi.id(), 'kvmibm')
        self.assertEqual(distroi.name(), 'KVM for IBM z Systems')
        self.assertEqual(distroi.name(pretty=True), 'KVM for IBM z Systems 1.1.1 (Z)')
        self.assertEqual(distroi.version(), '1.1.1')
        self.assertEqual(distroi.version(pretty=True), '1.1.1 (Z)')
        self.assertEqual(distroi.version(best=True), '1.1.1')
        self.assertEqual(distroi.like(), 'rhel fedora')
        self.assertEqual(distroi.codename(), 'Z')

    def test_linuxmint17_os_release(self):
        os_release = os.path.join(DISTROS, 'linuxmint17', 'etc', 'os-release')

        distroi = distro.LinuxDistribution(False, os_release, 'non')

        # Note: LinuxMint 17 actually *does* have Ubuntu 14.04 data in its
        #       os-release file. See discussion in GitHub issue #78.

        self.assertEqual(distroi.id(), 'ubuntu')
        self.assertEqual(distroi.name(), 'Ubuntu')
        self.assertEqual(distroi.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(distroi.version(), '14.04')
        self.assertEqual(distroi.version(pretty=True), '14.04 (Trusty Tahr)')
        self.assertEqual(distroi.version(best=True), '14.04.3')
        self.assertEqual(distroi.like(), 'debian')
        self.assertEqual(distroi.codename(), 'Trusty Tahr')

    def test_mageia5_os_release(self):
        os_release = os.path.join(DISTROS, 'mageia5', 'etc', 'os-release')

        distroi = distro.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(distroi.id(), 'mageia')
        self.assertEqual(distroi.name(), 'Mageia')
        self.assertEqual(distroi.name(pretty=True), 'Mageia 5')
        self.assertEqual(distroi.version(), '5')
        self.assertEqual(distroi.version(pretty=True), '5')
        self.assertEqual(distroi.version(best=True), '5')
        self.assertEqual(distroi.like(), 'mandriva fedora')
        self.assertEqual(distroi.codename(), '')

    def test_opensuse42_os_release(self):
        os_release = os.path.join(DISTROS, 'opensuse42', 'etc', 'os-release')

        distroi = distro.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(distroi.id(), 'opensuse')
        self.assertEqual(distroi.name(), 'openSUSE Leap')
        self.assertEqual(distroi.name(pretty=True), 'openSUSE Leap 42.1 (x86_64)')
        self.assertEqual(distroi.version(), '42.1')
        self.assertEqual(distroi.version(pretty=True), '42.1')
        self.assertEqual(distroi.version(best=True), '42.1')
        self.assertEqual(distroi.like(), 'suse')
        self.assertEqual(distroi.codename(), '')

    def test_rhel7_os_release(self):
        os_release = os.path.join(DISTROS, 'rhel7', 'etc', 'os-release')

        distroi = distro.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(distroi.id(), 'rhel')
        self.assertEqual(distroi.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            distroi.name(pretty=True),
            'Red Hat Enterprise Linux Server 7.0 (Maipo)')
        self.assertEqual(distroi.version(), '7.0')
        self.assertEqual(distroi.version(pretty=True), '7.0 (Maipo)')
        self.assertEqual(distroi.version(best=True), '7.0')
        self.assertEqual(distroi.like(), 'fedora')
        self.assertEqual(distroi.codename(), 'Maipo')

    def test_slackware14_os_release(self):
        os_release = os.path.join(DISTROS, 'slackware14', 'etc', 'os-release')

        distroi = distro.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(distroi.id(), 'slackware')
        self.assertEqual(distroi.name(), 'Slackware')
        self.assertEqual(distroi.name(pretty=True), 'Slackware 14.1')
        self.assertEqual(distroi.version(), '14.1')
        self.assertEqual(distroi.version(pretty=True), '14.1')
        self.assertEqual(distroi.version(best=True), '14.1')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), '')

    def test_sles12_os_release(self):
        os_release = os.path.join(DISTROS, 'sles12', 'etc', 'os-release')

        distroi = distro.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(distroi.id(), 'sles')
        self.assertEqual(distroi.name(), 'SLES')
        self.assertEqual(distroi.name(pretty=True),
                         'SUSE Linux Enterprise Server 12 SP1')
        self.assertEqual(distroi.version(), '12.1')
        self.assertEqual(distroi.version(pretty=True), '12.1')
        self.assertEqual(distroi.version(best=True), '12.1')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), '')

    def test_ubuntu14_os_release(self):
        os_release = os.path.join(DISTROS, 'ubuntu14', 'etc', 'os-release')

        distroi = distro.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(distroi.id(), 'ubuntu')
        self.assertEqual(distroi.name(), 'Ubuntu')
        self.assertEqual(distroi.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(distroi.version(), '14.04')
        self.assertEqual(distroi.version(pretty=True), '14.04 (Trusty Tahr)')
        self.assertEqual(distroi.version(best=True), '14.04.3')
        self.assertEqual(distroi.like(), 'debian')
        self.assertEqual(distroi.codename(), 'Trusty Tahr')


class TestLSBRelease(DistroTestCase):

    def test_linuxmint17_lsb_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'linuxmint17'))

        distroi = distro.LinuxDistribution(True, 'non', 'non')

        self.assertEqual(distroi.id(), 'linuxmint')
        self.assertEqual(distroi.name(), 'LinuxMint')
        self.assertEqual(distroi.name(pretty=True), 'Linux Mint 17.3 Rosa')
        self.assertEqual(distroi.version(), '17.3')
        self.assertEqual(distroi.version(pretty=True), '17.3 (rosa)')
        self.assertEqual(distroi.version(best=True), '17.3')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'rosa')

    def test_lsb_release_normal(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb',
                                            'ubuntu14_normal'))

        distroi = distro.LinuxDistribution(True, 'non', 'non')

        self.assertEqual(distroi.id(), 'ubuntu')
        self.assertEqual(distroi.name(), 'Ubuntu')
        self.assertEqual(distroi.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(distroi.version(), '14.04')
        self.assertEqual(distroi.version(pretty=True), '14.04 (trusty)')
        self.assertEqual(distroi.version(best=True), '14.04.3')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'trusty')

    def test_lsb_release_nomodules(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb',
                                            'ubuntu14_nomodules'))

        distroi = distro.LinuxDistribution(True, 'non', 'non')

        self.assertEqual(distroi.id(), 'ubuntu')
        self.assertEqual(distroi.name(), 'Ubuntu')
        self.assertEqual(distroi.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(distroi.version(), '14.04')
        self.assertEqual(distroi.version(pretty=True), '14.04 (trusty)')
        self.assertEqual(distroi.version(best=True), '14.04.3')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'trusty')

    def test_lsb_release_trailingblanks(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb',
                                            'ubuntu14_trailingblanks'))

        distroi = distro.LinuxDistribution(True, 'non', 'non')

        self.assertEqual(distroi.id(), 'ubuntu')
        self.assertEqual(distroi.name(), 'Ubuntu')
        self.assertEqual(distroi.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(distroi.version(), '14.04')
        self.assertEqual(distroi.version(pretty=True), '14.04 (trusty)')
        self.assertEqual(distroi.version(best=True), '14.04.3')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'trusty')

    def test_lsb_release_rc001(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb', 'lsb_rc001'))
        try:
            distroi = distro.LinuxDistribution(True, 'non', 'non')
            exc = None
        except Exception as _exc:
            exc = _exc
        self.assertEqual(isinstance(exc, subprocess.CalledProcessError), True)
        self.assertEqual(exc.returncode, 1)

    def test_lsb_release_rc002(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb', 'lsb_rc002'))
        try:
            distroi = distro.LinuxDistribution(True, 'non', 'non')
            exc = None
        except Exception as _exc:
            exc = _exc
        self.assertEqual(isinstance(exc, subprocess.CalledProcessError), True)
        self.assertEqual(exc.returncode, 2)

    def test_lsb_release_rc126(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb', 'lsb_rc126'))
        try:
            distroi = distro.LinuxDistribution(True, 'non', 'non')
            exc = None
        except Exception as _exc:
            exc = _exc
        self.assertEqual(isinstance(exc, subprocess.CalledProcessError), True)
        self.assertEqual(exc.returncode, 126)

    def test_lsb_release_rc130(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb', 'lsb_rc130'))
        try:
            distroi = distro.LinuxDistribution(True, 'non', 'non')
            exc = None
        except Exception as _exc:
            exc = _exc
        self.assertEqual(isinstance(exc, subprocess.CalledProcessError), True)
        self.assertEqual(exc.returncode, 130)

    def test_lsb_release_rc255(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb', 'lsb_rc255'))
        try:
            distroi = distro.LinuxDistribution(True, 'non', 'non')
            exc = None
        except Exception as _exc:
            exc = _exc
        self.assertEqual(isinstance(exc, subprocess.CalledProcessError), True)
        self.assertEqual(exc.returncode, 255)


class TestDistroRelease(testtools.TestCase):

    def setUp(self):
        super(TestDistroRelease, self).setUp()

    def test_arch_dist_release(self):
        distro_release = os.path.join(DISTROS, 'arch', 'etc', 'arch-release')

        distroi = distro.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(distroi.id(), 'arch')
        self.assertEqual(distroi.name(), '')
        self.assertEqual(distroi.name(pretty=True), '')
        self.assertEqual(distroi.version(), '')
        self.assertEqual(distroi.version(pretty=True), '')
        self.assertEqual(distroi.version(best=True), '')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), '')

    def test_centos5_dist_release(self):
        distro_release = os.path.join(DISTROS, 'centos5', 'etc',
                                      'centos-release')
        distroi = distro.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(distroi.id(), 'centos')
        self.assertEqual(distroi.name(), 'CentOS')
        self.assertEqual(distroi.name(pretty=True), 'CentOS 5.11 (Final)')
        self.assertEqual(distroi.version(), '5.11')
        self.assertEqual(distroi.version(pretty=True), '5.11 (Final)')
        self.assertEqual(distroi.version(best=True), '5.11')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'Final')
        self.assertEqual(distroi.major_version(), '5')
        self.assertEqual(distroi.minor_version(), '11')
        self.assertEqual(distroi.build_number(), '')

    def test_centos7_dist_release(self):
        distro_release = os.path.join(DISTROS, 'centos7', 'etc',
                                      'centos-release')

        distroi = distro.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(distroi.id(), 'centos')
        self.assertEqual(distroi.name(), 'CentOS Linux')
        self.assertEqual(distroi.name(pretty=True), 'CentOS Linux 7.1.1503 (Core)')
        self.assertEqual(distroi.version(), '7.1.1503')
        self.assertEqual(distroi.version(pretty=True), '7.1.1503 (Core)')
        self.assertEqual(distroi.version(best=True), '7.1.1503')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'Core')
        self.assertEqual(distroi.major_version(), '7')
        self.assertEqual(distroi.minor_version(), '1')
        self.assertEqual(distroi.build_number(), '1503')

    def test_empty_dist_release(self):
        distro_release = os.path.join(SPECIAL, 'empty-release')

        distroi = distro.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(distroi.id(), 'empty')
        self.assertEqual(distroi.name(), '')
        self.assertEqual(distroi.name(pretty=True), '')
        self.assertEqual(distroi.version(), '')
        self.assertEqual(distroi.version(pretty=True), '')
        self.assertEqual(distroi.version(best=True), '')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), '')

    def test_fedora19_dist_release(self):
        distro_release = os.path.join(DISTROS, 'fedora19', 'etc',
                                      'fedora-release')

        distroi = distro.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(distroi.id(), 'fedora')
        self.assertEqual(distroi.name(), 'Fedora')
        self.assertEqual(distroi.name(pretty=True), u'Fedora 19 (Schr\u00F6dinger\u2019s Cat)')
        self.assertEqual(distroi.version(), '19')
        self.assertEqual(distroi.version(pretty=True), u'19 (Schr\u00F6dinger\u2019s Cat)')
        self.assertEqual(distroi.version(best=True), '19')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), u'Schr\u00F6dinger\u2019s Cat')

    def test_fedora23_dist_release(self):
        distro_release = os.path.join(DISTROS, 'fedora23', 'etc',
                                      'fedora-release')

        distroi = distro.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(distroi.id(), 'fedora')
        self.assertEqual(distroi.name(), 'Fedora')
        self.assertEqual(distroi.name(pretty=True), 'Fedora 23 (Twenty Three)')
        self.assertEqual(distroi.version(), '23')
        self.assertEqual(distroi.version(pretty=True), '23 (Twenty Three)')
        self.assertEqual(distroi.version(best=True), '23')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'Twenty Three')

    def test_kvmibm1_dist_release(self):
        distro_release = os.path.join(DISTROS, 'kvmibm1', 'etc',
                                      'base-release')

        distroi = distro.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(distroi.id(), 'base')
        self.assertEqual(distroi.name(), 'KVM for IBM z Systems')
        self.assertEqual(distroi.name(pretty=True), 'KVM for IBM z Systems 1.1.1 (Z)')
        self.assertEqual(distroi.version(), '1.1.1')
        self.assertEqual(distroi.version(pretty=True), '1.1.1 (Z)')
        self.assertEqual(distroi.version(best=True), '1.1.1')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'Z')

    def test_mageia5_dist_release(self):
        distro_release = os.path.join(DISTROS, 'mageia5', 'etc',
                                      'mageia-release')

        distroi = distro.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(distroi.id(), 'mageia')
        self.assertEqual(distroi.name(), 'Mageia')
        self.assertEqual(distroi.name(pretty=True), 'Mageia 5 (Official)')
        self.assertEqual(distroi.version(), '5')
        self.assertEqual(distroi.version(pretty=True), '5 (Official)')
        self.assertEqual(distroi.version(best=True), '5')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'Official')

    def test_opensuse42_dist_release(self):
        distro_release = os.path.join(DISTROS, 'opensuse42', 'etc',
                                      'SuSE-release')

        distroi = distro.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(distroi.id(), 'suse')
        self.assertEqual(distroi.name(), 'openSUSE')
        self.assertEqual(distroi.name(pretty=True), 'openSUSE 42.1 (x86_64)')
        self.assertEqual(distroi.version(), '42.1')
        self.assertEqual(distroi.version(pretty=True), '42.1 (x86_64)')
        self.assertEqual(distroi.version(best=True), '42.1')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'x86_64')
        self.assertEqual(distroi.major_version(), '42')
        self.assertEqual(distroi.minor_version(), '1')
        self.assertEqual(distroi.build_number(), '')

    def test_oracle7_dist_release(self):
        distro_release = os.path.join(DISTROS, 'oracle7', 'etc',
                                      'oracle-release')

        distroi = distro.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(distroi.id(), 'oracle')
        self.assertEqual(distroi.name(), 'Oracle Linux Server')
        self.assertEqual(distroi.name(pretty=True), 'Oracle Linux Server 7.1')
        self.assertEqual(distroi.version(), '7.1')
        self.assertEqual(distroi.version(pretty=True), '7.1')
        self.assertEqual(distroi.version(best=True), '7.1')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), '')

    def test_rhel6_dist_release(self):
        distro_release = os.path.join(DISTROS, 'rhel6', 'etc',
                                      'redhat-release')

        distroi = distro.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(distroi.id(), 'rhel')
        self.assertEqual(distroi.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            distroi.name(pretty=True),
            'Red Hat Enterprise Linux Server 6.5 (Santiago)')
        self.assertEqual(distroi.version(), '6.5')
        self.assertEqual(distroi.version(pretty=True), '6.5 (Santiago)')
        self.assertEqual(distroi.version(best=True), '6.5')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'Santiago')
        self.assertEqual(distroi.version_parts(), ('6', '5', ''))

    def test_rhel7_dist_release(self):
        distro_release = os.path.join(DISTROS, 'rhel7', 'etc',
                                      'redhat-release')

        distroi = distro.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(distroi.id(), 'rhel')
        self.assertEqual(distroi.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            distroi.name(pretty=True),
            'Red Hat Enterprise Linux Server 7.0 (Maipo)')
        self.assertEqual(distroi.version(), '7.0')
        self.assertEqual(distroi.version(pretty=True), '7.0 (Maipo)')
        self.assertEqual(distroi.version(best=True), '7.0')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'Maipo')
        self.assertEqual(distroi.version_parts(), ('7', '0', ''))

    def test_slackware14_dist_release(self):
        distro_release = os.path.join(DISTROS, 'slackware14', 'etc',
                                      'slackware-version')

        distroi = distro.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(distroi.id(), 'slackware')
        self.assertEqual(distroi.name(), 'Slackware')
        self.assertEqual(distroi.name(pretty=True), 'Slackware 14.1')
        self.assertEqual(distroi.version(), '14.1')
        self.assertEqual(distroi.version(pretty=True), '14.1')
        self.assertEqual(distroi.version(best=True), '14.1')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), '')

    def test_sles12_dist_release(self):
        distro_release = os.path.join(DISTROS, 'sles12', 'etc', 'SuSE-release')

        distroi = distro.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(distroi.id(), 'suse')
        self.assertEqual(distroi.name(), 'SUSE Linux Enterprise Server')
        self.assertEqual(distroi.name(pretty=True),
                         'SUSE Linux Enterprise Server 12 (s390x)')
        self.assertEqual(distroi.version(), '12')
        self.assertEqual(distroi.version(pretty=True), '12 (s390x)')
        self.assertEqual(distroi.version(best=True), '12')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 's390x')


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
      * `amazon` - Amazon Linux
      * `cloudlinux` - CloudLinux OS
      * `gentoo` - GenToo Linux
      * `ibm_powerkvm` - IBM PowerKVM
      * `mandriva` - Mandriva Linux
      * `parallels` - Parallels
      * `pidora` - Pidora (Fedora remix for Raspberry Pi)
      * `raspbian` - Raspbian
      * `scientific` - Scientific Linux
      * `xenserver` - XenServer
    """

    def test_arch_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'arch'))

        distroi = distro.LinuxDistribution()

        self.assertEqual(distroi.id(), 'arch')
        self.assertEqual(distroi.name(), 'Arch Linux')
        self.assertEqual(distroi.name(pretty=True), 'Arch Linux')
        # Arch Linux has a continuous release concept:
        self.assertEqual(distroi.version(), '')
        self.assertEqual(distroi.version(pretty=True), '')
        self.assertEqual(distroi.version(best=True), '')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), '')

        # Test the info from the searched distro release file
        # Does not have one; The empty /etc/arch-release file is not
        # considered a valid distro release file:
        self.assertEqual(distroi.distro_release_file, '')
        self.assertEqual(len(distroi.distro_release_info()), 0)

    def test_centos5_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'centos5'))

        distroi = distro.LinuxDistribution()

        self.assertEqual(distroi.id(), 'centos')
        self.assertEqual(distroi.name(), 'CentOS')
        self.assertEqual(distroi.name(pretty=True), 'CentOS 5.11 (Final)')
        self.assertEqual(distroi.version(), '5.11')
        self.assertEqual(distroi.version(pretty=True), '5.11 (Final)')
        self.assertEqual(distroi.version(best=True), '5.11')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'Final')
        self.assertEqual(distroi.major_version(), '5')
        self.assertEqual(distroi.minor_version(), '11')
        self.assertEqual(distroi.build_number(), '')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(distroi.distro_release_file),
                         'centos-release')
        distro_info = distroi.distro_release_info()
        self.assertEqual(distro_info['id'], 'centos')
        self.assertEqual(distro_info['name'], 'CentOS')
        self.assertEqual(distro_info['version_id'], '5.11')
        self.assertEqual(distro_info['codename'], 'Final')

    def test_centos7_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'centos7'))

        distroi = distro.LinuxDistribution()

        self.assertEqual(distroi.id(), 'centos')
        self.assertEqual(distroi.name(), 'CentOS Linux')
        self.assertEqual(distroi.name(pretty=True), 'CentOS Linux 7 (Core)')
        self.assertEqual(distroi.version(), '7')
        self.assertEqual(distroi.version(pretty=True), '7 (Core)')
        self.assertEqual(distroi.version(best=True), '7.1.1503')
        self.assertEqual(distroi.like(), 'rhel fedora')
        self.assertEqual(distroi.codename(), 'Core')
        self.assertEqual(distroi.major_version(), '7')
        self.assertEqual(distroi.minor_version(), '')
        self.assertEqual(distroi.build_number(), '')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(distroi.distro_release_file),
                         'centos-release')
        distro_info = distroi.distro_release_info()
        self.assertEqual(distro_info['id'], 'centos')
        self.assertEqual(distro_info['name'], 'CentOS Linux')
        self.assertEqual(distro_info['version_id'], '7.1.1503')
        self.assertEqual(distro_info['codename'], 'Core')

    def test_debian8_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'debian8'))

        distroi = distro.LinuxDistribution()

        self.assertEqual(distroi.id(), 'debian')
        self.assertEqual(distroi.name(), 'Debian GNU/Linux')
        self.assertEqual(distroi.name(pretty=True), 'Debian GNU/Linux 8 (jessie)')
        self.assertEqual(distroi.version(), '8')
        self.assertEqual(distroi.version(pretty=True), '8 (jessie)')
        self.assertEqual(distroi.version(best=True), '8.2')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'jessie')

        # Test the info from the searched distro release file
        # Does not have one:
        self.assertEqual(distroi.distro_release_file, '')
        self.assertEqual(len(distroi.distro_release_info()), 0)

    def test_exherbo_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'exherbo'))

        distroi = distro.LinuxDistribution()

        self.assertEqual(distroi.id(), 'exherbo')
        self.assertEqual(distroi.name(), 'Exherbo')
        self.assertEqual(distroi.name(pretty=True), 'Exherbo Linux')
        self.assertEqual(distroi.version(), '')
        self.assertEqual(distroi.version(pretty=True), '')
        self.assertEqual(distroi.version(best=True), '')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), '')

    def test_fedora19_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'fedora19'))

        distroi = distro.LinuxDistribution()

        self.assertEqual(distroi.id(), 'fedora')
        self.assertEqual(distroi.name(), 'Fedora')
        self.assertEqual(distroi.name(pretty=True), u'Fedora 19 (Schr\u00F6dinger\u2019s Cat)')
        self.assertEqual(distroi.version(), '19')
        self.assertEqual(distroi.version(pretty=True), u'19 (Schr\u00F6dinger\u2019s Cat)')
        self.assertEqual(distroi.version(best=True), '19')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), u'Schr\u00F6dinger\u2019s Cat')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(distroi.distro_release_file),
                         'fedora-release')
        distro_info = distroi.distro_release_info()
        self.assertEqual(distro_info['id'], 'fedora')
        self.assertEqual(distro_info['name'], 'Fedora')
        self.assertEqual(distro_info['version_id'], '19')
        self.assertEqual(distro_info['codename'], u'Schr\u00F6dinger\u2019s Cat')

    def test_fedora23_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'fedora23'))

        distroi = distro.LinuxDistribution()

        self.assertEqual(distroi.id(), 'fedora')
        self.assertEqual(distroi.name(), 'Fedora')
        self.assertEqual(distroi.name(pretty=True), 'Fedora 23 (Twenty Three)')
        self.assertEqual(distroi.version(), '23')
        self.assertEqual(distroi.version(pretty=True), '23 (Twenty Three)')
        self.assertEqual(distroi.version(best=True), '23')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'Twenty Three')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(distroi.distro_release_file),
                         'fedora-release')
        distro_info = distroi.distro_release_info()
        self.assertEqual(distro_info['id'], 'fedora')
        self.assertEqual(distro_info['name'], 'Fedora')
        self.assertEqual(distro_info['version_id'], '23')
        self.assertEqual(distro_info['codename'], 'Twenty Three')

    def test_kvmibm1_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'kvmibm1'))

        distroi = distro.LinuxDistribution()

        self.assertEqual(distroi.id(), 'kvmibm')
        self.assertEqual(distroi.name(), 'KVM for IBM z Systems')
        self.assertEqual(distroi.name(pretty=True), 'KVM for IBM z Systems 1.1.1 (Z)')
        self.assertEqual(distroi.version(), '1.1.1')
        self.assertEqual(distroi.version(pretty=True), '1.1.1 (Z)')
        self.assertEqual(distroi.version(best=True), '1.1.1')
        self.assertEqual(distroi.like(), 'rhel fedora')
        self.assertEqual(distroi.codename(), 'Z')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(distroi.distro_release_file),
                         'base-release')
        distro_info = distroi.distro_release_info()
        self.assertEqual(distro_info['id'], 'base')
        self.assertEqual(distro_info['name'], 'KVM for IBM z Systems')
        self.assertEqual(distro_info['version_id'], '1.1.1')
        self.assertEqual(distro_info['codename'], 'Z')

    def test_linuxmint17_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'linuxmint17'))

        distroi = distro.LinuxDistribution()

        # Note: LinuxMint 17 actually *does* have Ubuntu 14.04 data in its
        #       os-release file. See discussion in GitHub issue #78.

        self.assertEqual(distroi.id(), 'ubuntu')
        self.assertEqual(distroi.name(), 'Ubuntu')
        self.assertEqual(distroi.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(distroi.version(), '14.04')
        self.assertEqual(distroi.version(pretty=True), '14.04 (Trusty Tahr)')
        self.assertEqual(distroi.version(best=True), '14.04.3')
        self.assertEqual(distroi.like(), 'debian')
        self.assertEqual(distroi.codename(), 'Trusty Tahr')

        # Test the info from the searched distro release file
        # Does not have one:
        self.assertEqual(distroi.distro_release_file, '')
        self.assertEqual(len(distroi.distro_release_info()), 0)

    def test_mageia5_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'mageia5'))

        distroi = distro.LinuxDistribution()

        self.assertEqual(distroi.id(), 'mageia')
        self.assertEqual(distroi.name(), 'Mageia')
        self.assertEqual(distroi.name(pretty=True), 'Mageia 5')
        self.assertEqual(distroi.version(), '5')
        self.assertEqual(distroi.version(pretty=True), '5 (thornicroft)')
        self.assertEqual(distroi.version(best=True), '5')
        self.assertEqual(distroi.like(), 'mandriva fedora')
        # TODO: Codename differs between distro release file and lsb_release.
        self.assertEqual(distroi.codename(), 'thornicroft')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(distroi.distro_release_file),
                         'mageia-release')
        distro_info = distroi.distro_release_info()
        self.assertEqual(distro_info['id'], 'mageia')
        self.assertEqual(distro_info['name'], 'Mageia')
        self.assertEqual(distro_info['version_id'], '5')
        self.assertEqual(distro_info['codename'], 'Official')

    def test_opensuse42_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'opensuse42'))

        distroi = distro.LinuxDistribution()

        self.assertEqual(distroi.id(), 'opensuse')
        self.assertEqual(distroi.name(), 'openSUSE Leap')
        self.assertEqual(distroi.name(pretty=True), 'openSUSE Leap 42.1 (x86_64)')
        self.assertEqual(distroi.version(), '42.1')
        self.assertEqual(distroi.version(pretty=True), '42.1 (x86_64)')
        self.assertEqual(distroi.version(best=True), '42.1')
        self.assertEqual(distroi.like(), 'suse')
        self.assertEqual(distroi.codename(), 'x86_64')
        self.assertEqual(distroi.major_version(), '42')
        self.assertEqual(distroi.minor_version(), '1')
        self.assertEqual(distroi.build_number(), '')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(distroi.distro_release_file),
                         'SuSE-release')
        distro_info = distroi.distro_release_info()
        self.assertEqual(distro_info['id'], 'SuSE')
        self.assertEqual(distro_info['name'], 'openSUSE')
        self.assertEqual(distro_info['version_id'], '42.1')
        self.assertEqual(distro_info['codename'], 'x86_64')

    def test_oracle7_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'oracle7'))

        distroi = distro.LinuxDistribution()

        self.assertEqual(distroi.id(), 'oracle')
        self.assertEqual(distroi.name(), 'Oracle Linux Server')
        self.assertEqual(distroi.name(pretty=True), 'Oracle Linux Server 7.1')
        self.assertEqual(distroi.version(), '7.1')
        self.assertEqual(distroi.version(pretty=True), '7.1')
        self.assertEqual(distroi.version(best=True), '7.1')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), '')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(distroi.distro_release_file),
                         'oracle-release')
        distro_info = distroi.distro_release_info()
        self.assertEqual(distro_info['id'], 'oracle')
        self.assertEqual(distro_info['name'], 'Oracle Linux Server')
        self.assertEqual(distro_info['version_id'], '7.1')
        self.assertTrue('codename' not in distro_info)

    def test_rhel6_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'rhel6'))

        distroi = distro.LinuxDistribution()

        self.assertEqual(distroi.id(), 'rhel')
        self.assertEqual(distroi.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            distroi.name(pretty=True),
            'Red Hat Enterprise Linux Server 6.5 (Santiago)')
        self.assertEqual(distroi.version(), '6.5')
        self.assertEqual(distroi.version(pretty=True), '6.5 (Santiago)')
        self.assertEqual(distroi.version(best=True), '6.5')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'Santiago')
        self.assertEqual(distroi.version_parts(), ('6', '5', ''))

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(distroi.distro_release_file),
                         'redhat-release')
        distro_info = distroi.distro_release_info()
        self.assertEqual(distro_info['id'], 'redhat')
        self.assertEqual(distro_info['name'],
                         'Red Hat Enterprise Linux Server')
        self.assertEqual(distro_info['version_id'], '6.5')
        self.assertEqual(distro_info['codename'], 'Santiago')

    def test_rhel7_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'rhel7'))

        distroi = distro.LinuxDistribution()

        self.assertEqual(distroi.id(), 'rhel')
        self.assertEqual(distroi.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            distroi.name(pretty=True),
            'Red Hat Enterprise Linux Server 7.0 (Maipo)')
        self.assertEqual(distroi.version(), '7.0')
        self.assertEqual(distroi.version(pretty=True), '7.0 (Maipo)')
        self.assertEqual(distroi.version(best=True), '7.0')
        self.assertEqual(distroi.like(), 'fedora')
        self.assertEqual(distroi.codename(), 'Maipo')
        self.assertEqual(distroi.version_parts(), ('7', '0', ''))

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(distroi.distro_release_file),
                         'redhat-release')
        distro_info = distroi.distro_release_info()
        self.assertEqual(distro_info['id'], 'redhat')
        self.assertEqual(distro_info['name'],
                         'Red Hat Enterprise Linux Server')
        self.assertEqual(distro_info['version_id'], '7.0')
        self.assertEqual(distro_info['codename'], 'Maipo')

    def test_slackware14_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'slackware14'))

        distroi = distro.LinuxDistribution()

        self.assertEqual(distroi.id(), 'slackware')
        self.assertEqual(distroi.name(), 'Slackware')
        self.assertEqual(distroi.name(pretty=True), 'Slackware 14.1')
        self.assertEqual(distroi.version(), '14.1')
        self.assertEqual(distroi.version(pretty=True), '14.1')
        self.assertEqual(distroi.version(best=True), '14.1')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), '')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(distroi.distro_release_file),
                         'slackware-version')
        distro_info = distroi.distro_release_info()
        self.assertEqual(distro_info['id'], 'slackware')
        self.assertEqual(distro_info['name'], 'Slackware')
        self.assertEqual(distro_info['version_id'], '14.1')
        self.assertTrue('codename' not in distro_info)

    def test_sles12_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'sles12'))

        distroi = distro.LinuxDistribution()

        self.assertEqual(distroi.id(), 'sles')
        self.assertEqual(distroi.name(), 'SLES')
        self.assertEqual(distroi.name(pretty=True),
                         'SUSE Linux Enterprise Server 12 SP1')
        self.assertEqual(distroi.version(), '12.1')
        self.assertEqual(distroi.version(pretty=True), '12.1 (n/a)')
        self.assertEqual(distroi.version(best=True), '12.1')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'n/a')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(distroi.distro_release_file),
                         'SuSE-release')
        distro_info = distroi.distro_release_info()
        self.assertEqual(distro_info['id'], 'SuSE')
        self.assertEqual(distro_info['name'], 'SUSE Linux Enterprise Server')
        self.assertEqual(distro_info['version_id'], '12')
        self.assertEqual(distro_info['codename'], 's390x')

    def test_ubuntu14_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'ubuntu14'))

        distroi = distro.LinuxDistribution()

        self.assertEqual(distroi.id(), 'ubuntu')
        self.assertEqual(distroi.name(), 'Ubuntu')
        self.assertEqual(distroi.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(distroi.version(), '14.04')
        self.assertEqual(distroi.version(pretty=True), '14.04 (Trusty Tahr)')
        self.assertEqual(distroi.version(best=True), '14.04.3')
        self.assertEqual(distroi.like(), 'debian')
        self.assertEqual(distroi.codename(), 'Trusty Tahr')

        # Test the info from the searched distro release file
        # Does not have one; /etc/debian_version is not considered a distro
        # release file:
        self.assertEqual(distroi.distro_release_file, '')
        self.assertEqual(len(distroi.distro_release_info()), 0)

    def test_unknowndistro_release(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'distro',
                                            'unknowndistro'))

        distroi = distro.LinuxDistribution()

        self.assertEqual(distroi.id(), 'unknowndistro')
        self.assertEqual(distroi.name(), 'Unknown Distro')
        self.assertEqual(distroi.name(pretty=True),
                         'Unknown Distro 1.0 (Unknown Codename)')
        self.assertEqual(distroi.version(), '1.0')
        self.assertEqual(distroi.version(pretty=True), '1.0 (Unknown Codename)')
        self.assertEqual(distroi.version(best=True), '1.0')
        self.assertEqual(distroi.like(), '')
        self.assertEqual(distroi.codename(), 'Unknown Codename')


class TestGetAttr(DistroTestCase):
    """Test the consistency between the results of
    `{source}_release_attr()` and `{source}_release_info()` for all
    distros in `DISTROS`."""

    def test_os_release_attr(self):
        distros = os.listdir(DISTROS)
        for dist in distros:
            self._setup_for_distro(os.path.join(DISTROS, dist))

            distroi = distro.LinuxDistribution()

            info = distroi.os_release_info()
            for key in info.keys():
                self.assertEqual(info[key],
                                 distroi.os_release_attr(key),
                                 "distro: %s, key: %s" % (dist, key))

    def test_lsb_release_attr(self):
        distros = os.listdir(DISTROS)
        for dist in distros:
            self._setup_for_distro(os.path.join(DISTROS, dist))

            distroi = distro.LinuxDistribution()

            info = distroi.lsb_release_info()
            for key in info.keys():
                self.assertEqual(info[key],
                                 distroi.lsb_release_attr(key),
                                 "distro: %s, key: %s" % (distro, key))

    def test_distro_release_attr(self):
        distros = os.listdir(DISTROS)
        for dist in distros:
            self._setup_for_distro(os.path.join(DISTROS, dist))

            distroi = distro.LinuxDistribution()

            info = distroi.distro_release_info()
            for key in info.keys():
                self.assertEqual(info[key],
                                 distroi.distro_release_attr(key),
                                 "distro: %s, key: %s" % (distro, key))


class TestInfo(testtools.TestCase):

    def setUp(self):
        super(TestInfo, self).setUp()
        self.rhel7_os_release = os.path.join(DISTROS, 'rhel7', 'etc',
                                             'os-release')

    def test_info(self):
        distroi = distro.LinuxDistribution(False, self.rhel7_os_release, 'non')

        info = distroi.info()
        self.assertEqual(info['id'], 'rhel')
        self.assertEqual(info['version'], '7.0')
        self.assertEqual(info['like'], 'fedora')
        self.assertEqual(info['version_parts']['major'], '7')
        self.assertEqual(info['version_parts']['minor'], '0')
        self.assertEqual(info['version_parts']['build_number'], '')

    def test_none(self):
        distroi = distro.LinuxDistribution(False, 'non', 'non')

        info = distroi.info()
        self.assertEqual(info['id'], '')
        self.assertEqual(info['version'], '')
        self.assertEqual(info['like'], '')
        self.assertEqual(info['version_parts']['major'], '')
        self.assertEqual(info['version_parts']['minor'], '')
        self.assertEqual(info['version_parts']['build_number'], '')

    def test_linux_disribution(self):
        distroi = distro.LinuxDistribution(False, self.rhel7_os_release)
        i = distroi.linux_distribution()
        self.assertEqual(
            i, ('Red Hat Enterprise Linux Server', '7.0', 'Maipo'))

    def test_linux_disribution_full_false(self):
        distroi = distro.LinuxDistribution(False, self.rhel7_os_release)
        i = distroi.linux_distribution(full_distribution_name=False)
        self.assertEqual(i, ('rhel', '7.0', 'Maipo'))


class TestOSReleaseParsing(testtools.TestCase):
    """Test the parsing of os-release files."""

    def setUp(self):
        self.distroi = distro.LinuxDistribution(False, None, None)
        self.distroi.debug = True
        super(TestOSReleaseParsing, self).setUp()

    def test_kv_01_empty_file(self):
        props = self.distroi._parse_os_release_content(StringIO(
            '',
        ))
        self.assertEqual(len(props), 0)

    def test_kv_02_empty_line(self):
        props = self.distroi._parse_os_release_content(StringIO(
            '\n',
        ))
        self.assertEqual(len(props), 0)

    def test_kv_03_empty_line_with_crlf(self):
        props = self.distroi._parse_os_release_content(StringIO(
            '\r\n',
        ))
        self.assertEqual(len(props), 0)

    def test_kv_04_empty_line_with_just_cr(self):
        props = self.distroi._parse_os_release_content(StringIO(
            '\r',
        ))
        self.assertEqual(len(props), 0)

    def test_kv_05_comment(self):
        props = self.distroi._parse_os_release_content(StringIO(
            '# KEY=value\n'
        ))
        self.assertEqual(len(props), 0)

    def test_kv_06_empty_value(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY=\n'
        ))
        self.assertEqual(props.get('key', None),
            '')

    def test_kv_07_empty_value_single_quoted(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY=\'\'\n'
        ))
        self.assertEqual(props.get('key', None),
            '')

    def test_kv_08_empty_value_double_quoted(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY=""\n'
        ))
        self.assertEqual(props.get('key', None),
            '')

    def test_kv_09_word(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY=value\n'
        ))
        self.assertEqual(props.get('key', None),
            'value')

    def test_kv_10_word_no_newline(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY=value'
        ))
        self.assertEqual(props.get('key', None),
            'value')

    def test_kv_11_word_with_crlf(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY=value\r\n'
        ))
        self.assertEqual(props.get('key', None),
            'value')

    def test_kv_12_word_with_just_cr(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY=value\r'
        ))
        self.assertEqual(props.get('key', None),
            'value')

    def test_kv_13_word_with_multi_blanks(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY=  cmd   \n'
        ))
        self.assertEqual(props.get('key', None),
            '')
        # Note: Without quotes, this assigns the empty string, and 'cmd' is
        # a separate token that is being ignored (it would be a command
        # in the shell).

    def test_kv_14_unquoted_words(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY=value cmd\n'
        ))
        self.assertEqual(props.get('key', None),
            'value')

    def test_kv_15_double_quoted_words(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY="a simple value" cmd\n'
        ))
        self.assertEqual(props.get('key', None),
            'a simple value')

    def test_kv_16_double_quoted_words_with_multi_blanks(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY=" a  simple   value "\n'
        ))
        self.assertEqual(props.get('key', None),
            ' a  simple   value ')

    def test_kv_17_double_quoted_word_with_single_quote(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY="it\'s value"\n'
        ))
        self.assertEqual(props.get('key', None),
            'it\'s value')

    def test_kv_18_double_quoted_word_with_double_quote(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY="a \\"bold\\" move"\n'
        ))
        self.assertEqual(props.get('key', None),
            'a "bold" move')

    def test_kv_19_single_quoted_words(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY=\'a simple value\'\n'
        ))
        self.assertEqual(props.get('key', None),
            'a simple value')

    def test_kv_20_single_quoted_words_with_multi_blanks(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY=\' a  simple   value \'\n'
        ))
        self.assertEqual(props.get('key', None),
            ' a  simple   value ')

    def test_kv_21_single_quoted_word_with_double_quote(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY=\'a "bold" move\'\n'
        ))
        self.assertEqual(props.get('key', None),
            'a "bold" move')

    def test_kv_22_quoted_unicode_wordchar(self):
        # "wordchar" means it is in the shlex.wordchars variable.
        props = self.distroi._parse_os_release_content(StringIO(
            u'KEY="wordchar: \u00CA (E accent grave)"\n'
        ))
        self.assertEqual(props.get('key', None),
            u'wordchar: \u00CA (E accent grave)')

    def test_kv_23_quoted_unicode_non_wordchar(self):
        # "non-wordchar" means it is not in the shlex.wordchars variable.
        props = self.distroi._parse_os_release_content(StringIO(
            u'KEY="non-wordchar: \u00A1 (inverted exclamation mark)"\n'
        ))
        self.assertEqual(props.get('key', None),
            u'non-wordchar: \u00A1 (inverted exclamation mark)')

    def test_kv_24_double_quoted_entire_single_quoted_word(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY="\'value\'"\n'
        ))
        self.assertEqual(props.get('key', None),
            "'value'")

    def test_kv_25_single_quoted_entire_double_quoted_word(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY=\'"value"\'\n'
        ))
        self.assertEqual(props.get('key', None),
            '"value"')

    def test_kv_26_double_quoted_multiline(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY="a multi\n'
            'line value"\n'
        ))
        self.assertEqual(props.get('key', None),
            'a multi\nline value')
        # TODO: Find out why the result is not 'a multi line value'

    def test_kv_27_double_quoted_multiline_2(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY="a multi\n'
            'line=value"\n'
        ))
        self.assertEqual(props.get('key', None),
            'a multi\nline=value')
        # TODO: Find out why the result is not 'a multi line=value'

    def test_kv_28_double_quoted_word_with_equal(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY="var=value"\n'
        ))
        self.assertEqual(props.get('key', None),
            'var=value')

    def test_kv_29_single_quoted_word_with_equal(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY=\'var=value\'\n'
        ))
        self.assertEqual(props.get('key', None),
            'var=value')

    def test_kx_01(self):
        props = self.distroi._parse_os_release_content(StringIO(
            'KEY1=value1\n'
            'KEY2="value  2"\n'
        ))
        self.assertEqual(props.get('key1', None),
            'value1')
        self.assertEqual(props.get('key2', None),
            'value  2')

    def test_kx_02(self):
        props = self.distroi._parse_os_release_content(StringIO(
            '# KEY1=value1\n'
            'KEY2="value  2"\n'
        ))
        self.assertEqual(props.get('key1', None),
            None)
        self.assertEqual(props.get('key2', None),
            'value  2')


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

        self.assertEqual(distro.linux_distribution(),
            MODULE_DISTROI.linux_distribution(full_distribution_name=True))
        self.assertEqual(distro.linux_distribution(full_distribution_name=True),
            MODULE_DISTROI.linux_distribution())
        self.assertEqual(distro.linux_distribution(full_distribution_name=False),
            MODULE_DISTROI.linux_distribution(full_distribution_name=False))

        self.assertEqual(distro.id(),
            MODULE_DISTROI.id())

        self.assertEqual(distro.name(),
            MODULE_DISTROI.name(pretty=False))
        self.assertEqual(distro.name(pretty=False),
            MODULE_DISTROI.name())
        self.assertEqual(distro.name(pretty=True),
            MODULE_DISTROI.name(pretty=True))

        self.assertEqual(distro.version(),
            MODULE_DISTROI.version(pretty=False))
        self.assertEqual(distro.version(pretty=False),
            MODULE_DISTROI.version())
        self.assertEqual(distro.version(pretty=True),
            MODULE_DISTROI.version(pretty=True))
        self.assertEqual(distro.version(),
            MODULE_DISTROI.version(best=False))
        self.assertEqual(distro.version(best=False),
            MODULE_DISTROI.version())
        self.assertEqual(distro.version(best=True),
            MODULE_DISTROI.version(best=True))

        self.assertEqual(distro.version_parts(),
            MODULE_DISTROI.version_parts(best=False))
        self.assertEqual(distro.version_parts(best=False),
            MODULE_DISTROI.version_parts())
        self.assertEqual(distro.version_parts(best=True),
            MODULE_DISTROI.version_parts(best=True))

        self.assertEqual(distro.major_version(),
            MODULE_DISTROI.major_version(best=False))
        self.assertEqual(distro.major_version(best=False),
            MODULE_DISTROI.major_version())
        self.assertEqual(distro.major_version(best=True),
            MODULE_DISTROI.major_version(best=True))

        self.assertEqual(distro.minor_version(),
            MODULE_DISTROI.minor_version(best=False))
        self.assertEqual(distro.minor_version(best=False),
            MODULE_DISTROI.minor_version())
        self.assertEqual(distro.minor_version(best=True),
            MODULE_DISTROI.minor_version(best=True))

        self.assertEqual(distro.build_number(),
            MODULE_DISTROI.build_number(best=False))
        self.assertEqual(distro.build_number(best=False),
            MODULE_DISTROI.build_number())
        self.assertEqual(distro.build_number(best=True),
            MODULE_DISTROI.build_number(best=True))

        self.assertEqual(distro.like(),
            MODULE_DISTROI.like())

        self.assertEqual(distro.codename(),
            MODULE_DISTROI.codename())

        self.assertEqual(distro.info(),
            MODULE_DISTROI.info())

        self.assertEqual(distro.os_release_info(),
            MODULE_DISTROI.os_release_info())

        self.assertEqual(distro.lsb_release_info(),
            MODULE_DISTROI.lsb_release_info())

        self.assertEqual(distro.distro_release_info(),
            MODULE_DISTROI.distro_release_info())

        os_release_keys = [
            'name',
            'version',
            'id',
            'id_like',
            'pretty_name',
            'version_id',
            'codename',
        ]
        for key in os_release_keys:
            self.assertEqual(distro.os_release_attr(key),
                MODULE_DISTROI.os_release_attr(key))

        lsb_release_keys = [
            'distributor_id',
            'description',
            'release',
            'codename',
        ]
        for key in lsb_release_keys:
            self.assertEqual(distro.lsb_release_attr(key),
                MODULE_DISTROI.lsb_release_attr(key))

        distro_release_keys = [
            'id',
            'name',
            'version_id',
            'codename',
        ]
        for key in distro_release_keys:
            self.assertEqual(distro.distro_release_attr(key),
                MODULE_DISTROI.distro_release_attr(key))


class TestRepr(testtools.TestCase):
    """Test the __repr__() method."""

    def test_repr(self):
        # We test that the class name and the names of all instance attributes
        # show up in the repr() string.
        repr_str = repr(distro._distroi)
        self.assertIn("LinuxDistribution", repr_str)
        for attr in MODULE_DISTROI.__dict__.keys():
            self.assertIn(attr+'=', repr_str)

