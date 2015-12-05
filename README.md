ld
==

[![Build Status](https://travis-ci.org/nir0s/ld.svg?branch=master)](https://travis-ci.org/nir0s/ld)
[![PyPI](http://img.shields.io/pypi/dm/ld.svg)](http://img.shields.io/pypi/dm/ld.svg)
[![PypI](http://img.shields.io/pypi/v/ld.svg)](http://img.shields.io/pypi/v/ld.svg)

Python 3.5 deprecates `platform.linux_distribution()`.
Python 3.7 removes it altogether.

Still, there are many cases in which you need access to that information.

`ld` (linux distribution) attempts to implement a more robust and inclusive way of retrieving the distro related information based on new standards and old methods - namely:

* `/etc/os-release`
* `/etc/lsb-release`
* `/etc/*-release`

## Installation

```shell
pip install ld
```

For dev:

```shell
pip install https://github.com/nir0s/ld/archive/master.tar.gz
```

## Distribution Support

The following distributions are handled:

* Red Hat
* CentOS
* Ubuntu
* Debian
* OpenSuSE
* SuSE
* Arch
* Slackware
* Exherbo
* Oracle

Soon:

* Gentoo
* Enterprise


## Usage

`ld` exposes the following parmeters:

* `ld.linux_distribution(full_distribution_name=False)` - attempts to implement Python's `platform.linux_distribution()`.

* `ld.id()` - e.g. `ubuntu`, `fedora`, `debian`...
* `ld.name()` - e.g. `Red Hat Enterprise Linux Server`, `Ubuntu`, `openSUSE Leap`
* `ld.name(pretty=True)` - e.g. `openSUSE Leap 42.1 (x86_64)`, `CentOS Linux 7 (Core)`, `Oracle Linux Server 7.1`
* `ld.version()` - e.g. .. well.. the version number.
* `ld.version(full=True)` - e.g. `7 (Core)`, `23 (Twenty Three)`
* `ld.like()` - e.g. `suse`, `rhel fedora`, `debian`
* `ld.codename()` - e.g. `Core`, `trusty`, `Maipo`
* `ld.base()` - e.g. `arch`, `gentoo`, `rhel`

You can also get the information from some of the release files:

* `ld.os_release_info()` - returns a dictionary containing the info found in `/etc/os-release`
* `ld.lsb_release_info()` - returns a dictionary containing the info found in `/etc/lsb-release`
* `ld.distro_release_info()` - returns a dictionary containing the info found in '/etc/*-release' matching your distribution.

## Implementation

* [os-release](http://www.freedesktop.org/software/systemd/man/os-release.html) is a new standard for providing distro-specific information. This is the first file looked at when attempting to retrieve the distro specific info.
* [lsb-release](http://linux.die.net/man/1/lsb_release) is usually found by default in Ubuntu. When `/etc/debian_version` is found, we also check for `/etc/lsb-release` to retrieve the information from it.
* `*-release` - We fallback to the release file specific to the distribution (e.g. `/etc/redhat-release`, `/etc/centos-release`) and try to extract information (like the version and codename) from it.

## Testing

NOTE: Running the tests require an internet connection

```shell
git clone git@github.com:nir0s/ld.git
cd ld
pip install tox
tox
```

## Contributions..

Pull requests are always welcome..
