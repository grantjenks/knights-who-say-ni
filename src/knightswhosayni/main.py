"""Knights Who Say Ni!

TODO

* Update license check by embedding check() code from __license__.py

* Provide more instructions on failure.

* Support generating keys! (untested)

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

    init_template = (parent_dir / 'template_init.py').read_text()
    init_template = init_template.replace('__NI_MODULE__', name)

    # Step 1: Inject codecs code into __init__.py
    init_path = (src_dir / name / '__init__.py')
    init_text = init_path.read_text()
    init_text += '\n\n' + init_template
    init_path.write_text(init_text)

    # Step 2: Compute sha256 of __init__.py
    hash_obj = hashlib.sha256(init_path.read_bytes())
    digest = hash_obj.digest()

    # Step 3: Copy __license__.py alongside __init__.py
    key = os.environ['KNIGHTS_WHO_SAY_NI_KEY']
    license_text = (parent_dir / 'template_license.py').read_text()
    license_text = (
        license_text
        .replace('__NI_MODULE__', name)
        .replace('__NI_PREFIX__', prefix)
        .replace('__NI_PREFIX_LOWER__', prefix.lower())
        .replace('__NI_PREFIX_STRIP__', prefix.rstrip('_'))
    )
    license_path = (src_dir / name / '__license__.py')
    license_path.write_text(license_text)

    # Step 4: Inject license checks in source code (except __license__.py and
    # __init__.py)
    license_check = f'__import__("{name}.__license__", 0, 0, 1).check()'
    for path in src_dir.rglob('*.py'):
        if path == init_path or path == license_path:
            continue
        text = path.read_text()
        # Randomly vary the line length by padding spaces.
        license_line = license_check + ' ' * random.randrange(0, 11)
        # Find a random line to inject license check.
        lines = text.split('\n')
        indices = [
            index
            for index, line in enumerate(lines)
            if line.startswith('import') or line.startswith('from')
        ]
        indices.append(len(lines))
        index = random.choice(indices)
        lines.insert(index, license_line)
        text = '\n'.join(lines)
        path.write_text(text)

    # Step 5: Encode all files (except __init__.py)
    coding = f'# coding=ninini-{name}\n'.encode()
    for path in src_dir.rglob('*.py'):
        if path == init_path:
            continue
        text = path.read_bytes()
        binary, _ = ninini_encode(text, digest)
        path.write_bytes(coding + binary)


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
