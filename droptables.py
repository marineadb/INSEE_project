# coding: utf-8
# ALVES DE BARROS MARINE - MAI 2020
# M1 BIOINFO BORDEAUX
# BDD - PROJET INSEE
# SUPPRESSION DES TABLES

import psycopg2


'''
Fichier permettant la suppréssion de toutes les relations correspondant à ce projet.
'''

def drop_all_tables():
    print('\n ------ \nTrying to connect to the database')
    try:
        #Connect to database
        conn = psycopg2.connect("host=dbserver dbname = madbarros user = madbarros")
    except Exception:
        print ("ERROR :Cannot connect to database\n ------ \n")
    print('Connected to the database\n ------ \n')
    cur = conn.cursor()
    cur.execute("DROP TABLE departements;")
    cur.execute("DROP TABLE regions;")
    cur.execute("DROP TABLE energies;")
    cur.execute("DROP TABLE valorisation;")
    cur.execute("DROP TABLE artificialisation;")
    cur.execute("DROP TABLE agbiologique;")
    cur.execute("DROP TABLE granulats;")
    cur.execute("DROP TABLE zoneinondable;")
    cur.execute("DROP TABLE esperancevie;")
    cur.execute("DROP TABLE eloignementservices;")
    cur.execute("DROP TABLE pauvrete;")
    cur.execute("DROP TABLE jeunesnoninseres;")
    cur.execute("DROP TABLE economiesociale;")
    conn.commit()
    cur.close()
    conn.close()
    print ("TOUTES LES TABLES ONT ETE EFFACEES\n --------------- \n" )

drop_all_tables()