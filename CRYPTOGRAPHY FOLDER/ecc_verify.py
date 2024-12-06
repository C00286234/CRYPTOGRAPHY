from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
import os
import time

x = 11  # Loop counter to measure time for multiple iterations

while x > 0:
    # Generate a new ECC private key using the SECP192R1 curve
    private_key = ec.generate_private_key(
        ec.SECP192R1()  # Using the SECP192R1 elliptic curve
    )

    # Generate the corresponding public key
    public_key = private_key.public_key()

    # Generate a random message to be signed and verified
    message = os.urandom(50)  # Randomly generated 50-byte message

    # Sign the message using the private key and ECDSA with SHA-256
    signature = private_key.sign(
        message,
        ec.ECDSA(hashes.SHA256())  # ECDSA signature scheme with SHA-256 hash
    )

    # Record the time before starting the signature verification process
    before = time.perf_counter()

    # Verify the signature using the public key
    # This raises an exception if the signature is invalid
    public_key.verify(
        signature,
        message,
        ec.ECDSA(hashes.SHA256())  # Use the same signature scheme and hash as for signing
    )

    # Record the time after completing the signature verification process
    after = time.perf_counter()

    # Print the time taken for the signature verification process
    print(f"{after - before:0.4f} seconds")
    x -= 1  # Decrement the loop counter
