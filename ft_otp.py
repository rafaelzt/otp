# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_otp.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rzamolo- <rzamolo-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/24 11:22:09 by rzamolo-          #+#    #+#              #
#    Updated: 2023/05/12 17:00:56 by rzamolo-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse, hashlib, re
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

re_hexa = re.compile("^[0-9a-fA-F]+$")
salt = get_random_bytes(16) # https://www.programcreek.com/python/example/95754/Crypto.Random.get_random_bytes

def generate(file):
    print(file)
    try:
        # Read and validate file content
        content = file.read()
        print(content)
        if not(re_hexa.match(content)):
            print("Error: File content is not hexadecimal")
            return
        if len(content) % 2 != 0:
            print(f"Error: File is not complete {len(content)} bytes")
            return
        # Cipher file content
        cipher = AES.new(get_password(), AES.MODE_CFB, salt)
        ciphered_content = salt + cipher.encrypt(content) # Why salt + ?
		# Write ciphered content to file
        name = file.name.split(".")[0] + ".key"
        with open(name, "wb") as file:
			(file, ciphered_content)
        
    except:
        print("Error: File not found")
        return

def get_password():
    secret = input("Enter your secret: ")
    secret_hash = hashlib.sha256(secret.encode()).hexdigest() # Search for hashlib.sha256
    return secret_hash
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="ft_otp.py",
                                    description="Generate OTP"
    )
    
    parser.add_argument("-g","--generate",
                        type=str,
                        dest="generate",
                        help="File containing hexadecimal and returns .key"
    )
    parser.add_argument("-k","--key",
                        type=str,
                        dest="key",
                        help="Generate a temporary key and display it on STDOUT"
    )
    
    arguments = parser.parse_args()

    filename = arguments.generate
    generate(filename)
    print(arguments.key)