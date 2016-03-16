Linux Distribution - a Linux OS platform information API
========================================================

The `ld` (for: Linux Distribution) package provides information about the
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

The `ld` package implements a robust and inclusive way of retrieving the
information about a Linux distribution based on new standards and old methods,
namely from these data sources (from high to low precedence):

* The os-release file `/etc/os-release`, if present.
* The output of the `lsb_release` command, if available.
* The distro release file (`/etc/*(-|_)(release|version)`), if present.

`ld` is tested on Python 2.6, 2.7 and 3.5.


## Installation

```shell
pip install ld
```

For dev:

```shell
pip install https://github.com/nir0s/ld/archive/master.tar.gz
```

## Distribution Support

The following distributions are tested (this is by no means an exhaustive list
of supported distros as any distro adhering to the same standards should work):

* Arch
* CentOS 5/7
* Debian 8
* Exherbo
* Fedora 23
* Mageia 5
* openSUSE Leap 42
* Oracle Linux Server 7
* RHEL 6/7
* Slackware 14
* Ubuntu 14

## Usage

```
python
>>> import ld
>>> ld.linux_distribution(full_distribution_name=False)
'('centos', '7.1.1503', 'Core')'
```

Several more functions are available. For a complete description of the
API, see the [latest API documentation](http://ld.readthedocs.org/en/latest/).
