from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec, dsa, padding
import os
import time

# Measures the average time to generate an RSA key pair
def time_rsa_keypair_generation(bits):
    x = 10  # Number of iterations for averaging
    total_time = 0
    while x > 0:
        before = time.perf_counter()  # Start timing
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=bits)
        public_key = private_key.public_key()
        after = time.perf_counter()  # End timing
        total_time += (after - before)
        x -= 1
    return total_time / 10  # Average time

# Measures the average time to encrypt a message with RSA
def time_rsa_encryption(bits):
    x = 10
    total_time = 0
    while x > 0:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=bits)
        public_key = private_key.public_key()

        def split_message(message, chunk_size):
            return [message[i:i + chunk_size] for i in range(0, len(message), chunk_size)]

        def encrypt_message(public_key, message, chunk_size):
            encrypted_chunks = []
            for chunk in split_message(message, chunk_size):
                encrypted_chunks.append(public_key.encrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ))
            return encrypted_chunks

        long_plaintext = os.urandom(10 * 1024)  # Generate 10 KB random plaintext
        before = time.perf_counter()  # Start timing
        encrypt_message(public_key, long_plaintext, 32)  # Encrypt in 32-byte chunks
        after = time.perf_counter()  # End timing
        total_time += (after - before)
        x -= 1
    return total_time / 10

# Measures the average time to decrypt a message with RSA
def time_rsa_decryption(bits):
    x = 10
    total_time = 0
    while x > 0:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=bits)
        public_key = private_key.public_key()

        def encrypt_message(public_key, message, chunk_size):
            return [
                public_key.encrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ) for chunk in [message[i:i + chunk_size] for i in range(0, len(message), chunk_size)]
            ]

        def decrypt_message(private_key, encrypted_chunks):
            return b"".join(
                private_key.decrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ) for chunk in encrypted_chunks
            )

        long_plaintext = os.urandom(10 * 1024)  # Generate 10 KB random plaintext
        long_ciphertext = encrypt_message(public_key, long_plaintext, 32)  # Encrypt the message
        before = time.perf_counter()  # Start timing
        decrypt_message(private_key, long_ciphertext)  # Decrypt the message
        after = time.perf_counter()  # End timing
        total_time += (after - before)
        x -= 1
    return total_time / 10

