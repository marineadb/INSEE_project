# coding: utf-8
# ALVES DE BARROS MARINE - MAI 2020
# M1 BIOINFO BORDEAUX
# BDD - PROJET INSEE
# AFFICHAGE GRAPHIQUE


from tkinter import *
from tkinter.ttk import Notebook
import psycopg2

# ------------------------------------------------ #

'''
Fonction permettant l'affichage de la liste des régions
'''
def affiche_regions():
    # ------- CONNECT TO DATABASE ------- # 
    print('\n\n---------- \nTrying to connect to the database')
    try:
        conn = psycopg2.connect("host=dbserver dbname = madbarros user = madbarros")
    except Exception:
        print ("ERROR :Cannot connect to database \n ---------- ")
        
    print('Connected to the database \n ---------- ' )
    cur = conn.cursor()
    # ----- EXECUTE QUERY ----- #
    cur.execute("SELECT * FROM regions;")
    rows = cur.fetchall() 
   
    #New window
    regions=Toplevel()
    regions.title("Régions de France")
    regions.minsize(480,360)
    result_frame = Frame(regions, bg = '#494444')
    headings = ["Numero de région", "Chef-lieu", "Type de nom en clair (tncc)","Nom en clair majuscules(ncc)","	Nom en clair, typographie riche(nccenr)","Libellé"]
    rows.insert(0,headings)
    for i in range (len(rows)):
        for j in range (len(rows[i])):
            if i == 0:
                label = Label(result_frame, text = rows[i][j])
                label.config(font=("Arial",13, "bold"), bg = '#d2dbd7', fg = '#494444')
                label.grid(row=i, column=j, sticky="nsew", padx=1,pady=1)
                result_frame.grid_columnconfigure(j,weight=1)
            else :
                label = Label(result_frame, text = rows[i][j])
                label.config(font=("Arial",12), bg = '#d2dbd7', fg = '#494444')
                label.grid(row=i, column=j, sticky="nsew",padx=1,pady=1)
                result_frame.grid_columnconfigure(j,weight=1)
    result_frame.pack()
    

    conn.close()

    
'''
Fonction permettant l'affichage de la liste des départements
'''
def affiche_departements():

    # ------- CONNECT TO DATABASE ------- # 
    print('\n\n---------- \nTrying to connect to the database')
    try:
        conn = psycopg2.connect("host=dbserver dbname = madbarros user = madbarros")
    except Exception:
        print ("ERROR :Cannot connect to database \n ---------- ")
        
    print('Connected to the database \n ---------- ' )
    cur = conn.cursor()
    # ----- EXECUTE QUERY ----- #
    cur.execute("SELECT * FROM departements;")
    rows = cur.fetchall() 
   
    #New window
    deps=Toplevel()
    deps.title("Départements de France")
    deps.minsize(940,490)
    canvas = Canvas(deps)
    scroll_y = Scrollbar(deps, orient="vertical", command=canvas.yview)
    result_frame = Frame(canvas,bg = '#494444')
    headings = ["Numero de\ndépartement", "région", "Chef-lieu", "Type de nom en clair\n(tncc)","Nom en clair \nmajuscules(ncc)","	Nom en clair typographie\nriche(nccenr)","Libellé"]
    rows.insert(0,headings)
    for i in range (len(rows)):
        for j in range (len(rows[i])):
            if i == 0:
                label = Label(result_frame, text = rows[i][j])
                label.config(font=("Arial",13, "bold"), bg = '#d2dbd7', fg = '#494444')
                label.grid(row=i, column=j, sticky="nsew", padx=1,pady=1)
                result_frame.grid_columnconfigure(j,weight=1)
            else :
                label = Label(result_frame, text = rows[i][j])
                label.config(font=("Arial",12), bg = '#d2dbd7', fg = '#494444')
                label.grid(row=i, column=j, sticky="nsew",padx=1,pady=1)
                result_frame.grid_columnconfigure(j,weight=1)
   
    canvas.create_window(0, 0, anchor='nw', window=result_frame)
    canvas.update_idletasks()

    canvas.configure(scrollregion=canvas.bbox('all'), 
                    yscrollcommand=scroll_y.set)
                    
    canvas.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')

    conn.close()


