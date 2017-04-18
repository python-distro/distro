import os
import re
import sys
import shlex
import subprocess
from ._distribution import Distribution


_UNIXCONFDIR = os.environ.get('UNIXCONFDIR', '/etc')
_OS_RELEASE_BASENAME = 'os-release'

#: Translation table for normalizing the "ID" attribute defined in os-release
#: files, for use by the :func:`distro.id` method.
#:
#: * Key: Value as defined in the os-release file, translated to lower case,
#:   with blanks translated to underscores.
#:
#: * Value: Normalized value.
NORMALIZED_OS_ID = {}

#: Translation table for normalizing the "Distributor ID" attribute returned by
#: the lsb_release command, for use by the :func:`distro.id` method.
#:
#: * Key: Value as returned by the lsb_release command, translated to lower
#:   case, with blanks translated to underscores.
#:
#: * Value: Normalized value.
NORMALIZED_LSB_ID = {
    'enterpriseenterprise': 'oracle',  # Oracle Enterprise Linux
    'redhatenterpriseworkstation': 'rhel',  # RHEL 6, 7 Workstation
    'redhatenterpriseserver': 'rhel',  # RHEL 6, 7 Server
}

#: Translation table for normalizing the distro ID derived from the file name
#: of distro release files, for use by the :func:`distro.id` method.
#:
#: * Key: Value as derived from the file name of a distro release file,
#:   translated to lower case, with blanks translated to underscores.
#:
#: * Value: Normalized value.
NORMALIZED_DISTRO_ID = {
    'redhat': 'rhel',  # RHEL 6.x, 7.x
}

# Pattern for content of distro release file (reversed)
_DISTRO_RELEASE_CONTENT_REVERSED_PATTERN = re.compile(
    r'(?:[^)]*\)(.*)\()? *(?:STL )?([\d.+\-a-z]*\d) *(?:esaeler *)?(.+)')

# Pattern for base file name of distro release file
_DISTRO_RELEASE_BASENAME_PATTERN = re.compile(
    r'(\w+)[-_](release|version)$')

# Base file names to be ignored when searching for distro release file
_DISTRO_RELEASE_IGNORE_BASENAMES = (
    'debian_version',
    'lsb-release',
    'oem-release',
    _OS_RELEASE_BASENAME,
    'system-release'
)


def _normalize_id(distro_id, table):
    distro_id = distro_id.lower().replace(' ', '_')
    return table.get(distro_id, distro_id)


