"""License Check

Utility functions for license check.
"""

import builtins
import configparser
import contextlib
import hashlib
import logging
import os
import pathlib


class LicenseError(Exception):
    pass


def get_value_from_license_file(prefix, key):
    config = configparser.ConfigParser()
    config.read('__NI_PREFIX_LOWER__license.ini')
    section = config['__NI_PREFIX_STRIP__']
    value = section[key]
    return value


def get_user():
    with contextlib.suppress(Exception):
        return __NI_PREFIX__LICENSE_USER
    with contextlib.suppress(Exception):
        return os.environ['__NI_PREFIX__LICENSE_USER']
    with contextlib.suppress(Exception):
        return get_value_from_license_file('LICENSE_USER')
    raise LicenseError('license user is not set')


def get_code():
    with contextlib.suppress(Exception):
        return __NI_PREFIX__LICENSE_CODE
    with contextlib.suppress(Exception):
        return os.environ['__NI_PREFIX__LICENSE_CODE']
    with contextlib.suppress(Exception):
        return get_value_from_license_file('LICENSE_CODE')
    raise LicenseError('license code is not set')


__license_user = get_user()
__license_code = get_code()
__license_pairs = zip(__license_user, __license_code)
__license_xor = [u ^ c for u, c in __license_pairs]
__license_key = __NI_LICENSE_KEY__
__license_key = [byte for byte in __license_key]
if __license_xor != __license_key:
    print(message_key_mismatch)
    logging.critical(message_key_mismatch)
    import os; os._exit(1)
    raise LicenseError(message_key_mismatch)
