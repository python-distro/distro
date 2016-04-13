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


import dist


RESOURCES = os.path.join('tests', 'resources')
DISTROS = os.path.join(RESOURCES, 'distros')
TESTDISTROS = os.path.join(RESOURCES, 'testdistros')
SPECIAL = os.path.join(RESOURCES, 'special')

RELATIVE_UNIXCONFDIR = dist._UNIXCONFDIR.lstrip('/')

MODULE_DISTI = dist._disti


class DistroTestCase(testtools.TestCase):
    """A base class for any testcase classes that test the distributions
    represented in the `DISTROS` subtree."""

    def setUp(self):
        super(DistroTestCase, self).setUp()
        # The environment stays the same across all testcases, so we
        # save and restore the PATH env var in each test case that
        # changes it:
        self._saved_path = os.environ["PATH"]
        self._saved_UNIXCONFDIR = dist._UNIXCONFDIR

    def tearDown(self):
        super(DistroTestCase, self).tearDown()
        os.environ["PATH"] = self._saved_path
        dist._UNIXCONFDIR = self._saved_UNIXCONFDIR

    def _setup_for_distro(self, distro_root):
        distro_bin = os.path.join(os.getcwd(), distro_root, 'bin')
        # We don't want to pick up a possibly present lsb_release in the
        # distro that runs this test, so we use a PATH with only one entry:
        os.environ["PATH"] = distro_bin
        dist._UNIXCONFDIR = os.path.join(distro_root, RELATIVE_UNIXCONFDIR)


