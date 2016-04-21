Distro - a Linux OS platform information API
========================================================

[![Build Status](https://travis-ci.org/nir0s/distro.svg?branch=master)](https://travis-ci.org/nir0s/distro)
[![PyPI downloads](http://img.shields.io/pypi/dm/distro.svg)](https://pypi.python.org/pypi/distro)
[![PyPI version](http://img.shields.io/pypi/v/distro.svg)](https://pypi.python.org/pypi/distro)


The `distro` (for: Linux Distribution) package provides information about the
Linux distribution it runs on, such as a reliable machine-readable ID, or
version information.

It is a renewed alternative implementation for Python's
original `platform.linux_distribution` function, but it also provides much more
functionality.
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


## Installation

Installation of the latest released version from PyPI:

```shell
pip install distro
```

Installation of the latest development version:

```shell
pip install https://github.com/nir0s/distro/archive/master.tar.gz
```

## Documentation

The API documentation for the `distro` package is on RTD:
[latest API documentation](http://distro.readthedocs.org/en/latest/).

## Python and Distribution Support

The `distro` package is supported on Python 2.6, 2.7, 3.4 and 3.5, and on
any Linux distribution that provides one or more of the data sources
used by this package.

This package is tested on Python 2.6, 2.7, 3.4 and 3.5, with test
data that mimics the exact behavior of the data sources of
[a number of Linux distributions](https://github.com/nir0s/distro/tree/master/tests/resources/distros).

## Usage

```
python
>>> import distro
>>> distro.linux_distribution(full_distribution_name=False)
'('centos', '7.1.1503', 'Core')'
```

Several more functions are available. For a complete description of the
API, see the [latest API documentation](http://distro.readthedocs.org/en/latest/).

## Contributions

Pull requests are always welcome to deal with specific distributions or just
for general merriment.

Reference implementations for supporting additional distributions and file
formats can be found here:

* https://github.com/saltstack/salt/blob/develop/salt/grains/core.py#L1172
* https://github.com/chef/ohai/blob/master/lib/ohai/plugins/linux/platform.rb
