from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
import os
import time

x = 11  # Loop counter to measure time for multiple iterations

while x > 0:
    # Record the time before starting the key pair generation
    before = time.perf_counter()

    # Generate a new ECC private key using the SECP192R1 curve
    private_key = ec.generate_private_key(
        ec.SECP192R1()  # Using the SECP192R1 elliptic curve
    )

    # Generate the corresponding public key
    public_key = private_key.public_key()

    # Record the time after completing the key pair generation
    after = time.perf_counter()


    # Print the time taken for the key pair generation process
    print(f"{after - before:0.4f} seconds")
    x -= 1  # Decrement the loop counter
