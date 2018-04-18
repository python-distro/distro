## Unreleased

ENHANCEMENTS:
* Update docs with regards to #207 [[#209](#209)]
* Added support for OpenBSD, FreeBSD, and NetBSD [[#207](#207)]


## 1.2.0 (2017.12.24)

BACKWARD COMPATIBILITY:
* Don't raise ImportError on non-linux platforms [[#202](#202)]

ENHANCEMENTS:
* Lazily load the LinuxDistribution data [[#201](#201)]

BUG FIXES:
* Stdout of shell should be decoded with sys.getfilesystemencoding() [[#203](#203)]

TESTS:
* Explicitly set Python versions on Travis for flake [[#204](#204)]


## 1.1.0 (2017.11.28)

BACKWARD COMPATIBILITY:
* Drop python3.3 support [[#199](#199)]
* Remove Official Python26 support [[#195](#195)]

TESTS:
* Add MandrivaLinux test case [[#181](#181)]
* Add test cases for CloudLinux 5, 6, and 7 [[#180](#180)]

RELEASE:
* Modify MANIFEST to include resources for tests and docs in source tarballs [[97c91a1](97c91a1)]

## 1.0.4 (2017.04.01)

BUG FIXES:
* Guess common *-release files if /etc not readable [[#175](#175)]

## 1.0.3 (2017.03.19)

ENHANCEMENTS:
* Show keys for empty values when running distro from the CLI [[#160](#160)]
* Add manual mapping for `redhatenterpriseserver` (previously only redhatenterpriseworkstation was mapped) [[#148](#148)]
* Race condition in `_parse_distro_release_file` [[#163](#163)]

TESTS:
* Add RHEL5 test case [[#165](#165)]
* Add OpenELEC test case [[#166](#166)]
* Replace nose with pytest [[#158](#158)]

RELEASE:
* Update classifiers
* Update supported Python versions (with py36)

## 1.0.2 (2017.01.12)

TESTS:
* Test on py33, py36 and py3 based flake8

RELEASE:
* Add MANIFEST file (which also includes the LICENSE as part of Issue [[#139](#139)])
* Default to releasing using Twine [[#121](#121)]
* Add setup.cfg file [[#145](#145)]
* Update license in setup.py

## 1.0.1 (2016-11-03)

ENHANCEMENTS:
* Prettify distro -j's output and add more elaborate docs [[#147](#147)]
* Decode output of `lsb_release` as utf-8 [[#144](#144)]
* Logger now uses `message %s, string` form to not-evaulate log messages if unnecessary [[#145](#145)]

TESTS:
* Increase code-coverage [[#146](#146)]
* Fix landscape code-quality warnings [[#145](#145)]

RELEASE:
* Add CONTRIBUTING.md

## 1.0.0 (2016-09-25)

BACKWARD COMPATIBILITY:
* raise exception when importing on non-supported platforms [[#129](#129)]

ENHANCEMENTS:
* Use `bytes` invariantly [[#135](#135)]
* Some minor code adjustments plus a CLI [[#134](#134)]
* Emit stderr if `lsb_release` fails

BUG FIXES:
* Fix some encoding related issues

TESTS:
* Add many test cases (e.g. Raspbian 8, CoreOS, Amazon Linux, Scientific Linux, Gentoo, Manjaro)
* Completely redo the testing framework to make it easier to add tests
* Test on pypy

RELEASE:
* Remove six as a dependency

## 0.6.0 (2016-04-21)

This is the first release of `distro`.
All previous work was done on `ld` and therefore unmentioned here. See the release log in GitHub if you want the entire log.

BACKWARD COMPATIBILITY:
* No longer a package. constants.py has been removed and distro is now a single module

ENHANCEMENTS:
* distro.info() now receives best and pretty flags
* Removed get_ prefix from get_*_release_attr functions
* Codename is now passed in distro.info()

TESTS:
* Added Linux Mint test case
* Now testing on Python 3.4

DOCS:
* Documentation fixes

