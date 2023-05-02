# CollegeBook
## Auteurs
Cette application à été réalisée par Janssens van der Maelen Emile, Miglionico Massimo , Leclerq Théo, Pierard Anthony,
Piras Antoine et Verly Jonah dans le cadre du cours de "Génie logicielle" en master 1 à l'Université de Namur.


## Description 
CollegeBook est une application web réalisée pour le Collège Saint Pierre de Uccle (CSPU). Cette application permet 
au CSPU de mettre en ligne les différentes représentations (spectacles, concerts, présentations, etc.) qu'ils souhaitent
organiser. L'application va permettre de :
* Créer des événements
* Paramétrer des configurations de salle 
* Réserver des places ainsi que des tickets boisson et de nourriture en temps que clients 
* Payer sa réservation en temps que client

## Technologies et libraires
L'application est développée en Django avec une base de données SQLite. \
La gestion des paiements est réalisée avec Stripe. 

## WINDOWS

To launch the project :
```bash

python -m venv env
./env/Scripts/activate
pip install -r requirements.txt
sh restore_BD.sh 
python ./src/manage.py runserver
```

## LINUX
To launch the project : 
```bash
python -m venv env
source ./env/bin/activate
pip install -r unix_requirements.txt
sh restore_BD.sh
python ./src/manage.py runserver
```
