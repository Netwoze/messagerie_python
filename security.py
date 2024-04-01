import base64
from bdd import *
from datePY import *
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os
from hashlib import sha512

def create_key(name):
    username_windows = os.environ.get( "USERNAME" ) #récupération du nom d'utilisateur
    directory = rf'C:\Users\{username_windows}\.python_project_priv_key' #chemin d'accès de la clé privée
    key = RSA.generate(1024)
    pub_key = key.publickey().export_key("PEM")
    priv_key = key.exportKey("PEM")
    #key_decode = pub_key.decode('utf-8')
    if not os.path.exists(directory): #Si le repertoire n'existe pas alors celui est créé
        os.makedirs(directory)
    with open(rf'{directory}\private_{name}.pem','wb') as k: # lecture de la clé privée
        k.write(priv_key)
    """with open(f'pub_{name}.pem','wb') as k:
        k.write(pub_key)"""
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
    """
    déchiffre les messages de l'utilisateur
    """
    username_windows = os.environ.get( "USERNAME" )
    try:
        with open(rf'C:\Users\{username_windows}\.python_project_priv_key\private_{user}.pem','rb') as p:
            priv = p.read()
        private_key = RSA.importKey(priv)
        private_key = PKCS1_OAEP.new(private_key)
        message = decode_base64(message)
        decrypted_text = private_key.decrypt(message)
        return decrypted_text.decode("utf-8")
    except:
        return 



def encrypt(message,usera,userb):

    """
    chiffre les messages de l'utilisateur pour l'emmeteur et le récepteur
    """
    message = message.encode()
    tab_key = []
    tab_to_send = []
    tab_to_send.append(time_stamp()) #récupération de la date timestamp
    #requete à la base de donnée pour réccupérer les clés publiques de user1 et user 2
    key_usera = req_bdd(usera, "get_key")
    key_usera = decode_base64(list(key_usera)[0])
    key_userb = req_bdd(userb, "get_key")
    key_userb = decode_base64(list(key_userb)[0])
    tab_key.append(key_usera)
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
