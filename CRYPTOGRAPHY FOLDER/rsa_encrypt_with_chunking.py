from cryptography.hazmat.primitives import hashes, serialization
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

    # Helper function to split a large message into smaller chunks
    def split_message(message, chunk_size):
        return [message[i:i + chunk_size] for i in range(0, len(message), chunk_size)]

    # Helper function to encrypt a message in chunks using the public key
    def encrypt_message(public_key, message, chunk_size):
        encrypted_chunks = []
        for chunk in split_message(message, chunk_size):
            encrypted_chunks.append(public_key.encrypt(
                chunk,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Mask Generation Function with SHA-256
                    algorithm=hashes.SHA256(),  # Hashing algorithm for OAEP padding
                    label=None                 # Optional label for OAEP, set to None
                )
            ))
        return encrypted_chunks

    # Generate a random large plaintext message
    long_plaintext = os.urandom(10 * 1024)  # Randomly generated 10 KB message

    # Record the time before starting the encryption process with chunking
    before = time.perf_counter()

    # Encrypt the large message in chunks
    long_ciphertext = encrypt_message(public_key, long_plaintext, 32)  # Encrypt in 32-byte chunks

    # Record the time after completing the encryption process
    after = time.perf_counter()

    # Print the time taken for the encryption process
    print(f"{after - before:0.4f} seconds")
    x -= 1  # Decrement the loop counter
