# pip install pycryptodome
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad

# 3DES secret key 24 bits in bytes format for encryption of data
encryption_key = '93bd9vn&Bke7qoH*#bk86N8n'

def encrypt_Text(plaintext: str, secret_key=encryption_key):
    secret_key = bytes(secret_key, encoding='utf-8')
    cipher = DES3.new(secret_key, DES3.MODE_ECB)

    bytes_text = plaintext.encode("utf-8")

    padded_plaintext = pad(bytes_text, DES3.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)

    hex_ciphertext = ciphertext.hex()

    return hex_ciphertext


def decrypt_Text(cipher_text: str, secret_key=encryption_key):
    secret_key = bytes(secret_key, encoding='utf-8')
    cipher = DES3.new(secret_key, DES3.MODE_ECB)

    bytes_ciphertext = bytes.fromhex(cipher_text)

    decrypted_data = cipher.decrypt(bytes_ciphertext)
    plaintext = unpad(decrypted_data, DES3.block_size).decode('utf-8')

    return plaintext