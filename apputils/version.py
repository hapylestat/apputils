
# How versioning works:
#
# Branches:
# master     - can produce only alpha versions with dev build number =>  __version__a.devN
# testing    - can produce beta builds and RC candidates (commit msg should contain [RC]) => __version__b|rc.devN
# production - produces release build => __version_.N

__version__ = "0.1.3"
