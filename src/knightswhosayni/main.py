"""Knights Who Say Ni!

TODO

* Current "import foo.__license__" allows easy bypassing with sys.modules.
  Would be stronger to inject the license check code directly into the files.

from foo import __license__
__license_user = __license__.get_user()
__license_code = __license__.get_code()
__license_key = '__NI_LICENSE_KEY__'
__license_keykey = __license__.UUID(__license_key)
__license_pairs = zip(__license_user, __license_code)
__license_xor = bytes(u ^ c for u, c in __license_pairs)
if __license_xor != __license_key:
    raise __license__.LicenseError(__license__.message)

^-- This won't work either. It still allows copy/pasting a solution.
The license key must be embedded in every encoded file and the check done there.

* Provide more instructions on failure.

* Support generating keys! (untested)

* Reserve last two bytes for license expiry -- recorded in dates since epoch
  with any number over 100 years considered "forever".
"""

import argparse
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
        .replace('__NI_LICENSE_KEY__', key)
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
        text = path.read_text()
        binary, _ = ninini_encode(text, digest)
        path.write_bytes(coding + binary)


def ninini_encode(text, digest):
    offsets = itertools.cycle(digest)
    chars = []
    for char, offset in zip(text, offsets):
        ord_char = ord(char)
        if 32 <= ord_char <= 126:
            code = (ord_char + offset - 32) % 95 + 32
            char = chr(code)
        chars.append(char)
    enc_text = ''.join(chars)
    binary = enc_text.encode('utf8')
    return binary, len(text)
