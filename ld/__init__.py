import os
import re
import subprocess

from . import constants as const

# Pattern for content of distro release file (reversed)
_DISTRO_RELEASE_CONTENT_REVERSED_PATTERN = re.compile(
    r'(?:[^)]*\)(.*)\()? *([\d.+\-a-z]*\d) *(?:esaeler *)?(.+)')

# Pattern for base file name of distro release file
_DISTRO_RELEASE_BASENAME_PATTERN = re.compile(
    r'(\w+)[-_](release|version)')

# Base file names to be ignored when searching for distro release file
_DISTRO_RELEASE_IGNORE_BASENAMES = [
    'debian_version',
    'system-release',
    const._OS_RELEASE_BASENAME
]


class LinuxDistribution(object):
    def __init__(self,
                 include_lsb=True,
                 os_release_file='',
                 distro_release_file=''):
        self.os_release_file = os_release_file or \
            os.path.join(const._UNIXCONFDIR, const._OS_RELEASE_BASENAME)
        self.distro_release_file = distro_release_file or ''
        self._os_release_info = self._get_os_release_info()
        self._lsb_release_info = self._get_lsb_release_info() \
            if include_lsb else {}
        self._distro_release_info = self._get_distro_release_info()

    def __repr__(self):
        return \
            "LinuxDistribution(" \
            "os_release_file=%r, " \
            "distro_release_file=%r, " \
            "_os_release_info=%r, " \
            "_lsb_release_info=%r, " \
            "_distro_release_info=%r)" % \
            (self.os_release_file,
             self.distro_release_file,
             self._os_release_info,
             self._lsb_release_info,
             self._distro_release_info)

    def os_release_info(self):
        """Returns a dictionary containing key-value pairs for all attributes
        found in the `os-release` file. If the file does not exist, an
        empty dictionary is returned. The `os-release` file is expected in the
        `/etc` directory.

        Lines not containing `attr=value` (that is, no `=`), will be ignored.

        TODO: See issue #50 on lines starting with `#`.

        The attribute names found in the file are processed by translating
        them to lower case, before they become the keys of the returned
        dictionary.

        The attribute values found in the file are cleaned up (whitespace,
        quotes), before they become the values of the returned dictionary.

        TODO: See issue #50 on the processing of the values.

        If the attribute "VERSION" is found in the file, the codename is
        extracted from its value if it can be found there. If a codename is
        found, it will be in an additional key "codename" of the returned
        dictionary.

        See http://www.freedesktop.org/software/systemd/man/os-release.html
        for a description of standard attributes defined in the `os-release`
        file.
        """
        # For the code of this description, see _parse_key_value_files()
        return self._os_release_info

    def _get_os_release_info(self):
        if os.path.isfile(self.os_release_file):
            with open(self.os_release_file, 'r') as f:
                return self._parse_key_value_files(f)
        return {}

    def lsb_release_info(self):
        """Returns a dictionary containing key-value pairs for all attributes
        returned by the `lsb_release -a` command in its standard output. If
        the command cannot be executed, an empty dictionary is returned.

        Lines not containing `attr: value` (that is, no `:`), will be ignored.

        The attribute names found in the command output are processed by
        stripping surrounding blanks, translating any remaining blanks to
        underscores, and translating them to lower case, before they become
        the keys of the returned dictionary.

        The attribute values found in the command output are stripped from
        surrounding blanks, before they become the values of the returned
        dictionary.

        See
        http://refspecs.linuxfoundation.org/LSB_5.0.0/LSB-Core-generic/LSB-Core-generic/lsbrelease.html  # NOQA
        for a description of standard attributes returned by the `lsb_release`
        command.
        """
        # For the code of this description, see _parse_lsb_release()
        return self._lsb_release_info

    def _get_lsb_release_info(self):
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE
        r = subprocess.Popen(
            'lsb_release -a',
            shell=True,
            stdout=stdout,
            stderr=stderr).stdout
        content = r.read().decode('ascii').splitlines()
        return self._parse_lsb_release(content) or {}

    def distro_release_info(self):
        """Returns a dictionary containing key-value pairs with information
        from a distro release file.

        If `self.distro_release_file` is set (i.e. `distro_release_file` was
        specified in the constructor), it is used as the path name of the
        distro release file, and the returned dictionary will have those
        entries for which data was found. Note that the returned dictionary
        may be empty.

        If `self.distro_release_file` is not set, a distro release file is
        searched in the `/etc` directory that satisfies all of the following
        conditions:

        * Its file name matches the file name patterns `*-release`,
          `*_release`, `*-version`, or `*_version`.
        * Its first line matches the pattern
          `<name> [[[release] <release>] (<codename>)]`,
          whereby components in square brackets are optional.

        If such a file is found, the returned dictionary will have those
        entries for which data was found, and `self.distro_release_file` is set
        to the path name of the file.
        If such a file is not found, an empty dictionary is returned.

        The returned dictionary will have zero or more of the following
        entries:

        * `id`: (string) Distro ID (e.g. `ubuntu`, `centos`, `redhat`), taken
          from the first part of the file name (that matches the "*" in the
          file name patterns shown above).
        * `name`: (string) Distro name (e.g. `Ubuntu`, `Debian GNU/Linux`),
          as found in the first line of the file.
        * `version_id`: (string) Distro version (e.g. `14.04 LTS`),
          as found in the first line of the file. If not found, this key
          will not be in the dictionary.
        * `codename`: (string) Distro code name (e.g. `Trusty Tahr`),
          as found in the first line of the file. If not found, this key
          will not be in the dictionary.

        TODO: In some cases the code name may be irrelevant (e.g.
        `openSUSE 42.1 (x86_64)`). A possible solution for such code names
        could be to not allow code names which have digits in them as there
        might not be any.
        """
        # For the code of this description, see _get_distro_release_info()
        return self._distro_release_info

    def _get_distro_release_info(self):
        """Parses a distro release file and returns a dictionary
        containing all information found within the file.

        For details, see the description of `distro_release_info()`.
        """
        if self.distro_release_file:
            # If it was specified, we use it and parse what we can, even if
            # its file name or content does not match the expected pattern.
            distro_info = self._parse_distro_release_file(
                self.distro_release_file)
            basename = os.path.basename(self.distro_release_file)
            # The file name pattern for user-specified distro release files
            # is somewhat more tolerant (compared to when searching for the
            # file), because we want to use what was specified as best as
            # possible.
            match = _DISTRO_RELEASE_BASENAME_PATTERN.match(basename)
            if match:
                distro_info['id'] = match.group(1)
            return distro_info
        else:
            basenames = os.listdir(const._UNIXCONFDIR)
            # We sort for repeatability in cases where there are multiple
            # distro specific files; e.g. CentOS, Oracle, Enterprise all
            # containing `redhat-release` on top of their own.
            basenames.sort()
            for basename in basenames:
                if basename in _DISTRO_RELEASE_IGNORE_BASENAMES:
                    continue
                match = _DISTRO_RELEASE_BASENAME_PATTERN.match(basename)
                if match:
                    filepath = os.path.join(const._UNIXCONFDIR, basename)
                    distro_info = self._parse_distro_release_file(filepath)
                    if 'name' in distro_info:
                        # The name is always present if the pattern matches
                        self.distro_release_file = filepath
                        distro_info['id'] = match.group(1)
                        return distro_info
            return {}

    def get_distro_release_attr(self, attribute):
        return self._distro_release_info.get(attribute, '')

    def get_os_release_attr(self, attribute):
        return self._os_release_info.get(attribute, '')

    def get_lsb_release_attr(self, attribute):
        return self._lsb_release_info.get(attribute, '')

    @staticmethod
    def _parse_key_value_files(content):
        """Parses the content of an `os-release` file and returns a dictionary
        containing all information found within the file.

        For details, see the description of `os_release_info()`.

        content: Iterable through the lines in the `os-release` file.
        """
        props = {}
        for line in content:
            if '=' in line:
                k, v = line.split('=')
                # cleanup value
                v = v.replace('"', '')
                v = v.replace("'", '')
                v = v.rstrip('\n\r')
                props[k.lower()] = v
                if k == 'VERSION':
                    # this handles cases in which the codename is in
                    # the `(CODENAME)` (rhel, centos, fedora) format
                    # or in the `, CODENAME` format (Ubuntu).
                    codename = re.search(r'(\(\D+\))|,(\s+)?\D+', v)
                    if codename:
                        codename = codename.group()
                        codename = codename.strip('()')
                        codename = codename.strip(',')
                        codename = codename.strip()
                        # codename appears within paranthese.
                        props['codename'] = codename
                    else:
                        props['codename'] = ''
        return props

    @staticmethod
    def _parse_lsb_release(content):
        """Parses the content of the output of the `lsb_release -a` command
        and returns a dictionary containing all information found within the
        output.

        For details, see the description of `lsb_release_info()`.

        content: Iterable through the lines of the `lsb_release -a` output.
        """
        props = {}
        for obj in content:
            kv = obj.strip('\n').split(':', 1)
            if len(kv) != 2:
                # Ignore lines without colon.
                continue
            k, v = kv
            props.update({k.replace(' ', '_').lower(): v.strip()})
        return props

    def _parse_distro_release_file(self, filepath):
        if os.path.isfile(filepath):
            with open(filepath, 'r') as fp:
                # Only parse the first line. For instance, on SuSE there
                # are multiple lines. We don't want them...
                return self._parse_distro_release_content(fp.readline())
        return {}

    @staticmethod
    def _parse_distro_release_content(content):
        m = _DISTRO_RELEASE_CONTENT_REVERSED_PATTERN.match(
            content.strip()[::-1])
        distro_info = {}
        if m:
            distro_info['name'] = m.group(3)[::-1]   # regexp ensures non-None
            if m.group(2):
                distro_info['version_id'] = m.group(2)[::-1]
            if m.group(1):
                distro_info['codename'] = m.group(1)[::-1]
        return distro_info

    def id(self):
        """Returns the ID for the distribution, as a machine-readable string.

        For a number of Linux distributions, the returned distro ID value is
        *reliable*, in the sense that it is documented and that it does not
        change across releases of the distribution.

        This package maintains the following reliable distro ID values:

        TODO: This list is preliminary and needs review.

        * `ubuntu` - Ubuntu
        * `debian` - Debian
        * `rhel` - RedHat Enterprise Linux
        * `centos` - CentOS
        * `fedora` - Fedora
        * `sles` - SUSE Linux Enterprise Server
        * `opensuse` - openSUSE
        * `amazon` - Amazon Linux
        * `arch` - Arch Linux
        * `cloudlinux` - CloudLinux OS
        * `exherbo` - Exherbo Linux
        * `gentoo` - GenToo Linux
        * `ibm_powerkvm` - IBM PowerKVM
        * `linuxmint` - Linux Mint
        * `mageia` - Mageia
        * `mandriva` - Mandriva Linux
        * `nexus_centos` - TODO: Clarify
        * `parallels` - Parallels
        * `pidora` - Pidora
        * `raspbian` - Raspbian
        * `oracle` - Oracle Linux (and Oracle Enterprise Linux)
        * `scientific` - Scientific Linux
        * `slackware` - Slackware
        * `xenserver` - XenServer

        Note that the distro ID as provided by the `*_release_info()` and
        `get_*_release_attr()` methods is not reliable, these methods provide
        the values as obtained from the respective sources.

        Details:

        First, the ID is obtained from the following sources, in the specified
        order. The first available and non-empty value is used:

        * the value of the "ID" attribute of the `os-release` file,
        * the value of the "Distribution ID" attribute returned by the
          `lsb_release` command,
        * the first part of the file name of the distro release file,
        * the empty string.

        The so determined ID value then passes the following transformations,
        before it is returned by this method:

        * it is translated to lower case,
        * blanks (which should not be there anyway) are translated to
          underscores,
        * a normalization of the ID is performed, based upon translation
          tables in the `constants` module. The purpose of this normalization
          is to ensure that the ID is as reliable as possible, even across
          incompatible changes in the linux distributions. A common case for
          such a change is the addition of an `os-release` file or the addition
          of the `lsb_release` command, with ID values that differ from what
          was previously determined from the distro release file name.
        """
        distro_id = self.get_os_release_attr('id')
        if distro_id:
            distro_id = distro_id.lower().replace(' ', '_')
            return const.NORMALIZED_OS_ID.get(distro_id, distro_id)

        distro_id = self.get_lsb_release_attr('distributor_id')
        if distro_id:
            distro_id = distro_id.lower().replace(' ', '_')
            return const.NORMALIZED_LSB_ID.get(distro_id, distro_id)

        distro_id = self.get_distro_release_attr('id')
        if distro_id:
            distro_id = distro_id.lower().replace(' ', '_')
            return const.NORMALIZED_DISTRO_ID.get(distro_id, distro_id)

        return ''

    def name(self, pretty=False):
        """Returns the name of the distribution.

        If pretty=False returns the name without the version
        and codename (e.g. CentOS Linux)

        If pretty=True, appends the version and codename.
        (e.g. CentOS Linux 7.1.1503 (Core))

        Note that if the name cannot be retrieved and the id
        is available, it will be used instead.
        """
        name = self.get_os_release_attr('name') \
            or self.get_lsb_release_attr('distributor_id') \
            or self.get_distro_release_attr('name')
        if pretty:
            name = self.get_os_release_attr('pretty_name') \
                or self.get_lsb_release_attr('description')
            if not name:
                name = self.get_distro_release_attr('name')
                version = self.version(pretty=True)
                if version:
                    name = name + ' ' + version
        return name or ''

    def version(self, pretty=False):
        """Returns the version of a specific distribution.

        If pretty=False, the version is returned without codename (e.g. 7.0).
        If pretty=True, codename is appended (e.g. 7.0 (Maipo))
        """
        version = self.get_os_release_attr('version_id') \
            or self.get_lsb_release_attr('release') \
            or self.get_distro_release_attr('version_id') \
            or ''
        if pretty and version and self.codename():
            version = '{0} ({1})'.format(version, self.codename())
        return version

    def version_parts(self):
        """Returns a tuple with (major, minor, build_number).
        """
        if self.version():
            g = re.compile(r'(\d+)\.?(\d+)?\.?(\d+)?')
            major, minor, build_number = g.match(self.version()).groups()
            return (major, minor or '', build_number or '')
        return ('', '', '')

    def major_version(self):
        return self.version_parts()[0]

    def minor_version(self):
        return self.version_parts()[1]

    def build_number(self):
        return self.version_parts()[2]

    def like(self):
        """Returns the ID_LIKE field contents from os-release if provided.
        """
        return self.get_os_release_attr('id_like') or ''

    def codename(self):
        """Returns the codename for the distribution's release.

        Note that not all distributions have codenames in which case
        an empty string is returned.

        RedHat, CentOS and Ubuntu (for example) have codenames.

        e.g. trusty (Ubuntu 14.04)
             Santiago (Red Hat 6.5)
             Core (CentOS 7)
        """
        return self.get_os_release_attr('codename') \
            or self.get_lsb_release_attr('codename') \
            or self.get_distro_release_attr('codename') \
            or ''

    def linux_distribution(self, full_distribution_name=True):
        """This attempts to mimic the original `platform.linux_distribution()`
        function.

        The mimicing can never be perfect as the names of the distributions
        themselves changed between versions. For instance, the id of redhat
        in version 7 is `rhel` instead of `redhat`.

        This will return a tuple of (id, version, codename):

        for full_distribution_name=False:
        e.g. ('rhel', '7.0', 'Maipo')
        e.g. ('centos', '7.1.1503', 'Core')
        e.g. ('ubuntu', '14.04', 'trusty')
        e.g. ('Oracle Linux Server', '7.1', '')

        for full_distribution_name=True:
        e.g. ('Red Hat Enterprise Linux Server', '7.0', 'Maipo')
        e.g. ('CentOS Linux', '7.1.1503', 'Core')
        e.g. ('Ubuntu', '14.04', 'trusty')
        e.g. ('oracle', '7.1', '')
        """
        return (
            self.name() if full_distribution_name else self.id(),
            self.version(),
            self.codename()
        )

    def info(self):
        """Returns aggregated machine readable distribution info in lowercase.

        e.g.

        {
            'id': 'rhel',
            'version': '7.0',
            'version_parts': {
                'major': '7',
                'minor': '0',
                'build_number': ''
            },
            'like': 'fedora',
            'codename': 'maipo',
        }
        """
        return dict(
            id=self.id(),
            version=self.version(),
            version_parts=dict(
                major=self.major_version(),
                minor=self.minor_version(),
                build_number=build_number()
            ),
            like=self.like(),
        )

_ldi = LinuxDistribution()


def id():
    return _ldi.id()


def name(pretty=False):
    return _ldi.name(pretty)


def version(pretty=False):
    return _ldi.version(pretty)


def major_version():
    return _ldi.major_version()


def minor_version():
    return _ldi.minor_version()


def build_number():
    return _ldi.build_number()


def like():
    return _ldi.like()


def codename():
    return _ldi.codename()


def linux_distribution(full_distribution_name=True):
    return _ldi.linux_distribution(full_distribution_name)


def os_release_info():
    return _ldi.os_release_info()


def lsb_release_info():
    return _ldi.lsb_release_info()


def distro_release_info():
    return _ldi.distro_release_info()


def info():
    return _ldi.info()