'''
Fonction permettant l'affichage de la liste des régions
sous forme de boutons cliquables, chaque bouton entrainant 
l'appel de la fonction d'affichage
'''
def infos_region():

    # ------- CONNECT TO DATABASE ------- # 
    print('\n\n---------- \nTrying to connect to the database')
    try:
        conn = psycopg2.connect("host=dbserver dbname = madbarros user = madbarros")
    except Exception:
        print ("ERROR :Cannot connect to database \n ---------- ")
        
    print('Connected to the database \n ---------- ' )
    cur = conn.cursor()
    # ----- EXECUTE QUERY ----- #
    cur.execute("SELECT ncc FROM regions")
    rows = cur.fetchall() 
    choice_window = Toplevel()
    choice_window.title("Choix de la région")
    choice_window.config(bg='#d2dbd7')
    title = Label(choice_window, text="Choisissez la région", bg='#d2dbd7', font=("Helvetica",15,'bold'))
    title.pack()
    for region in rows:
        region_ = region[0]
        button = Button(choice_window, text=region_, font = ("Helvetica",15), fg = '#494444', command = lambda region_= region_:print_regions_infos(region_))
        button.pack()
    
    conn.close()


'''
Fonction permettant l'affichage des données d'une région,
précédemment sélectionnée (boutons cliquables)
'''

def print_regions_infos(region):
    # ------- CONNECT TO DATABASE ------- # 
    print('\n\n---------- \nTrying to connect to the database')
    try:
        conn = psycopg2.connect("host=dbserver dbname = madbarros user = madbarros")
    except Exception:
        print ("ERROR :Cannot connect to database \n ---------- ")
        
    print('Connected to the database \n ---------- ' )
    cur = conn.cursor()
    # ----- EXECUTE QUERY ----- #
    select = "SELECT poids,taux,annee,part FROM regions R JOIN economiesociale E ON R.region = E.region JOIN pauvrete P ON R.region = P.region JOIN jeunesnoninseres J ON R.region = J.region WHERE ncc = %s;"
    cur.execute(select,[region])
    rows = cur.fetchall() 
    response = ''
    response = response + " Poids de l'économie sociale dans les emplois salariés du territoire en 2015 : " +str(rows[0][0])+ "%.\n"
    response = response + "Taux de pauvreté en 2014 : " + str(rows[0][1]) +"%."
    response = response + " Taux de pauvreté en 2014 : " + str(rows[0][1]) + "%. \n"
    response = response + "Part des jeunes non insérés en " + str(rows[0][2]) + ": " + str(rows[0][3])+ "%.\n"
    response = response + " Part des jeunes non insérés en " + str(rows[1][2]) + ": " +str(rows[1][3])+ "%.\n\n"
    response = response + "Si une valeur apparait comme 'NaN', l'information est manquante"
    
    response_window = Toplevel()
    response_window.title("Informations sur la région " + region)
    response_window.config(bg='#d2dbd7')
    label = Label(response_window, text = response, bg='#d2dbd7' )
    label.pack()
    conn.close()

'''
Fonction permettant l'affichage de la liste des départements
sous forme de boutons cliquables, chaque bouton entrainant 
l'appel d'une fonction d'affichage.
'''

def dep_choice(donnees):
        # ------- CONNECT TO DATABASE ------- # 
    print('\n\n---------- \nTrying to connect to the database')
    try:
        conn = psycopg2.connect("host=dbserver dbname = madbarros user = madbarros")
    except Exception:
        print ("ERROR :Cannot connect to database \n ---------- ")
        
    print('Connected to the database \n ---------- ' )
    cur = conn.cursor()
    # ----- EXECUTE QUERY ----- #
    cur.execute("SELECT ncc FROM departements")
    rows = cur.fetchall() 
    choice_window = Toplevel()
    choice_window.title("Choix du département")
    choice_window.config(bg='#d2dbd7')
    title = Label(choice_window, text="Choisissez le departement", bg='#d2dbd7', font=("Helvetica",17,'bold'))
    title.pack()
    frame = Frame(choice_window,bg='#d2dbd7')
    frame.pack()
    count = 0
    row = 0
    
    column_length = len(rows)/3
    for departement in rows:
        nom_dep = departement[0]
        if donnees == 'env':
            button = Button(frame,text=nom_dep, font = ("Helvetica",15), fg = '#494444', command = lambda nom_dep=nom_dep:print_dep_env(nom_dep))
        else :
            button = Button(frame,text=nom_dep, font = ("Helvetica",15), fg = '#494444', command = lambda nom_dep=nom_dep:print_dep_soc(nom_dep))
        if count < column_length:
            button.grid(column=0, row = row)
        elif count < column_length*2:
            button.grid(column=1,row = row)
        else:
            button.grid(column=3,row = row)
        count = count +1
        row = row+1
        if row > column_length :
            row = 0
    
    conn.close()

