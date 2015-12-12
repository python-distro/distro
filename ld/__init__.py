import os
import re
import constants as const


class LinuxDistribution(object):
    def __init__(self,
                 os_release_file='',
                 lsb_release_file='',
                 distro_release_file=''):
        self.os_release_file = os_release_file or const.OS_RELEASE
        self.lsb_release_file = lsb_release_file or const.LSB_RELEASE
        self.distro_release_file = distro_release_file or ''
        self._os_release_info = self.os_release_info()
        self._lsb_release_info = self.lsb_release_info()
        self._dist_release_info = self.distro_release_info()

    def os_release_info(self):
        if os.path.isfile(self.os_release_file):
            with open(self.os_release_file, 'r') as f:
                return self._parse_key_value_files(f)
        return {}

    def lsb_release_info(self):
        if os.path.isfile(self.lsb_release_file):
            with open(self.lsb_release_file, 'r') as f:
                return self._parse_key_value_files(f)
        return {}

    def distro_release_info(self):
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
    def _parse_release_file(content):
        """Parses a release file.

        This will create a dict with the name, version and codename
        extracted from a release file.
        """
        # this assumes that codename can only be made out of letters.
        # for instance, in SuSE's release file, you might find (x86_64)
        # in parantheses which is obviously not a codename.
        _release_version = re.compile(
            r'([^0-9]+)?(?: release )?([\d+.]+)[^(]*(?:\(([\D]+)\))?')
        name, version, codename = _release_version.match(content).groups()
        props = {
            # `release` is appended to the name.
            # TODO: get rid of it completely during grouping.
            'name': (name or '').replace('release', '').strip(),
            'version_id': version or '',
            'codename': codename or ''
        }
        return props

    @staticmethod
    def _get_dist_from_release_file(some_file):
        """Retrieves the distribution from a release file's name if the file
        provided is indeed a release file.

        This will only return a distribution if it's supported. Otherwise,
        this will return False.
        """
        some_file = os.path.basename(some_file)
        release_file_pattern = re.compile(r'(\w+)([-_])(release|version)')
        match = release_file_pattern.match(some_file)
        if match:
            # release files are like: redhat-release or slackware_version.
            # the first part is always assumed to be the dist name.
            dist = match.groups()[0]
            if dist in const.DIST_TO_BASE.keys():
                return dist

    def _attempt_to_get_release_file(self):
        """Looks for release files in the system.

        If a file is found that matches one of the supported distros,
        this will return it.
        """
        # we sort for very specific cases in which
        # there are two distro specific files e.g. CentOS, Oracle, Enterprise
        # all also containing `redhat-release` on top of their own.
        files = os.listdir(const.UNIXCONFDIR)
        files.sort()
        for f in files:
            if self._get_dist_from_release_file(f):
                return f
        return ''

    def set_distribution_properties(self):
        """WIP! This should handle all exceptional release files."""
        if os.path.isfile(const.DEBIAN_VERSION):
            dist = self.get_lsb_release_attr('distrib_id').lower()
            if dist:
                self.dist = dist
                self.ver = self.get_lsb_release_attr(
                    'distrib_release').lower()
                self.code = self.get_lsb_release_attr(
                    'distrib_codename').lower()
                return
            else:
                if os.path.isfile('/usr/bin/raspi-config'):
                    self.dist = 'raspbian'
                else:
                    self.dist = 'debian'
                self.distro_release_file = const.DEBIAN_VERSION
        elif os.path.isfile(const.SUSE_RELEASE):
            with open(const.SUSE_RELEASE, 'r') as f:
                if re.search('opensuse', f.read()):
                    self.dist = 'opensuse'
                else:
                    self.dist = 'suse'
                self.distro_release_file = const.SUSE_RELEASE

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
            or self.get_lsb_release_attr('distrib_id').lower() \
            or self.dist \
            or self.get_dist_release_attr('name') \
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
        if pretty:
            # pretty name should be: name, version (codename)
            # this might not be true for lsb, but we do it here
            # to force consistency.
            name = self.get_os_release_attr('pretty_name')
            if not name:
                name = self.get_lsb_release_attr('distrib_id') \
                    or self.get_dist_release_attr('name') \
                    or self.id()
                version = self.version(pretty=True)
                # this is only eligable if `name` exists..
                if version and name:
                    name = '{0} {1}'.format(name, version)
        else:
            name = self.get_os_release_attr('name') \
                or self.get_lsb_release_attr('distrib_id') \
                or self.get_dist_release_attr('name') \
                or self.id()
        return name or ''

    def version(self, pretty=False):
        """Returns the version of a specific distribution.

        If pretty=False, the version is returned without codename (e.g. 7.0).
        If pretty=True, codename is appended (e.g. 7.0 (Maipo))
        """
        if pretty:
            version = self.get_os_release_attr('version')
            if not version:
                version = self.get_lsb_release_attr('distrib_release') \
                    or self.get_dist_release_attr('version_id')
                # this is only eligable if `version` exists..
                if version and self.codename():
                    version = '{0} ({1})'.format(version, self.codename())
        else:
            version = self.get_os_release_attr('version_id') \
                or self.get_lsb_release_attr('distrib_release') \
                or self.get_dist_release_attr('version_id')
        return version or ''

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
            or self.get_lsb_release_attr('distrib_codename') \
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
        return const.DIST_TO_BASE.get(
            self.name().lower(),
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
        i = dict(
            id=self.id(),
            name=self.name(),
            version=self.version(),
            version_parts=dict(
                major=self.major_version(),
                minor=self.minor_version(),
                build_number=build_number()
            ),
            like=self.like(),
            codename=self.codename(),
            base=self.base()
        )
        for k, v in i.items():
            if isinstance(v, str):
                i[k] = v.lower()
        return i


ldi = LinuxDistribution()


def id():
    return ldi.id()


def name(pretty=False):
    return ldi.name(pretty)


def version(pretty=False):
    return ldi.version(pretty)


def major_version():
    return ldi.major_version()


def minor_version():
    return ldi.minor_version()


def build_number():
    return ldi.build_number()


def like():
    return ldi.like()


def codename():
    return ldi.codename()


def base():
    return ldi.base()


def linux_distribution(full_distribution_name=True):
    return ldi.linux_distribution(full_distribution_name)


def os_release_info():
    return ldi.os_release_info()


def lsb_release_info():
    return ldi.lsb_release_info()


def distro_release_info():
    return ldi.distro_release_info()


def info():
    return ldi.info()
