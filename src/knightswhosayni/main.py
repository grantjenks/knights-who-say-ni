"""Knights Who Say Ni!

$ export KNIGHTS_WHO_SAY_NI_KEY=$(python -c "import uuid; print(uuid.uuid4())")
$ export KNIGHTS_WHO_SAY_NI_KEY=6f42e628-0aa4-45da-ab41-e734e7e2b1c8
$ knightswhosayni transform src django_codemirror6 DJANGO_CODEMIRROR6_
$ knightswhosayni keygen grant.jenks@gmail.com 7

TODO

* Generate real keys in web form for trial

* Workflow for sale:

1. Visit PyPI, click link to buy license.

2. Visit popcountsoftware.com/django-rrweb/ -- click link to buy

3. Visit gumroad.com/l/django-rrweb -- pay and get redirected
   https://app.gumroad.com/api#resource-subscriptions

4. Visit popcountsoftware.com/django-rrweb/ and receive license
   https://help.gumroad.com/article/154-custom-delivery-products

* Use license key as salt for username hash

* Provide reusable GitHub workflow for testing and releasing code.

"""

import argparse
import base64
import datetime as dt
import glob
import hashlib
import itertools
import os
import pathlib
import random
import uuid


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command', help='sub-command help')
    subparsers.required = True

    parser_transform = subparsers.add_parser('transform')
    parser_transform.add_argument('src')
    parser_transform.add_argument('name')
    parser_transform.add_argument('prefix')

    parser_keygen = subparsers.add_parser('keygen')
    parser_keygen.add_argument('license_user')
    parser_keygen.add_argument('days', default=0, nargs='?', type=int)

    args = parser.parse_args()

    if args.command == 'transform':
        transform(args.src, args.name, args.prefix)
    if args.command == 'keygen':
        keygen(args.license_user, args.days)


def transform(src_dir, name, prefix):
    src_dir = pathlib.Path(src_dir)
    parent_dir = pathlib.Path(__file__).parent

    # Setup __init__.py template for injection.
    init_template = (parent_dir / 'template_init.py').read_text()
    init_template = init_template.replace('__NI_MODULE__', name)
    init_template = (
        init_template
        .replace('__NI_MODULE__', name)
        .replace('__NI_PREFIX__', prefix)
        .replace('__NI_PREFIX_LOWER__', prefix.lower())
        .replace('__NI_PREFIX_STRIP__', prefix.rstrip('_'))
    )

    # Inject codecs code into __init__.py
    init_path = (src_dir / name / '__init__.py')
    init_text = init_path.read_text()
    init_lines = init_text.split('\n')
    index = init_lines.index('"""') + 1
    init_lines.insert(index, '\n\n' + init_template)
    init_text = '\n'.join(init_lines)
    init_path.write_text(init_text)

    # Compute sha256 of __init__.py
    init_digest = hashlib.sha256(init_path.read_bytes()).digest()

    # Encode all files (except __init__.py)
    key = os.environ['KNIGHTS_WHO_SAY_NI_KEY']
    key_bytes = uuid.UUID(key).bytes
    xor_bytes = [x ^ y for x, y in zip(init_digest, key_bytes)]
    del xor_bytes[-2:]
    coding = f'# coding=ninini-{name}\n"""\n'.encode()
    for path in src_dir.rglob('*.py'):
        if path == init_path:
            continue
        text = path.read_bytes()
        binary = ninini_encode(text, xor_bytes)
        path.write_bytes(coding + binary + b'"""\n')


def ninini_encode(binary, key_bytes):
    offsets = itertools.cycle(key_bytes)
    bin64 = base64.b64encode(binary)
    chars = []
    for ord_char, offset in zip(bin64, offsets):
        if 32 <= ord_char <= 126:
            code = (ord_char + offset - 32) % 95 + 32
        chars.append(code)
    enc_bytes = bytes(chars)
    offsets = range(0, len(bin64), 79)
    lines = [enc_bytes[offset:offset + 79] + b'\n' for offset in offsets]
    output = b''.join(lines)
    return output


def keygen(license_user, days=0):
    if days == 0:
        expiry_days = 0
    else:
        expiry_days = (dt.date.today() - dt.date(1970, 1, 1)).days + days
    key = os.environ['KNIGHTS_WHO_SAY_NI_KEY']
    key_bytes = uuid.UUID(key).bytes

    user_bytes = license_user.encode('utf-8')
    user_digest = hashlib.sha256(user_bytes).digest()

    code_bytes = bytearray(x ^ y for x, y in zip(key_bytes, user_digest))
    code_bytes[-2] = user_digest[-2] ^ (expiry_days // 256)
    code_bytes[-1] = user_digest[-1] ^ (expiry_days % 256)
    code_uuid = uuid.UUID(bytes=bytes(code_bytes))
    print(code_uuid)
