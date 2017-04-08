import re


class Distribution(object):
    def distribution(self, full_distribution_name=True):
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
        raise NotImplementedError()

    def name(self, pretty=False):
        """
        Return the name of the Linux distribution, as a string.

        For details, see :func:`distro.name`.
        """
        raise NotImplementedError()

    def version(self, pretty=False, best=False):
        """
        Return the version of the Linux distribution, as a string.

        For details, see :func:`distro.version`.
        """
        raise NotImplementedError()

    def version_parts(self, best=False):
        """
        Return the version of the Linux distribution, as a tuple of version
        numbers.

        For details, see :func:`distro.version_parts`.
        """
        version_str = self.version(best=best)
        if version_str:
            version_regex = re.compile(r'(\d+)\.?(\d+)?\.?(\d+)?')
            matches = version_regex.match(version_str)
            if matches:
                major, minor, build_number = matches.groups()
                return major, minor or '', build_number or ''
        return '', '', ''

    def major_version(self, best=False):
        """
        Return the major version number of the current distribution.

        For details, see :func:`distro.major_version`.
        """
        return self.version_parts(best)[0]

    def minor_version(self, best=False):
        """
        Return the minor version number of the Linux distribution.

        For details, see :func:`distro.minor_version`.
        """
        return self.version_parts(best)[1]

    def build_number(self, best=False):
        """
        Return the build number of the Linux distribution.

        For details, see :func:`distro.build_number`.
        """
        return self.version_parts(best)[2]

    def like(self):
        """
        Return the IDs of distributions that are like the Linux distribution.

        For details, see :func:`distro.like`.
        """
        raise NotImplementedError()

    def codename(self):
        """
        Return the codename of the Linux distribution.

        For details, see :func:`distro.codename`.
        """
        raise NotImplementedError()

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
