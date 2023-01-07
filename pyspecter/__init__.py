import sys

major, minor, *_ = sys.version_info
if major == 3 and minor < 10:
    print(major,minor)
    raise RuntimeError("pyspecter only runs above 3.10, current version")


from .src.pyspecter import *
