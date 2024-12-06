from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa
import os
import time

x = 11  # Loop counter to measure time for multiple iterations

while x > 0:
    # Generate a new DSA private key with a key size of 1024 bits
    private_key = dsa.generate_private_key(
        key_size=1024  # DSA key size in bits
    )

    # Generate the corresponding public key
    public_key = private_key.public_key()

    # Generate a random message to be signed
    message = os.urandom(50)  # Randomly generated 50-byte message

    # Record the time before starting the signing process
    before = time.perf_counter()

    # Sign the message using the private key and SHA-256 hash algorithm
    signature = private_key.sign(
        message,
        hashes.SHA256()  # Hash algorithm for signing
    )

    # Record the time after completing the signing process
    after = time.perf_counter()

    # Print the time taken for the signing process
    print(f"{after - before:0.4f} seconds")
    x -= 1  # Decrement the loop counter
