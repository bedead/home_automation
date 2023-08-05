from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec


def get_Hex_From_EllipticCurvePrivateKey(
    EllipticCurvePrivateKey: ec.EllipticCurvePrivateKey,
):
    """
    This function takes an EllipticCurvePrivateKey object and
    converts it to a hex string. It serializes the private key using PEM encoding
    without encryption and returns its hex representation.
    """
    private_key_hex = EllipticCurvePrivateKey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).hex()
    return private_key_hex


def get_Hex_From_Bytes(bytes_key: bytes):
    """
    This function converts a bytes object to its hex representation.
    """
    return bytes_key.hex()


def get_EllipticCurvePrivateKey_From_Hex(hex_key: str):
    """
    This function takes a hex string representing a private
    key and reconstructs the EllipticCurvePrivateKey object from it.
    It loads the private key using PEM encoding.
    """
    public_key_bytes = bytes.fromhex(hex_key)
    # print(public_key_bytes)
    public_key = serialization.load_pem_private_key(public_key_bytes, password=None)
    return public_key


def get_EllipticCurvePublicKey_From_Hex(hex_key: str):
    """
    Similar to the previous function, this one takes a hex string representing a public key
    and reconstructs the EllipticCurvePublicKey object from it.
    """
    public_key_bytes = bytes.fromhex(hex_key)
    public_key = serialization.load_pem_public_key(
        public_key_bytes,
    )
    return public_key


def generate_Hex_Private_Public_Key():
    """
    This function generates a new pair of private and public keys
    using the ECDH elliptic curve. It returns the
    hex representations of both the private and public keys.
    """
    user_private_key = ec.generate_private_key(ec.ECDH())
    user_public_key = user_private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    user_private_key_hex = get_Hex_From_EllipticCurvePrivateKey(user_private_key)
    user_public_key_hex = get_Hex_From_Bytes(user_public_key)

    return user_private_key_hex, user_public_key_hex


def get_Shared_Key(private_hex, public_hex):
    """
    This function computes the shared key using the Elliptic
    Curve Diffie-Hellman (ECDH) key exchange method. It
    takes two hex strings representing private and public
    keys, derives the shared key using ECDH,
    and returns the shared key in its hex representation.
    """
    private_key_new = get_EllipticCurvePrivateKey_From_Hex(private_hex)
    public_key_new = get_EllipticCurvePublicKey_From_Hex(public_hex)

    shared_key = private_key_new.exchange(ec.ECDH(), public_key_new)
    hex_shared = shared_key.hex()

    return hex_shared


"""Example implementation of above methods"""
# pr, pu = generate_Hex_Private_Public_Key()
# pr1, pu1 = generate_Hex_Private_Public_Key()
# print(get_Shared_Key(pr, pu1))
# print(get_Shared_Key(pr1, pu))
