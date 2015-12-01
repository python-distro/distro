import os

import testtools

import ld


RESOURCES_DIR = os.path.join('ld', 'tests', 'resources')


class TestBase(testtools.TestCase):

    def setUp(self):
        super(TestBase, self).setUp()
        self.os_release = os.path.join(RESOURCES_DIR, 'os-release')
        self.lsb_release = os.path.join(RESOURCES_DIR, 'lsb-release')
        self.redhat_release = os.path.join(RESOURCES_DIR, 'redhat-release')

    def test_os_release(self):
        self.ld = ld.LinuxDistribution(
            'non', 'non', self.redhat_release)

        self.assertEqual(self.ld.id(), 'redhat')
        self.assertEqual(self.ld.name(), 'Red Hat Enterprise Linux Server')
        self.assertEqual(
            self.ld.name(pretty=True),
            'Red Hat Enterprise Linux Server 7.0 (Maipo)')
        self.assertEqual(self.ld.version(), '7.0')
        self.assertEqual(self.ld.version(full=True), '7.0 (Maipo)')
        self.assertEqual(self.ld.like(), 'fedora')
        self.assertEqual(self.ld.codename(), 'Maipo')
        self.assertEqual(self.ld.base(), 'fedora')

    # def test_lsb_release(self):
    #     self.ld = ld.LinuxDistribution(
    #         self.os_release, self.lsb_release, self.redhat_release)