'''
Fonction permettant l'affichage des données environnementales
pour un département sélectionné (boutons)
'''
def print_dep_env(dep):
    try:
    #Connect to database
        conn = psycopg2.connect("host=dbserver dbname = madbarros user = madbarros")
    except Exception:
        print ("ERROR :Cannot connect to database \n ---------- ")
    cur = conn.cursor()
    select_energie = "SELECT annee,eolien,photovoltaique,autre FROM departements D JOIN energies E ON D.departement = E.departement WHERE ncc = %s;" 
    select_granulats = "SELECT annee,production FROM departements D JOIN granulats G ON D.departement = G.departement WHERE ncc = %s;"
    select_AB = "SELECT annee, part FROM departements D JOIN agbiologique A ON D.departement = A.departement WHERE ncc = %s;"
    select_art = "SELECT annee, part FROM departements D JOIN artificialisation A ON D.departement = A.departement WHERE ncc = %s;"
    select_val = "SELECT annee, taux FROM departements D JOIN valorisation V ON D.departement = V.departement WHERE ncc = %s;"
    page = ''
    cur.execute(select_energie,[dep])
    rows = cur.fetchall()
    for row in rows:
        page = page + "Part des différents types d'énergie en " +str(row[0]) + ":"
        page = page +" \n- Eolien : " +str(row[1]) + "% \n- Photovoltaique : "+ str(row[2]) + "% \n- Autres : " + str(row[3])+ "%."
    cur.execute(select_granulats,[dep])
    rows=cur.fetchall()
    page = page + "\n\nProduction de granulats :"
    for row in rows :
        page = page +  "\n- En " + str(row[0])+ " : "+ str(row[1]) + " tonnes."
    cur.execute(select_AB,[dep])
    rows = cur.fetchall()
    page = page + "\n\nPart de l'agriculture biologique dans la surface agricole totale : "
    for row in rows:
        page = page+ "\n- En "+ str(row[0]) + " : "+ str(row[1])+ "%"
    cur.execute(select_art,[dep])
    rows = cur.fetchall()
    page = page + "\n\nPart de surfaces artificialisées : "   
    for row in rows:
        page = page+"\n- En "+ str(row[0]) + " : "+ str(row[1]) +"%"
    cur.execute(select_val,[dep])
    rows = cur.fetchall()
    page = page + "\n\nTaux de valorisation de la matière organique : " 
    for row in rows:
        page = page+ "\n- En " + str(row[0]) + " : " + str(row[1]) + "%"
    page = page + "\n\nSi une valeur apparait comme 'NaN', l'information est manquante."

    response_window = Toplevel()
    response_window.title("Informations sur le département " + dep)
    response_window.config(bg='#d2dbd7')
    label = Label(response_window, text = page, bg='#d2dbd7' )
    label.pack()
    conn.close()

'''
Fonction permettant l'affichage des données sociales
pour un département sélectionné (boutons)
'''
def print_dep_soc(dep_name):
    try:
    #Connect to database
        conn = psycopg2.connect("host=dbserver dbname = madbarros user = madbarros")
    except Exception:
        print ("ERROR :Cannot connect to database \n ---------- ")
    cur = conn.cursor()
    select_ev = "SELECT annee, esperanceh, esperancef FROM departements D JOIN esperancevie E ON D.departement = E.departement WHERE ncc = %s;"
    select_zi = "SELECT annee, part FROM departements D JOIN zoneinondable Z ON D.departement = Z.departement WHERE ncc = %s;"
    select_elserv = "SELECT part FROM departements D JOIN eloignementservices E ON D.departement = E.departement WHERE ncc = %s;"
    cur.execute(select_ev,[dep_name])
    rows = cur.fetchall()
    page = ''
    for dep in rows:
        page = page + "\nEspérance de vie à la naissance, en "+ str(dep[0])+ " : \n Hommes : "+ str(dep[1]) +" ans. \n Femmes : "+  str(dep[2])+ " ans. \n"
    cur.execute(select_zi,[dep_name])
    rows = cur.fetchall()
    page = page + "\nPart de la population estimée en zone inondable : \n"
    for dep in rows:
        page = page + "En " +  str(dep[0]) + ": " + str(dep[1])+ " %. \n"
    cur.execute(select_elserv,[dep_name])
    row = cur.fetchall()
    page = page + "\nPart de la population eloignée de plus de 7 minutes des services de santé de proximité en 2016: " + str(row[0][0]) +" %.\n"
    page = page + "\n\n Si une valeur apparait comme 'NaN', l'information est manquante "

    response_window = Toplevel()
    response_window.title("Informations sur le département " + dep_name)
    response_window.config(bg='#d2dbd7')
    label = Label(response_window, text = page, bg='#d2dbd7' )
    label.pack()
    conn.close()


