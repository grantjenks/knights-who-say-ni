# lickey -- Software License Key System

Lickey -- source transform to obfuscate source code and validate license.

How to validate?

1. key in published code  (uuid.UUID4)

>>> import uuid
>>> # uuid.uuid4()
>>> key = uuid.UUID('379a508d-2a6c-4c45-8dc6-51e916dcde13')

2. registered user name  (grant.jenks@gmail.com)

>>> import hashlib
>>> u = hashlib.md5('grant.jenks@gmail.com'.encode()).digest()

3. license code  hex(md5(username) ^ key)

>>> c = b''.join((a ^ b).to_bytes() for a, b in zip(key.bytes, u))
>>> uuid.UUID(bytes=c)

TODO: Reserve last two bytes for license expiry -- recorded in days since epoch
- Any number over 100 years is considered "forever"


## Names

1. lickey -- license key


# Mechanism

RSA -- https://build-system.fman.io/generating-license-keys
https://stuvel.eu/python-rsa-doc/usage.html#signing-and-verification

1. Give me your email
2. Pay
3. Receive license key by email (signature of email)
4. Configure software with email and license key


## Ergonomics

```python
__import__('freegames.__license__').check()
```

```python
# __license__.py

def check():
    module = __import__('freegames')
    module.__title__
    module.__version__

    env_user = 'DJANGO_RRWEB_1_5_3_LICENSE_USER'
    env_code = 'DJANGO_RRWEB_1_5_3_LICENSE_CODE'

    filename = 'django_rrweb_1_5_3_license.ini'
    
    import builtins
    builtins.DJANGO_RRWEB_1_5_3_LICENSE_USER
    builtins.DJANGO_RRWEB_1_5_3_LICENSE_CODE
```

1. File on system
2. Environment variable
3. Value in code



## Validate

1. RSA check
2. Web call
   - Scan for keys and invalidate those published publicly
3. Code check  <-- this one :(



# rot13 obfuscation

```python
import codecs
import glob
import sys

directory = sys.argv[1].rstrip('/')

print('Directory:', directory)

paths = glob.glob(directory + '/**/*.py')

for path in paths:
    print(path)
    with open(path) as reader:
        lines = reader.readlines()
    offset = 1 if lines[0].startswith('#!') else 0
    lines[offset:] = [codecs.encode(line, 'rot13') for line in lines[offset:]]
    lines.insert(offset, '# -*- coding: hex13 -*-\n')
    with open(path, 'w') as writer:
        writer.writelines(lines)
    exit()


init_blurb = """
import codecs as __c
__c.register(
    lambda _: __c.CodecInfo(
        None,
        lambda b: (__c.decode(bytes(b).decode('utf8'), 'rot13'), len(b)),
        name='hex13',
    )
)
"""
```
