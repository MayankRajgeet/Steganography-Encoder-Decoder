## decode.py
import cv2
import numpy as np
from Crypto.Cipher import AES
import base64
import hashlib
import os

def decrypt_message(encrypted_message, password):
    key = hashlib.sha256(password.encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(encrypted_message))
    return decrypted.decode().rstrip(chr(16 - len(decrypted) % 16))

def generate_indices(img, password, length):
    np.random.seed(int(hashlib.sha256(password.encode()).hexdigest(), 16) % (10**8))
    indices = [(i, j, k) for i in range(img.shape[0]) for j in range(img.shape[1]) for k in range(3)]
    np.random.shuffle(indices)
    return indices[:length]

def adaptive_decode(img, password):
    indices = generate_indices(img, password, 32)  # Read message length first
    
    length_bin = "".join(str(int(img[i, j, k]) & 1) for i, j, k in indices)
    message_length = int(length_bin, 2)
    
    indices = generate_indices(img, password, message_length + 32)
    binary_data = "".join(str(int(img[i, j, k]) & 1) for i, j, k in indices[32:])
    return binary_data

def decode_message(password):
    img_path = "encoded_image.png"  # Default encoded image
    
    if not os.path.exists(img_path):
        print("Error: Encoded image not found!")
        return
    
    img = cv2.imread(img_path)
    if img is None:
        print("Error: Image not found!")
        return
    
    binary_data = adaptive_decode(img, password)
    message_bits = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    encrypted_message = ''.join(chr(int(b, 2)) for b in message_bits if int(b, 2) != 0)
    
    try:
        decrypted_message = decrypt_message(encrypted_message, password)
        print(f"Decryption Successful: {decrypted_message}")
    except:
        print("Error: Incorrect password or corrupted data!")

if __name__ == "__main__":
    password = input("Enter password: ")
    decode_message(password)