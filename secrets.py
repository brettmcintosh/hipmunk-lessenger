import os
from binascii import unhexlify
from nacl.secret import SecretBox


def decrypt_key(ciphertext: bytes) -> str:
    master_key = os.environ.get('SECRET_KEY')
    if master_key is None:
        raise Exception('SECRET_KEY environment variable not found')
    secrets = SecretBox(key=str.encode(master_key, 'ascii'))
    return bytes.decode(secrets.decrypt(unhexlify(ciphertext)), 'utf-8')


DARK_SKY_API_KEY = decrypt_key(b'3eb06f17b4361aaf9764f516ac825f8d10ee29a0dc8e9197053b28c1e1f4711be723a7f7694a73caee88848eb13e47998f391df1f4a71129a122e85b8c91dfa72369984f0524b6b7')
GMAPS_API_KEY = decrypt_key(b'146ee894beb9fcb67b69e85569b17bdfef1df8e3bef55a8a556cfb8356357d8fd4a2fa87995364e79b36d31c3223d65a13c073215888ce0e2f140da8d401c108b3cd9b529821bbc051111ce697d83d')