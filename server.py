import socket
import threading
import logging
from bdd import *
import sys
from datePY import *
from security import *
import re
import time
HOST = '0.0.0.0' #IP DU SERVEUR 
PORT = 9090
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
logging.basicConfig(filename=fr'C:\Users\alexa\OneDrive\Documents\Python\modif\V10.1 - a upload\logs.txt', filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=logging.INFO)
clients = {}

def broadcast(message,user):
    for key,client in clients.items():
        if key == user:
            client.send(message.encode("utf-8"))
            time.sleep(0.0000000000000000001)

def messages_start(user1, user2):
    ### msg bdd de la conv entre username and send_to_user
    messages_recv = req_bdd(user1, user2, "print_message_start")
    for elem in messages_recv:
        broadcast(elem,user1)

def handle(client,username, user2,):
    motif = "^new-conv-.*_.*$"
    tab_user = [username,user2]
    while True:
        try:
            print("Wait message")
            message = client.recv(1024).decode('utf-8')
            res = re.search(motif, message)
            
            if res == None:
                message_to_send = message.split()
                #if message_to_send:
                print(f"message send : {message_to_send}")

                ##enregistrement du message dans la base de données
                for i in range(1,len(message_to_send)):
                    res = req_bdd(username,user2, message_to_send[i], message_to_send[0],i,"save_message")
                    res = list(res)

                #print(f"{usernames[clients.index(client)]} says {message}")
                for i in range(len(tab_user)):
                    user = tab_user[i]
                    message_ = f"{message_to_send[0]}:{username}:{message_to_send[i+1]}"
                    long = len(message_)
                    message_=f"{long}:{message_}"
            
                    broadcast(message_,user)

        
            else:
                user_2 = message[message.index("_")+1:]
                if user_2 != user2:
                    user2 = user_2
                    broadcast("new_conversation",username)
                    messages_start(username, user_2)
      

            
        except:
            del clients[username]
            client.close()
            break

def receive_new_user(client, address):
    try:
        username = client.recv(1024).decode("utf-8")
        client.send(" ".encode("utf-8"))
        password = client.recv(1024).decode("utf-8")
        ### verification dans la base de donnée de user + password
        res = req_bdd(username,password,"connect_user")
        res = list(res)
        print(res[0])
        if res[0] == "Accepted":
            logging.info(f'User {username} logged - {address[0]}:{address[1]}')
            client.send("Accepted".encode("utf-8"))
            null = (client.recv(1024)).decode('utf-8')
            tab_users = req_bdd("all_users")
            tab_users = list(tab_users)[0]
            tab_keys = req_bdd("all_users_keys")
            tab_keys = list(tab_keys)[0]
        
            client.send(tab_users.encode("utf-8"))
            null = (client.recv(1024)).decode('utf-8')
            client.send(tab_keys.encode("utf-8"))
            clients[username] = client

            print(f"username of the is {username}")
            conversation = (client.recv(1024)).decode('utf-8')
            #print(conversation)

            user2 = conversation[conversation.index("_")+1:]
            #print(username, user2,conversation)
            messages_start(username, user2)
            
            thread = threading.Thread(target=handle, args=(client,username,user2,))
            thread.start()
        
        elif res[0] == None:
            print("create user srv 1")
            client.send("nop".encode("utf-8"))
            ans = (client.recv(2048)).decode('utf-8')
            print("ans= ",ans)
            if ans == "new_user":
                client.send(" ".encode("utf-8"))
                key= (client.recv(2048)).decode('utf-8')
            
                req = req_bdd(username, password, key, "create_user")
                
                req = list(req)
            else:
                logging.info(f'Fail connection : User {username} - {address[0]}:{address[1]}')


    except:
        pass
      
def receive_client():
    while True:
        try:
            client, address = server.accept()
            print(f"Connected with {str(address)}!")
            thread = threading.Thread(target=receive_new_user, args=(client,address))
            thread.start()
        except:
            pass
        
print("Server running... ")
receive_client()