class TestOSRelease(testtools.TestCase):

    def setUp(self):
        super(TestOSRelease, self).setUp()

    def test_arch_os_release(self):
        os_release = os.path.join(DISTROS, 'arch', 'etc', 'os-release')

        disti = dist.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(disti.id(), 'arch')
        self.assertEqual(disti.name(), 'Arch Linux')
        self.assertEqual(disti.name(pretty=True), 'Arch Linux')
        self.assertEqual(disti.version(), '')
        self.assertEqual(disti.version(pretty=True), '')
        self.assertEqual(disti.version(best=True), '')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), '')

    def test_centos7_os_release(self):
        os_release = os.path.join(DISTROS, 'centos7', 'etc', 'os-release')

        disti = dist.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(disti.id(), 'centos')
        self.assertEqual(disti.name(), 'CentOS Linux')
        self.assertEqual(disti.name(pretty=True), 'CentOS Linux 7 (Core)')
        self.assertEqual(disti.version(), '7')
        self.assertEqual(disti.version(pretty=True), '7 (Core)')
        self.assertEqual(disti.version(best=True), '7')
        self.assertEqual(disti.like(), 'rhel fedora')
        self.assertEqual(disti.codename(), 'Core')

    def test_debian8_os_release(self):
        os_release = os.path.join(DISTROS, 'debian8', 'etc', 'os-release')

        disti = dist.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(disti.id(), 'debian')
        self.assertEqual(disti.name(), 'Debian GNU/Linux')
        self.assertEqual(disti.name(pretty=True), 'Debian GNU/Linux 8 (jessie)')
        self.assertEqual(disti.version(), '8')
        self.assertEqual(disti.version(pretty=True), '8 (jessie)')
        self.assertEqual(disti.version(best=True), '8')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'jessie')

    def test_fedora19_os_release(self):
        os_release = os.path.join(DISTROS, 'fedora19', 'etc', 'os-release')

        disti = dist.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(disti.id(), 'fedora')
        self.assertEqual(disti.name(), 'Fedora')
        self.assertEqual(disti.name(pretty=True), u'Fedora 19 (Schr\u00F6dinger\u2019s Cat)')
        self.assertEqual(disti.version(), '19')
        self.assertEqual(disti.version(pretty=True), u'19 (Schr\u00F6dinger\u2019s Cat)')
        self.assertEqual(disti.version(best=True), '19')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), u'Schr\u00F6dinger\u2019s Cat')

    def test_fedora23_os_release(self):
        os_release = os.path.join(DISTROS, 'fedora23', 'etc', 'os-release')

        disti = dist.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(disti.id(), 'fedora')
        self.assertEqual(disti.name(), 'Fedora')
        self.assertEqual(disti.name(pretty=True), 'Fedora 23 (Twenty Three)')
        self.assertEqual(disti.version(), '23')
        self.assertEqual(disti.version(pretty=True), '23 (Twenty Three)')
        self.assertEqual(disti.version(best=True), '23')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'Twenty Three')

    def test_kvmibm1_os_release(self):
        os_release = os.path.join(DISTROS, 'kvmibm1', 'etc', 'os-release')

        disti = dist.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(disti.id(), 'kvmibm')
        self.assertEqual(disti.name(), 'KVM for IBM z Systems')
        self.assertEqual(disti.name(pretty=True), 'KVM for IBM z Systems 1.1.1 (Z)')
        self.assertEqual(disti.version(), '1.1.1')
        self.assertEqual(disti.version(pretty=True), '1.1.1 (Z)')
        self.assertEqual(disti.version(best=True), '1.1.1')
        self.assertEqual(disti.like(), 'rhel fedora')
        self.assertEqual(disti.codename(), 'Z')

    def test_mageia5_os_release(self):
        os_release = os.path.join(DISTROS, 'mageia5', 'etc', 'os-release')

        disti = dist.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(disti.id(), 'mageia')
        self.assertEqual(disti.name(), 'Mageia')
        self.assertEqual(disti.name(pretty=True), 'Mageia 5')
        self.assertEqual(disti.version(), '5')
        self.assertEqual(disti.version(pretty=True), '5')
        self.assertEqual(disti.version(best=True), '5')
        self.assertEqual(disti.like(), 'mandriva fedora')
        self.assertEqual(disti.codename(), '')

    def test_opensuse42_os_release(self):
        os_release = os.path.join(DISTROS, 'opensuse42', 'etc', 'os-release')

        disti = dist.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(disti.id(), 'opensuse')
        self.assertEqual(disti.name(), 'openSUSE Leap')
        self.assertEqual(disti.name(pretty=True), 'openSUSE Leap 42.1 (x86_64)')
        self.assertEqual(disti.version(), '42.1')
        self.assertEqual(disti.version(pretty=True), '42.1')
        self.assertEqual(disti.version(best=True), '42.1')
        self.assertEqual(disti.like(), 'suse')
        self.assertEqual(disti.codename(), '')

    def test_rhel7_os_release(self):
        os_release = os.path.join(DISTROS, 'rhel7', 'etc', 'os-release')

        disti = dist.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(disti.id(), 'rhel')
        self.assertEqual(disti.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            disti.name(pretty=True),
            'Red Hat Enterprise Linux Server 7.0 (Maipo)')
        self.assertEqual(disti.version(), '7.0')
        self.assertEqual(disti.version(pretty=True), '7.0 (Maipo)')
        self.assertEqual(disti.version(best=True), '7.0')
        self.assertEqual(disti.like(), 'fedora')
        self.assertEqual(disti.codename(), 'Maipo')

    def test_slackware14_os_release(self):
        os_release = os.path.join(DISTROS, 'slackware14', 'etc', 'os-release')

        disti = dist.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(disti.id(), 'slackware')
        self.assertEqual(disti.name(), 'Slackware')
        self.assertEqual(disti.name(pretty=True), 'Slackware 14.1')
        self.assertEqual(disti.version(), '14.1')
        self.assertEqual(disti.version(pretty=True), '14.1')
        self.assertEqual(disti.version(best=True), '14.1')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), '')

    def test_sles12_os_release(self):
        os_release = os.path.join(DISTROS, 'sles12', 'etc', 'os-release')

        disti = dist.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(disti.id(), 'sles')
        self.assertEqual(disti.name(), 'SLES')
        self.assertEqual(disti.name(pretty=True),
                         'SUSE Linux Enterprise Server 12 SP1')
        self.assertEqual(disti.version(), '12.1')
        self.assertEqual(disti.version(pretty=True), '12.1')
        self.assertEqual(disti.version(best=True), '12.1')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), '')

    def test_ubuntu14_os_release(self):
        os_release = os.path.join(DISTROS, 'ubuntu14', 'etc', 'os-release')

        disti = dist.LinuxDistribution(False, os_release, 'non')

        self.assertEqual(disti.id(), 'ubuntu')
        self.assertEqual(disti.name(), 'Ubuntu')
        self.assertEqual(disti.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(disti.version(), '14.04')
        self.assertEqual(disti.version(pretty=True), '14.04 (Trusty Tahr)')
        self.assertEqual(disti.version(best=True), '14.04')
        self.assertEqual(disti.like(), 'debian')
        self.assertEqual(disti.codename(), 'Trusty Tahr')


class TestLSBRelease(DistroTestCase):

    def test_lsb_release_normal(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb',
                                            'ubuntu14_normal'))

        disti = dist.LinuxDistribution(True, 'non', 'non')

        self.assertEqual(disti.id(), 'ubuntu')
        self.assertEqual(disti.name(), 'Ubuntu')
        self.assertEqual(disti.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(disti.version(), '14.04')
        self.assertEqual(disti.version(pretty=True), '14.04 (trusty)')
        self.assertEqual(disti.version(best=True), '14.04')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'trusty')

    def test_lsb_release_nomodules(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb',
                                            'ubuntu14_nomodules'))

        disti = dist.LinuxDistribution(True, 'non', 'non')

        self.assertEqual(disti.id(), 'ubuntu')
        self.assertEqual(disti.name(), 'Ubuntu')
        self.assertEqual(disti.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(disti.version(), '14.04')
        self.assertEqual(disti.version(pretty=True), '14.04 (trusty)')
        self.assertEqual(disti.version(best=True), '14.04')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'trusty')

    def test_lsb_release_trailingblanks(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb',
                                            'ubuntu14_trailingblanks'))

        disti = dist.LinuxDistribution(True, 'non', 'non')

        self.assertEqual(disti.id(), 'ubuntu')
        self.assertEqual(disti.name(), 'Ubuntu')
        self.assertEqual(disti.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(disti.version(), '14.04')
        self.assertEqual(disti.version(pretty=True), '14.04 (trusty)')
        self.assertEqual(disti.version(best=True), '14.04')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'trusty')

    def test_lsb_release_rc001(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb', 'lsb_rc001'))
        try:
            disti = dist.LinuxDistribution(True, 'non', 'non')
            exc = None
        except Exception as _exc:
            exc = _exc
        self.assertEqual(isinstance(exc, subprocess.CalledProcessError), True)
        self.assertEqual(exc.returncode, 1)

    def test_lsb_release_rc002(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb', 'lsb_rc002'))
        try:
            disti = dist.LinuxDistribution(True, 'non', 'non')
            exc = None
        except Exception as _exc:
            exc = _exc
        self.assertEqual(isinstance(exc, subprocess.CalledProcessError), True)
        self.assertEqual(exc.returncode, 2)

    def test_lsb_release_rc126(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb', 'lsb_rc126'))
        try:
            disti = dist.LinuxDistribution(True, 'non', 'non')
            exc = None
        except Exception as _exc:
            exc = _exc
        self.assertEqual(isinstance(exc, subprocess.CalledProcessError), True)
        self.assertEqual(exc.returncode, 126)

    def test_lsb_release_rc130(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb', 'lsb_rc130'))
        try:
            disti = dist.LinuxDistribution(True, 'non', 'non')
            exc = None
        except Exception as _exc:
            exc = _exc
        self.assertEqual(isinstance(exc, subprocess.CalledProcessError), True)
        self.assertEqual(exc.returncode, 130)

    def test_lsb_release_rc255(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'lsb', 'lsb_rc255'))
        try:
            disti = dist.LinuxDistribution(True, 'non', 'non')
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

        disti = dist.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(disti.id(), 'arch')
        self.assertEqual(disti.name(), '')
        self.assertEqual(disti.name(pretty=True), '')
        self.assertEqual(disti.version(), '')
        self.assertEqual(disti.version(pretty=True), '')
        self.assertEqual(disti.version(best=True), '')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), '')

    def test_centos5_dist_release(self):
        distro_release = os.path.join(DISTROS, 'centos5', 'etc',
                                      'centos-release')
        disti = dist.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(disti.id(), 'centos')
        self.assertEqual(disti.name(), 'CentOS')
        self.assertEqual(disti.name(pretty=True), 'CentOS 5.11 (Final)')
        self.assertEqual(disti.version(), '5.11')
        self.assertEqual(disti.version(pretty=True), '5.11 (Final)')
        self.assertEqual(disti.version(best=True), '5.11')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'Final')
        self.assertEqual(disti.major_version(), '5')
        self.assertEqual(disti.minor_version(), '11')
        self.assertEqual(disti.build_number(), '')

    def test_centos7_dist_release(self):
        distro_release = os.path.join(DISTROS, 'centos7', 'etc',
                                      'centos-release')

        disti = dist.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(disti.id(), 'centos')
        self.assertEqual(disti.name(), 'CentOS Linux')
        self.assertEqual(disti.name(pretty=True), 'CentOS Linux 7.1.1503 (Core)')
        self.assertEqual(disti.version(), '7.1.1503')
        self.assertEqual(disti.version(pretty=True), '7.1.1503 (Core)')
        self.assertEqual(disti.version(best=True), '7.1.1503')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'Core')
        self.assertEqual(disti.major_version(), '7')
        self.assertEqual(disti.minor_version(), '1')
        self.assertEqual(disti.build_number(), '1503')

    def test_empty_dist_release(self):
        distro_release = os.path.join(SPECIAL, 'empty-release')

        disti = dist.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(disti.id(), 'empty')
        self.assertEqual(disti.name(), '')
        self.assertEqual(disti.name(pretty=True), '')
        self.assertEqual(disti.version(), '')
        self.assertEqual(disti.version(pretty=True), '')
        self.assertEqual(disti.version(best=True), '')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), '')

    def test_fedora19_dist_release(self):
        distro_release = os.path.join(DISTROS, 'fedora19', 'etc',
                                      'fedora-release')

        disti = dist.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(disti.id(), 'fedora')
        self.assertEqual(disti.name(), 'Fedora')
        self.assertEqual(disti.name(pretty=True), u'Fedora 19 (Schr\u00F6dinger\u2019s Cat)')
        self.assertEqual(disti.version(), '19')
        self.assertEqual(disti.version(pretty=True), u'19 (Schr\u00F6dinger\u2019s Cat)')
        self.assertEqual(disti.version(best=True), '19')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), u'Schr\u00F6dinger\u2019s Cat')

    def test_fedora23_dist_release(self):
        distro_release = os.path.join(DISTROS, 'fedora23', 'etc',
                                      'fedora-release')

        disti = dist.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(disti.id(), 'fedora')
        self.assertEqual(disti.name(), 'Fedora')
        self.assertEqual(disti.name(pretty=True), 'Fedora 23 (Twenty Three)')
        self.assertEqual(disti.version(), '23')
        self.assertEqual(disti.version(pretty=True), '23 (Twenty Three)')
        self.assertEqual(disti.version(best=True), '23')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'Twenty Three')

    def test_kvmibm1_dist_release(self):
        distro_release = os.path.join(DISTROS, 'kvmibm1', 'etc',
                                      'base-release')

        disti = dist.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(disti.id(), 'base')
        self.assertEqual(disti.name(), 'KVM for IBM z Systems')
        self.assertEqual(disti.name(pretty=True), 'KVM for IBM z Systems 1.1.1 (Z)')
        self.assertEqual(disti.version(), '1.1.1')
        self.assertEqual(disti.version(pretty=True), '1.1.1 (Z)')
        self.assertEqual(disti.version(best=True), '1.1.1')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'Z')

    def test_mageia5_dist_release(self):
        distro_release = os.path.join(DISTROS, 'mageia5', 'etc',
                                      'mageia-release')

        disti = dist.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(disti.id(), 'mageia')
        self.assertEqual(disti.name(), 'Mageia')
        self.assertEqual(disti.name(pretty=True), 'Mageia 5 (Official)')
        self.assertEqual(disti.version(), '5')
        self.assertEqual(disti.version(pretty=True), '5 (Official)')
        self.assertEqual(disti.version(best=True), '5')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'Official')

    def test_opensuse42_dist_release(self):
        distro_release = os.path.join(DISTROS, 'opensuse42', 'etc',
                                      'SuSE-release')

        disti = dist.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(disti.id(), 'suse')
        self.assertEqual(disti.name(), 'openSUSE')
        self.assertEqual(disti.name(pretty=True), 'openSUSE 42.1 (x86_64)')
        self.assertEqual(disti.version(), '42.1')
        self.assertEqual(disti.version(pretty=True), '42.1 (x86_64)')
        self.assertEqual(disti.version(best=True), '42.1')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'x86_64')
        self.assertEqual(disti.major_version(), '42')
        self.assertEqual(disti.minor_version(), '1')
        self.assertEqual(disti.build_number(), '')

    def test_oracle7_dist_release(self):
        distro_release = os.path.join(DISTROS, 'oracle7', 'etc',
                                      'oracle-release')

        disti = dist.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(disti.id(), 'oracle')
        self.assertEqual(disti.name(), 'Oracle Linux Server')
        self.assertEqual(disti.name(pretty=True), 'Oracle Linux Server 7.1')
        self.assertEqual(disti.version(), '7.1')
        self.assertEqual(disti.version(pretty=True), '7.1')
        self.assertEqual(disti.version(best=True), '7.1')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), '')

    def test_rhel6_dist_release(self):
        distro_release = os.path.join(DISTROS, 'rhel6', 'etc',
                                      'redhat-release')

        disti = dist.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(disti.id(), 'rhel')
        self.assertEqual(disti.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            disti.name(pretty=True),
            'Red Hat Enterprise Linux Server 6.5 (Santiago)')
        self.assertEqual(disti.version(), '6.5')
        self.assertEqual(disti.version(pretty=True), '6.5 (Santiago)')
        self.assertEqual(disti.version(best=True), '6.5')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'Santiago')
        self.assertEqual(disti.version_parts(), ('6', '5', ''))

    def test_rhel7_dist_release(self):
        distro_release = os.path.join(DISTROS, 'rhel7', 'etc',
                                      'redhat-release')

        disti = dist.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(disti.id(), 'rhel')
        self.assertEqual(disti.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            disti.name(pretty=True),
            'Red Hat Enterprise Linux Server 7.0 (Maipo)')
        self.assertEqual(disti.version(), '7.0')
        self.assertEqual(disti.version(pretty=True), '7.0 (Maipo)')
        self.assertEqual(disti.version(best=True), '7.0')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'Maipo')
        self.assertEqual(disti.version_parts(), ('7', '0', ''))

    def test_slackware14_dist_release(self):
        distro_release = os.path.join(DISTROS, 'slackware14', 'etc',
                                      'slackware-version')

        disti = dist.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(disti.id(), 'slackware')
        self.assertEqual(disti.name(), 'Slackware')
        self.assertEqual(disti.name(pretty=True), 'Slackware 14.1')
        self.assertEqual(disti.version(), '14.1')
        self.assertEqual(disti.version(pretty=True), '14.1')
        self.assertEqual(disti.version(best=True), '14.1')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), '')

    def test_sles12_dist_release(self):
        distro_release = os.path.join(DISTROS, 'sles12', 'etc', 'SuSE-release')

        disti = dist.LinuxDistribution(False, 'non', distro_release)

        self.assertEqual(disti.id(), 'suse')
        self.assertEqual(disti.name(), 'SUSE Linux Enterprise Server')
        self.assertEqual(disti.name(pretty=True),
                         'SUSE Linux Enterprise Server 12 (s390x)')
        self.assertEqual(disti.version(), '12')
        self.assertEqual(disti.version(pretty=True), '12 (s390x)')
        self.assertEqual(disti.version(best=True), '12')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 's390x')


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

        disti = dist.LinuxDistribution()

        self.assertEqual(disti.id(), 'arch')
        self.assertEqual(disti.name(), 'Arch Linux')
        self.assertEqual(disti.name(pretty=True), 'Arch Linux')
        # Arch Linux has a continuous release concept:
        self.assertEqual(disti.version(), '')
        self.assertEqual(disti.version(pretty=True), '')
        self.assertEqual(disti.version(best=True), '')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), '')

        # Test the info from the searched distro release file
        # Does not have one; The empty /etc/arch-release file is not
        # considered a valid distro release file:
        self.assertEqual(disti.distro_release_file, '')
        self.assertEqual(len(disti.distro_release_info()), 0)

    def test_centos5_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'centos5'))

        disti = dist.LinuxDistribution()

        self.assertEqual(disti.id(), 'centos')
        self.assertEqual(disti.name(), 'CentOS')
        self.assertEqual(disti.name(pretty=True), 'CentOS 5.11 (Final)')
        self.assertEqual(disti.version(), '5.11')
        self.assertEqual(disti.version(pretty=True), '5.11 (Final)')
        self.assertEqual(disti.version(best=True), '5.11')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'Final')
        self.assertEqual(disti.major_version(), '5')
        self.assertEqual(disti.minor_version(), '11')
        self.assertEqual(disti.build_number(), '')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(disti.distro_release_file),
                         'centos-release')
        distro_info = disti.distro_release_info()
        self.assertEqual(distro_info['id'], 'centos')
        self.assertEqual(distro_info['name'], 'CentOS')
        self.assertEqual(distro_info['version_id'], '5.11')
        self.assertEqual(distro_info['codename'], 'Final')

    def test_centos7_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'centos7'))

        disti = dist.LinuxDistribution()

        self.assertEqual(disti.id(), 'centos')
        self.assertEqual(disti.name(), 'CentOS Linux')
        self.assertEqual(disti.name(pretty=True), 'CentOS Linux 7 (Core)')
        self.assertEqual(disti.version(), '7')
        self.assertEqual(disti.version(pretty=True), '7 (Core)')
        self.assertEqual(disti.version(best=True), '7.1.1503')
        self.assertEqual(disti.like(), 'rhel fedora')
        self.assertEqual(disti.codename(), 'Core')
        self.assertEqual(disti.major_version(), '7')
        self.assertEqual(disti.minor_version(), '')
        self.assertEqual(disti.build_number(), '')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(disti.distro_release_file),
                         'centos-release')
        distro_info = disti.distro_release_info()
        self.assertEqual(distro_info['id'], 'centos')
        self.assertEqual(distro_info['name'], 'CentOS Linux')
        self.assertEqual(distro_info['version_id'], '7.1.1503')
        self.assertEqual(distro_info['codename'], 'Core')

    def test_debian8_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'debian8'))

        disti = dist.LinuxDistribution()

        self.assertEqual(disti.id(), 'debian')
        self.assertEqual(disti.name(), 'Debian GNU/Linux')
        self.assertEqual(disti.name(pretty=True), 'Debian GNU/Linux 8 (jessie)')
        self.assertEqual(disti.version(), '8')
        self.assertEqual(disti.version(pretty=True), '8 (jessie)')
        self.assertEqual(disti.version(best=True), '8.2')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'jessie')

        # Test the info from the searched distro release file
        # Does not have one:
        self.assertEqual(disti.distro_release_file, '')
        self.assertEqual(len(disti.distro_release_info()), 0)

    def test_exherbo_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'exherbo'))

        disti = dist.LinuxDistribution()

        self.assertEqual(disti.id(), 'exherbo')
        self.assertEqual(disti.name(), 'Exherbo')
        self.assertEqual(disti.name(pretty=True), 'Exherbo Linux')
        self.assertEqual(disti.version(), '')
        self.assertEqual(disti.version(pretty=True), '')
        self.assertEqual(disti.version(best=True), '')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), '')

    def test_fedora19_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'fedora19'))

        disti = dist.LinuxDistribution()

        self.assertEqual(disti.id(), 'fedora')
        self.assertEqual(disti.name(), 'Fedora')
        self.assertEqual(disti.name(pretty=True), u'Fedora 19 (Schr\u00F6dinger\u2019s Cat)')
        self.assertEqual(disti.version(), '19')
        self.assertEqual(disti.version(pretty=True), u'19 (Schr\u00F6dinger\u2019s Cat)')
        self.assertEqual(disti.version(best=True), '19')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), u'Schr\u00F6dinger\u2019s Cat')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(disti.distro_release_file),
                         'fedora-release')
        distro_info = disti.distro_release_info()
        self.assertEqual(distro_info['id'], 'fedora')
        self.assertEqual(distro_info['name'], 'Fedora')
        self.assertEqual(distro_info['version_id'], '19')
        self.assertEqual(distro_info['codename'], u'Schr\u00F6dinger\u2019s Cat')

    def test_fedora23_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'fedora23'))

        disti = dist.LinuxDistribution()

        self.assertEqual(disti.id(), 'fedora')
        self.assertEqual(disti.name(), 'Fedora')
        self.assertEqual(disti.name(pretty=True), 'Fedora 23 (Twenty Three)')
        self.assertEqual(disti.version(), '23')
        self.assertEqual(disti.version(pretty=True), '23 (Twenty Three)')
        self.assertEqual(disti.version(best=True), '23')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'Twenty Three')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(disti.distro_release_file),
                         'fedora-release')
        distro_info = disti.distro_release_info()
        self.assertEqual(distro_info['id'], 'fedora')
        self.assertEqual(distro_info['name'], 'Fedora')
        self.assertEqual(distro_info['version_id'], '23')
        self.assertEqual(distro_info['codename'], 'Twenty Three')

    def test_kvmibm1_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'kvmibm1'))

        disti = dist.LinuxDistribution()

        self.assertEqual(disti.id(), 'kvmibm')
        self.assertEqual(disti.name(), 'KVM for IBM z Systems')
        self.assertEqual(disti.name(pretty=True), 'KVM for IBM z Systems 1.1.1 (Z)')
        self.assertEqual(disti.version(), '1.1.1')
        self.assertEqual(disti.version(pretty=True), '1.1.1 (Z)')
        self.assertEqual(disti.version(best=True), '1.1.1')
        self.assertEqual(disti.like(), 'rhel fedora')
        self.assertEqual(disti.codename(), 'Z')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(disti.distro_release_file),
                         'base-release')
        distro_info = disti.distro_release_info()
        self.assertEqual(distro_info['id'], 'base')
        self.assertEqual(distro_info['name'], 'KVM for IBM z Systems')
        self.assertEqual(distro_info['version_id'], '1.1.1')
        self.assertEqual(distro_info['codename'], 'Z')

    def test_mageia5_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'mageia5'))

        disti = dist.LinuxDistribution()

        self.assertEqual(disti.id(), 'mageia')
        self.assertEqual(disti.name(), 'Mageia')
        self.assertEqual(disti.name(pretty=True), 'Mageia 5')
        self.assertEqual(disti.version(), '5')
        self.assertEqual(disti.version(pretty=True), '5 (thornicroft)')
        self.assertEqual(disti.version(best=True), '5')
        self.assertEqual(disti.like(), 'mandriva fedora')
        # TODO: Codename differs between distro release file and lsb_release.
        self.assertEqual(disti.codename(), 'thornicroft')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(disti.distro_release_file),
                         'mageia-release')
        distro_info = disti.distro_release_info()
        self.assertEqual(distro_info['id'], 'mageia')
        self.assertEqual(distro_info['name'], 'Mageia')
        self.assertEqual(distro_info['version_id'], '5')
        self.assertEqual(distro_info['codename'], 'Official')

    def test_opensuse42_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'opensuse42'))

        disti = dist.LinuxDistribution()

        self.assertEqual(disti.id(), 'opensuse')
        self.assertEqual(disti.name(), 'openSUSE Leap')
        self.assertEqual(disti.name(pretty=True), 'openSUSE Leap 42.1 (x86_64)')
        self.assertEqual(disti.version(), '42.1')
        self.assertEqual(disti.version(pretty=True), '42.1 (x86_64)')
        self.assertEqual(disti.version(best=True), '42.1')
        self.assertEqual(disti.like(), 'suse')
        self.assertEqual(disti.codename(), 'x86_64')
        self.assertEqual(disti.major_version(), '42')
        self.assertEqual(disti.minor_version(), '1')
        self.assertEqual(disti.build_number(), '')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(disti.distro_release_file),
                         'SuSE-release')
        distro_info = disti.distro_release_info()
        self.assertEqual(distro_info['id'], 'SuSE')
        self.assertEqual(distro_info['name'], 'openSUSE')
        self.assertEqual(distro_info['version_id'], '42.1')
        self.assertEqual(distro_info['codename'], 'x86_64')

    def test_oracle7_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'oracle7'))

        disti = dist.LinuxDistribution()

        self.assertEqual(disti.id(), 'oracle')
        self.assertEqual(disti.name(), 'Oracle Linux Server')
        self.assertEqual(disti.name(pretty=True), 'Oracle Linux Server 7.1')
        self.assertEqual(disti.version(), '7.1')
        self.assertEqual(disti.version(pretty=True), '7.1')
        self.assertEqual(disti.version(best=True), '7.1')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), '')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(disti.distro_release_file),
                         'oracle-release')
        distro_info = disti.distro_release_info()
        self.assertEqual(distro_info['id'], 'oracle')
        self.assertEqual(distro_info['name'], 'Oracle Linux Server')
        self.assertEqual(distro_info['version_id'], '7.1')
        self.assertTrue('codename' not in distro_info)

    def test_rhel6_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'rhel6'))

        disti = dist.LinuxDistribution()

        self.assertEqual(disti.id(), 'rhel')
        self.assertEqual(disti.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            disti.name(pretty=True),
            'Red Hat Enterprise Linux Server 6.5 (Santiago)')
        self.assertEqual(disti.version(), '6.5')
        self.assertEqual(disti.version(pretty=True), '6.5 (Santiago)')
        self.assertEqual(disti.version(best=True), '6.5')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'Santiago')
        self.assertEqual(disti.version_parts(), ('6', '5', ''))

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(disti.distro_release_file),
                         'redhat-release')
        distro_info = disti.distro_release_info()
        self.assertEqual(distro_info['id'], 'redhat')
        self.assertEqual(distro_info['name'],
                         'Red Hat Enterprise Linux Server')
        self.assertEqual(distro_info['version_id'], '6.5')
        self.assertEqual(distro_info['codename'], 'Santiago')

    def test_rhel7_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'rhel7'))

        disti = dist.LinuxDistribution()

        self.assertEqual(disti.id(), 'rhel')
        self.assertEqual(disti.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            disti.name(pretty=True),
            'Red Hat Enterprise Linux Server 7.0 (Maipo)')
        self.assertEqual(disti.version(), '7.0')
        self.assertEqual(disti.version(pretty=True), '7.0 (Maipo)')
        self.assertEqual(disti.version(best=True), '7.0')
        self.assertEqual(disti.like(), 'fedora')
        self.assertEqual(disti.codename(), 'Maipo')
        self.assertEqual(disti.version_parts(), ('7', '0', ''))

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(disti.distro_release_file),
                         'redhat-release')
        distro_info = disti.distro_release_info()
        self.assertEqual(distro_info['id'], 'redhat')
        self.assertEqual(distro_info['name'],
                         'Red Hat Enterprise Linux Server')
        self.assertEqual(distro_info['version_id'], '7.0')
        self.assertEqual(distro_info['codename'], 'Maipo')

    def test_slackware14_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'slackware14'))

        disti = dist.LinuxDistribution()

        self.assertEqual(disti.id(), 'slackware')
        self.assertEqual(disti.name(), 'Slackware')
        self.assertEqual(disti.name(pretty=True), 'Slackware 14.1')
        self.assertEqual(disti.version(), '14.1')
        self.assertEqual(disti.version(pretty=True), '14.1')
        self.assertEqual(disti.version(best=True), '14.1')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), '')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(disti.distro_release_file),
                         'slackware-version')
        distro_info = disti.distro_release_info()
        self.assertEqual(distro_info['id'], 'slackware')
        self.assertEqual(distro_info['name'], 'Slackware')
        self.assertEqual(distro_info['version_id'], '14.1')
        self.assertTrue('codename' not in distro_info)

    def test_sles12_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'sles12'))

        disti = dist.LinuxDistribution()

        self.assertEqual(disti.id(), 'sles')
        self.assertEqual(disti.name(), 'SLES')
        self.assertEqual(disti.name(pretty=True),
                         'SUSE Linux Enterprise Server 12 SP1')
        self.assertEqual(disti.version(), '12.1')
        self.assertEqual(disti.version(pretty=True), '12.1 (n/a)')
        self.assertEqual(disti.version(best=True), '12.1')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'n/a')

        # Test the info from the searched distro release file
        self.assertEqual(os.path.basename(disti.distro_release_file),
                         'SuSE-release')
        distro_info = disti.distro_release_info()
        self.assertEqual(distro_info['id'], 'SuSE')
        self.assertEqual(distro_info['name'], 'SUSE Linux Enterprise Server')
        self.assertEqual(distro_info['version_id'], '12')
        self.assertEqual(distro_info['codename'], 's390x')

    def test_ubuntu14_release(self):
        self._setup_for_distro(os.path.join(DISTROS, 'ubuntu14'))

        disti = dist.LinuxDistribution()

        self.assertEqual(disti.id(), 'ubuntu')
        self.assertEqual(disti.name(), 'Ubuntu')
        self.assertEqual(disti.name(pretty=True), 'Ubuntu 14.04.3 LTS')
        self.assertEqual(disti.version(), '14.04')
        self.assertEqual(disti.version(pretty=True), '14.04 (Trusty Tahr)')
        self.assertEqual(disti.version(best=True), '14.04')
        self.assertEqual(disti.like(), 'debian')
        self.assertEqual(disti.codename(), 'Trusty Tahr')

        # Test the info from the searched distro release file
        # Does not have one; /etc/debian_version is not considered a distro
        # release file:
        self.assertEqual(disti.distro_release_file, '')
        self.assertEqual(len(disti.distro_release_info()), 0)

    def test_unknowndistro_release(self):
        self._setup_for_distro(os.path.join(TESTDISTROS, 'distro',
                                            'unknowndistro'))

        disti = dist.LinuxDistribution()

        self.assertEqual(disti.id(), 'unknowndistro')
        self.assertEqual(disti.name(), 'Unknown Distro')
        self.assertEqual(disti.name(pretty=True),
                         'Unknown Distro 1.0 (Unknown Codename)')
        self.assertEqual(disti.version(), '1.0')
        self.assertEqual(disti.version(pretty=True), '1.0 (Unknown Codename)')
        self.assertEqual(disti.version(best=True), '1.0')
        self.assertEqual(disti.like(), '')
        self.assertEqual(disti.codename(), 'Unknown Codename')


