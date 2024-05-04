# messagerie_python
### 1 - Architecture du projet 

![architecture](https://github.com/Netwoze/messagerie_python/assets/93689421/e9bf6200-535a-43f3-b7aa-72374fa20f68)

### 2 - Architecture du code
1. Les fichiers suivants doivent être placés sur un serveur distant
   - bdd.py
   - date.PY
   - security.py
   - server.py
   - bdd_messagerie.sql

2. Les fichiers suivants doivent être placés sur un client
   - main.py
   - date.PY
   - security.py

### 3 - Installation des modules
1. Fichier requirements
  ```
    pip install -r requirements.txt
  ```
   

### 4 - Modifications à apporter
1. Les fichiers suivants doivent être édités
   - main.py (ligne 19 et 20)
   ```
     self.HOST = '0.0.0.0' #IP du serveur
     self.PORT = 9090 #port applicatif
     ```
   - server.py (ligne 10 et 11)
   ```
     HOST = '0.0.0.0'
     PORT = 9090 #port applicatif
    ```
     
   - bdd.py (ligne 4 à 7)
     Configurer les variables environnements et paramètres de la base de données
   ```
    'host': "",
    'user': os.environ.get(''),
    'password': os.environ.get(''),
    'database': "",
    ```


### 5 - Démonstration

https://github.com/Netwoze/messagerie_python/assets/93689421/55658b1f-1e19-4c33-9889-188a65f268e1



