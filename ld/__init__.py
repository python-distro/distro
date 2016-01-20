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
        self._os_release_info = self.os_release_info()
        self._lsb_release_info = self.lsb_release_info() if include_lsb else {}
        self._dist_release_info = self.distro_release_info()

    def os_release_info(self):
        """Returns a dictionary containing key value pairs
        of an /etc/os-release file attributes.

        See http://www.freedesktop.org/software/systemd/man/os-release.html
        as a reference.
        """
        if os.path.isfile(self.os_release_file):
            with open(self.os_release_file, 'r') as f:
                return self._parse_key_value_files(f)
        return {}

    def lsb_release_info(self):
        """Returns the parsed output of the `lsb_release -a` command.

        See http://refspecs.linuxfoundation.org/LSB_5.0.0/LSB-Core-generic/LSB-Core-generic/lsbrelease.html  # NOQA
        as a reference.
        """
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
        """Returns a dictionary containing parsed information
        from the /etc/*-release file matching the relevant platform.

        The dict contains the following keys:
        `name` - the name of the distribution.
        `version` - the distribution's release version.
        `codename` - the distribution's codename.

        Note that any of these could be empty if not found.
        """
        release_file = self.distro_release_file \
            or self._attempt_to_get_release_file()
        self.dist = self._get_dist_from_release_file(release_file)
        if os.path.isfile(release_file):
            with open(release_file, 'r') as f:
                # only parse the first line. For instance, on SuSE there are
                # multiple lines. We don't want them...
                return self._parse_release_file(f.readline())
        return {}

    def get_dist_release_attr(self, attribute):
        return self._dist_release_info.get(attribute, '')

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

    @staticmethod
    def _parse_release_file(content):
        """Parses a release file.

        This will create a dict with the name, version and codename
        extracted from a release file.

        In some cases the codename may be irrelevant.
        (e.g. openSUSE 42.1 (x86_64)).

        Under consideration:
        A possible solution could be to not allow codenames which have
        digits in them as there might not be any.
        """
        _release_version = re.compile(
            r'(?:\)(.*)\()? *([\d.+\-a-z]*\d) *(?:esaeler *)?(.+)')
        m = _release_version.match(content.strip()[::-1])
        if not m:
            name = version = codename = ''
            # TODO: Maybe improve this way of handling non-matching
        else:
            name = m.group(3)[::-1]   # regexp ensures it is non-None
            version = m.group(2)[::-1]   # regexp ensures it is non-None
            codename = (m.group(1) or '')[::-1]   # may be None
        props = {
            'name': name,
            'version_id': version,
            'codename': codename
        }
        return props

    @staticmethod
    def _get_dist_from_release_file(some_file):
        """Retrieves the distribution from a release file's name if the file
        provided is indeed a release file.

        This will only return a distribution if it's supported.
        """
        some_file = os.path.basename(some_file)
        release_file_pattern = re.compile(r'(\w+)([-_])(release|version)')
        match = release_file_pattern.match(some_file)
        if match:
            # release files are like: redhat-release or slackware_version.
            # the first part is always assumed to be the dist name.
            dist = match.groups()[0]
            if dist in const._DIST_TO_BASE.keys():
                return dist

    def _attempt_to_get_release_file(self):
        """Looks for release files in the system.

        If a file is found that matches one of the supported distros,
        this will return it.
        """
        # we sort for very specific cases in which
        # there are two distro specific files e.g. CentOS, Oracle, Enterprise
        # all also containing `redhat-release` on top of their own.
        files = os.listdir(const._UNIXCONFDIR)
        files.sort()
        for f in files:
            if self._get_dist_from_release_file(f):
                return f
        return ''

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
            or self.dist \
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
            or self.get_dist_release_attr('name')
        if pretty:
            name = self.get_os_release_attr('pretty_name') \
                or self.get_lsb_release_attr('description')
            if not name:
                name = self.get_dist_release_attr('name')
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
            or self.get_dist_release_attr('version_id') \
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
            or self.get_dist_release_attr('codename') \
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
