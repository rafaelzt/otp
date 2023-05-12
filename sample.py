import re
import hashlib
import argparse
import hmac
import struct
import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


parser = argparse.ArgumentParser(description='')

parser.add_argument('-g',
					type=str,
					dest='g',
					help="pide fichero hexadecimal y debuelbe .key")

parser.add_argument('-k',
					type=str,
					dest='k',
					help="pide un .key y retorna una clave de tiempo")

args = parser.parse_args()

re_hexa = re.compile("^[0-9a-fA-F]+$")

# Definir clave maestra
#clave_maestra = b"clave_maestra_1234"
#clave_maestra = clave_maestra[:16]


def cifrar(mensaje, clave_maestra):
	iv = get_random_bytes(16)
	cifrador = AES.new(clave_maestra, AES.MODE_CFB, iv)
	mensaje_cifrado = iv + cifrador.encrypt(mensaje.encode())
	return mensaje_cifrado

def descifrar(mensaje_cifrado, clave_maestra):
	# Obtener el vector de inicialización del mensaje cifrado
	iv = mensaje_cifrado[:16]

	# Crear un descifrador AES con la clave maestra y el vector de inicialización
	descifrador = AES.new(clave_maestra, AES.MODE_CFB, iv)

	# Descifrar el mensaje
	mensaje_descifrado = descifrador.decrypt(mensaje_cifrado[16:]).decode()

	return mensaje_descifrado


####crear id de tiempo
def get_hotp_token(secret, intervals_no):
	key = bytes.fromhex(secret)
	# Decodificar la clave secreta en una cadena de bytes
	msg = struct.pack(">8B", *(intervals_no).to_bytes(8, byteorder='big'))
	# Empaquetar el mensaje como una cadena de 8 bytes
	h = hmac.new(key, msg, hashlib.sha1).digest()
	o = o = h[19] & 15
	# Generar un hash usando ambos. El algoritmo de hash es HMAC
	h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
	#unpacking
	return h

def get_totp_token(secret):
	#ensuring to give the same otp for 30 seconds
	x = str(get_hotp_token(secret,intervals_no=int(time.time())//30))
	#adding 0 in the beginning till OTP has 6 digits
	return x.zfill(6)

def create_file_key(file, contenido):
	## ESCIRBIR EN EL FICHERO
	name = file.split(".")[0] + ".key"
	with open(name, "wb") as archivo:
		archivo.write(contenido)
		archivo.close()
	print(f"Key was successfully saved in {name}.")

def create_key(file):
	hexa = leer_fichero(file, "r")
	if not(re_hexa.match(hexa)) or len(hexa) < 64:
		print("./ft_otp: error: key must be 64 hexadecimal characters.")
		return
	hex_dig = cifrar(hexa, clave_maestra)
	create_file_key(file, hex_dig)

def get_passwd():
	secret = input("Introduce la contraeña: ")
	secret_hash = hashlib.sha256(secret.encode('utf-8')).digest()
	####
	passwd = secret_hash
	return passwd
	####

clave_maestra = get_passwd()
if (args.g != None):
	create_key(args.g)
elif (args.k != None):
	secret = leer_fichero(args.k, "rb")
	try:
		plain_text = descifrar(secret, clave_maestra)
	except:
		print("Error descifrado")
	else:
		key = get_totp_token(plain_text)

		print(key)
