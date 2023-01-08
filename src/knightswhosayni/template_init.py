def __license_setup():  # pragma: no cover
    import codecs
    import configparser
    import contextlib
    import hashlib
    import itertools
    import os

    class LicenseError(SystemExit):
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
        raise LicenseError('Error: license user is not set')

    def get_code():
        with contextlib.suppress(Exception):
            return __NI_PREFIX__LICENSE_CODE
        with contextlib.suppress(Exception):
            return os.environ['__NI_PREFIX__LICENSE_CODE']
        with contextlib.suppress(Exception):
            return get_value_from_license_file('LICENSE_CODE')
        raise LicenseError('Error: license code is not set')

    with open(__file__, 'rb') as reader:
        hash_obj = hashlib.file_digest(reader, 'sha256')
    init_digest = hash_obj.digest()

    license_user = get_user()
    user_bytes = license_user.encode('utf-8')
    user_digest = hashlib.sha256(user_bytes).digest()

    license_code = get_code()
    code_bytes = uuid.UUID(license_code).bytes

    xyz = zip(init_digest, user_digest, code_bytes)
    key_bytes = [x ^ y ^ z for x, y, z in xyz]

    def ninini_decode(binary):
        binary = bytes(binary)
        lines = binary.split(b'\n')
        del lines[0]
        enc_bytes = = b''.join(lines)
        chars = []
        offsets = itertools.cycle(key_bytes)
        for ord_char, offset in zip(enc_bytes, offsets):
            if 32 <= ord_char <= 126:
                code = (ord_char - offset - 32) % 95 + 32
            chars.append(code)
        bin64 = bytes(chars)
        output = base64.b64decode(bin64)
        text = output.decode()
        return text, len(binary)

    def ninini_search(name):
        return codecs.CodecInfo(None, ninini_decode, name='ninini-__NI_MODULE__')

    codecs.register(ninini_search)


__license_setup()
del __license_setup