class TestGetAttr(DistroTestCase):
    """Test the consistency between the results of
    `get_{source}_release_attr()` and `{source}_release_info()` for all
    distros in `DISTROS`."""

    def test_os_release_attr(self):
        distros = os.listdir(DISTROS)
        for distro in distros:
            self._setup_for_distro(os.path.join(DISTROS, distro))

            disti = dist.LinuxDistribution()

            info = disti.os_release_info()
            for key in info.keys():
                self.assertEqual(info[key],
                                 disti.get_os_release_attr(key),
                                 "distro: %s, key: %s" % (distro, key))

    def test_lsb_release_attr(self):
        distros = os.listdir(DISTROS)
        for distro in distros:
            self._setup_for_distro(os.path.join(DISTROS, distro))

            disti = dist.LinuxDistribution()

            info = disti.lsb_release_info()
            for key in info.keys():
                self.assertEqual(info[key],
                                 disti.get_lsb_release_attr(key),
                                 "distro: %s, key: %s" % (distro, key))

    def test_distro_release_attr(self):
        distros = os.listdir(DISTROS)
        for distro in distros:
            self._setup_for_distro(os.path.join(DISTROS, distro))

            disti = dist.LinuxDistribution()

            info = disti.distro_release_info()
            for key in info.keys():
                self.assertEqual(info[key],
                                 disti.get_distro_release_attr(key),
                                 "distro: %s, key: %s" % (distro, key))


