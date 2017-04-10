import platform
from ._distribution import Distribution


class WindowsDistribution(Distribution):
    def id(self):
        return 'windows'

    def codename(self):
        return ''

    def name(self, pretty=False):
        name = 'Windows'
        if pretty:
            version = self.version(pretty=True)
            if version:
                name = name + ' ' + version
        return name or ''

    def version(self, pretty=False, best=False):
        version = platform.win32_ver()[1]
        if pretty and version and self.codename():
            version = u'{0} ({1})'.format(version, self.codename())
        return version

    def like(self):
        return ''
