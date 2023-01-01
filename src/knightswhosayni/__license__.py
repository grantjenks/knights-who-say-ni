"""License Check

TODO

1. Reserve last two bytes for license expiry -- recorded in dates since epoch
with any number over 100 years considered "forever".
"""

import builtins
import configparser
import contextlib
import hashlib
import os
import pathlib


class LicenseError(Exception):
    pass


def get_value_from_license_file(prefix, module, key):
    filename = f'{prefix.lower()}license.ini'
    path = pathlib.Path(__import__(module).__file__)
    # TODO: This ^^ won't work! The license file should go in the consumer.
    config = configparser.ConfigParser()
    config.read(path)
    section config[prefix.rstrip('_')]
    value = section[key]
    return value


def check():
    """Check license.

    __import__('freegames.__license__').check()
    """
    prefix = '__NI_PREFIX__'
    module = '__NI_MODULE__'

    env_user = f'{prefix}LICENSE_USER'
    env_code = f'{prefix}LICENSE_CODE'

    license_user = None
    license_code = None

    # Support license keys in code.
    with contextlib.suppress(Exception):
        license_user = getattr(builtins, env_user)

    with contextlib.suppress(Exception):
        license_code = getattr(builtins, env_code)

    # Support environment variables.
    with contextlib.suppress(Exception):
        license_user = os.environ.get(env_user)

    with contextlib.suppress(Exception):
        license_code = os.environ.get(env_code)

    # Support license file.

    with contextlib.suppress(Exception):
        license_user = get_value_from_license_file('LICENSE_USER')

    with contextlib.suppress(Exception):
        license_code = get_value_from_license_file('LICENSE_CODE')

    if license_user is None:
        raise LicenseError('license user is not set')

    if license_code is None:
        raise LicenseError('license code is not set')

    user_digest = hashlib.sha256(license_user.encode()).digest()
    code = uuid.UUID(license_code)
    code_bytes = code.bytes + code.bytes
    xor_bytes = bytes(u ^ c for u, c in zip(user_digest, code_bytes))
    key = uuid.UUID('__NI_LICENSE_KEY__')
    key_bytes = key.bytes + key.bytes

    if xor_bytes != key_bytes:
        raise LicenseError('invalid license')
