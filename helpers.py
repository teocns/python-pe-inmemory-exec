from enum import Enum


class OSType:
    UNIX = 'UNIX'
    WINDOWS = 'WINDOWS'


def get_os_type():
    import platform
    if platform.system() == 'Windows':
        return OSType.WINDOWS
    else:
        return OSType.UNIX
