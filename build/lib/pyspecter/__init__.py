import sys

major, minor, *_ = sys.version_info

if major == 3 and minor < 10:
    raise RuntimeError("pyspecter only runs above 3.10, current version")

if major == 2:
    raise RuntimeError("pyspecter only runs above 3.10, current version is Python 2.x")

from .pyspecter import *
