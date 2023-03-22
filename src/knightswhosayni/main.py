"""Knights Who Say Ni!

$ export KNIGHTS_WHO_SAY_NI_KEY=$(python -c "import uuid; print(uuid.uuid4())")
$ export KNIGHTS_WHO_SAY_NI_KEY=6f42e628-0aa4-45da-ab41-e734e7e2b1c8
$ knightswhosayni transform src django_codemirror6 DJANGO_CODEMIRROR6_
$ knightswhosayni keygen grant.jenks@gmail.com 7
$ knightswhosayni setup-gumroad https://smee.io/WzrHSiR2F6G6mzQ
{'resource_subscription': {'id': 'Ufqct5DQzP0s8w70vqOOCw==',
                           'post_url': 'https://smee.io/WzrHSiR2F6G6mzQ',
                           'resource_name': 'sale'},
 'success': True}
$ knightswhosayni list-gumroad
{'resource_subscriptions': [{'id': 'Ufqct5DQzP0s8w70vqOOCw==',
                             'post_url': 'https://smee.io/WzrHSiR2F6G6mzQ',
                             'resource_name': 'sale'}],
 'success': True}
$ knightswhosayni delete-gumroad Ufqct5DQzP0s8w70vqOOCw==
{'message': 'The resource_subscription '
            'was deleted successfully.',
 'success': True}


TODO

* Support customization of the project logo.

* Add license legal details to template.

* Provide reusable GitHub workflow for testing and releasing code.
"""

import argparse
import base64
import datetime as dt
import functools
import glob
import hashlib
import itertools
import os
import pathlib
import pprint
import random
import requests
import uuid

from . import utils

pprint40 = functools.partial(pprint.pprint, width=40)


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command', help='sub-command help')
    subparsers.required = True

    parser_transform = subparsers.add_parser('transform')
    parser_transform.add_argument('src')
    parser_transform.add_argument('name')
    parser_transform.add_argument('prefix')
    parser_transform.set_defaults(func=transform)

    parser_keygen = subparsers.add_parser('keygen')
    parser_keygen.add_argument('license_user')
    parser_keygen.add_argument('days', default=0, nargs='?', type=int)
    parser_keygen.set_defaults(func=keygen)

    parser_setup_gumroad = subparsers.add_parser('setup-gumroad')
    parser_setup_gumroad.add_argument('post_url')
    parser_setup_gumroad.set_defaults(func=setup_gumroad)

    parser_list_gumroad = subparsers.add_parser('list-gumroad')
    parser_list_gumroad.set_defaults(func=list_gumroad)

    parser_delete_gumroad = subparsers.add_parser('delete-gumroad')
    parser_delete_gumroad.add_argument('resource_id')
    parser_delete_gumroad.set_defaults(func=delete_gumroad)

    args = parser.parse_args()
    kwargs = vars(args)
    del kwargs['command']
    func = kwargs.pop('func')
    func(**kwargs)


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
    key = os.environ['KNIGHTS_WHO_SAY_NI_KEY']
    code_uuid = utils.keygen(key, license_user, days)
    print(code_uuid)


def setup_gumroad(post_url):
    endpoint = 'https://api.gumroad.com/v2/resource_subscriptions'
    payload = {
        'access_token': os.environ['GUMROAD_ACCESS_TOKEN'],
        'resource_name': 'sale',
        'post_url': post_url,
    }
    response = requests.put(endpoint, data=payload)
    assert response.status_code == 200
    pprint40(response.json())


def list_gumroad():
    endpoint = 'https://api.gumroad.com/v2/resource_subscriptions'
    payload = {
        'access_token': os.environ['GUMROAD_ACCESS_TOKEN'],
        'resource_name': 'sale',
    }
    response = requests.get(endpoint, params=payload)
    assert response.status_code == 200
    pprint40(response.json())


def delete_gumroad(resource_id):
    endpoint = f'https://api.gumroad.com/v2/resource_subscriptions/{resource_id}'
    payload = {
        'access_token': os.environ['GUMROAD_ACCESS_TOKEN'],
    }
    response = requests.delete(endpoint, data=payload)
    assert response.status_code == 200
    pprint40(response.json())
