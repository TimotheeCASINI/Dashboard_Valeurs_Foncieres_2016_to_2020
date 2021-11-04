# Dashboard Streamlit des Valeurs Foncieres 2016-2020

## Projet M1 de Data Visualization sur les valeurs foncières française de 2016 à 2020

### Introduction

Ce projet se décompose en 4 dossiers :
* `infos`: Contient toute les informations utiles, consignes, résultats du projet
* `src`: Contient le fichier source de l'application et le fichier texte d'hortodatage
* `img`: Contient les screenshots utiles du projet
* `data`: Contient les données des valeurs foncières sous format *csv*

Le développement de l'application est détailé dans le notebook python afin de coder 'step by step' l'application de A à Z !

Tout au long du développement, nous utiliserons les différentes notions et techniques vus en cours (décorateur, processus d'exploration, modularité du code, ...) afin d'avoir un code partagable, le plus performant possible et répondant aux éxigences du projet.


#### Objectifs

Dans ce projet nous alllons appliquer le processus d'exploration visuelle de données au jeu de données "**Demandes de foncières valeurs**".

Nous traiterons ce problème sous `Python` avec l'aide du module `Streamlit` afin de générer une application locale pour la visualisation de nos données et de nos différents traitements.

Le jeu de données complet est disponible via ce lien : <https://drive.google.com/drive/folders/1R_9A9yPOzRQzMCyTDBEJms0u1ZCN7MbY>

Le dossier contient 5 fichiers CSV et 2 fichiers pdf : 
* 1 pour la FAQ
* 1 pour la description des colonnes

Le jeu de données est accessible au public sur le site ***data.gouv.fr*** : <https://www.data.gouv.fr/en/datasets/demandes-de-valeurs-foncieres/>

Par défaut d'espace sur le Git, nous avons fractionné les données afin que vous puissez tout de même les télécharger, les visualiser, etc.

**Je vous conseil d'utiliser les véritables données disponibles depuis les liens ci-dessus car ils seront nettement plus complet, en effet, ces données fractionnés représentent seulement 4% de l'ensemble des données**


#### Processus d'exploration

On rappel le processus d'exploration visuel :

1. **Chargement des données** : Import des bibliothèques et structure de données 

2. **Traitement des données** : Nettoyage, prétraitement, transformation et enrichissement des données

3. **Visualisation des données** :Représentation visuelle et analyse

4. **Exploration des données** : Extraction de résultat suite aux analyse


#### Contraintes

Plusieurs contraintes sont indiqué pour la réalisation du projet, tout celà est détailé dans le *notebook*.

1. Vous disposez de 5 fichiers csv et devez utiliser au MINIMUM 1 fichier

2. Lire la FAQ et la notice descriptive avant commencer à coder

3. Utiliser l'un des deux packages python EDA automatisés dans un notebook distinct afin d'explorer rapidement les fichiers

<br>

Votre application streamlit doit respecter les exigences suivantes :

- Organiser votre code en fonctions modulaires
       
- 2 plot interne streamlit : `st.line` ou `st.bar_chart` ET `st.map`
       
- 4 graphiques externes différents intégrés à votre application à partir de bibliothèques externes
       
- 2 checkboxs qui interagissent avec votre jeu de données
       
- Un slider qui intéragit avec un ou plusieurs plots
       
- Au minimum un cache pour le chargement et le pré-traitement des données avec `st.cache`
       
- Un décorateur qui consigne dans un fichier l'intervalle de temps d'exécution en secondes et l'horodatage de l'appel de la fonction appelée via le décorateur
       
- Facultatif : essayez d'organiser vos appels de fonctions en une fonction principale afin d'avoir un workflow clair de votre application

- Facultatif : Intégrez tous les fichiers ensemble afin d'avoir une perspective sur plusieurs années

- Facultatif : Imaginez des formulaires - textes, dates ou chiffres - pour récupérer les saisies de vos utilisateurs et leur restituer des analyses et des visualisations correspondant à leurs critères de recherche et de choix


### Prérequis

Afin de mener à bien ce projet, vous aurez besoin de quelques outils intallé préalablement sur votre machine.

Vous aurez besoin des outils suivants :
- IDE Python
- Environnement virtuel Python
- Un kernel Jupyter Notebook
- Un gestionnaire de package Python

* Installation de python

Pour verifier l'installation de python : `python --version`

<sub>Si python n'est pas reconnue, veuillez suivre les instruction [ici (Window)](https://medium.com/co-learning-lounge/how-to-download-install-python-on-windows-2021-44a707994013) ou [ici (MacOS)](https://docs.python.org/fr/3/using/mac.html)</sub>

