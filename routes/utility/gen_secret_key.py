import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh

# Generate Diffie-Hellman parameters
parameters = dh.generate_parameters(generator=2, key_size=2048)

# Generate Diffie-Hellman private/public key pair
private_key = parameters.generate_private_key()
public_key = private_key.public_key()

private_key_1 = parameters.generate_private_key()
public_key_1 = private_key_1.public_key()

# Perform Diffie-Hellman key exchange
shared_key = private_key.exchange(public_key)
shared_key_1 = private_key_1.exchange(public_key_1)

print(shared_key.hex())
print(shared_key_1.hex())
# Generate a random 24-character key
# random_key = ''.join(random.choices('0123456789', k=24))

# # Derive a cryptographic key using the shared key and random key
# digest = hashes.Hash(hashes.SHA256())
# digest.update(shared_key + random_key.encode())
# derived_key = digest.finalize()

# print("Random 24-character key:", random_key)
# print("Derived key:", derived_key.hex())
