# Secure Data Hiding in Images Using Steganography

## Introduction

This project implements **secure data hiding in images using steganography** with **AES encryption** and **password-based randomized pixel selection**. It consists of two independent scripts:

- `encode.py` – Encrypts a message and hides it in an image.
- `decode.py` – Extracts and decrypts the hidden message.

## Features

✅ **AES Encryption for Extra Security**

- The message is **encrypted before hiding**, making it unreadable without the correct password.

✅ **Password-Based Random Pixel Selection**

- Uses a **random order** of pixels for data embedding based on the password.
- Prevents detection by simple sequential analysis.

✅ **Automatic Image Selection**

- Detects and selects **any image file in the folder**.
- Supports multiple formats: `.png, .jpg, .jpeg, .bmp, .tiff`

✅ **Fixed Output Image (****`encoded_image.png`****)**

- Ensures that **the original image is not overwritten**.

✅ **Error Handling & Security Checks**

- Prevents encoding if the message is too large.
- Alerts the user if decryption fails due to a wrong password.

## How It Works

### **Encoding (****`encode.py`****)**

1. The script scans for an image file in the folder.
2. Encrypts the secret message using **AES encryption** with a password.
3. Converts the encrypted message into **binary format**.
4. Uses **password-based random pixel selection** to embed the data.
5. Saves the **encoded image** as `encoded_image.png`.

### **Decoding (****`decode.py`****)**

1. The script reads `encoded_image.png`.
2. Extracts **message length** stored in the first 32 bits.
3. Uses **password-based randomization** to extract the correct bits.
4. Converts binary data back into **an encrypted string**.
5. Decrypts the message using the **same password**.
6. Displays the **original message** if decryption is successful.

## Installation

Before running the scripts, install the required dependencies:

```sh
pip install opencv-python numpy pycryptodome
```

## Usage

### **Encoding a Message**

Run the following command:

```sh
python encode.py
```

Enter the **message** and **password** when prompted.

### **Decoding a Message**

Run the following command:

```sh
python decode.py
```

Enter the **password** to retrieve the hidden message.

## Deployment

- The project consists of **two separate Python scripts** for encoding and decoding.
- The **output image (****`encoded_image.png`****) is generated automatically**.
- Suitable for **secure message transmission** using **steganography and encryption**.

## Security Considerations

- Without the correct password, the extracted data **remains encrypted**.
- The use of **random pixel selection** makes it resistant to **simple steganalysis**.

## License

This project is **open-source** and free to use for educational purposes.

---

### **Project by: Mayank Rajgeet**