'''
Fonction permettant la récupération des données d'une requête 
placée un paramètre, et retournant ces données. 
Permet d'éviter une duplication du code pour les 6 questions posées dans le sujet du projet.
'''
def query_execute(select):
    try:
        #Connect to database
        conn = psycopg2.connect("host=dbserver dbname = madbarros user = madbarros")
    except Exception:
        print ("ERROR :Cannot connect to database \n ---------- ")
    cur = conn.cursor()
    cur.execute(select)
    rows = cur.fetchall()
    conn.close()
    return rows


'''
Fonction permettant d'afficher les résultats de la question choisie
'''

def results(select,num_question):
    rows = query_execute(select)
    results_window = Toplevel()
    results_window.minsize(340,290)
    results_window.title("Resultats pour la question" + str(num_question))
    results_window.config(bg='#d2dbd7')
    canvas = Canvas(results_window,bg='#d2dbd7')
    scroll_y = Scrollbar(results_window, orient="vertical", command=canvas.yview)
    page = ''
    if num_question == 1 :
        page = "Les départements sont :\n" 
        for row in rows:
            page = page + str(row[0])+ " (region n°"+ str(row[1]) +") \n"
    elif num_question == 2 :
        for row in rows:
            page = page+str(row[0])+ " (Part d'énergie éolienne : "+str(row[1])+"%)\n"
    elif num_question == 3 :
        page = "La région est : " + str(rows[0][0]) + "(département : "+ str(rows[0][1])+ ")\n"
    elif num_question == 4 :
        page = "La part d'agriculture biologique est : " + str(rows[0][0]) + "(inconnue) \n"
    elif num_question == 5 :
        page = "Taux de pauvreté en 2014 : \n"
        page = page + "(les valeurs notées 'NaN' sont des valeurs inconnues)\n\n"
        for row in rows:
            page = page +" Region " + str(row[0]) + " : "+ str(row[1]) + "%.\n"
    elif num_question == 6 :
        page = "Poids de l'économie sociale : \n"
        page = page+"(les valeurs notées 'NaN' sont des valeurs inconnues)\n\n"
        for row in rows:
            page= page + " Region "+ str(row[0]) + " : " + str(row[1]) + "%. \n"
    
    label = Label(canvas, text = page, bg='#d2dbd7' )
    label.pack()
    canvas.create_window(0, 0, anchor='nw', window=label)
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'), 
                    yscrollcommand=scroll_y.set)              
    canvas.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')

'''
Fonction permettant à l'utilisateur de choisir un type d'énergie
'''

def energies():
    choice_window = Toplevel()
    choice_window.title("Choix du département")
    choice_window.config(bg='#d2dbd7')
    title = Label(choice_window, text="Choisissez le type d'énergie qui vous intéresse", bg='#d2dbd7', font=("Helvetica",17,'bold'))
    title.pack()
    B1 = Button(choice_window, text ="Energie éolienne",font=("Helvetica",18), fg ='#494444', command =lambda :aff_energies('eolien'))
    B2 = Button(choice_window, text ="Energie photovoltaique",font=("Helvetica",18), fg ='#494444', command =lambda :aff_energies('photovoltaique'))
    B3 = Button(choice_window, text ="Autres énergies",font=("Helvetica",18), fg ='#494444', command =lambda :aff_energies('autre'))
    B1.pack()
    B2.pack()
    B3.pack()


