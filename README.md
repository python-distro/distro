Distro - an OS platform information API
=======================================

[![Build Status](https://travis-ci.org/nir0s/distro.svg?branch=master)](https://travis-ci.org/nir0s/distro)
[![Build status](https://ci.appveyor.com/api/projects/status/e812qjk1gf0f74r5/branch/master?svg=true)](https://ci.appveyor.com/project/nir0s/distro/branch/master)
[![PyPI version](http://img.shields.io/pypi/v/distro.svg)](https://pypi.python.org/pypi/distro)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/distro.svg)](https://img.shields.io/pypi/pyversions/distro.svg)
[![Requirements Status](https://requires.io/github/nir0s/distro/requirements.svg?branch=master)](https://requires.io/github/nir0s/distro/requirements/?branch=master)
[![Code Coverage](https://codecov.io/github/nir0s/distro/coverage.svg?branch=master)](https://codecov.io/github/nir0s/distro?branch=master)
[![Code Quality](https://landscape.io/github/nir0s/distro/master/landscape.svg?style=flat)](https://landscape.io/github/nir0s/distro)
[![Is Wheel](https://img.shields.io/pypi/wheel/distro.svg?style=flat)](https://pypi.python.org/pypi/distro)
[![Latest Github Release](https://readthedocs.org/projects/distro/badge/?version=stable)](http://distro.readthedocs.io/en/latest/)
[![Join the chat at https://gitter.im/nir0s/distro](https://badges.gitter.im/nir0s/distro.svg)](https://gitter.im/nir0s/distro?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

`distro` (for: Linux Distribution) provides information about the
Linux distribution it runs on, such as a reliable machine-readable ID, or
version information.

It is a renewed alternative implementation for Python's
original `platform.linux_distribution` function, but it also provides much more
functionality which isn't necessarily Python bound like a command-line interface.


## Installation

Installation of the latest released version from PyPI:

```shell
pip install distro
```

Installation of the latest development version:

```shell
pip install https://github.com/nir0s/distro/archive/master.tar.gz
```


## Usage

```bash
$ distro
Name: Antergos Linux
Version: 2015.10 (ISO-Rolling)
Codename: ISO-Rolling

$ distro -j
{
    "codename": "ISO-Rolling",
    "id": "antergos",
    "like": "arch",
    "version": "16.9",
    "version_parts": {
        "build_number": "",
        "major": "16",
        "minor": "9"
    }
}


$ python
>>> import distro
>>> distro.linux_distribution(full_distribution_name=False)
('centos', '7.1.1503', 'Core')
```


## Documentation

On top of the aforementioned API, several more functions are available. For a complete description of the
API, see the [latest API documentation](http://distro.readthedocs.org/en/latest/).

## Background

An alternative implementation became necessary because Python 3.5 deprecated
this function, and Python 3.7 is expected to remove it altogether.
Its predecessor function `platform.dist` was already deprecated since
Python 2.6 and is also expected to be removed in Python 3.7.
Still, there are many cases in which access to that information is needed.
See [Python issue 1322](https://bugs.python.org/issue1322) for more
information.

The `distro` package implements a robust and inclusive way of retrieving the
information about a Linux distribution based on new standards and old methods,
namely from these data sources (from high to low precedence):

* The os-release file `/etc/os-release`, if present.
* The output of the `lsb_release` command, if available.
* The distro release file (`/etc/*(-|_)(release|version)`), if present.


## Python and Distribution Support

`distro` is supported and tested on Python 2.7, 3.4+ and PyPy and on
any Linux distribution that provides one or more of the data sources
covered.

This package is tested with test data that mimics the exact behavior of the data sources of [a number of Linux distributions](https://github.com/nir0s/distro/tree/master/tests/resources/distros).


## Testing

```shell
git clone git@github.com:nir0s/distro.git
cd distro
pip install tox
tox
```


## Contributions

Pull requests are always welcome to deal with specific distributions or just
for general merriment.

See [CONTRIBUTIONS](https://github.com/nir0s/distro/blob/master/CONTRIBUTING.md) for contribution info.

Reference implementations for supporting additional distributions and file
formats can be found here:

* https://github.com/saltstack/salt/blob/develop/salt/grains/core.py#L1172
* https://github.com/chef/ohai/blob/master/lib/ohai/plugins/linux/platform.rb

## Package manager distributions

* https://admin.fedoraproject.org/pkgdb/package/rpms/python-distro/
* https://aur.archlinux.org/packages/python-distro/
* https://launchpad.net/ubuntu/+source/python-distro
* https://packages.debian.org/sid/python-distro
* https://packages.gentoo.org/packages/dev-python/distro
* https://pkgs.org/download/python2-distro
* https://slackbuilds.org/repository/14.2/python/python-distro/
