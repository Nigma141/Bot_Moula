import sqlite3

def CreateBase(pth):
    con = sqlite3.connect(pth)
    cur=con.cursor()

    cur.execute('create TABLE joueur (idJoueur integer PRIMARY KEY,compte real,MontantPtfTot real,gain real)')

    cur.execute('create TABLE action (idYahoo text,nomAction text,PrixAct real,dateAction smalldatetime)')

    cur.execute('create TABLE portefeuille (idportefeuille IDENTITY(1, 1) PRIMARY KEY,idJoueur integer,Montantptf real,IDAction integer,VolumeAction integer)')

    cur.execute('create TABLE liveAction (idLive IDENTITY(1, 1) PRIMARY KEY,idAction text,valeur real,ouverture real,date smalldatetime)')

    cur.execute(
        'create TABLE Ope(idOpe IDENTITY(12485, 1) PRIMARY KEY,idJoueur integer,idAction integer,AchatVente integer,VolumeAction integer)')
    con.commit()
    con.close()
    return()

def AjoutJouer(Id_joueur,pth):
    con = sqlite3.connect(pth)
    cur = con.cursor()
    print('ajout du joueur a la bd')
    print(int(Id_joueur))
    cur.execute("insert into joueur values (?,?,?,?)",(int(Id_joueur),1000,0,0))
    con.commit()
    con.close()
    # creer un joueur avec un portefeuille de  1000€
    return()

def AcheterAction(Id_joueur,Id_Action,Volume):
    con = sqlite3.connect(pth)
    cur = con.cursor()

    cur.execute('SELECT PrixAct from action where Id_Action=iddelaction', {"iddelaction":Id_Action})
    prixAct = cur.fetchall()[0]
    cur.execute("select compte from joueur where idJoueur=:iddujoueur", {"iddujoueur": Id_joueur})
    Compte = cur.fetchall()[0]

    if prixAct>Compte:
        con.close()
        return ('T as pas les sous Voleur')
    else:
        cur.execute("select idportefeuille, from portefeuille WHERE (idJoueur=:iddujoueur) AND Id_Action=iddelaction ", {"iddujoueur": Id_joueur,"iddelaction":Id_Action})
        requete = cur.fetchall()[0]

        if len(requete)==0:
            cur.execute("insert into portefeuille (idJoueur,Montantptf,IDAction,VolumeAction) values (?,?,?,?)",(int(Id_joueur),prixAct*Volume,Id_Action,Volume))
        else:
            IDportefeuille=int(requete(0))
            NouVolume=requete(1)+int(Volume)
            cur.execute("UPDATE portefeuille SET VolumeAction=NvVolume  WHERE idportefeuille=idduptfl ",{"NvVolume": NouVolume,"idduptfl":int(IDportefeuille)})
        con.commit()
        con.close()
        return('L operation a bien été réalisée')

def VendreActiondef (Id_joueur,Id_Action,Volume):
    # change le volume du portefeuille en question
    return()

def StatusJoueur(pth,id_joueur):
    con = sqlite3.connect(pth)
    cur = con.cursor()
    cur.execute("select compte,MontantPtfTot from joueur where idJoueur=:iddujoueur", {"iddujoueur":id_joueur})
    result=cur.fetchall()[0]
    con.close()
    #retourne le portefeuiltotal
    # retourne le compte en banque
    return(result)

def LogJoueur():
    #retourne l ensemble des operations d un jouer
    return()

def HistoJoueur():
    # retourne le prix du portefeuille au cours du temps
    # retourne le volume de chaque action au cours du temps
    return ()

def Actualisation(pth,Val,Lab,date):
    con = sqlite3.connect(pth)
    cur = con.cursor()

    print('Actualisation')
    #for i in range(len(Val)):


    # creer la nouvelle valeur de l action
    # actualise la valeur des portefeuilles
    #
    con.close()
    return()

def tableauScore():
    # sur la dernière journée
    # retourne les gain des joueurs
    # retourne le compte+portefeuille
    return()

def initAction(pth,Label,name,Valeur,date):
    con = sqlite3.connect(pth)
    cur = con.cursor()

    for i in range(len(Label)):
        print(name[i])
        cur.execute("insert into action  values (?,?,?,?)", (Label[i], name[i], Valeur[i],date))
        cur.execute("insert into liveAction (idAction,valeur,ouverture,date) values (?,?,?,?)", (Label[i],  Valeur[i],Valeur[i], date))
    con.commit()
    con.close()
    return()
