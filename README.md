## `Repository name : OC_Project_12_Repository`
## Développez une architecture back-end sécurisée en utilisant Django ORM
### 📖 Vue d'ensemble
Élaborer un système CRM sécurisé interne à l'entreprise `Epic Events` en utilisant `Django` et une base de données `PostgreSQL`, qui
permet aux utilisateurs autorisés de se connecter ou se déconnecter via la page de connexion du site d'administration Django.    
- Ce système permet aux membres de l'équipe de vente de créer, afficher ou mettre à jour des clients, créer des événements pour un contrat, 
afficher et modifier les contrats.
- Il permet aussi aux membres de l'équipe de support d'afficher ou mettre à jour les événements 
et afficher les clients des événements qui leur sont attribués
### 💿 Installer Python
### ⚙️ Cloner depuis GitHub le projet Django
```bash
git clone https://github.com/RochdiGZ/OC_Project_12_Repository.git
```
### ⚙️ Modifier les propriétés du dossier OC_Project_12_Repository comme source de données
-  A l'aide de PyCharm, il suffit de sélectionner le dossier et d'utiliser le bouton droit de la souris pour choisir 
`Mark Directory as > Sources Root`
### 💿 Créer et activer un nouvel environnement virtuel `.env` & Choisir l'interpréteur Python
```bash
cd OC_Project_12_Repository
```
```bash
python -m venv .env
```
```bash
.env/Scripts/activate
```
### 💿 Installer tous les paquets du projet Django
```bash
python.exe -m pip install --upgrade pip
``` 
```bash
pip install -r requirements.txt
```
### ⚙️ Créer le dossier flake8_report
```bash
flake8 --format=html --htmldir=flake8_report --max-line-length=119
```
### ⚙️ Lancer le serveur de développement
```bash
python manage.py runserver
``` 
### ⚙️ Appliquer toutes les migrations
```bash
python manage.py migrate
``` 
### ⚙️ Créer un super utilisateur pour se connecter à partir de l'interface de l'administration Django
```bash
python.exe manage.py createsuperuser
``` 
Dans l'étape suivante, il suffit de rester dans le terminal pour taper un nom d'utilisateur (email) et un mot de passe 
avec confirmation du mot de passe. Par exemple, 
- Email: rochdi@gmail.com
- First_name : Rochdi
- Last_name : GUEZGUEZ
- Password: secret@django
### ⚙️ Se connecter avec l'interface de l'administration Django
- Une fois le serveur de développement lancé, vous pouvez voir, dans un navigateur web, la page de l'administration 
Django via `http://127.0.0.1:8000/admin`. 
### 📖 Information utile
Pour toute information sur les besoins d'exécution de l'application `Epic_Events_CRM`, veuillez me contacter par email :
`Rochdi.GUEZGUEZ@Gmail.Com`
`Vous pouvez ainsi accéder à la documentation `Postman` de notre application via :`
https://documenter.getpostman.com/view/26440710/2s93ecuUsb
