#!/bin/env python

import ld

print 'os_release_info: {0}'.format(ld.os_release_info())
print 'lsb_release_info: {0}'.format(ld.lsb_release_info())
print 'distro_release_info: {0}'.format(ld.distro_release_info())
print 'id: {0}'.format(ld.id())
print 'name: {0}'.format(ld.name())
print 'name_pretty: {0}'.format(ld.name(True))
print 'version: {0}'.format(ld.version())
print 'version_pretty: {0}'.format(ld.version(True))
print 'like: {0}'.format(ld.like())
print 'codename: {0}'.format(ld.codename())
print 'linux_distribution_full: {0}'.format(ld.linux_distribution())
print 'linux_distribution: {0}'.format(ld.linux_distribution(False))
print 'major_version: {0}'.format(ld.major_version())
print 'minor_version: {0}'.format(ld.minor_version())
print 'build_number: {0}'.format(ld.build_number())
