from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
import base64

encryption_key = b'93bd9vn&Bke7qoH*#bk86N8n'
cipher = DES3.new(encryption_key, DES3.MODE_ECB)

def encrypt_Text(plaintext: str):
    bytes_text = plaintext.encode("utf-8")

    padded_plaintext = pad(bytes_text, DES3.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)

    hex_ciphertext = ciphertext.hex()

    return hex_ciphertext
    


def decrypt_Text(cipher_text):
    bytes_ciphertext = bytes.fromhex(cipher_text)

    decrypted_data = cipher.decrypt(bytes_ciphertext)
    plaintext = unpad(decrypted_data, DES3.block_size).decode('utf-8')

    return plaintext




# def encrypt_Numbers(plainnumber):
#     number_bytes = plainnumber.to_bytes((plainnumber.bit_length() + 7) // 8, 'big')
#     padded_number = pad(number_bytes, 8)
#     encrypted_number = cipher.encrypt(padded_number)

#     return encrypted_number


# def decrypt_Numbers(cipher_number ):
#     # cipher_number = cipher_number.encode('latin-1')
#     decrypted_data = cipher.decrypt(cipher_number)
#     unpadded_data = unpad(decrypted_data, 8)

#     decrypted_number = int.from_bytes(unpadded_data, 'big')

#     return decrypted_number

