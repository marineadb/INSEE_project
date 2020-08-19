# coding: utf-8
# ALVES DE BARROS MARINE - MAI 2020
# M1 BIOINFO BORDEAUX
# BDD - PROJET INSEE
# CREATION ET REMPLISSAGE DES TABLES

import psycopg2
import pandas as pd
import matplotlib as plt
import csv
import numpy as np


#Chargement du fichier des départements
def charge_dep(departements):
    file=open("departement2020.csv","r")
    reader = csv.reader(file, delimiter = ",") 
    for row in reader:
        departements.append(row)
    return(departements)


#Chargement du fichier des régions    
def charge_reg(regions):
    file=open("region2020.csv","r")
    reader = csv.reader(file, delimiter = ",") 
    for row in reader:
        regions.append(row)
    return(regions)

#Remplace les données non existantes par des 0 (NULL)
def replace_nan(data):
    data= data.replace(to_replace='nd', value=np.nan)
    data= data.replace(to_replace='nd ', value=np.nan) #Parfois il y a des espaces apres 'nd'
    data= data.replace(to_replace='nc', value= np.nan)
    return data

# Supprime les 3 lignes correspondant à la france, la france metropolitaine et la province.
def delete_france(data):
    data = data.drop(['F','P','M'], axis=0)
    return data

#Charge les données environnementales
def env_data():
    myFile = 'DD-indic-reg-dep_janv2018.xls'
    sp = pd.ExcelFile(myFile)
    myData = sp.parse('Environnement')
    myData.columns=['num_dep','dep','MO_2013', 'MO_2009','surf_2012','surf_2006','AB_2016','AB_2010','granul_2014','granul_2009','eolien_2015','eolien_2010','photo_2015','photo_2010','autres_2015','autres_2010']
    myData = myData.iloc[2:106]
    myData = replace_nan(myData)
    myData = myData.set_index('num_dep')
    myData = delete_france(myData)
    myData = myData.reset_index()
    myData = myData.round(1)
    return myData

#Charge les données sociales des régions
def social_data_reg():
    myFile = 'DD-indic-reg-dep_janv2018.xls'
    sp = pd.ExcelFile(myFile)
    myData = sp.parse('Social')
    myData = myData.iloc[2:23]
    myData = myData.drop(['Unnamed: 6','Unnamed: 7', 'Unnamed: 8'],axis=1)
    myData.columns=['num_reg','reg','pauvrete','jeunes_2014','jeunes_2009','economie']
    myData = replace_nan(myData)
    myData = myData.set_index('num_reg')
    myData = delete_france(myData)
    myData = myData.reset_index()
    myData = myData.round(1)
    return myData

#Charge les données sociales des départements
def social_data_dep():
    myFile = 'DD-indic-reg-dep_janv2018.xls'
    sp = pd.ExcelFile(myFile)
    myData = sp.parse('Social')
    myData = myData.iloc[27:131]
    myData.columns = ['num_dep','dep','evh_2015','evh_2010','evf_2015','evf_2010','eloigne','inondable_2013','inondable_2008']
    myData = replace_nan(myData)
    myData = myData.set_index('num_dep')
    myData = delete_france(myData)
    myData = myData.reset_index()
    myData = myData.round(1)
    return myData


