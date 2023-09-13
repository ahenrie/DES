# Encryption Program Overview

This Python program implements a simplified encryption algorithm inspired by the Data Encryption Standard (DES). It allows users to encrypt a message with a provided key. Below, we provide an overview of the key components and functionality of the program:

## Key Components

### 1. Input Handling
   - The program prompts the user to input a message and a key.
   - Both the message and key are converted to uppercase for consistency.

### 2. Binary Conversion
   - Functions are defined for converting hexadecimal characters to binary and vice versa.
   - Conversion functions are used to manipulate and process the message and key.

### 3. Key Generation
   - The provided key undergoes various permutations and transformations to generate round keys.
   - Round keys are used in the encryption process.

### 4. Encryption
   - The message is divided into left and right halves.
   - A series of encryption rounds are performed (16 rounds in total).
   - Each round involves various permutations, substitutions, and bitwise operations.
   - The result is an encrypted ciphertext.

### 5. Decryption 
   - It uses the generated round keys in reverse order to decrypt the ciphertext back to the original message.

## Usage
`python DES.py`
