## 1.8.0 (2022.10.10)

BACKWARD COMPATIBILITY:
* Replace `setup.py` with `build` [[#342](https://github.com/python-distro/distro/pull/342)]

ENHANCEMENTS:
* Lowered `LinuxDistribution._distro_release_info` method complexity [[#327](https://github.com/python-distro/distro/pull/327)]
* Added official support for Buildroot distribution [[#329](https://github.com/python-distro/distro/pull/329)]
* Added official support for Guix distribution [[#330](https://github.com/python-distro/distro/pull/330)]
* Added support for `/etc/debian_version` [[#333](https://github.com/python-distro/distro/pull/333)] & [[#349](https://github.com/python-distro/distro/pull/349)]
* Fixed a typography in CONTRIBUTING.md [[#340](https://github.com/python-distro/distro/pull/340)]
* Improved README.md "Usage" code block [[#343](https://github.com/python-distro/distro/pull/343)]

RELEASE:
* Bumped black to v22.3.0 in pre-commit.ci configuration [[#331](https://github.com/python-distro/distro/pull/331)]
* Enabled GitHub Dependabot to keep GitHub Actions up to date [[#335](https://github.com/python-distro/distro/pull/335)]

## 1.7.0 (2022.02.15)

BACKWARD COMPATIBILITY:
* Dropped support for EOL Pythons 2.7, 3.4 and 3.5 [[#281](https://github.com/python-distro/distro/pull/281)]
* Dropped support for LSB and `uname` back-ends when `--root-dir` is specified [[#311](https://github.com/python-distro/distro/pull/311)]
* Moved `distro.py` to `src/distro/distro.py` [[#315](https://github.com/python-distro/distro/pull/315)]

ENHANCEMENTS:
* Documented that `distro.version()` can return an empty string on rolling releases [[#312](https://github.com/python-distro/distro/pull/312)]
* Documented support for Python 3.10 [[#316](https://github.com/python-distro/distro/pull/316)]
* Added official support for Rocky Linux distribution [[#318](https://github.com/python-distro/distro/pull/318)]
* Added a shebang to `distro.py` to allow standalone execution [[#313](https://github.com/python-distro/distro/pull/313)]
* Added support for AIX platforms [[#311](https://github.com/python-distro/distro/pull/311)]
* Added compliance for PEP-561 [[#315](https://github.com/python-distro/distro/pull/315)]

BUG FIXES:
* Fixed `include_uname` parameter oversight [[#305](https://github.com/python-distro/distro/pull/305)]
* Fixed crash when `uname -rs` output is empty [[#304](https://github.com/python-distro/distro/pull/304)]
* Fixed Amazon Linux identifier in `distro.id()` documentation [[#318](https://github.com/python-distro/distro/pull/318)]
* Fixed OpenSuse >= 15 support [[#319](https://github.com/python-distro/distro/pull/319)]
* Fixed encoding issues when opening distro release files [[#324](https://github.com/python-distro/distro/pull/324)]
* Fixed `linux_distribution` regression introduced in [[#230](https://github.com/python-distro/distro/pull/230)] [[#325](https://github.com/python-distro/distro/pull/325)]

## 1.6.0 (2021.7.30)

BACKWARDS COMPATIBILITY:
* Deprecated the `distro.linux_distribution()` function. Use
  `distro.id()`, `distro.version()` and `distro.name()` instead
  [[#296](https://github.com/python-distro/distro/pull/296)]
* Deprecated Python 2.7, 3.4 and 3.5 support. Further releases
  will only support Python 3.6+ 

ENHANCEMENTS:
* Added type hints to `distro` module [[#269](https://github.com/python-distro/distro/pull/269)]
* Added `__version__` for checking `distro` version [[#292](https://github.com/python-distro/distro/pull/292)]
* Added support for arbitrary rootfs via the `root_dir` parameter [[#247](https://github.com/python-distro/distro/pull/247)]
* Added the `--root-dir` option to CLI [[#161](https://github.com/python-distro/distro/issues/161)]
* Added fallback to `/usr/lib/os-release` when `/etc/os-release` isn't available [[#262](https://github.com/python-distro/distro/pull/262)]

BUG FIXES:
* Fixed `subprocess.CalledProcessError` when running `lsb_release` [[#261](https://github.com/python-distro/distro/pull/261)]
* Ignore `/etc/iredmail-release` file while parsing distribution [[#268](https://github.com/python-distro/distro/pull/268)]
* Use a binary file for `/dev/null` to avoid `TextIOWrapper` overhead [[#271](https://github.com/python-distro/distro/pull/271)]

RELEASE:
* Moved repository from `nir0s/distro` to
  [`python-distro/distro`](https://github.com/python-distro/distro) on GitHub.

## 1.5.0 (2020.3.30)

BACKWARD COMPATIBILITY:
* Keep output as native string so we can compatible with python2 interface [[#248](https://github.com/python-distro/distro/pull/248)]

ENHANCEMENTS:

BUG FIXES:
* Fix detection of RHEL 6 ComputeNode [[#255](https://github.com/python-distro/distro/issues/255)]
* Fix Oracle 4/5 lsb_release id and names [[#250](https://github.com/python-distro/distro/pull/250)]
* Ignore /etc/plesk-release file while parsing distribution [[#246](https://github.com/python-distro/distro/pull/246)]

TESTS:
* Test on MidnightBSD [[#254](https://github.com/python-distro/distro/issues/254)]

RELEASE:
* Remove build testing on Python 3.3 and add pypy 3.5 and Python 3.7 and 3.8 [[#244](https://github.com/python-distro/distro/pull/244)]
* Fix Windows build due to Appveyor not supporting builds on Python 2.7 anymore [[#257](https://github.com/python-distro/distro/pull/257)]

Additionally, The Python2.6 branch was fixed to support distro version 1.4.0. It is now passing all tests. Thanks [abadger](https://github.com/abadger)!

## 1.4.0 (2019.2.4)

BACKWARD COMPATIBILITY:
* Prefer the VERSION_CODENAME field of os-release to parsing it from VERSION [[#230](https://github.com/python-distro/distro/pull/230)]

BUG FIXES:
* Return _uname_info from the uname_info() method [[#233](https://github.com/python-distro/distro/pull/233)]
* Fixed CloudLinux id discovery [[#234](https://github.com/python-distro/distro/pull/234)]
* Update Oracle matching [[#224](https://github.com/python-distro/distro/pull/224)]

DOCS:
* Update Fedora package link [[#225](https://github.com/python-distro/distro/pull/225)]
* Distro is the recommended replacement for platform.linux_distribution [[#220](https://github.com/python-distro/distro/pull/220)]

RELEASE:
* Use Markdown for long description in setup.py [[#219](https://github.com/python-distro/distro/pull/219)]

Additionally, The Python2.6 branch was fixed and rebased on top of master. It is now passing all tests. Thanks [abadger](https://github.com/abadger)!

## 1.3.0 (2018.05.09)

ENHANCEMENTS:
* Added support for OpenBSD, FreeBSD, and NetBSD [[#207](https://github.com/python-distro/distro/issues/207)]

TESTS:
* Add test for Kali Linux Rolling [[#214](https://github.com/python-distro/distro/issues/214)]

DOCS:
* Update docs with regards to #207 [[#209](https://github.com/python-distro/distro/issues/209)]
* Add Ansible reference implementation and fix arch-linux link [[#213](https://github.com/python-distro/distro/issues/213)]
* Add facter reference implementation [[#213](https://github.com/python-distro/distro/issues/213)]

## 1.2.0 (2017.12.24)

BACKWARD COMPATIBILITY:
* Don't raise ImportError on non-linux platforms [[#202](https://github.com/python-distro/distro/issues/202)]

ENHANCEMENTS:
* Lazily load the LinuxDistribution data [[#201](https://github.com/python-distro/distro/issues/201)]

BUG FIXES:
* Stdout of shell should be decoded with sys.getfilesystemencoding() [[#203](https://github.com/python-distro/distro/issues/203)]

TESTS:
* Explicitly set Python versions on Travis for flake [[#204](https://github.com/python-distro/distro/issues/204)]


## 1.1.0 (2017.11.28)

BACKWARD COMPATIBILITY:
* Drop python3.3 support [[#199](https://github.com/python-distro/distro/issues/199)]
* Remove Official Python26 support [[#195](https://github.com/python-distro/distro/issues/195)]

TESTS:
* Add MandrivaLinux test case [[#181](https://github.com/python-distro/distro/issues/181)]
* Add test cases for CloudLinux 5, 6, and 7 [[#180](https://github.com/python-distro/distro/issues/180)]

RELEASE:
* Modify MANIFEST to include resources for tests and docs in source tarballs [[97c91a1](97c91a1)]

## 1.0.4 (2017.04.01)

BUG FIXES:
* Guess common \*-release files if /etc not readable [[#175](https://github.com/python-distro/distro/issues/175)]

## 1.0.3 (2017.03.19)

ENHANCEMENTS:
* Show keys for empty values when running distro from the CLI [[#160](https://github.com/python-distro/distro/issues/160)]
* Add manual mapping for `redhatenterpriseserver` (previously only redhatenterpriseworkstation was mapped) [[#148](https://github.com/python-distro/distro/issues/148)]
* Race condition in `_parse_distro_release_file` [[#163](https://github.com/python-distro/distro/issues/163)]

TESTS:
* Add RHEL5 test case [[#165](https://github.com/python-distro/distro/issues/165)]
* Add OpenELEC test case [[#166](https://github.com/python-distro/distro/issues/166)]
* Replace nose with pytest [[#158](https://github.com/python-distro/distro/issues/158)]

RELEASE:
* Update classifiers
* Update supported Python versions (with py36)

## 1.0.2 (2017.01.12)

TESTS:
* Test on py33, py36 and py3 based flake8

RELEASE:
* Add MANIFEST file (which also includes the LICENSE as part of Issue [[#139](https://github.com/python-distro/distro/issues/139)])
* Default to releasing using Twine [[#121](https://github.com/python-distro/distro/issues/121)]
* Add setup.cfg file [[#145](https://github.com/python-distro/distro/issues/145)]
* Update license in setup.py

## 1.0.1 (2016-11-03)

ENHANCEMENTS:
* Prettify distro -j's output and add more elaborate docs [[#147](https://github.com/python-distro/distro/issues/147)]
* Decode output of `lsb_release` as utf-8 [[#144](https://github.com/python-distro/distro/issues/144)]
* Logger now uses `message %s, string` form to not-evaulate log messages if unnecessary [[#145](https://github.com/python-distro/distro/issues/145)]

TESTS:
* Increase code-coverage [[#146](https://github.com/python-distro/distro/issues/146)]
* Fix landscape code-quality warnings [[#145](https://github.com/python-distro/distro/issues/145)]

RELEASE:
* Add CONTRIBUTING.md

## 1.0.0 (2016-09-25)

BACKWARD COMPATIBILITY:
* raise exception when importing on non-supported platforms [[#129](https://github.com/python-distro/distro/issues/129)]

ENHANCEMENTS:
* Use `bytes` invariantly [[#135](https://github.com/python-distro/distro/issues/135)]
* Some minor code adjustments plus a CLI [[#134](https://github.com/python-distro/distro/issues/134)]
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
