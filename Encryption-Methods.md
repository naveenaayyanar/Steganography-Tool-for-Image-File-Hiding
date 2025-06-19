In my steganography project, the encryption method used is **AES (Advanced Encryption Standard)** in Galois/Counter Mode (GCM):

### Encryption Method: AES-GCM

1. **AES (Advanced Encryption Standard)**:
   - AES is a symmetric encryption algorithm widely used across the globe to secure data. It operates on fixed block sizes of 128 bits and supports key sizes of 128, 192, or 256 bits.
   - In your project, the AES encryption is implemented using the `cryptography` library, specifically the `AESGCM` class.

2. **Galois/Counter Mode (GCM)**:
   - GCM is an authenticated encryption mode that provides both confidentiality and integrity. It combines the counter mode of encryption with the Galois mode of authentication.
   - This means that not only is the data encrypted, but it is also protected against tampering.

### How It Works in Your Project

- **Encryption**:
  - When a user wants to embed a message in an image, they can optionally provide a password. If a password is provided, the message is encrypted using AES-GCM before being embedded in the image.
  - The `aes_encrypt` function handles the encryption:
    ```python
    def aes_encrypt(key: bytes, data: bytes):
        aesgcm = AESGCM(key.ljust(32, b'\0')[:32])  # Ensure the key is 32 bytes
        nonce = secrets.token_bytes(12)  # Generate a random nonce
        ct = aesgcm.encrypt(nonce, data, None)  # Encrypt the data
        return nonce + ct  # Return the nonce concatenated with the ciphertext
    ```

- **Decryption**:
  - When a user extracts a message from an image, they can also provide the password. If the message was encrypted, the `aes_decrypt` function is used to decrypt it:
    ```python
    def aes_decrypt(key: bytes, data: bytes):
        aesgcm = AESGCM(key.ljust(32, b'\0')[:32])  # Ensure the key is 32 bytes
        nonce = data[:12]  # Extract the nonce from the data
        ct = data[12:]  # The rest is the ciphertext
        return aesgcm.decrypt(nonce, ct, None)  # Decrypt the data
    ```

### Summary

In summary, your project uses AES encryption in Galois/Counter Mode (GCM) to securely encrypt messages before embedding them in images. This ensures that even if someone extracts the message from the image, they cannot read it without the correct password. 
The use of a nonce (number used once) adds an additional layer of security by ensuring that the same plaintext encrypted multiple times will yield different ciphertexts.
