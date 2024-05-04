import mysql.connector

connection_params = {
"""
Paramètres de connexion à la base de données
"""
    'host': "",
    'user': "",
    'password': "",
    'database': "",
}
def req_bdd(*values):
    with mysql.connector.connect(**connection_params) as db :
        db.autocommit = True
        with db.cursor() as c:
            def create_user(user, password, keys):
                request = f"insert into comptes (usernames,password_users,public_keys) values ('{user}','{password}', '{keys}')"
                c.execute(request)
                return "user created bdd"

            def connect_user(user,password):
                c.execute(f"SELECT * FROM comptes WHERE usernames = '{user}' AND password_users = '{password}'")
                res = c.fetchone()
                if res == None:
                    return res
                else:
                    return "Accepted"


            def verif_name():
                request = f"SELECT * FROM comptes WHERE usernames = 'test'"
                c.execute(request)
            
            def print_message_start(usera, userb):
                
                user_a = f"{usera}_{userb}_1"
                user_b = f"{userb}_{usera}_2"
                
                request = f"SELECT date_heure, conversations, messages FROM messages WHERE conversations = '{user_a}' OR conversations = '{user_b}' ORDER BY date_heure"

                long_user_a = len(usera)
                long_user_b = len(userb) 
                c.execute(request)
                tab_mess = []
                res = c.fetchall()
                if res != None:
                    for elem in res:
                        if elem[1].startswith(usera):
                            message = f"{elem[0]}:{elem[1][:long_user_a]}:{elem[2]}"
                        else:
                            message = f"{elem[0]}:{elem[1][:long_user_b]}:{elem[2]}"
                        long = len(message)
                        message=f"{long}:{message}"
                        tab_mess.append(message)
                    return tab_mess
                        
                else:
                    return 

            
            def all_users():
                request = f"SELECT usernames FROM comptes"
                c.execute(request)
                tab_users = []
                res = c.fetchall()
                for elem in res:
                    tab_users.append(elem[0])
                return " ".join(tab_users)
            
            def all_users_keys():
                request = f"SELECT usernames,public_keys FROM comptes"
                c.execute(request)
                tab_users = []
                res = c.fetchall()
                for elem in res:
                    tab_users.append(elem[1])
                return " ".join(tab_users)

            def save_message(name_a, name_b, message, ts, nb):
                """
                Enregistrer message dans la base de données
                """
                conv = f"{str(name_a)}_{str(name_b)}_{str(nb)}"
                request = f"insert into messages (conversations,messages,date_heure) values ('{conv}','{message}', '{ts}')"
                #print(f"req: {request}")
                c.execute(request)


            def get_key(user):
                """
                Récuppérer clé publique d'un utilisateur
                """
                request = f"SELECT public_keys FROM comptes WHERE usernames = '{user}'"
                c.execute(request)
                return c.fetchone()[0]
                
            """
            Récuppération du dernier argument de la fonction pour déterminer la requête à effectuer.
            """
            if values[-1] == "connect_user":
                 yield connect_user(values[0],values[1])

            elif values[-1] == "save_message":
                yield save_message(values[0],values[1],values[2],values[3],values[4])

            elif values[-1] == "all_users":
                yield all_users()

            elif values[-1] == "print_message_start":
                res = print_message_start(values[0],values[1])
                for elem in res:
                    yield elem
              
            elif values[-1] == "get_key":
                yield get_key(values[0])

            elif values[-1] == "create_user":
                yield create_user(values[0],values[1],values[2])

            elif values[-1] == "all_users_keys":
                yield all_users_keys()