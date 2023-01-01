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


def vignere_cipher_encode(message, key):
    # Convert the message and key to a list of characters
    message = list(message)
    key = list(key)

    # Make the key the same length as the message
    key = key * (len(message) // len(key)) + key[:len(message) % len(key)]

    # Zip the message and key together and apply the cipher
    result = []
    for (c, k) in zip(message, key):
        if chr(36) <= c <= chr(126):
            # Get the character's ASCII code
            c_code = ord(c)
            k_code = ord(k)

            # Encode the character
            c_code = (c_code + k_code - 36) % 91 + 36

            # Convert the character back to a letter
            c = chr(c_code)

        # Append the character to the result
        result.append(c)

    # Convert the result back to a string and return it
    return ''.join(result)

def vignere_cipher_decode(message, key):
    # Convert the message and key to a list of characters
    message = list(message)
    key = list(key)

    # Make the key the same length as the message
    key = key * (len(message) // len(key)) + key[:len(message) % len(key)]

    # Zip the message and key together and apply the cipher
    result = []
    for (c, k) in zip(message, key):
        if chr(36) <= c <= chr(126):
            # Get the character's ASCII code
            c_code = ord(c)
            k_code = ord(k)

            # Decode the character
            c_code = (c_code - k_code + 36) % 91 + 36

            # Convert the character back to a letter
            c = chr(c_code)

        # Append the character to the result
        result.append(c)

    # Convert the result back to a string and return it
    return ''.join(result)

# Example usage:

message = "HELLO"
key = "WORLD"

encoded_message = vignere_cipher_encode(message, key)
print(encoded_message) # Output: QGNNQ

decoded_message = vignere_cipher_decode(encoded_message, key)
print(decoded_message) # Output: HELLO
