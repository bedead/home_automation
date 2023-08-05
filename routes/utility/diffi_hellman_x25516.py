from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization


def reference_mechinsim():
    # Generate user1's key pair
    user1_private_key = x25519.X25519PrivateKey.generate()
    # user public key of type (X25519PrivateKey)
    user1_public_key = user1_private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    )

    # Generate user2's key pair
    user2_private_key = x25519.X25519PrivateKey.generate()
    user2_public_key = user2_private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    )

    # User1 sends public key to User2, and vice versa

    # User1 computes shared secret key
    user1_shared_key = user1_private_key.exchange(
        x25519.X25519PublicKey.from_public_bytes(user2_public_key)
    )
    user1_shared_key_hex = user1_shared_key.hex()

    # User2 computes shared secret key
    user2_shared_key = user2_private_key.exchange(
        x25519.X25519PublicKey.from_public_bytes(user1_public_key)
    )
    user2_shared_key_hex = user2_shared_key.hex()

    # The shared keys should be the same for User1 and User2
    print("User1 shared key:", user1_shared_key_hex)
    print("User2 shared key:", user2_shared_key_hex)


def get_Hex_From_X25519PrivateKey(private_Key: x25519.X25519PrivateKey):
    private_key_hex = private_Key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    ).hex()
    # return hex equvalent
    return private_key_hex


def get_Hex_From_Bytes(byte_key: bytes):
    return byte_key.hex()


def get_Bytes_From_Hex(hex_key: str):
    return bytes.fromhex(hex_key)


def get_X25519PrivateKey_From_Hex(hex_key: str):
    private_key_bytes = bytes.fromhex(hex_key)
    private_key = x25519.X25519PrivateKey.from_private_bytes(private_key_bytes)

    return private_key


def get_X25519PublicKey_From_Hex(hex_key: str):
    public_key_bytes = bytes.fromhex(hex_key)
    public_key = serialization.load_pem_public_key(
        public_key_bytes,
    )
    return public_key


def generate_Hex_Private_Public_Key():
    # user private key of type (X25519PrivateKey)
    user_private_key = x25519.X25519PrivateKey().generate

    # user public key of type (bytes)
    user_public_key = user_private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    )

    user_private_key_hex = get_Hex_From_X25519PrivateKey(user_private_key)
    user_public_key_hex = get_Hex_From_Bytes(user_public_key)

    print(user_private_key_hex)
    print(user_public_key_hex)

    return user_private_key_hex, user_public_key_hex


def get_Shared_Key(private_key_hex, public_key_hex):
    private_key = get_X25519PrivateKey_From_Hex(private_key_hex)
    bytes_public_key = get_Bytes_From_Hex(public_key_hex)

    bytes_shared_key = private_key.exchange(
        x25519.X25519PublicKey.from_public_bytes(bytes_public_key)
    )
    shared_key_hex = bytes_shared_key.hex()

    return shared_key_hex
