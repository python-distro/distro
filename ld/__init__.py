import os
import re
import subprocess

from . import constants as const


class LinuxDistribution(object):
    def __init__(self,
                 include_lsb=True,
                 os_release_file='',
                 distro_release_file=''):
        self.os_release_file = os_release_file or const._OS_RELEASE
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
        """Returns a dictionary containing key value pairs
        of an /etc/os-release file attributes.

        See http://www.freedesktop.org/software/systemd/man/os-release.html
        as a reference.
        """
        return self._os_release_info

    def _get_os_release_info(self):
        if os.path.isfile(self.os_release_file):
            with open(self.os_release_file, 'r') as f:
                return self._parse_key_value_files(f)
        return {}

    def lsb_release_info(self):
        """Returns the parsed output of the `lsb_release -a` command.

        See http://refspecs.linuxfoundation.org/LSB_5.0.0/LSB-Core-generic/LSB-Core-generic/lsbrelease.html  # NOQA
        as a reference.
        """
        return self._lsb_release_info

    def _get_lsb_release_info(self):
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE
        r = subprocess.Popen(
            'lsb_release -a',
            shell=True,
            stdout=stdout,
            stderr=stderr).stdout
        return self._parse_lsb_release(
            r.read().decode('ascii').splitlines()) or {}

    def distro_release_info(self):
        """Returns a dict with information from a distro release file.

        If `self.distro_release_file` is set (i.e. `distro_release_file` was
        specified in the constructor), it is used as the path name of the
        distro release file, and the returned dict will have those entries for
        which data was found. Note that the returned dict may be empty.

        If `self.distro_release_file` is not set, a distro release file is
        searched in the `/etc` directory that satisfies all of the following
        conditions:
        * Its file name matches the file name patterns `*-release` or
          `*_release`.
        * Its first line matches the pattern
          `<name> [[[release] <release>] (<codename>)]`,
          whereby components in square brackets are optional.
        If such a file is found, the returned dict will have those entries for
        which data was found, and `self.distro_release_file` is set to the
        path name of the file. If such a file is not found, an empty dict is
        returned.

        The returned dict will have zero or more of the following entries:
        * `id`: (string) Distro ID (e.g. `ubuntu`, `centos`, `redhat`), taken
          from the first part of the file name.
        * `name`: (string) Distro name (e.g. `Ubuntu`, `Debian GNU/Linux`),
          as found in the first line of the file.
        * `version_id`: (string) Distro version (e.g. `14.04 LTS`),
          as found in the first line of the file.
        * `codename`: (string) Distro code name (e.g. `Trusty Tahr`),
          as found in the first line of the file.

        TODO: In some cases the code name may be irrelevant (e.g.
        `openSUSE 42.1 (x86_64)`). A possible solution for such code names
        could be to not allow code names which have digits in them as there
        might not be any.
        """
        return self._distro_release_info

    def _get_distro_release_info(self):
        if self.distro_release_file:
            # If it was specified, we use it and parse what we can, even if
            # its file name or content does not match the expected pattern.
            distro_info = self._parse_distro_release_file(
                self.distro_release_file)
            basefile = os.path.basename(self.distro_release_file)
            # The file name pattern for user-specified distro release files
            # is somewhat more tolerant (compared to when searching for the
            # file), because we want to use what was specified as best as
            # possible.
            release_file_pattern = re.compile(r'(\w+)[-_](release|version)')
            match = release_file_pattern.match(basefile)
            if match:
                distro_id = match.group(1)
                # TODO: Normalize distro_id
                distro_info['id'] = distro_id
            return distro_info
        else:
            files = os.listdir(const._UNIXCONFDIR)
            # We sort for repeatability in cases where there are multiple
            # distro specific files; e.g. CentOS, Oracle, Enterprise all
            # containing `redhat-release` on top of their own.
            files.sort()
            release_file_pattern = re.compile(r'(\w+)[-_]release')
            for basefile in files:
                match = release_file_pattern.match(basefile)
                if match:
                    distro_id = match.group(1)
                    # TODO: Normalize distro_id
                    filepath = os.path.join(const._UNIXCONFDIR, basefile)
                    distro_info = self._parse_distro_release_file(filepath)
                    if 'name' in distro_info:
                        # The name is always present if the pattern matches
                        self.distro_release_file = filepath
                        distro_info['id'] = distro_id
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
        """Parses an os-release or lsb-release file and returns a
        dict containing all information found within the file.

        Lines not containing key=value (that is, no `=`), wil be ignored.
        Specifically, if "VERSION" is found, this will try to extract
        the codename from it as it is sometimes found there.
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
        """Returns a dict containing key:value pairs of the output
        of the `lsb_release -a` command.

        Note that all keys will be in lower case and any spaces
        contained within the keys will be replaced with underscores.
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
        _release_version = re.compile(
            r'(?:[^)]*\)(.*)\()? *([\d.+\-a-z]*\d) *(?:esaeler *)?(.+)')
        m = _release_version.match(content.strip()[::-1])
        distro_info = {}
        if m:
            distro_info['name'] = m.group(3)[::-1]   # regexp ensures non-None
            if m.group(2):
                distro_info['version_id'] = m.group(2)[::-1]
            if m.group(1):
                distro_info['codename'] = m.group(1)[::-1]
        return distro_info

    def id(self):
        """Returns the id for the distribution.

        This should be a machine readable name.

        e.g. ubuntu, centos, oracle, slackware, etc.

        If os-release and lsb-release do not exist, an attempt to
        extract the id from the name of the release file will be
        attempted. It's important to note that this falls back to the name
        of the distribution if the id cannot be retrieved by any other means.
        """
        return self.get_os_release_attr('id') \
            or self.get_lsb_release_attr('distributor_id').lower() \
            or self.get_distro_release_attr('id') \
            or ''

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

    def base(self):
        """Returns the base distribution upon which the distro is based.

        A table for that is provided in `constants.py` where each supported
        distribution is converted to its base distribution.

        e.g. 'ubuntu': 'debian'
             'oracle': 'rhel'
             'redhat': 'rhel'
        """
        return const._DIST_TO_BASE.get(
            self.id().lower(),
            self.like().lower()) \
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
            'base': 'fedora'
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
            base=self.base()
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


def base():
    return _ldi.base()


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