class LinuxDistribution(Distribution):
    """
    Provides information about a Linux distribution.

    This package creates a private module-global instance of this class with
    default initialization arguments, that is used by the
    `consolidated accessor functions`_ and `single source accessor functions`_.
    By using default initialization arguments, that module-global instance
    returns data about the current Linux distribution (i.e. the distro this
    package runs on).

    Normally, it is not necessary to create additional instances of this class.
    However, in situations where control is needed over the exact data sources
    that are used, instances of this class can be created with a specific
    distro release file, or a specific os-release file, or without invoking the
    lsb_release command.
    """

    def __init__(self,
                 include_lsb=True,
                 os_release_file='',
                 distro_release_file=''):
        """
        The initialization method of this class gathers information from the
        available data sources, and stores that in private instance attributes.
        Subsequent access to the information items uses these private instance
        attributes, so that the data sources are read only once.

        Parameters:

        * ``include_lsb`` (bool): Controls whether the
          `lsb_release command output`_ is included as a data source.

          If the lsb_release command is not available in the program execution
          path, the data source for the lsb_release command will be empty.

        * ``os_release_file`` (string): The path name of the
          `os-release file`_ that is to be used as a data source.

          An empty string (the default) will cause the default path name to
          be used (see `os-release file`_ for details).

          If the specified or defaulted os-release file does not exist, the
          data source for the os-release file will be empty.

        * ``distro_release_file`` (string): The path name of the
          `distro release file`_ that is to be used as a data source.

          An empty string (the default) will cause a default search algorithm
          to be used (see `distro release file`_ for details).

          If the specified distro release file does not exist, or if no default
          distro release file can be found, the data source for the distro
          release file will be empty.

        Public instance attributes:

        * ``os_release_file`` (string): The path name of the
          `os-release file`_ that is actually used as a data source. The
          empty string if no distro release file is used as a data source.

        * ``distro_release_file`` (string): The path name of the
          `distro release file`_ that is actually used as a data source. The
          empty string if no distro release file is used as a data source.

        Raises:

        * :py:exc:`IOError`: Some I/O issue with an os-release file or distro
          release file.

        * :py:exc:`subprocess.CalledProcessError`: The lsb_release command had
          some issue (other than not being available in the program execution
          path).

        * :py:exc:`UnicodeError`: A data source has unexpected characters or
          uses an unexpected encoding.
        """
        self.os_release_file = os_release_file or \
            os.path.join(_UNIXCONFDIR, _OS_RELEASE_BASENAME)
        self.distro_release_file = distro_release_file or ''  # updated later
        self._os_release_info = self._get_os_release_info()
        self._lsb_release_info = self._get_lsb_release_info() \
            if include_lsb else {}
        self._distro_release_info = self._get_distro_release_info()

    def __repr__(self):
        """Return repr of all info
        """
        return \
            "LinuxDistribution(" \
            "os_release_file={0!r}, " \
            "distro_release_file={1!r}, " \
            "_os_release_info={2!r}, " \
            "_lsb_release_info={3!r}, " \
            "_distro_release_info={4!r})".format(
                self.os_release_file,
                self.distro_release_file,
                self._os_release_info,
                self._lsb_release_info,
                self._distro_release_info)

    def linux_distribution(self, full_distribution_name=True):
        """
        Return information about the Linux distribution that is compatible
        with Python's :func:`platform.linux_distribution`, supporting a subset
        of its parameters.

        For details, see :func:`distro.linux_distribution`.
        """
        return (
            self.name() if full_distribution_name else self.id(),
            self.version(),
            self.codename()
        )

    def id(self):
        """Return the distro ID of the Linux distribution, as a string.

        For details, see :func:`distro.id`.
        """
        distro_id = self.os_release_attr('id')
        if distro_id:
            return _normalize_id(distro_id, NORMALIZED_OS_ID)

        distro_id = self.lsb_release_attr('distributor_id')
        if distro_id:
            return _normalize_id(distro_id, NORMALIZED_LSB_ID)

        distro_id = self.distro_release_attr('id')
        if distro_id:
            return _normalize_id(distro_id, NORMALIZED_DISTRO_ID)

        return ''

    def name(self, pretty=False):
        """
        Return the name of the Linux distribution, as a string.

        For details, see :func:`distro.name`.
        """
        name = self.os_release_attr('name') \
            or self.lsb_release_attr('distributor_id') \
            or self.distro_release_attr('name')
        if pretty:
            name = self.os_release_attr('pretty_name') \
                or self.lsb_release_attr('description')
            if not name:
                name = self.distro_release_attr('name')
                version = self.version(pretty=True)
                if version:
                    name = name + ' ' + version
        return name or ''

    def version(self, pretty=False, best=False):
        """
        Return the version of the Linux distribution, as a string.

        For details, see :func:`distro.version`.
        """
        versions = [
            self.os_release_attr('version_id'),
            self.lsb_release_attr('release'),
            self.distro_release_attr('version_id'),
            self._parse_distro_release_content(
                self.os_release_attr('pretty_name')).get('version_id', ''),
            self._parse_distro_release_content(
                self.lsb_release_attr('description')).get('version_id', '')
        ]
        version = ''
        if best:
            # This algorithm uses the last version in priority order that has
            # the best precision. If the versions are not in conflict, that
            # does not matter; otherwise, using the last one instead of the
            # first one might be considered a surprise.
            for v in versions:
                if v.count(".") > version.count(".") or version == '':
                    version = v
        else:
            for v in versions:
                if v != '':
                    version = v
                    break
        if pretty and version and self.codename():
            version = u'{0} ({1})'.format(version, self.codename())
        return version

    def like(self):
        """
        Return the IDs of distributions that are like the Linux distribution.

        For details, see :func:`distro.like`.
        """
        return self.os_release_attr('id_like') or ''

    def codename(self):
        """
        Return the codename of the Linux distribution.

        For details, see :func:`distro.codename`.
        """
        return self.os_release_attr('codename') \
            or self.lsb_release_attr('codename') \
            or self.distro_release_attr('codename') \
            or ''

    def info(self, pretty=False, best=False):
        """
        Return certain machine-readable information about the Linux
        distribution.

        For details, see :func:`distro.info`.
        """
        return dict(
            id=self.id(),
            version=self.version(pretty, best),
            version_parts=dict(
                major=self.major_version(best),
                minor=self.minor_version(best),
                build_number=self.build_number(best)
            ),
            like=self.like(),
            codename=self.codename(),
        )

    def os_release_info(self):
        """
        Return a dictionary containing key-value pairs for the information
        items from the os-release file data source of the Linux distribution.

        For details, see :func:`distro.os_release_info`.
        """
        return self._os_release_info

    def lsb_release_info(self):
        """
        Return a dictionary containing key-value pairs for the information
        items from the lsb_release command data source of the Linux
        distribution.

        For details, see :func:`distro.lsb_release_info`.
        """
        return self._lsb_release_info

    def distro_release_info(self):
        """
        Return a dictionary containing key-value pairs for the information
        items from the distro release file data source of the Linux
        distribution.

        For details, see :func:`distro.distro_release_info`.
        """
        return self._distro_release_info

    def os_release_attr(self, attribute):
        """
        Return a single named information item from the os-release file data
        source of the Linux distribution.

        For details, see :func:`distro.os_release_attr`.
        """
        return self._os_release_info.get(attribute, '')

    def lsb_release_attr(self, attribute):
        """
        Return a single named information item from the lsb_release command
        output data source of the Linux distribution.

        For details, see :func:`distro.lsb_release_attr`.
        """
        return self._lsb_release_info.get(attribute, '')

    def distro_release_attr(self, attribute):
        """
        Return a single named information item from the distro release file
        data source of the Linux distribution.

        For details, see :func:`distro.distro_release_attr`.
        """
        return self._distro_release_info.get(attribute, '')

    def _get_os_release_info(self):
        """
        Get the information items from the specified os-release file.

        Returns:
            A dictionary containing all information items.
        """
        if os.path.isfile(self.os_release_file):
            with open(self.os_release_file) as release_file:
                return self._parse_os_release_content(release_file)
        return {}

    @staticmethod
    def _parse_os_release_content(lines):
        """
        Parse the lines of an os-release file.

        Parameters:

        * lines: Iterable through the lines in the os-release file.
                 Each line must be a unicode string or a UTF-8 encoded byte
                 string.

        Returns:
            A dictionary containing all information items.
        """
        props = {}
        lexer = shlex.shlex(lines, posix=True)
        lexer.whitespace_split = True

        # The shlex module defines its `wordchars` variable using literals,
        # making it dependent on the encoding of the Python source file.
        # In Python 2.6 and 2.7, the shlex source file is encoded in
        # 'iso-8859-1', and the `wordchars` variable is defined as a byte
        # string. This causes a UnicodeDecodeError to be raised when the
        # parsed content is a unicode object. The following fix resolves that
        # (... but it should be fixed in shlex...):
        if sys.version_info[0] == 2 and isinstance(lexer.wordchars, bytes):
            lexer.wordchars = lexer.wordchars.decode('iso-8859-1')

        tokens = list(lexer)
        for token in tokens:
            # At this point, all shell-like parsing has been done (i.e.
            # comments processed, quotes and backslash escape sequences
            # processed, multi-line values assembled, trailing newlines
            # stripped, etc.), so the tokens are now either:
            # * variable assignments: var=value
            # * commands or their arguments (not allowed in os-release)
            if '=' in token:
                k, v = token.split('=', 1)
                if isinstance(v, bytes):
                    v = v.decode('utf-8')
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
            else:
                # Ignore any tokens that are not variable assignments
                pass
        return props

    def _get_lsb_release_info(self):
        """
        Get the information items from the lsb_release command output.

        Returns:
            A dictionary containing all information items.
        """
        cmd = 'lsb_release -a'
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        stdout, stderr = stdout.decode('utf-8'), stderr.decode('utf-8')
        code = process.returncode
        if code == 0:
            content = stdout.splitlines()
            return self._parse_lsb_release_content(content)
        elif code == 127:  # Command not found
            return {}
        else:
            if sys.version_info[:2] >= (3, 5):
                raise subprocess.CalledProcessError(code, cmd, stdout, stderr)
            elif sys.version_info[:2] >= (2, 7):
                raise subprocess.CalledProcessError(code, cmd, stdout)
            elif sys.version_info[:2] == (2, 6):
                raise subprocess.CalledProcessError(code, cmd)

    @staticmethod
    def _parse_lsb_release_content(lines):
        """
        Parse the output of the lsb_release command.

        Parameters:

        * lines: Iterable through the lines of the lsb_release output.
                 Each line must be a unicode string or a UTF-8 encoded byte
                 string.

        Returns:
            A dictionary containing all information items.
        """
        props = {}
        for line in lines:
            line = line.decode('utf-8') if isinstance(line, bytes) else line
            kv = line.strip('\n').split(':', 1)
            if len(kv) != 2:
                # Ignore lines without colon.
                continue
            k, v = kv
            props.update({k.replace(' ', '_').lower(): v.strip()})
        return props

    def _get_distro_release_info(self):
        """
        Get the information items from the specified distro release file.

        Returns:
            A dictionary containing all information items.
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
            try:
                basenames = os.listdir(_UNIXCONFDIR)
                # We sort for repeatability in cases where there are multiple
                # distro specific files; e.g. CentOS, Oracle, Enterprise all
                # containing `redhat-release` on top of their own.
                basenames.sort()
            except OSError:
                # This may occur when /etc is not readable but we can't be
                # sure about the *-release files. Check common entries of
                # /etc for information. If they turn out to not be there the
                # error is handled in `_parse_distro_release_file()`.
                basenames = ['SuSE-release',
                             'arch-release',
                             'base-release',
                             'centos-release',
                             'fedora-release',
                             'gentoo-release',
                             'mageia-release',
                             'mandrake-release',
                             'mandriva-release',
                             'mandrivalinux-release',
                             'manjaro-release',
                             'oracle-release',
                             'redhat-release',
                             'sl-release',
                             'slackware-version']
            for basename in basenames:
                if basename in _DISTRO_RELEASE_IGNORE_BASENAMES:
                    continue
                match = _DISTRO_RELEASE_BASENAME_PATTERN.match(basename)
                if match:
                    filepath = os.path.join(_UNIXCONFDIR, basename)
                    distro_info = self._parse_distro_release_file(filepath)
                    if 'name' in distro_info:
                        # The name is always present if the pattern matches
                        self.distro_release_file = filepath
                        distro_info['id'] = match.group(1)
                        return distro_info
            return {}

    def _parse_distro_release_file(self, filepath):
        """
        Parse a distro release file.

        Parameters:

        * filepath: Path name of the distro release file.

        Returns:
            A dictionary containing all information items.
        """
        try:
            with open(filepath) as fp:
                # Only parse the first line. For instance, on SLES there
                # are multiple lines. We don't want them...
                return self._parse_distro_release_content(fp.readline())
        except (OSError, IOError):
            # Ignore not being able to read a specific, seemingly version
            # related file.
            # See https://github.com/nir0s/distro/issues/162
            return {}

    @staticmethod
    def _parse_distro_release_content(line):
        """
        Parse a line from a distro release file.

        Parameters:
        * line: Line from the distro release file. Must be a unicode string
                or a UTF-8 encoded byte string.

        Returns:
            A dictionary containing all information items.
        """
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        matches = _DISTRO_RELEASE_CONTENT_REVERSED_PATTERN.match(
            line.strip()[::-1])
        distro_info = {}
        if matches:
            # regexp ensures non-None
            distro_info['name'] = matches.group(3)[::-1]
            if matches.group(2):
                distro_info['version_id'] = matches.group(2)[::-1]
            if matches.group(1):
                distro_info['codename'] = matches.group(1)[::-1]
        elif line:
            distro_info['name'] = line.strip()
        return distro_info


class LinuxMintDistribution(LinuxDistribution):
    """ LinuxMint has the same /etc/os-release file as
    Ubuntu and will give incorrect information as os-release
    is always prioritized over lsb-release. """
    def os_release_attr(self, attribute):
        if attribute == 'id_like':
            return super(LinuxMintDistribution, self).os_release_attr(attribute)
        return ''


def get_distribution():
    ld = LinuxDistribution()
    if (_normalize_id(ld.os_release_attr('id'),
                      NORMALIZED_OS_ID) == 'ubuntu' and
                _normalize_id(ld.lsb_release_attr('distributor_id'),
                              NORMALIZED_OS_ID) == 'linuxmint'):
        return LinuxMintDistribution()
    else:
        return ld
