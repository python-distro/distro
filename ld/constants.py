_UNIXCONFDIR = '/etc'
_OS_RELEASE_BASENAME = 'os-release'

# Translation table for normalizing the `ID` attribute defined in `os-release`
# files, for use by the `id()` method.
# * Key: Value as defined in the `os-release` file, translated to lower case,
#   with blanks translated to underscores.
# * Value: Normalized value.
NORMALIZED_OS_ID = {
}

# Translation table for normalizing the `Distribution ID` attribute returned by
# the `lsb_release` command, for use by the `id()` method.
# * Key: Value as returned by the `lsb_release` command, translated to lower
#   case, with blanks translated to underscores.
# * Value: Normalized value.
NORMALIZED_LSB_ID = {
    'enterpriseenterprise': 'oracle',  # Oracle Enterprise Linux TODO version?
    'redhatenterpriseworkstation': 'rhel',  # RHEL 6.7
}

# Translation table for normalizing the distro ID derived from the file name
# of distro release files, for use by the `id()` method.
# * Key: Value as derived from the file name of a distro release file,
#   translated to lower case, with blanks translated to underscores.
# * Value: Normalized value.
NORMALIZED_DISTRO_ID = {
    'suse': 'opensuse',  # openSUSE Linux 13
    'redhat': 'rhel',  # RHEL 6.x, 7.x
}
