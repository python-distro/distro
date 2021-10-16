#!/usr/bin/env python
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

from pprint import pformat

import distro


def pprint(obj: object) -> None:
    for line in pformat(obj).split("\n"):
        print(4 * " " + line)


print("os_release_info:")
pprint(distro.os_release_info())
print("lsb_release_info:")
pprint(distro.lsb_release_info())
print("distro_release_info:")
pprint(distro.distro_release_info())
print(f"id: {distro.id()}")
print(f"name: {distro.name()}")
print(f"name_pretty: {distro.name(True)}")
print(f"version: {distro.version()}")
print(f"version_pretty: {distro.version(True)}")
print(f"like: {distro.like()}")
print(f"codename: {distro.codename()}")
print(f"linux_distribution_full: {distro.linux_distribution()}")
print(f"linux_distribution: {distro.linux_distribution(False)}")
print(f"major_version: {distro.major_version()}")
print(f"minor_version: {distro.minor_version()}")
print(f"build_number: {distro.build_number()}")