def create_tables(cur,conn):
    cur.execute("CREATE TABLE regions(region INT PRIMARY KEY, cheflieu VARCHAR(10), tncc INT, ncc VARCHAR(30), nccenr VARCHAR(30), libelle VARCHAR(30));")
    cur.execute("CREATE TABLE departements(departement VARCHAR(3) PRIMARY KEY, region INT, cheflieu VARCHAR(10),tncc INT, ncc VARCHAR(30), nccenr VARCHAR(30), libelle VARCHAR(30));")
    cur.execute("CREATE TABLE energies(departement VARCHAR(3), annee INT, eolien DECIMAL, photovoltaique DECIMAL, autre DECIMAL, PRIMARY KEY(departement, annee));")
    cur.execute("CREATE TABLE valorisation(departement VARCHAR(3), annee INT, taux DECIMAL, PRIMARY KEY(departement,annee));")
    cur.execute("CREATE TABLE artificialisation(departement VARCHAR(3), annee INT, part DECIMAL  , PRIMARY KEY(departement,annee));")
    cur.execute("CREATE TABLE agbiologique(departement VARCHAR(3), annee INT, part DECIMAL  , PRIMARY KEY(departement,annee));")
    cur.execute("CREATE TABLE granulats(departement VARCHAR(3), annee INT, production DECIMAL, PRIMARY KEY(departement,annee));")
    cur.execute("CREATE TABLE zoneinondable(departement VARCHAR(3), annee INT, part DECIMAL  ,PRIMARY KEY(departement,annee));")
    cur.execute("CREATE TABLE esperancevie(departement VARCHAR(3), annee INT, esperanceh DECIMAL  , esperancef DECIMAL  , PRIMARY KEY(departement,annee));")
    cur.execute("CREATE TABLE eloignementservices(departement VARCHAR(3) PRIMARY KEY, part DECIMAL  );")
    cur.execute("CREATE TABLE economiesociale(region INT PRIMARY KEY, poids DECIMAL  );")
    cur.execute("CREATE TABLE pauvrete(region INT PRIMARY KEY, taux DECIMAL  );")
    cur.execute("CREATE TABLE jeunesnoninseres(region INT, annee INT, part DECIMAL  , PRIMARY KEY(region,annee));")



def fill_regions(cur,conn):
    insert = "INSERT INTO regions (region, cheflieu, tncc, ncc, nccenr, libelle) VALUES (%s, %s, %s, %s, %s, %s);"
    for i in range(len(regions)):
        if i==0 :
            pass
        else:
            r = regions[i]
            values = (r[0], r[1],r[2],r[3],r[4],r[5])
            cur.execute(insert, values)
            conn.commit()
    print ("Regions ajoutées à la base de données, dans la relation 'regions'")

def fill_departements(cur,conn):
    insert = "INSERT INTO departements(departement, region, cheflieu, tncc, ncc, nccenr, libelle) VALUES (%s, %s,%s,%s,%s,%s,%s);"
    for i in range(len(departements)):
        if i==0 :
            pass
        elif i<10:
            d = departements[i]
            d[0]= "0"+d[0]
            values = (d[0],d[1],d[2],d[3],d[4],d[5],d[6])
            cur.execute(insert, values)
            conn.commit()
        else:
            d = departements[i]
            values = (d[0],d[1],d[2],d[3],d[4],d[5],d[6])
            cur.execute(insert, values)
            conn.commit()
    print ("Départements ajoutés à base de données, relation 'departements'")

def fill_energies(cur,conn,myData):
    insert = "INSERT INTO energies(departement, annee, eolien, photovoltaique, autre) VALUES (%s, %s,%s,%s,%s);"
    for index, row in myData.iterrows():
        values1 = (row['num_dep'], 2010, row['eolien_2010'], row['photo_2010'], row['autres_2010'])
        values2 =(row['num_dep'], 2015, row['eolien_2015'], row['photo_2015'], row['autres_2015'])
        cur.execute(insert,values1)
        cur.execute(insert,values2)
        conn.commit()



def fill_agbiologiques(cur,conn,myData):
    insert = "INSERT INTO agbiologique(departement, annee, part) VALUES (%s, %s,%s);"
    for index, row in myData.iterrows():
        values1 = (row['num_dep'], 2010, row['AB_2010'])
        values2 =(row['num_dep'], 2016, row['AB_2016'])
        cur.execute(insert,values1)
        cur.execute(insert,values2)
        conn.commit()

def fill_artificialisations(cur,conn,myData):
    insert = "INSERT INTO artificialisation(departement, annee, part) VALUES (%s, %s,%s);"
    for index, row in myData.iterrows():
        values1 = (row['num_dep'], 2012, row['surf_2012'])
        values2 =(row['num_dep'], 2006, row['surf_2006'])
        cur.execute(insert,values1)
        cur.execute(insert,values2)
        conn.commit()


def fill_valorisations(cur,conn,myData):
    insert = "INSERT INTO valorisation(departement, annee, taux ) VALUES (%s, %s,%s);"
    for index, row in myData.iterrows():
        values1 = (row['num_dep'], 2013, row['MO_2013'])
        values2 =(row['num_dep'], 2009, row['MO_2009'])
        cur.execute(insert,values1)
        cur.execute(insert,values2)
        conn.commit()