def aff_energies(energie):
    
    results_window = Toplevel()
    results_window.title("Informations sur le type " + energie)
    results_window.config(bg='#d2dbd7')
    results_window.minsize(450,290)
    canvas = Canvas(results_window,bg='#d2dbd7')
    scroll_y = Scrollbar(results_window, orient="vertical", command=canvas.yview)
    select_energie = ''
    if energie== "eolien":
        select_energie = "SELECT ncc FROM departements D JOIN (SELECT eolien, departement FROM energies WHERE annee = 2010) A ON D.departement = A.departement JOIN (SELECT eolien, departement FROM energies WHERE annee = 2015) B ON A.departement = B.departement WHERE A.eolien< B.eolien ORDER BY (B.eolien- A.eolien) desc;"
    elif energie== "photovoltaique":
        select_energie = "SELECT ncc FROM departements D JOIN (SELECT photovoltaique, departement FROM energies WHERE annee = 2010) A ON D.departement = A.departement JOIN (SELECT photovoltaique, departement FROM energies WHERE annee = 2015) B ON A.departement = B.departement WHERE A.photovoltaique< B.photovoltaique ORDER BY (B.photovoltaique- A.photovoltaique) desc;"
    elif energie == "autre":
        select_energie = "SELECT ncc FROM departements D JOIN (SELECT autre, departement FROM energies WHERE annee = 2010) A ON D.departement = A.departement JOIN (SELECT autre, departement FROM energies WHERE annee = 2015) B ON A.departement = B.departement WHERE A.autre< B.autre ORDER BY (B.autre - A.autre) desc;"
    try:
        #Connect to database
        conn = psycopg2.connect("host=dbserver dbname = madbarros user = madbarros")
    except Exception:
        print ("ERROR :Cannot connect to database \n ---------- ")
    cur = conn.cursor()
    cur.execute(select_energie)
    rows = cur.fetchall()
    page = "Departements ayant vu leur énergie augmenter\nentre 2010 et 2015 (ordre décroissant par rapport à l'augmentation):\n"
    for row in rows:
        page = page + str(row[0]) + "\n"
    conn.close()
    label = Label(canvas, text = page, bg='#d2dbd7' )
    label.pack()
    canvas.create_window(0, 0, anchor='nw', window=label)
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'),yscrollcommand=scroll_y.set)              
    canvas.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')


'''
Fonction permettant d'afficher les questions posées dans le sujet, 
et des boutons correspondant aux réponses de ces questions, permettant l'accès à la réponse
'''

