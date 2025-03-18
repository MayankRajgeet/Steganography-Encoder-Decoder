## encode.py
import cv2
import numpy as np
from Crypto.Cipher import AES
import base64
import hashlib
import glob
import os

def pad_message(message):
    return message + (16 - len(message) % 16) * chr(16 - len(message) % 16)

def encrypt_message(message, password):
    key = hashlib.sha256(password.encode()).digest()[:16]  # Derive key from password
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad_message(message).encode())
    return base64.b64encode(encrypted).decode()

def generate_indices(img, password, length):
    np.random.seed(int(hashlib.sha256(password.encode()).hexdigest(), 16) % (10**8))
    indices = [(i, j, k) for i in range(img.shape[0]) for j in range(img.shape[1]) for k in range(3)]
    np.random.shuffle(indices)
    return indices[:length]

def adaptive_encode(img, message_bin, password):
    indices = generate_indices(img, password, len(message_bin) + 32)  # Extra 32 bits for length
    length_bin = format(len(message_bin), '032b')
    full_message_bin = length_bin + message_bin
    
    for index, (i, j, k) in enumerate(indices):
        pixel_value = int(img[i, j, k])  # Convert to standard integer before bitwise operation
        new_value = (pixel_value & ~1) | int(full_message_bin[index])
        img[i, j, k] = np.uint8(np.clip(new_value, 0, 255))  # Ensure value stays within 0-255
    return img

def encode_message(message, password):
    image_formats = ('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff')
    img_files = [f for fmt in image_formats for f in glob.glob(fmt) if f != "encoded_image.png"]
    
    if not img_files:
        print("Error: No unencoded image file found in the folder!")
        return
    
    img_path = img_files[0]  # Take the first found unencoded image
    output_path = "encoded_image.png"
    img = cv2.imread(img_path)
    
    if img is None:
        print("Error: Image not found!")
        return
    
    encrypted_message = encrypt_message(message, password)
    message_bin = ''.join(format(ord(i), '08b') for i in encrypted_message)
    
    data_len = len(message_bin) + 32  # Include space for length storage
    total_pixels = img.shape[0] * img.shape[1] * 3
    
    if data_len > total_pixels:
        print("Error: Message is too large to fit in the image!")
        return
    
    img = adaptive_encode(img, message_bin, password)
    cv2.imwrite(output_path, img)
    print(f"Message encoded and saved as {output_path}")

if __name__ == "__main__":
    message = input("Enter message to hide: ")
    password = input("Enter password: ")
    encode_message(message, password)