def fill_granulats(cur,conn,myData):
    insert = "INSERT INTO granulats(departement, annee, production ) VALUES (%s, %s,%s);"
    for index, row in myData.iterrows():
        values1 = (row['num_dep'], 2014, row['granul_2014'])
        values2 =(row['num_dep'], 2009, row['granul_2009'])
        cur.execute(insert,values1)
        cur.execute(insert,values2)
        conn.commit()

def fill_environnement(cur,conn):
    myData = env_data()
    fill_energies(cur,conn,myData)
    fill_agbiologiques(cur,conn,myData)
    fill_valorisations(cur,conn,myData)
    fill_artificialisations(cur,conn,myData)
    fill_granulats(cur,conn,myData)
    conn.commit()
    print ("Données environnementales ajoutées à la base de données")


def fill_zoneinondable(cur,conn,data):
    insert = "INSERT INTO zoneinondable(departement, annee, part ) VALUES (%s, %s,%s);"
    for index, row in data.iterrows():
            values1 = (row['num_dep'], 2013, row['inondable_2013'])
            values2 =(row['num_dep'], 2008, row['inondable_2008'])
            cur.execute(insert,values1)
            cur.execute(insert,values2)
            conn.commit()

def fill_esperancevie(cur,conn,data):
    insert = "INSERT INTO esperancevie(departement, annee, esperanceh,esperancef ) VALUES (%s, %s,%s,%s);"
    for index, row in data.iterrows():
            values1 = (row['num_dep'], 2010, row['evh_2010'], row['evf_2010'])
            values2 =(row['num_dep'], 2015, row['evh_2015'], row['evf_2015'])
            cur.execute(insert,values1)
            cur.execute(insert,values2)
            conn.commit()

def fill_eloignementservices(cur,conn,data):
    insert = "INSERT INTO eloignementservices(departement, part ) VALUES (%s, %s);"
    for index, row in data.iterrows():
        values = (row['num_dep'],row['eloigne'])
        cur.execute(insert, values)
        conn.commit()
    
def fill_jeunesnoninseres(cur,conn,data):
    insert = "INSERT INTO jeunesnoninseres(region, annee, part ) VALUES (%s, %s,%s);"
    for index, row in data.iterrows():
        values1 = (row['num_reg'], 2014, row['jeunes_2014'])
        values2 =(row['num_reg'], 2009, row['jeunes_2009'])
        cur.execute(insert,values1)
        cur.execute(insert,values2)
        conn.commit()

def fill_pauvrete(cur,conn,data):
    insert = "INSERT INTO pauvrete(region, taux ) VALUES (%s, %s);"
    for index, row in data.iterrows():
        values = (row['num_reg'],row['pauvrete'])
        cur.execute(insert, values)
        conn.commit()

def fill_economiesociale(cur,conn,data):
    insert = "INSERT INTO economiesociale(region, poids ) VALUES (%s, %s);"
    for index, row in data.iterrows():
        values = (row['num_reg'],row['economie'])
        cur.execute(insert, values)
        conn.commit()


def fill_social(cur,conn):
    myDataD = social_data_dep()
    myDataR = social_data_reg()
    fill_zoneinondable(cur,conn,myDataD)
    fill_esperancevie(cur,conn,myDataD)
    fill_eloignementservices(cur,conn,myDataD)
    fill_jeunesnoninseres(cur,conn,myDataR)
    fill_pauvrete(cur,conn,myDataR)
    fill_economiesociale(cur,conn,myDataR)
    print ("Données sociales ajoutées à la base de données")


def fill_database(regions, departements):  # Remplit la base de données 
    print('\n ------ \nTrying to connect to the database')
    try:
        #Connect to database
        conn = psycopg2.connect("host=dbserver dbname = madbarros user = madbarros")
    except Exception:
        print ("ERROR :Cannot connect to database\n ------ \n")
    print('Connected to the database\n ------ \n')
    cur = conn.cursor()
    create_tables(cur,conn)
    fill_regions(cur,conn)
    fill_departements(cur,conn)
    fill_environnement(cur,conn)
    fill_social(cur,conn)

    cur.close()
    conn.close()

    print ("Fin du remplissage de la base de données.\n ----------------------------\n")
   




departements =[]
regions = []
departements = charge_dep(departements)
regions = charge_reg(regions)
fill_database(regions,departements)