def questions():
    S1 = "SELECT ncc, region FROM departements WHERE region IN( SELECT R.region FROM regions R JOIN departements D ON R.region = D.region JOIN granulats G ON D.departement = G.departement WHERE annee = 2014 and production != 'NaN' GROUP BY R.region HAVING SUM(production)>25000000) ORDER BY region;"
    S2 = "SELECT ncc, eolien FROM departements D JOIN energies E ON D.departement = E.departement WHERE annee = 2015 and eolien != 'NaN' ORDER BY eolien DESC LIMIT 5;"
    S3 = "SELECT R.ncc, D.ncc FROM regions R JOIN departements D ON D.region = R.region WHERE departement = (SELECT D.departement FROM departements D JOIN valorisation V ON D.departement = V.departement WHERE annee = 2013 and taux != 'NaN' ORDER BY taux ASC LIMIT 1);"
    S4 = "SELECT A.part, A.departement FROM agbiologique A JOIN eloignementservices E ON A.departement = E.departement WHERE annee= 2016 AND E.part!='NaN' ORDER BY (E.part) DESC LIMIT 1;"
    S5 = "SELECT ncc, P.taux FROM regions R JOIN pauvrete P ON P.region = R.region JOIN jeunesnoninseres J on R.region = J.region WHERE annee = 2014 AND J.part > 30;"
    S6 = "SELECT ncc, poids FROM economiesociale E JOIN regions R on E.region = R.region WHERE R.region IN (SELECT region from departements D JOIN energies E on D.departement = E.departement WHERE annee = 2015 AND photovoltaique != 'NaN' GROUP BY region HAVING AVG(photovoltaique)>10)AND R.region IN (SELECT region FROM departements D JOIN agbiologique A on A.departement = D.departement WHERE A.part !='NaN' AND A.annee = 2016 GROUP BY region HAVING AVG(A.part)>5);"
    list_ = "\nQUESTION 1 : Quels sont les départements dont la région a eu une production de granulats supérieure à 25 000 000 tonnes en 2014 ?\n"
    list_ = list_ + "QUESTION 2 : Quels sont les 5 départements avec le plus grand taux d’énergie éolienne comme source de la puissance électrique en 2015 ?\n"
    list_ = list_ + "QUESTION 3 : Dans quelle région se trouve le département ayant le plus faible taux de valorisation matière et organique en 2013 ?\n"
    list_ = list_ + "QUESTION 4 : En 2016, quelle est la part (en %) de l’agriculture biologique dans la surface agricole totale \ndu département contenant le plus grand pourcentage de population éloignée de plus de 7 minutes des services de santé de proximité ?\n"
    list_ = list_ + "QUESTION 5 : Quel est le taux de pauvreté en 2014 des régions dont la part des jeunes non insérés est supérieure à 30% en 2014 ?\n"
    list_ = list_ + "QUESTION 6 : En 2015, quelle était le poids de l'économie sociale dans les emplois salariés de la région dont la source de la puissance électrique \nen énergies renouvelables provenait à au moins 10% de l’énergie photovoltaïque et dont la part de l’agriculture biologique dans la surface agricole totale était d’au moins 5% ?"
    choice_window = Toplevel()
    choice_window.title("Choix de la question")
    choice_window.config(bg='#d2dbd7')
    upframe = Frame(choice_window,bg='#d2dbd7')
    questions_list =Label(upframe,bg='#d2dbd7', fg = '#494444' , text = list_)
    questions_list.pack()
    upframe.pack()
    B1 = Button(choice_window, text ="Réponse à la question 1",font=("Helvetica",18), fg ='#494444', command =lambda :results(S1,1))
    B2 = Button(choice_window, text ="Réponse à la question 2",font=("Helvetica",18), fg ='#494444', command =lambda :results(S2,2))
    B3 = Button(choice_window, text ="Réponse à la question 3",font=("Helvetica",18), fg ='#494444', command =lambda :results(S3,3))
    B4 = Button(choice_window, text ="Réponse à la question 4",font=("Helvetica",18), fg ='#494444', command =lambda :results(S4,4))
    B5 = Button(choice_window, text ="Réponse à la question 5",font=("Helvetica",18), fg ='#494444', command =lambda :results(S5,5))
    B6 = Button(choice_window, text ="Réponse à la question 6",font=("Helvetica",18), fg ='#494444', command =lambda :results(S6,6))
    B1.pack()
    B2.pack()
    B3.pack()
    B4.pack()
    B5.pack()
    B6.pack()


'''
----------------  AFFICHAGE GRAPHIQUE DE LA FENETRE D'ACCUEIL -------------------
'''

#Fenetre générale
root = Tk()
root.title ("Base de données de l'INSEE")
root.geometry("800x500")
root.minsize(480,360)
root.config(background = '#d2dbd7')

#Titre 
frame = Frame(root, bg = '#ededed', bd=3 , relief = SUNKEN)
frame2 = Frame(root, bg = '#d2dbd7')
label_title = Label(frame,text = "Bienvenue sur la base de données de L'INSEE", font=("Helvetica",30), bg ='#ededed', fg ='#494444')
label_title.pack()
label_subtitle = Label(frame,text = "Que voulez vous faire?", font=("Helvetica",20), bg ='#ededed', fg ='#494444')
label_subtitle.pack()

#Cretion des boutons
regions_button = Button(frame2, text="Afficher la liste des régions",font=("Helvetica",18), fg ='#494444', command = affiche_regions)
dep_button = Button(frame2, text="Afficher la liste des départements",font=("Helvetica",18),fg ='#494444', command = affiche_departements)
info_regions_button = Button(frame2, text="Afficher les données d'une région",font=("Helvetica",18),fg ='#494444', command = infos_region)
info_departements_button =Button(frame2, text="Afficher les données environnementales d'un département",font=("Helvetica",18),fg ='#494444', command = lambda :dep_choice('env'))
info_departements_button2 =Button(frame2, text="Afficher les données sociales d'un département",font=("Helvetica",18),fg ='#494444', command = lambda :dep_choice('soc'))
energies_button=Button(frame2, text="Afficher les données sur l'énergie",font=("Helvetica",18),fg ='#494444', command =energies)
questions_button = Button(frame2, text="Réponses aux questions",font=("Helvetica",18),fg ='#494444', command = questions)
regions_button.pack()
dep_button.pack()
info_regions_button.pack()
info_departements_button.pack()
info_departements_button2.pack()
energies_button.pack()
questions_button.pack()

frame.pack(expand = YES)
frame2.pack(expand = YES)


#Apparition constante de la fenetre
root.mainloop()