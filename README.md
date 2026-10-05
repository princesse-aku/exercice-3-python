\# Exercice 3 - RodiumAI Python SDK



Ce projet utilise le SDK Python RodiumAI pour interagir avec trois fonctionnalités :

\- Chat

\- Génération d'images

\- Génération de vidéos



\## Prérequis



\- Python 3.13 ou version compatible

\- Une clé API RodiumAI



\## Installation



Installer les dépendances :



```bash

pip install -r requirements.txt





Configuration



Copier .env.example vers .env :



copy .env.example .env



Puis renseigner votre clé API RodiumAI dans .env :



RODIUMAI\_API\_KEY=rd\_sk\_votre\_cle



Ne partagez jamais votre fichier .env.



Lancement



Exécuter :



python main.py



Le programme propose successivement :



une interaction avec le Chat ;

une génération d'image ;

une génération de vidéo.



Chaque étape permet de refaire l'action ou de passer à l'étape suivante.

