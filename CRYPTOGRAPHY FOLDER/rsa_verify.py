from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
import os
import time

x = 11  # Loop counter to measure time for multiple iterations

while x > 0:
    # Generate a new RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # Commonly used public exponent for RSA
        key_size=1024           # Size of the RSA key in bits
    )

    # Generate the corresponding public key
    public_key = private_key.public_key()

    # Generate a random message to be signed and verified
    message = os.urandom(1024)  # Randomly generated 1024-byte message

    # Sign the message using the private key and PSS padding
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),  # Mask Generation Function (MGF1) with SHA-256
            salt_length=padding.PSS.MAX_LENGTH  # Maximum salt length
        ),
        hashes.SHA256()  # Hashing algorithm used for signing
    )

    # Record the time before starting the signature verification process
    before = time.perf_counter()

    # Verify the signature using the public key
    # This raises an exception if the signature is invalid
    public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),  # Same MGF1 and hash algorithm as used during signing
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Record the time after completing the signature verification process
    after = time.perf_counter()


    # Print the time taken for the signature verification process
    print(f"{after - before:0.4f} seconds")
    x -= 1  # Decrement the loop counter
