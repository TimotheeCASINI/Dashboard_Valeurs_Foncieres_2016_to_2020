### Timothée CASINI - DS§ - Projet Data Visualization ###


# Bibliothèques:
import os
import time
import random
import json
import datetime as dt
import streamlit as st
import pydeck as pdk
import numpy as np
import pandas as pd 
import altair as alt
import matplotlib.pyplot as plt
from datetime import datetime as d

writepath = './src/running_time.txt'

# Fonction d'hortodatage et de file d'exécution:
def init_file(writepath):
    if os.path.exists(writepath):
        mode ='a'
    else:
        mode ='w'
    with open(writepath, mode) as file:
        dt_string = '##########  Exécution du '
        dt_string += d.now().strftime("%d/%m/%Y %H:%M:%S")
        dt_string += '  ##########\n'

        file.write(dt_string)

init_file(writepath)

# Décorateur avec temps d'execution:
def log(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        val = func(*args, **kwargs)
        with open(writepath, "a+") as f:
            f.write( "Fonction = " + func.__name__ + " | Temps d'éxécution = " + str(time.time() - start_time)+ "\n" )
        return val
    return wrapper


# Fonction de d'initiation de l'app:
@log
def init_app():
    st.title('Dashboard Valeurs Foncières')

    st.header('Projet Data Visualization - Timothée CASINI - DS6')

    st.subheader('Données portant sur les valeurs foncières déclarées de 2016 à 2020')

    st.markdown("<p style='text-align: justify; color: grey; position:left;'>Ce projet à pour objectif d'appliquer le processus d'exploration visuelle de données que nous avons vu pendant les labs au jeu de données 'Demandes de foncières valeurs'. Nous allons visualiser à travers différents diagrammes les données mais également leurs appliquées différents traitements et les explorer sous plusieurs formes afin d'en faire ressortir des annalyses pertinantes. ",unsafe_allow_html=True)

init_app()

# Chargement des donées:
file_2016 = './data/full_2016.csv'
file_2017 = './data/full_2017.csv'
file_2018 = './data/full_2018.csv'
file_2019 = './data/full_2019.csv'
file_2020 = './data/full_2020.csv'

files = [file_2016, file_2017, file_2018, file_2019, file_2020]
@st.cache(suppress_st_warning=True, allow_output_mutation=True)
@log
def init_df(files):

     df_2016 = pd.read_csv(
          files[0],
          header=0,low_memory=False)

     df_2017 = pd.read_csv(
          files[1],
          header=0,low_memory=False)

     df_2018 = pd.read_csv(
          files[2],
          header=0,low_memory=False)

     df_2019 = pd.read_csv(
          files[3],
          header=0,low_memory=False)

     df_2020 = pd.read_csv(
          files[4],
          header=0,low_memory=False)

     return df_2016, df_2017, df_2018, df_2019, df_2020

# Taux de valeurs manquantes:
@st.cache(suppress_st_warning=True, allow_output_mutation=True)
@log
def missing_rate(df):
    miss_data = df.isna()
    miss_data = miss_data.sum()
    miss_data = miss_data/len(df)
    miss_data_bool = miss_data > 0.5

    return miss_data[miss_data_bool == True]

# Suppression des données manquantes :
@st.cache(suppress_st_warning=True, allow_output_mutation=True)
@log
def cleaning(df, indexes):
    df = df.drop(labels=indexes, axis=1)
    
    df['valeur_fonciere'] = df['valeur_fonciere'].fillna(value=df['valeur_fonciere'].mean()) # on affecte la moyenne aux éléments vides
    df['surface_terrain'] = df['surface_terrain'].fillna(value=df['surface_terrain'].mean())
    df['nombre_pieces_principales'] = df['nombre_pieces_principales'].fillna(value=df['nombre_pieces_principales'].mean())
    
    for i in df.columns:
        if (df[i].isnull().values.any() == True):
            df.dropna(subset = [i,], inplace=True) # supression ligne si vide
    return df

# Transformation des types:
@st.cache(suppress_st_warning=True, allow_output_mutation=True)
@log
def pre_processing(df):
    for y in df.columns:
        if(df[y].dtype == object):
            df[y] = df[y].convert_dtypes()
    df['date_mutation'] = pd.to_datetime(df['date_mutation'])

    return df

# Mois:
def get_mth(dt): 
    return dt.month

# Jour du mois:
def get_dom(dt): 
    return dt.day
    
# Nombre de lignes:
def get_rows(rows):
    return len(rows)

# Prix par mètre carré:
def get_price_by_square (df):
    return (df.valeur_fonciere / df.surface_terrain)

# Région:
def get_regions (code_departement):
    auvergne = ['01','03','07','15','26','38','42','43','63','69','73','74']
    bourgogne = ['21','25','39','58','70','71','89','90']
    bretagne = ['22','29','35','56']
    val_loire = ['18','28','36','37','41','45']
    corse = ['20']
    ile_de_france = ['75','77','78','91','92','93','94','95']
    est = ['08','10','51','52','54','55','57','67','68','88']
    haut_france = ['02','59','60','62','80']
    normandie = ['14','27','50','61','76']
    aquitaine = ['16','17','19','23','24','33','40','47','64','79','86','87']
    occitanie = ['09','11','12','30','31','32','34','46','48','65','66','81','82']
    pays_loire = ['44','49','53','72','85']
    provence = ['04','05','06','13','83','84']

    region =''

    if (code_departement in auvergne):
        region = "AUVERGNE-RHÔNE-ALPES"

    elif (code_departement in bourgogne):
        region = "BOURGOGNE-FRANCHE-COMTÉ"
    
    elif (code_departement in bretagne):
        region = "BRETAGNE"
    
    elif (code_departement in val_loire):
        region = "CENTRE-VAL-DE-LOIRE"
    
    elif (code_departement in corse):
        region = "CORSE"

    elif (code_departement in ile_de_france):
        region = "ÎLE-DE-FRANCE"

    elif (code_departement in est):
        region = "GRAND-EST"

    elif (code_departement in haut_france):
        region = "HAUT-DE-FRANCE"

    elif (code_departement in normandie):
        region = "NORMANDIE"

    elif (code_departement in aquitaine):
        region = "NOUVELLE-AQUITAINE"

    elif (code_departement in occitanie):
        region = "OCCITANIE"

    elif (code_departement in pays_loire):
        region = "PAYS-DE-LA-LOIRE"

    elif (code_departement in provence):
        region = "PROVENCE-ALPES-CÔTE D'AZUR"
    
    else:
        region = "CORSE"

    return region

@log
@st.cache(suppress_st_warning=True)
def process_square(df):

    # On regroupe les données selon le prix par mètre carré moyen:
    group_by_square = df.groupby(['code_departement','region']).agg({'surface_terrain':'mean','valeur_fonciere':'mean'})
    
    return group_by_square

@log
@st.cache(suppress_st_warning=True)
def process_commune(df):
    
    # On regroupe les données par commune:
    group_by_commune = df.groupby('nom_commune').size()
    group_by_commune = group_by_commune.sort_values()

    return group_by_commune

@log
@st.cache(suppress_st_warning=True)
def process_commune_square(df):

    # On regroupe les données selon le prix par mètre carré moyen:
    group_by_commune_square = df.groupby('nom_commune').agg({'price_by_square':'mean'})
    group_by_commune_square = group_by_commune_square.sort_values(by='price_by_square')
    
    return group_by_commune_square

@log
@st.cache(suppress_st_warning=True)
def process_commune_departement_square(df):

    # On regroupe les données selon le prix par mètre carré moyen:
    group_by_commune_departement_square = df.groupby(['code_departement','nom_commune']).agg({'price_by_square':'mean'})

    
    return group_by_commune_departement_square

@log
@st.cache(suppress_st_warning=True)
def process_departement(df):

    # On regroupe les données par département:
    group_by_departement = df.groupby('code_departement').size()
    group_by_departement = group_by_departement.sort_values()
    
    return group_by_departement

@log
@st.cache(suppress_st_warning=True)
def process_departement_square(df):

    # On regroupe les données selon le prix par mètre carré moyen:
    group_by_departement_square = df.groupby('code_departement').agg({'price_by_square':'mean'})
    group_by_departement_square = group_by_departement_square.sort_values(by='price_by_square')
    
    return group_by_departement_square

@log
@st.cache(suppress_st_warning=True)
def process_month(df):
    group_by_dom = df.groupby('dom').size()
    
    return group_by_dom

@log
@st.cache(suppress_st_warning=True)
def process_region(df):
    group_by_depatement_region = df.groupby(['region','code_departement']).size().unstack(level=0)
    group_by_depatement_region = group_by_depatement_region.fillna(0)
    return group_by_depatement_region

@log
@st.cache(suppress_st_warning=True)
def process_local(df):
    group_by_local = df.groupby(['code_departement','type_local']).size().unstack(level=1)
    group_by_local = group_by_local.fillna(0)
    return group_by_local

@log
@st.cache(suppress_st_warning=True)
def process_local_region(df):
    group_by_local_region = df.groupby(['region','type_local']).size().unstack(level=1)
    group_by_local_region = group_by_local_region.fillna(0)
    return group_by_local_region

# Traitement des données:
@log
@st.cache(suppress_st_warning=True)
def processing(df):

    df['mth']  = df['date_mutation'].map(get_mth)
    df['dom']  = df['date_mutation'].map(get_dom)
    df['price_by_square'] = get_price_by_square(df)
    df['region']  = df['code_departement'].map(get_regions)
    
    return df

option_data = st.sidebar.selectbox(
            "Quels données voulez vous choisir ? ", ['Valeurs Foncières 2016','Valeurs Foncières 2017', 'Valeurs Foncières 2018', 'Valeurs Foncières 2019', 'Valeurs Foncières 2020'])
    
# Choix du dataframe:
@log
def init_data():
    df_2016, df_2017, df_2018, df_2019, df_2020 = init_df(files)
    
    if (option_data == 'Valeurs Foncières 2016'):
            df = df_2016
            st.markdown('##### Données des valeurs foncières déclarées en 2016')
            st.write("On observe de nombreuse données manquantes, mal codées ou nécessitant un pré-traitement. Nous allons d'abords nettoyer les données en supprimans les colonnes où le pourcentage de données manquantes est trop importantes. Ensuite, nous supprimerons les lignes où des données manquent encore à l'appel. On intégrera de nouvelles données et on transformera les colonnes dont le type n'est pas correct. On inserera de nouvelles colonne et on remplira celle dont les valeurs manquantes peuvent être déduites.")

            st.caption('Dataframe initial')
            st.dataframe(df.head())

    elif (option_data == 'Valeurs Foncières 2017'):
            df = df_2017
            st.markdown('##### Données des valeurs foncières déclarées en 2017')
            st.write("On observe de nombreuse données manquantes, mal codées ou nécessitant un pré-traitement. Nous allons d'abords nettoyer les données en supprimans les colonnes où le pourcentage de données manquantes est trop importantes. Ensuite, nous supprimerons les lignes où des données manquent encore à l'appel. On intégrera de nouvelles données et on transformera les colonnes dont le type n'est pas correct. On inserera de nouvelles colonne et on remplira celle dont les valeurs manquantes peuvent être déduites.")

            st.caption('Dataframe initial')
            st.dataframe(df.head())

    elif (option_data == 'Valeurs Foncières 2018'):
            df = df_2018
            st.markdown('##### Données des valeurs foncières déclarées en 2018')
            st.write("On observe de nombreuse données manquantes, mal codées ou nécessitant un pré-traitement. Nous allons d'abords nettoyer les données en supprimans les colonnes où le pourcentage de données manquantes est trop importantes. Ensuite, nous supprimerons les lignes où des données manquent encore à l'appel. On intégrera de nouvelles données et on transformera les colonnes dont le type n'est pas correct. On inserera de nouvelles colonne et on remplira celle dont les valeurs manquantes peuvent être déduites.")
            st.caption('Dataframe initial')
            st.dataframe(df.head())

    elif (option_data == 'Valeurs Foncières 2019'):
            df = df_2019
            st.markdown('##### Données des valeurs foncières déclarées en 2019')
            st.write("On observe de nombreuse données manquantes, mal codées ou nécessitant un pré-traitement. Nous allons d'abords nettoyer les données en supprimans les colonnes où le pourcentage de données manquantes est trop importantes. Ensuite, nous supprimerons les lignes où des données manquent encore à l'appel. On intégrera de nouvelles données et on transformera les colonnes dont le type n'est pas correct. On inserera de nouvelles colonne et on remplira celle dont les valeurs manquantes peuvent être déduites.")
            st.caption('Dataframe initial')
            st.dataframe(df.head())

    elif (option_data == 'Valeurs Foncières 2020'):
            df = df_2020
            st.markdown('##### Données des valeurs foncières déclarées en 2020')
            st.write("On observe de nombreuse données manquantes, mal codées ou nécessitant un pré-traitement. Nous allons d'abords nettoyer les données en supprimans les colonnes où le pourcentage de données manquantes est trop importantes. Ensuite, nous supprimerons les lignes où des données manquent encore à l'appel. On intégrera de nouvelles données et on transformera les colonnes dont le type n'est pas correct. On inserera de nouvelles colonne et on remplira celle dont les valeurs manquantes peuvent être déduites.")
            st.caption('Dataframe initial')
            st.dataframe(df.head()) 

    st.markdown("**Pour visualiser le traitement des données, veuillez cliquer sur le bouton `Voir le traitement des données`.**")
    
    col1, col2, col3 = st.columns(3)

    with col1:
            pass
    with col3:
            pass
    with col2 :
            btn = st.button('Voir le traitement des données')

    if btn:
            st.subheader('Traitement des données')
            
            miss = missing_rate(df)
            miss.name = 'missing_rate'
            st.markdown('##### Nettoyage des données')
            st.caption("Rapport de données manquantes par variables")
            col1, col2 = st.columns([3,1])
            col1.dataframe(miss)
            col2.markdown("<p style='text-align: justify; color: grey; position:left;'>Nous allons supprimer toute les colonnes où le taux de valeurs manquantes est supérieurs à 50%, afin de ne remplacer qu'un minimum de valeurs manquantes.",unsafe_allow_html=True)
            
            df = cleaning(df, miss.index)
            st.caption('Dataframe nettoyé')   
            st.dataframe(df.head()) 
            st.markdown("On s'assure que le dataframe ne contient plus de valeure manquante :")
            st.code('df.isnull().values.any() == False')

            if (df.isnull().values.any() == False):
                    st.code(">>> True")

            df = pre_processing(df)
            st.markdown('##### Transformation des données')
            st.caption("Modification des types")
            st.image('./img/img1.jpg')
            st.markdown("On corrige l'encodage des données puis nous allons integrer de nouvelles variables afin d'enrichir notre dataframe et d'effectuer différent traitements dessus.")

            df = processing(df)
            group_by_commune = process_commune(df)
            group_by_departement = process_departement(df)
            group_by_commune_square = process_commune_square(df)
            group_by_departement_square = process_departement_square(df)
            
            st.markdown('##### Intégration des données')
            st.caption('Dataframe enrichie')
            st.dataframe(df.head())
            
            col1, col2 = st.columns(2)
            col1.caption('Données par commune')
            col2.caption('Prix moyen par commune')

            col1, col2 = st.columns(2)
            group_by_commune_tail = group_by_commune.tail()
            group_by_commune_square_tail = group_by_commune_square.tail()
            col1.table(group_by_commune_tail.to_frame().style.highlight_max(axis=0))
            col2.table(group_by_commune_square_tail.style.highlight_max(axis=0))

            col1, col2 = st.columns(2)
            col1.caption('Données par département')
            col2.caption('Prix moyen par département')

            col1, col2 = st.columns(2)
            group_by_departement_tail = group_by_departement.tail()
            group_by_departement_square_tail = group_by_departement_square.tail()
            col1.table(group_by_departement_tail.to_frame().style.highlight_max(axis=0))
            col2.table(group_by_departement_square_tail.style.highlight_max(axis=0))
            
            agree = st.checkbox('Voir moins')

            if agree:
                    btn = False

    else:
            miss = missing_rate(df)
            df = cleaning(df, miss.index)
            df = pre_processing(df)
            df = processing(df)
           
    st.caption('Dataframe final')
    st.dataframe(df.head())
    st.write("On peut désormais effectué différents traitements sur le dataframe car il est correctement implémenté. Nous allons dans un premier temps analyser les données dans leurs ensembles et s'intéresser au information comme le taux de croissance, les villes/départements/régions avec le plus de transactions immobilière/le plus prix moyen au mètre carré. Nous visuliserons également la fréquence de transaction selon les mois et selon le type de local.")
    st.write("Dans un autre temps, nous gererons la visualisation des données selon les différents traitements effectués précédement comme par exemple le prix aumètre carré moyen par région ou selon différents mois.")
    st.markdown("**Pour visualiser les différents traitements, utiliser les `widgets` dans la slidebar.**")
    
    return df, df_2016, df_2017, df_2018, df_2019, df_2020           

df, df_2016, df_2017, df_2018, df_2019, df_2020 = init_data()

# Création des fonctionnalités de la sidebar:
@log
def init_sidebar(df):
        
        pick = None
        options = None
        format = 'Y-M'  # format output
        start_date = dt.date(2016, 1, 1)
        end_date = dt.date(2016, 12, 30)

        if (option_data == 'Valeurs Foncières 2016'):
                start_date = dt.date(2016, 1, 1)
                end_date = dt.date(2016, 12, 30)

        elif (option_data == 'Valeurs Foncières 2017'):
                start_date = dt.date(2017, 1, 1)
                end_date = dt.date(2017, 12, 30)

        elif (option_data == 'Valeurs Foncières 2018'):
                start_date = dt.date(2018, 1, 1)
                end_date = dt.date(2018, 12, 30)

        elif (option_data == 'Valeurs Foncières 2019'):
                start_date = dt.date(2019, 1, 1)
                end_date = dt.date(2019, 12, 30)

        elif (option_data == 'Valeurs Foncières 2020'):
                start_date = dt.date(2020, 1, 1)
                end_date = dt.date(2020, 12, 30)

        agree = st.sidebar.checkbox('Spécifier un date')
        if agree:
                pick = st.sidebar.slider('Choisir un mois spécifique', min_value=start_date, value=end_date ,max_value=end_date, format=format)
                st.sidebar.write("Mois choisie :", pick.strftime('%b'))
                mask1 = df['mth'] == pick.month
                df = df[mask1]
  
        else:
                pick = 1;
    
        


        options = st.sidebar.multiselect('Quelles régions ?',
        ["AUVERGNE-RHÔNE-ALPES", "BOURGOGNE-FRANCHE-COMTÉ", "BRETAGNE", "CENTRE-VAL-DE-LOIRE", "CORSE",
        "ÎLE-DE-FRANCE", "GRAND-EST","HAUT-DE-FRANCE","NORMANDIE", "NOUVELLE-AQUITAINE", "OCCITANIE", "PAYS-DE-LA-LOIRE", "PROVENCE-ALPES-CÔTE D'AZUR"])
        
        if options:
                mask2 = df['region'].isin(options)
                df = df[mask2]
                
        else:
                options = 1;
       
        st.caption('Dataframe réduit')
        st.dataframe(df.head())
        st.text("La taille du dataframe séléctionné est :" + str(df.shape))

        return pick, options
pick, options = init_sidebar(df)

@log
def init_charts(df):

    st.subheader('Visualisation des données sélectionnées')
    st.markdown("<p style='text-align: justify; color: grey; position:left;'>Nous allons visualiser les données à travers différents graphiques et traitements. Nous analyseron la fréquences de transactions financière, le taux de croissance, le prix au mètre carré moyen selon plusieurs paramètres et catégories comme le type de local, la région, le mois, ... ",unsafe_allow_html=True)

    if (type(pick) != int):
        mask1 = df['mth'] == pick.month
        df = df[mask1]
    
    if (type(options) != int):
        mask2 = df['region'].isin(options)
        df = df[mask2]

    st.markdown("##### Fréquence des transaction finnancière")
    st.write("Nous allons nous interesser ici aux nombre de transactions finnancières. On peut visualiser la fréquences selon les communes, les départements, les régions et les mois. Vous pouvez également y appliquer les différents paramètres de la sidebar.")
    
    group_by_commune = process_commune(df)
    group_by_commune.name = 'Transactions'
    group_by_departement = process_departement(df)
    group_by_departement.name = 'Transactions'
    group_by_commune_square = process_commune_square(df)
    group_by_commune_square.name = 'Prix moyen'

    col1, col2 = st.columns(2)
    col1.metric("Ville avec le plus de transactions :",group_by_commune.idxmax(), group_by_commune.tail(1).item())
    col2.metric("Département avec le plus de transactions :", group_by_departement.idxmax(), group_by_departement.tail(1).item())

    st.caption("Nombre de transactions par commune - Top 10")
    st.area_chart(group_by_commune.tail(10))


    st.caption("Nombre de transactions par département - Top 10")
    st.area_chart(group_by_departement.tail(10))

    fig1 = plt.figure()
    x1 = group_by_commune.tail(10)
    ax = x1.plot(kind="bar", label = "Top 10 communes", width=0.5)
    ax.set_xlabel('Communes')
    ax.set_ylabel('Fréquence transaction')
    ax.set_title('Fréquence par commune - Top 10')

    fig2 = plt.figure()
    x2 = group_by_departement.tail(10)
    ax = x2.plot(kind="bar", label = "Top 10 départements", width=0.5)
    ax.set_xlabel('Département')
    ax.set_ylabel('Fréquence transaction')
    ax.set_title('Fréquence par département - Top 10')

    col1, col2 = st.columns([3,2])
    col1.caption('Histogramme trié des fréquences par commune')
    col2.caption('Dataframe des fréquences par commune')

    col1, col2 = st.columns([3,2])
    col1.pyplot(fig1)
    col2.write(group_by_commune.tail(10))
    
    col1, col2 = st.columns([2,3])
    col2.caption('Histogramme trié des fréquences par département')
    col1.caption('Dataframe des fréquences par département')

    col1, col2 = st.columns([2,3])
    col2.pyplot(fig2)
    col1.write(group_by_departement.tail(10))
    
    plt.set_loglevel('WARNING')

        
    if not(type(pick) != int):

        fig, ax = plt.subplots()
        ax.hist(df.mth, bins=12, rwidth=0.8, label = "Mois")
        ax.set_title("Fréquence par mois")
        ax.set_xlabel("Mois")
        ax.set_ylabel("Nombre de transactions")
        ax.set_xticks(range(1,13))
        ax.set_xticklabels(['JANV','FEV','MARS','AVRL','BMAI','JUIN','JUILLT', 'AOUT', 'SEPT', 'OCT', 'NOV', 'DEC'])
        st.caption("Histogramme des fréquences par mois")
        st.pyplot(fig)

    else:

        group_by_dom = process_month(df)
        st.caption("Fréquences par jours du mois")

        fig, ax = plt.subplots()
        ax.plot(group_by_dom.index, group_by_dom)
        ax.set_title("Fréquence par jour du mois")
        ax.set_xlabel("Jours du mois")
        ax.set_ylabel("Nombre de transactions")
        st.pyplot(fig)

    
    if not(type(options) != int):

        labels = ["AVRGN", "BRGN", 
                    "BRTN", "VDL", "CRS",
                    "IDF", "GRD-EST","HDF",
                    "NRMND", "NVL-ACQT", "OCTN", 
                    "PDLL", "PACA"]
        st.caption('Histogramme des fréquences par région')

        fig, ax = plt.subplots()
        ax.hist(df['region'], bins=13, rwidth=0.8)
        ax.set_xlabel('Régions')
        ax.xaxis.set_tick_params(labelsize=6)
        ax.set_xticks(range(0,13))
        ax.set_xticklabels(labels)
        ax.set_ylabel('Nombre de transactions')
        ax.set_title('Fréquence par région')

        st.pyplot(fig)

        group_by_local_region = process_local_region(df)
        group_by_local_region.columns = group_by_local_region.columns.values
        st.caption('Fréquences des transactions par région selon le type de local')
        st.bar_chart(group_by_local_region)
   



    else:

        group_by_departement_region = process_region(df)
        st.caption('Nuage de points des fréquences par département selon chaque région')
        
        fig,ax = plt.subplots()
        plt.set_loglevel('WARNING')
        ax.plot(group_by_departement_region,'o', label=group_by_departement_region.columns.values)
        ax.legend(loc='upper right', prop={'size': 6})
        ax.xaxis.set_tick_params(labelsize=4) 
        ax.set_xlabel('Département')
        ax.set_ylabel('Fréquence')
        ax.set_title('Fréquence par département selon chaque région')

        st.pyplot(fig)

        if (len(options) != 1):
            group_by_local_region = process_local_region(df)
            group_by_local_region.columns = group_by_local_region.columns.values
            st.caption('Fréquences des transactions par région selon le type de local')
            st.bar_chart(group_by_local_region)
        else :
            group_by_local = process_local(df)
            group_by_local.columns = group_by_local.columns.values
            st.caption('Fréquences des transactions par région selon le type de local')
            st.line_chart(group_by_local)
        

init_charts(df)

@log
def init_square(df):

    st.markdown('##### Visualisation des prix des biens fonciers')
    st.write("On s'intéresse ici au prix du terrain (en mètre carré). Nous avons divisé la valeurf foncière par la surface du terrain, obtenant ainsi cette variable. Grace à différents graphique (ligne, nuage de point, histogramme) nous allons pouvoir en tirer quelque analyses.")

    if (type(pick) != int):
        mask1 = df['mth'] == pick.month
        df = df[mask1]
    
    if (type(options) != int):
        mask2 = df['region'].isin(options)
        df = df[mask2]  
        
    group_by_commune_square = process_commune_square(df)
    group_by_commune_square.name = 'Prix moyen'
  
    group_by_departement_square = process_departement_square(df)
    group_by_departement_square.name = 'Prix moyen'

    col1, col2 = st.columns(2)
    col1.metric("Ville avec le prix moyen le plus haut:",group_by_commune_square.tail(1).last_valid_index(), str(group_by_commune_square.values[-1:]).strip('[]') + "€")
    col2.metric("Département avec le prix moyen le plus haut:", group_by_departement_square.tail(1).last_valid_index(), str(group_by_departement_square.values[-1:]).strip('[]') + "€")

    st.caption("Prix moyen par commune - Top 10")
    st.bar_chart(group_by_commune_square.tail(10))

    
    st.caption("Prix moyen par departement - Top 10")
    st.bar_chart(group_by_departement_square.tail(10))
    
    group_by_square = process_square(df)
    group_by_square  = group_by_square.reset_index()


    # Mask pour s'assurer d'avoir une visualisation correcte : on n'affiche pas les données dont l'achat a couté plus de 1 millions d'euros ou dont la surface dépasse 2000 mètres carrés
    if (type(options) != int):

        c = alt.Chart(group_by_square).mark_circle().encode(
            x='valeur_fonciere', y='surface_terrain', size='region', color='region', tooltip=['code_departement','region','valeur_fonciere','surface_terrain'])

        st.caption('Rapport moyen (Valeurs_Foncière/Surface) dans les différents départements de chaque région')
        st.altair_chart(c, use_container_width=True)

        group_by_commune_departement_square = process_commune_departement_square(df)

        group_by_commune_departement_square = group_by_commune_departement_square.reset_index()


        fig, ax = plt.subplots(figsize=(20,5))
        ax.scatter(group_by_commune_departement_square['code_departement'], group_by_commune_departement_square['price_by_square'])

        ax.set_xlabel('Régions')
        ax.set_ylabel('Prix moyen')
        ax.set_ylim(0,200000)
        ax.xaxis.set_tick_params(labelsize=8)
        ax.set_title('Prix moyen pour chaque ville de chaque region')
        st.caption("Prix moyen des villes de chaque region")
        st.pyplot(fig)
    
        st.caption('Prix moyen des transactions pour chaque departement de chaque région')
        c = alt.Chart(df).mark_circle().encode(x='code_departement', y='price_by_square', size='region', color='region', tooltip=['nom_commune','region','code_departement','price_by_square'])

        st.altair_chart(c, use_container_width=True)
        


    else:

        mask = group_by_square['valeur_fonciere'] < 1000000
        group_by_square = group_by_square[mask]
        mask = group_by_square['surface_terrain'] < 2000
        group_by_square = group_by_square[mask]


        c = alt.Chart(group_by_square).mark_circle().encode(
            x='valeur_fonciere', y='surface_terrain', size='region', color='region', tooltip=['code_departement','region','valeur_fonciere','surface_terrain'])

        st.caption('Rapport moyen Valeurs dans les différents départements de chaque région (sans IDF)')
        st.altair_chart(c, use_container_width=True)

        
        fig, ax = plt.subplots(figsize=(20,5))
        ax.scatter(df['region'], df['price_by_square'])

        ax.set_xlabel('Départements')
        ax.set_ylabel('Prix moyen')
    
        ax.xaxis.set_tick_params(labelsize=8)
        ax.set_title('Prix moyen pour chaque transactions de chaque département')

        st.caption('Prix moyen des transactions pour chaque département')
        st.pyplot(fig)


init_square(df)


@log
def init_map(df):

    st.markdown('##### Visualisation des positions etde la map')
    st.write("On s'intéresse désormais à la position des individus, à leurs densités, leurs représentation sur une map, ... Nous allons visualiser ces éléments afin d'en dégager plusieurs analyses.")

    if (type(pick) != int):
        mask1 = df['mth'] == pick.month
        df = df[mask1]
    
    if (type(options) != int):
        mask2 = df['region'].isin(options)
        df = df[mask2]  

    st.caption('Nuage de points des positions')
    fig, axs = plt.subplots()
    axs.plot(df.longitude,df.latitude,'.', alpha=.5)
    axs.set_title("Positions")
    axs.set_xlabel("Longitude")
    axs.set_ylabel("Latitude")
    st.pyplot(fig)

    fig, ax = plt.subplots()
    ax.hist(df.latitude,alpha=0.5, color='b', label = "Latitude")
    ax.legend(loc='upper right')
    ax.twiny()
    ax.hist(df.longitude,alpha=0.5, color='r', label = "Longitude")
    ax.set_title("Histogramme Latitude/Longitude")
    ax.legend(loc='upper left')
    st.pyplot(fig)

    df = df.sample(frac =.04)
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
        latitude=48.8534,
        longitude=2.3488,
        zoom=12,
        pitch=50,
        ),
        layers=[
        pdk.Layer('HexagonLayer',
        data=df,
        get_position='[longitude, latitude]',
        radius=200,
        elevation_scale=4,
        elevation_range=[0, 1000],
        pickable=True,
        extruded=True,),
        pdk.Layer(
        'ScatterplotLayer',
        data=df,
        get_position='[longitude, latitude]',
        get_radius=200,
        ),
        ],))
        
init_map(df)