class TestInfo(testtools.TestCase):

    def setUp(self):
        super(TestInfo, self).setUp()
        self.rhel7_os_release = os.path.join(DISTROS, 'rhel7', 'etc',
                                             'os-release')

    def test_info(self):
        disti = dist.LinuxDistribution(False, self.rhel7_os_release, 'non')

        info = disti.info()
        self.assertEqual(info['id'], 'rhel')
        self.assertEqual(info['version'], '7.0')
        self.assertEqual(info['like'], 'fedora')
        self.assertEqual(info['version_parts']['major'], '7')
        self.assertEqual(info['version_parts']['minor'], '0')
        self.assertEqual(info['version_parts']['build_number'], '')

    def test_none(self):
        disti = dist.LinuxDistribution(False, 'non', 'non')

        info = disti.info()
        self.assertEqual(info['id'], '')
        self.assertEqual(info['version'], '')
        self.assertEqual(info['like'], '')
        self.assertEqual(info['version_parts']['major'], '')
        self.assertEqual(info['version_parts']['minor'], '')
        self.assertEqual(info['version_parts']['build_number'], '')

    def test_linux_disribution(self):
        disti = dist.LinuxDistribution(False, self.rhel7_os_release)
        i = disti.linux_distribution()
        self.assertEqual(
            i, ('Red Hat Enterprise Linux Server', '7.0', 'Maipo'))

    def test_linux_disribution_full_false(self):
        disti = dist.LinuxDistribution(False, self.rhel7_os_release)
        i = disti.linux_distribution(full_distribution_name=False)
        self.assertEqual(i, ('rhel', '7.0', 'Maipo'))


