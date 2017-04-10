import platform
from ._distribution import Distribution

_MAC_OS_CODENAMES = {('10', '0'): 'Cheetah',
                     ('10', '1'): 'Puma',
                     ('10', '2'): 'Jaguar',
                     ('10', '3'): 'Panther',
                     ('10', '4'): 'Tiger',
                     ('10', '5'): 'Leopard',
                     ('10', '6'): 'Snow Leopard',
                     ('10', '7'): 'Lion',
                     ('10', '8'): 'Mountain Lion',
                     ('10', '9'): 'Mavericks',
                     ('10', '10'): 'Yosemite',
                     ('10', '11'): 'El Capitan',
                     ('10', '12'): "Sierra"}


class MacOSDistribution(Distribution):
    def id(self):
        return 'osx'

    def codename(self):
        key = (self.major_version(), self.minor_version())
        return _MAC_OS_CODENAMES.get(key, '')

    def name(self, pretty=False):
        name = 'Mac OS'
        if pretty:
            version = self.version(pretty=True)
            if version:
                name = name + ' ' + version
        return name or ''

    def version(self, pretty=False, best=False):
        _, (version, _, _), _ = platform.mac_ver()
        if pretty and version and self.codename():
            version = u'{0} ({1})'.format(version, self.codename())
        return version
