import codecs
import hashlib
import itertools


def ninini_decode(binary):
    binary = bytes(binary)
    enc_text = binary.decode('utf8')
    with open(__file__, 'rb') as reader:
        hash_obj = hashlib.file_digest(reader, 'sha256')
    digest = hash_obj.digest()
    offsets = itertools.cycle(digest)
    chars = []
    iter_enc_text = iter(enc_text)
    for char in iter_enc_text:
        if char == '\n':
            break
    pairs = zip(iter_enc_text, offsets)
    for char, offset in pairs:
        ord_char = ord(char)
        if 32 <= ord_char <= 126:
            code = (ord_char - offset - 32) % 95 + 32
            char = chr(code)
        chars.append(char)
    text = ''.join(chars)
    return text, len(binary)


def ninini_search(name):
    return codecs.CodecInfo(None, ninini_decode, name='ninini-__NI_MODULE__')


codecs.register(ninini_search)
