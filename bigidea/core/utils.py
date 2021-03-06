import hashlib
import string
import random

# Gerar caracteres randomicos 
def random_key(size=5):
	chars = string.ascii_uppercase + string.digits

	return ''.join(random.choice(chars) for x in range(size))

# Adicionando um dados do cliente (salt - username ou email) para gerar uma
# chave realmente unica
def generate_hash_key(salt, random_str_size = 5):
	random_str = random_key(random_str_size)
	text       = random_str + salt

	return hashlib.sha224(text.encode('utf-8')).hexdigest()    