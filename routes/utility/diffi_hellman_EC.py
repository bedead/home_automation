from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec


def get_Hex_From_EllipticCurvePrivateKey(
    EllipticCurvePrivateKey: ec.EllipticCurvePrivateKey,
):
    private_key_hex = EllipticCurvePrivateKey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).hex()
    return private_key_hex


def get_Hex_From_Bytes(bytes_key: bytes):
    return bytes_key.hex()


def get_EllipticCurvePrivateKey_From_Hex(hex_key: str):
    public_key_bytes = bytes.fromhex(hex_key)
    # print(public_key_bytes)
    public_key = serialization.load_pem_private_key(public_key_bytes, password=None)
    return public_key


def get_EllipticCurvePublicKey_From_Hex(hex_key: str):
    public_key_bytes = bytes.fromhex(hex_key)
    public_key = serialization.load_pem_public_key(
        public_key_bytes,
    )
    return public_key


def generate_Hex_Private_Public_Key():
    """Generating Private and Public key for new User"""
    user_private_key = ec.generate_private_key(ec.SECP384R1())
    user_public_key = user_private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    user_private_key_hex = get_Hex_From_EllipticCurvePrivateKey(user_private_key)
    user_public_key_hex = get_Hex_From_Bytes(user_public_key)

    return user_private_key_hex, user_public_key_hex


def get_Shared_Key(private_hex, public_hex):
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
