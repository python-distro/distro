ld
==

[![Build Status](https://travis-ci.org/nir0s/ld.svg?branch=master)](https://travis-ci.org/nir0s/ld)
[![PyPI](http://img.shields.io/pypi/dm/ld.svg)](http://img.shields.io/pypi/dm/ld.svg)
[![PypI](http://img.shields.io/pypi/v/ld.svg)](http://img.shields.io/pypi/v/ld.svg)

Python 3.5 deprecates `platform.linux_distribution()` and Python 3.7 removes it altogether.

Still, there are many cases in which you need access to that information.

see [https://bugs.python.org/issue1322](https://bugs.python.org/issue1322) for more information.

THIS IS WIP! It is is no means production ready. See caveats section.


`ld` (linux distribution) attempts to implement a more robust and inclusive way of retrieving the distro related information based on new standards and old methods - namely:

* `/etc/os-release`
* the output of the `lsb_release -a` command
* `/etc/*-release`

`ld` is tested on Python 2.6, 2.7 and 3.5


## Installation

```shell
pip install ld
```

For dev:

```shell
pip install https://github.com/nir0s/ld/archive/master.tar.gz
```

## Distribution Support

The following distributions are tested (this is by no means an exhaustive list of supported distros as any distro adhering to the same standards should work):

* Arch
* CentOS 5/7
* Debian 8
* Exherbo
* Fedora 23
* OpenSuSE 42
* Oracle 7
* Red Hat 6/7
* Slackware 14
* Ubuntu 14


## Usage

```python

import ld

ld.linux_distribution(full_distribution_name=False)

'('centos', '7.1.1503', 'Core')'
```

## Exposed Distribution Properties

`ld` exposes the following parmeters:

### `ld.linux_distribution(full_distribution_name=False)`

Attempts to implement Python's `platform.linux_distribution()`.

If `full_distribution_name` is set to `True`, the `name` will be returned instead of the `id`.

### `ld.id()`

Returns the id of the distribution - e.g. `ubuntu`, `fedora`, `debian`...

The id should be machine-readable.

#### Lookup Hierarchy

* os-release['ID']
* lsb-release['Distributor ID'] in lowercase.
* *-release file name prefix (e.g. redhat from redhat-release)

### `ld.name()`

Returns the name of the distribution - e.g. `Red Hat Enterprise Linux Server`, `Ubuntu`, `openSUSE Leap`

#### Lookup Hierarchy

* os-release['NAME']
* lsb-release['Distributor ID']
* first part of the first line of the *-release file

### `ld.name(pretty=True)`

Returns a prettified name of the distribution - e.g. `openSUSE Leap 42.1 (x86_64)`, `CentOS Linux 7 (Core)`, `Oracle Linux Server 7.1`

#### Lookup Hierarchy

* os-release['PRETTY_NAME']
* lsb-release['Description']
* first part of the first line of the *-release file + `ld.version(pretty=True)`

### `ld.version()`

Returns the version (i.e. release) of the distribution - e.g. .. well.. the version number.

### Lookup Hierarchy

* os-release['VERSION_ID']
* lsb-release['Release']
* second part of the first line of the *-release file

`ld.minor_version()`, `ld.major_version()` and `ld.build_number()` are also exposed and are based on `ld.version_parts()`.

### `ld.version(pretty=True)`

Returns a prettified version of the distribution  - e.g. `7 (Core)`, `23 (Twenty Three)`

### Lookup Hierarchy

* os-release['VERSION']
* lsb-release['Release'] + `ld.codename()` (if codename exists)
* second part of the first line of the *-release file + `ld.codename()` (if codename exists)

### `ld.like()`

Returns the os-release['ID_LIKE'] field - e.g. `suse`, `rhel fedora`, `debian`


### `ld.codename()`

Returns the distribution version's codename - e.g. `Core`, `trusty`, `Maipo`

Note that not all distributions provide a codename for their releases.

#### Lookup Hierarchy

* The second part of os-release['VERSION'] (between parentheses or after a comma)
* lsb-release['Codename']
* third part of the first line of the *-release files (between parentheses)

### `ld.base()`

Returns the base distribution - e.g. `arch`, `gentoo`, `rhel`

`constants.py` contains the table in which each distro is mapped to its base distro.

Matching is one first by `ld.name()` and then by `ld.like()`

### `ld.info()`

Returns a dictionary with machine readable info of the distribution.
This is just an aggregate of the rest of the information.

Example:

```python
{
    'id': 'rhel',
    'version': '7.0',
    'version_parts': {
        'major': '7',
        'minor': '0',
        'build_number': ''
    },
    'like': 'fedora',
    'base': 'fedora'
}
```


### Retrieving information directly

* `ld.os_release_info()` - returns a dictionary containing the info found in `/etc/os-release`
* `ld.lsb_release_info()` - returns a dictionary containing the info parsed from `lsb_release -a`
* `ld.distro_release_info()` - returns a dictionary containing the info found in '/etc/*-release' matching your distribution.

You can also get the information from some of the release files directly. This allows you to retrieve information that is not exposed via the API.

For instance, RHEL 7's os-release file contains the following:

`REDHAT_BUGZILLA_PRODUCT="Red Hat Enterprise Linux 7"`

`ld.get_os_release_attr('redhat_bugzilla_product')` will get the value for that field.

`ld.get_lsb_release_attr()` and `ld.get_dist_release_attr()` are also exposed.


## Lookup Locations

* [os-release](http://www.freedesktop.org/software/systemd/man/os-release.html) is a new standard for providing distro-specific information. This is the first file looked at when attempting to retrieve the distro specific info.
* [lsb_release](http://linux.die.net/man/1/lsb_release) is found by default in Ubuntu. We also check for `lsb_release -a` to retrieve the information from it if it is available.
* `*-release` - We fallback to the release file specific to the distribution (e.g. `/etc/redhat-release`, `/etc/centos-release`) and try to extract information (like the version and codename) from it. This is done by looking up the a release file and parsing it.

## Caveats

contributors, please read.

* There will be some consistency issues depending on the system you're running. For instance, `os-release` returns `rhel` as an id while `redhat-release` returns `redhat`. This means that either the user will have to act upon "either redhat or rhel" or we'll have to decide on one of them and then convert in-code.
* `codename` of the same distro might be different in some cases. For instance, `os-release` returns `Trusty Tahr` for Ubuntu 14.04 while `lsb_release -a` returns `trusty`. This again means that we'll either have to tell the user to check `codename.lower().startswith(WHATEVER)` or find a consistent way of dealing with codenames. All in all, relying on version numbers is preferred.

## Testing

```shell
git clone git@github.com:nir0s/ld.git
cd ld
pip install tox
tox
```

## Contributions..

Pull requests are always welcome to deal with specific distributions or just for general merriment.

Reference implementations for supporting additional distributions and file formats can be found here:

* https://github.com/saltstack/salt/blob/develop/salt/grains/core.py#L1172
* https://github.com/chef/ohai/blob/master/lib/ohai/plugins/linux/platform.rb
