# OpenClassrooms: Projet 9: lITrevu
Ce programme a été créé dans le cadre du projet 9 d'OpenClassrooms. 
## Installation:
Veuillez installer Python.
telecharger le fichier zip  depuis cette adresse:
```
https://github.com/Mamath79/OC_P9_D-veloppez-une-application-Web-en-utilisant-Django.git

```
Unzipper le fichier

Placez vous dans le dossier , puis créez un nouvel environnement virtuel:
```
python -m venv env
```
Ensuite, activez-le.
Sous Windows:
```
env\scripts\activate.bat
```
Sous Linux ou Mac OS:
```
source env/bin/activate
```
Installattion les packages requis:
```
pip install -r requirements.txt
```
Vous pouvez enfin lancer le serveur:
```
python manage.py runserver
```

## Utilisation

### 1) 

1. 
### 2) Gestion des tournois

### 3) Menu destiné a l'affichage des rapport
Cette section a pour but d'afficher les rapports suivants:


## Creation rapport Flake 8

Installez flake8 avec la commande:

```
pip intall flake8-html
```

S'il n'existe pas, créer un fichier setup.cfg pour parametrer Flake 8 de la façon suivante.

[flake8]
exclude = .git, venv, __pycache__, .gitignore
max-line-length = 119

Tapez la commande:

```
flake8 . --format=html --htmldir=flake8_rapport
```

Le rapport sera généré dans le dossier flake8.
