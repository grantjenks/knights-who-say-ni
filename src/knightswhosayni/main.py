"""Knights Who Say Ni!

TODO

* Support generating keys! (untested)

* How to provide instructions on failure?

* Reserve last two bytes for license expiry -- recorded in dates since epoch
  with any number over 100 years considered "forever".
"""

import argparse
import base64
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

    args = parser.parse_args()

    if args.command == 'transform':
        transform(args.src, args.name, args.prefix)


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
    init_text += '\n\n' + init_template
    init_path.write_text(init_text)

    # Compute sha256 of __init__.py
    init_digest = hashlib.sha256(init_path.read_bytes()).digest()

    # Encode all files (except __init__.py)
    key = os.environ['KNIGHTS_WHO_SAY_NI_KEY']
    key_bytes = uuid.UUID(key).bytes
    coding = f'# coding=ninini-{name}\n'.encode()
    for path in src_dir.rglob('*.py'):
        if path == init_path:
            continue
        text = path.read_bytes()
        binary, _ = ninini_encode(text, key_bytes)
        path.write_bytes(coding + binary)

    print(init_digest)
    print(key_bytes)


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
