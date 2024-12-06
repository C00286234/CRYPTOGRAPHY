from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
import os
import time

x = 11  # Loop counter to measure time for multiple iterations

while x > 0:
    # Generate a new RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # Commonly used public exponent for RSA
        key_size=15360          # Size of the RSA key in bits (very large for demonstration purposes)
    )

    # Generate the corresponding public key
    public_key = private_key.public_key()

    # Generate a random message to be signed
    message = os.urandom(1024)  # Randomly generated 1024-byte message

    # Record the time before starting the signing process
    before = time.perf_counter()

    # Sign the message using the private key and PSS padding
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),  # Mask Generation Function (MGF1) with SHA-256
            salt_length=padding.PSS.MAX_LENGTH  # Maximum salt length
        ),
        hashes.SHA256()  # Hashing algorithm used for signing
    )

    # Record the time after completing the signing process
    after = time.perf_counter()

    # Print the time taken for the signing process
    print(f"{after - before:0.4f} seconds")
    x -= 1  # Decrement the loop counter
