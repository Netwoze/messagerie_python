import base64
from datePY import *
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os
from hashlib import sha512

def create_key(name):
    username_windows = os.environ.get( "USERNAME" )
    directory = rf'C:\Users\{username_windows}\MESSAGERIE_PYTHON\privates_keys'
    key = RSA.generate(1024)
    pub_key = key.publickey().export_key("PEM")
    priv_key = key.exportKey("PEM")
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(rf'{directory}\private_key_{name}.pem','wb') as k:
        k.write(priv_key)
    return encode_base64(pub_key)



# Encode data to base64
def encode_base64(data):
    encoded_data = base64.b64encode(data)
    return encoded_data.decode()

# Decode data from base64
def decode_base64(encoded_data):
    decoded_data = base64.b64decode(encoded_data)
    return decoded_data

def decrypt(message,user):
    username_windows = os.environ.get( "USERNAME" )
    with open(rf'C:\Users\{username_windows}\MESSAGERIE_PYTHON\privates_keys\private_key_{user}.pem','rb') as p:
        priv = p.read()
    private_key = RSA.importKey(priv)
    private_key = PKCS1_OAEP.new(private_key)
    message = decode_base64(message)
    decrypted_text = private_key.decrypt(message)
    return decrypted_text.decode("utf-8")

def encrypt(message,usera,userb, key_usera, key_userb):
    message = message.encode()
    tab_key = []
    tab_to_send = []
    tab_to_send.append(time_stamp()) #récupération de la date timestamp
    
    key_usera = decode_base64(key_usera)
 
    key_userb = decode_base64(key_userb)
    tab_key.append(key_usera)#requete à la base de donnée pour réccupérer les clés publiques de user1 et user 2
    tab_key.append(key_userb)

   
    for elem in tab_key:
        pub_key = RSA.importKey(elem)
        pub_key = PKCS1_OAEP.new(pub_key)
    
        encrypted = pub_key.encrypt(message)

        tab_to_send.append(encode_base64(encrypted))
        #fait appel à la fonction send pour envoyer le message et le timestamp send(*values)
    return tab_to_send

def hash_password(password):
    return sha512(password.encode()).hexdigest()




