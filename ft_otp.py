# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_otp.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rzamolo- <rzamolo-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/24 11:22:09 by rzamolo-          #+#    #+#              #
#    Updated: 2023/05/30 14:42:36 by rzamolo-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Add a check if a flag -g or -k is provided
# Add a check if the file is a .key or a hexadecimal file


import sys
import re
import hashlib
import argparse
import hmac
import struct
import time
# pip install qrcode-terminal
import qrcode_terminal
# pip install pycryptodome
# conda install pycrypto
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

parser = argparse.ArgumentParser(description='')

parser.add_argument('-g',
                    type=str,
                    dest='g',
                    help="Provide hexadecimal file and generate .key")

parser.add_argument('-k',
                    type=str,
                    dest='k',
                    help="provide a .key file and generate a time-based key")

args = parser.parse_args()

re_hexa = re.compile("^[0-9a-fA-F]+$")

def encrypt(message, master_key):
    # Generate a random initialization vector
    salt = get_random_bytes(16)

    # Create an AES cipher with the master key and initialization vector
    cipher = AES.new(master_key, AES.MODE_CFB, salt)

    # Encrypt the message and prepend the initialization vector to the encrypted message
    encrypted_message = salt + cipher.encrypt(message.encode())

    return encrypted_message

def decrypt(encrypted_message, master_key):
    # Get the initialization vector from the encrypted message
    salt = encrypted_message[:16]

    # Create an AES cipher with the master key and initialization vector
    cipher = AES.new(master_key, AES.MODE_CFB, salt)

    # Decrypt the message
    decrypted_message = cipher.decrypt(encrypted_message[16:]).decode()

    return decrypted_message

def get_hotp_token(secret, intervals_no):
    key = bytes.fromhex(secret)
    # Decode the secret key into a byte string
    msg = struct.pack(">8B", *(intervals_no).to_bytes(8, byteorder='big'))
    # Pack the message as an 8-byte string
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    # Generate a hash using HMAC as the hash algorithm
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h

def get_totp_token(secret):
    # Ensure to provide the same OTP for 30 seconds
    x = str(get_hotp_token(secret, intervals_no=int(time.time())//30))
    # Add leading zeros until the OTP has 6 digits
    return x.zfill(6)

def read_file(file, mode):
    try:
        with open(file, mode) as f:
            content = f.read()
    except:
        print("Error: File not found")
        sys.exit()
    return content

def create_key_file(file, content):
    # WRITE TO THE FILE
    name = file.split(".")[0] + ".key"
    with open(name, "wb") as f:
        f.write(content)
    print("Key was successfully saved in {}.".format(name))

def create_key(file):
    hexa = read_file(file, "r")
    if not (re_hexa.match(hexa)) or len(hexa) < 64:
        print("./ft_otp: error: key must be 64 hexadecimal characters.")
        return
    encrypted_hex = encrypt(hexa, master_key)
    create_key_file(file, encrypted_hex)

def get_password():
    secret = input("Enter the password: ")
    secret_hash = hashlib.sha256(secret.encode('utf-8')).digest()
    password = secret_hash
    return password

if (args.g is not None) and (args.k is not None):
    print("Too many arguments")
    sys.exit()

master_key = get_password()
if (args.g is not None):
    create_key(args.g)
elif (args.k is not None):
    secret = read_file(args.k, "rb")
    try:
        plain_text = decrypt(secret, master_key)
    except:
        print("Decryption error")
    else:
        key = get_totp_token(plain_text)
        print(key)
        qrcode_terminal.draw(str(key))
