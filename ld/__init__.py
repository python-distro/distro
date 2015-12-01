# /etc/issue
# /etc/system-release
# https://bugs.python.org/issue1322


import os
import re
import constants as const


class LinuxDistribution(object):
    def __init__(self,
                 os_release_file='',
                 lsb_release_file='',
                 distro_release_file='ld/'):
        self.os_release_file = os_release_file or const.OS_RELEASE
        self.lsb_release_file = lsb_release_file or const.LSB_RELEASE
        self.distro_release_file = distro_release_file or ''
        self._os_release_info = self.os_release_info() or {}
        self._lsb_release_info = self.lsb_release_info() or {}
        self._dist_release_info = self.distro_release_info() or {}
        # self.set_distribution_properties()

    def os_release_info(self):
        if os.path.isfile(self.os_release_file):
            with open(self.os_release_file, 'r') as f:
                return self._parse_os_release_file(f)

    def lsb_release_info(self):
        if os.path.isfile(self.lsb_release_file):
            with open(self.lsb_release_file, 'r') as f:
                return self._parse_lsb_release_file(f)

    def distro_release_info(self):
        release_file = self.distro_release_file \
            or self._attempt_to_get_release_file()
        self.dist = self._get_dist_from_release_file(release_file)
        if os.path.isfile(release_file):
            with open(release_file, 'r') as f:
                return self._parse_dist_specific_release_file(f.readline())

    def _parse_lsb_release_file(self, content):
        return self._parse_key_value_files(content)

    def _parse_os_release_file(self, content):
        return self._parse_key_value_files(content)

    def _parse_dist_specific_release_file(self, content):
        return self._parse_release_file(content)

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
        distinf = {}
        for line in content:
            if '=' in line:
                k, v = line.split('=')
                distinf[k.lower()] = v.replace('"', '').rstrip('\n\r')
                # specifically extract code name if possible.
                if k == 'VERSION':
                    codename = re.search(r'\(\w+\)', v)
                    if codename:
                        distinf['codename'] = codename.group().strip('()')
        return distinf

    @staticmethod
    def _parse_release_file(content):
        """Parses a release file.

        This will create a dict with the name, version and codename
        extracted from a release file.
        """
        _release_version = re.compile(
            r'([^0-9]+)(?: release )?([\d+.]+)[^(]*(?:\((.+)\))?')
        name, version, codename = _release_version.match(content).groups()
        distro_release_info = {
            # `release` is appended to the name.
            # TODO: get rid of it completely during grouping.
            'name': name.replace('release', '').strip(),
            'version_id': version,
            'codename': codename
        }
        return distro_release_info

    @staticmethod
    def _get_dist_from_release_file(release_file):
        """Retrieves the distribution from a release file's name.

        This will only return a distribution if it's supported. Otherwise,
        this will return False.
        """
        release_file = os.path.basename(release_file)
        release_file_pattern = re.compile(r'(\w+)([-_])(release|version)')
        m = release_file_pattern.match(release_file)
        if m:
            dist = m.groups()[0]
            if dist in const.DIST_TO_BASE.keys():
                return dist
            return False

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
        """Handles very specific cases to identify distro
        """
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
        return self.get_os_release_attr('id') \
            or self.get_lsb_release_attr('distrib_id').lower() \
            or self.dist \
            or self.get_dist_release_attr('name') \
            or ''

    def name(self, pretty=False):
        if pretty:
            # pretty name should be: name, version (codename)
            # this might not be true for lsb, but we do it here
            # to force consistency.
            name = self.get_os_release_attr('pretty_name') \
                or '{0} {1} ({2})'.format(
                    self.get_lsb_release_attr('distrib_id')
                    or self.get_dist_release_attr('name'),
                    self.get_lsb_release_attr('distrib_release')
                    or self.get_dist_release_attr('version'),
                    self.get_lsb_release_attr('distrib_codename')
                    or self.get_dist_release_attr('codename'))
        else:
            name = self.get_os_release_attr('name') \
                or self.get_lsb_release_attr('distrib_id') \
                or self.get_dist_release_attr('name')
        return name or ''

    def version(self, full=False):
        if full:
            version = self.get_os_release_attr('version') \
                or '{0} ({1})'.format(
                    self.get_lsb_release_attr('distrib_release')
                    or self.get_dist_release_attr('version_id'),
                    self.get_lsb_release_attr('distrib_codename')
                    or self.get_dist_release_attr('codename'))
        else:
            version = self.get_os_release_attr('version_id') \
                or self.get_lsb_release_attr('distrib_release') \
                or self.get_dist_release_attr('version_id')
        return version or ''

    def like(self):
        return self.get_os_release_attr('id_like') or ''

    def codename(self):
        return self.get_os_release_attr('codename') \
            or self.get_lsb_release_attr('distrib_codename') \
            or self.get_dist_release_attr('codename') \
            or ''

    def base(self):
        return const.DIST_TO_BASE.get(
            self.name().lower(),
            self.like().lower()) \
            or ''

    def linux_distribution(self, full_distribution_name=False):
        return (
            self.name() if full_distribution_name else self.id(),
            self.version(),
            self.codename()
        )

ld = LinuxDistribution()


def id():
    return ld.id()


def name(pretty=False):
    return ld.name(pretty)


def version(full=False):
    return ld.version(full)


def like():
    return ld.like()


def codename():
    return ld.codename()


def base():
    return ld.base()


def linux_distribution(full_distribution_name=False):
    return ld.linux_distribution(full_distribution_name)


def distro_release_info():
    return ld.distro_release_info()
