"""Crypto -- as secure as the Knights Who Say Ni

Process

1. Inject codecs code into __init__.py

2. Compute sha256 of __init__.py

3. Copy __license__.py alongside __init__.py

4. Inject license checks in source code (except __license__.py and __init__.py)

5. Use sha256 as cipher key for all files (except __init__.py)
"""

import codecs
import glob
import sys


def transform(src_dir):
    paths = glob.glob(directory + '/**/*.py')
    for path in paths:
        with open(path) as reader:
            text = reader.read()
        binary = ninini_encode(text)
        with open(path, 'wb') as writer:
            writer.write('# -*- coding: ninini -*-\n')
            writer.write(binary)


def ninini_encode(text):
    rot13_text = codecs.encode(text, 'rot13')
    binary = rot13_text.encode('utf8')
    return binary, len(text)


def ninini_decode(binary):
    rot13_text = binary.decode('utf8')
    text = codecs.decode(rot13_text, 'rot13')
    return text, len(binary)


def ninini_search(name):
    return codecs.CodecInfo(ninini_encode, ninini_decode, name='ninini')


codecs.register(ninini_search)