class TestOSReleaseParsing(testtools.TestCase):
    """Test the parsing of os-release files."""

    def setUp(self):
        self.disti = dist.LinuxDistribution(False, None, None)
        self.disti.debug = True
        super(TestOSReleaseParsing, self).setUp()

    def test_kv_01_empty_file(self):
        props = self.disti._parse_os_release_content(StringIO(
            '',
        ))
        self.assertEqual(len(props), 0)

    def test_kv_02_empty_line(self):
        props = self.disti._parse_os_release_content(StringIO(
            '\n',
        ))
        self.assertEqual(len(props), 0)

    def test_kv_03_empty_line_with_crlf(self):
        props = self.disti._parse_os_release_content(StringIO(
            '\r\n',
        ))
        self.assertEqual(len(props), 0)

    def test_kv_04_empty_line_with_just_cr(self):
        props = self.disti._parse_os_release_content(StringIO(
            '\r',
        ))
        self.assertEqual(len(props), 0)

    def test_kv_05_comment(self):
        props = self.disti._parse_os_release_content(StringIO(
            '# KEY=value\n'
        ))
        self.assertEqual(len(props), 0)

    def test_kv_06_empty_value(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY=\n'
        ))
        self.assertEqual(props.get('key', None),
            '')

    def test_kv_07_empty_value_single_quoted(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY=\'\'\n'
        ))
        self.assertEqual(props.get('key', None),
            '')

    def test_kv_08_empty_value_double_quoted(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY=""\n'
        ))
        self.assertEqual(props.get('key', None),
            '')

    def test_kv_09_word(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY=value\n'
        ))
        self.assertEqual(props.get('key', None),
            'value')

    def test_kv_10_word_no_newline(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY=value'
        ))
        self.assertEqual(props.get('key', None),
            'value')

    def test_kv_11_word_with_crlf(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY=value\r\n'
        ))
        self.assertEqual(props.get('key', None),
            'value')

    def test_kv_12_word_with_just_cr(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY=value\r'
        ))
        self.assertEqual(props.get('key', None),
            'value')

    def test_kv_13_word_with_multi_blanks(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY=  cmd   \n'
        ))
        self.assertEqual(props.get('key', None),
            '')
        # Note: Without quotes, this assigns the empty string, and 'cmd' is
        # a separate token that is being ignored (it would be a command
        # in the shell).

    def test_kv_14_unquoted_words(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY=value cmd\n'
        ))
        self.assertEqual(props.get('key', None),
            'value')

    def test_kv_15_double_quoted_words(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY="a simple value" cmd\n'
        ))
        self.assertEqual(props.get('key', None),
            'a simple value')

    def test_kv_16_double_quoted_words_with_multi_blanks(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY=" a  simple   value "\n'
        ))
        self.assertEqual(props.get('key', None),
            ' a  simple   value ')

    def test_kv_17_double_quoted_word_with_single_quote(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY="it\'s value"\n'
        ))
        self.assertEqual(props.get('key', None),
            'it\'s value')

    def test_kv_18_double_quoted_word_with_double_quote(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY="a \\"bold\\" move"\n'
        ))
        self.assertEqual(props.get('key', None),
            'a "bold" move')

    def test_kv_19_single_quoted_words(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY=\'a simple value\'\n'
        ))
        self.assertEqual(props.get('key', None),
            'a simple value')

    def test_kv_20_single_quoted_words_with_multi_blanks(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY=\' a  simple   value \'\n'
        ))
        self.assertEqual(props.get('key', None),
            ' a  simple   value ')

    def test_kv_21_single_quoted_word_with_double_quote(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY=\'a "bold" move\'\n'
        ))
        self.assertEqual(props.get('key', None),
            'a "bold" move')

    def test_kv_22_quoted_unicode_wordchar(self):
        # "wordchar" means it is in the shlex.wordchars variable.
        props = self.disti._parse_os_release_content(StringIO(
            u'KEY="wordchar: \u00CA (E accent grave)"\n'
        ))
        self.assertEqual(props.get('key', None),
            u'wordchar: \u00CA (E accent grave)')

    def test_kv_23_quoted_unicode_non_wordchar(self):
        # "non-wordchar" means it is not in the shlex.wordchars variable.
        props = self.disti._parse_os_release_content(StringIO(
            u'KEY="non-wordchar: \u00A1 (inverted exclamation mark)"\n'
        ))
        self.assertEqual(props.get('key', None),
            u'non-wordchar: \u00A1 (inverted exclamation mark)')

    def test_kv_24_double_quoted_entire_single_quoted_word(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY="\'value\'"\n'
        ))
        self.assertEqual(props.get('key', None),
            "'value'")

    def test_kv_25_single_quoted_entire_double_quoted_word(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY=\'"value"\'\n'
        ))
        self.assertEqual(props.get('key', None),
            '"value"')

    def test_kv_26_double_quoted_multiline(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY="a multi\n'
            'line value"\n'
        ))
        self.assertEqual(props.get('key', None),
            'a multi\nline value')
        # TODO: Find out why the result is not 'a multi line value'

    def test_kv_27_double_quoted_multiline_2(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY="a multi\n'
            'line=value"\n'
        ))
        self.assertEqual(props.get('key', None),
            'a multi\nline=value')
        # TODO: Find out why the result is not 'a multi line=value'

    def test_kv_28_double_quoted_word_with_equal(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY="var=value"\n'
        ))
        self.assertEqual(props.get('key', None),
            'var=value')

    def test_kv_29_single_quoted_word_with_equal(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY=\'var=value\'\n'
        ))
        self.assertEqual(props.get('key', None),
            'var=value')

    def test_kx_01(self):
        props = self.disti._parse_os_release_content(StringIO(
            'KEY1=value1\n'
            'KEY2="value  2"\n'
        ))
        self.assertEqual(props.get('key1', None),
            'value1')
        self.assertEqual(props.get('key2', None),
            'value  2')

    def test_kx_02(self):
        props = self.disti._parse_os_release_content(StringIO(
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

        self.assertEqual(dist.linux_distribution(),
            MODULE_DISTI.linux_distribution(full_distribution_name=True))
        self.assertEqual(dist.linux_distribution(full_distribution_name=True),
            MODULE_DISTI.linux_distribution())
        self.assertEqual(dist.linux_distribution(full_distribution_name=False),
            MODULE_DISTI.linux_distribution(full_distribution_name=False))

        self.assertEqual(dist.id(),
            MODULE_DISTI.id())

        self.assertEqual(dist.name(),
            MODULE_DISTI.name(pretty=False))
        self.assertEqual(dist.name(pretty=False),
            MODULE_DISTI.name())
        self.assertEqual(dist.name(pretty=True),
            MODULE_DISTI.name(pretty=True))

        self.assertEqual(dist.version(),
            MODULE_DISTI.version(pretty=False))
        self.assertEqual(dist.version(pretty=False),
            MODULE_DISTI.version())
        self.assertEqual(dist.version(pretty=True),
            MODULE_DISTI.version(pretty=True))
        self.assertEqual(dist.version(),
            MODULE_DISTI.version(best=False))
        self.assertEqual(dist.version(best=False),
            MODULE_DISTI.version())
        self.assertEqual(dist.version(best=True),
            MODULE_DISTI.version(best=True))

        self.assertEqual(dist.version_parts(),
            MODULE_DISTI.version_parts(best=False))
        self.assertEqual(dist.version_parts(best=False),
            MODULE_DISTI.version_parts())
        self.assertEqual(dist.version_parts(best=True),
            MODULE_DISTI.version_parts(best=True))

        self.assertEqual(dist.major_version(),
            MODULE_DISTI.major_version(best=False))
        self.assertEqual(dist.major_version(best=False),
            MODULE_DISTI.major_version())
        self.assertEqual(dist.major_version(best=True),
            MODULE_DISTI.major_version(best=True))

        self.assertEqual(dist.minor_version(),
            MODULE_DISTI.minor_version(best=False))
        self.assertEqual(dist.minor_version(best=False),
            MODULE_DISTI.minor_version())
        self.assertEqual(dist.minor_version(best=True),
            MODULE_DISTI.minor_version(best=True))

        self.assertEqual(dist.build_number(),
            MODULE_DISTI.build_number(best=False))
        self.assertEqual(dist.build_number(best=False),
            MODULE_DISTI.build_number())
        self.assertEqual(dist.build_number(best=True),
            MODULE_DISTI.build_number(best=True))

        self.assertEqual(dist.like(),
            MODULE_DISTI.like())

        self.assertEqual(dist.codename(),
            MODULE_DISTI.codename())

        self.assertEqual(dist.info(),
            MODULE_DISTI.info())

        self.assertEqual(dist.os_release_info(),
            MODULE_DISTI.os_release_info())

        self.assertEqual(dist.lsb_release_info(),
            MODULE_DISTI.lsb_release_info())

        self.assertEqual(dist.distro_release_info(),
            MODULE_DISTI.distro_release_info())

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
            self.assertEqual(dist.get_os_release_attr(key),
                MODULE_DISTI.get_os_release_attr(key))

        lsb_release_keys = [
            'distributor_id',
            'description',
            'release',
            'codename',
        ]
        for key in lsb_release_keys:
            self.assertEqual(dist.get_lsb_release_attr(key),
                MODULE_DISTI.get_lsb_release_attr(key))

        distro_release_keys = [
            'id',
            'name',
            'version_id',
            'codename',
        ]
        for key in distro_release_keys:
            self.assertEqual(dist.get_distro_release_attr(key),
                MODULE_DISTI.get_distro_release_attr(key))


class TestRepr(testtools.TestCase):
    """Test the __repr__() method."""

    def test_repr(self):
        # We test that the class name and the names of all instance attributes
        # show up in the repr() string.
        repr_str = repr(dist._disti)
        self.assertIn("LinuxDistribution", repr_str)
        for attr in MODULE_DISTI.__dict__.keys():
            self.assertIn(attr+'=', repr_str)

