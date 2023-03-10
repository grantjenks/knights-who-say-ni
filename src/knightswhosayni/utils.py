import datetime as dt
import hashlib
import uuid


def keygen(key, license_user, days=0):
    if days == 0:
        expiry_days = 0
    else:
        expiry_days = (dt.date.today() - dt.date(1970, 1, 1)).days + days
    key_bytes = uuid.UUID(key).bytes
    user_bytes = license_user.encode('utf-8')
    user_digest = hashlib.sha256(user_bytes).digest()
    code_bytes = bytearray(x ^ y for x, y in zip(key_bytes, user_digest))
    code_bytes[-2] = user_digest[-2] ^ (expiry_days // 256)
    code_bytes[-1] = user_digest[-1] ^ (expiry_days % 256)
    code_uuid = uuid.UUID(bytes=bytes(code_bytes))
    return code_uuid
