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

"""
Constants for the :mod:`ld` package.
"""

_UNIXCONFDIR = '/etc'
_OS_RELEASE_BASENAME = 'os-release'

#: Translation table for normalizing the "ID" attribute defined in os-release
#: files, for use by the :func:`ld.id` method.
#:
#: * Key: Value as defined in the os-release file, translated to lower case,
#:   with blanks translated to underscores.
#:
#: * Value: Normalized value.
NORMALIZED_OS_ID = {
}

#: Translation table for normalizing the "Distributor ID" attribute returned by
#: the lsb_release command, for use by the :func:`ld.id` method.
#:
#: * Key: Value as returned by the lsb_release command, translated to lower
#:   case, with blanks translated to underscores.
#:
#: * Value: Normalized value.
NORMALIZED_LSB_ID = {
    'enterpriseenterprise': 'oracle',  # Oracle Enterprise Linux
    'redhatenterpriseworkstation': 'rhel',  # RHEL 6.7
}

#: Translation table for normalizing the distro ID derived from the file name
#: of distro release files, for use by the :func:`ld.id` method.
#:
#: * Key: Value as derived from the file name of a distro release file,
#:   translated to lower case, with blanks translated to underscores.
#:
#: * Value: Normalized value.
NORMALIZED_DISTRO_ID = {
    'redhat': 'rhel',  # RHEL 6.x, 7.x
}
