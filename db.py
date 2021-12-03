import sqlite3

def CreateBase(pth):
    con = sqlite3.connect(pth)
    cur=con.cursor()

    cur.execute('create TABLE joueur (idJoueur integer PRIMARY KEY,compte real,MontantPtfTot real,gain real)')

    cur.execute('create TABLE action (idYahoo text,nomAction text,PrixAct real,dateAction smalldatetime)')

    cur.execute('create TABLE portefeuille (idportefeuille INTEGER PRIMARY KEY AUTOINCREMENT,idJoueur integer,Montantptf real,IDAction integer,VolumeAction integer)')

    cur.execute('create TABLE liveAction (idLive INTEGER PRIMARY KEY AUTOINCREMENT,idAction text,valeur real,ouverture real,date smalldatetime)')

    cur.execute(
        'create TABLE Ope(idOpe INTEGER PRIMARY KEY AUTOINCREMENT,idJoueur integer,idAction integer,AchatVente integer,VolumeAction integer)')
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

def StatusJoueur(pth,id_joueur):
    con = sqlite3.connect(pth)
    cur = con.cursor()
    cur.execute("select compte,MontantPtfTot from joueur where idJoueur=:iddujoueur", {"iddujoueur":id_joueur})
    result = cur.fetchall()[0]
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

def Actualisation(pth,Label,Valeur,date):
    con = sqlite3.connect(pth)
    cur = con.cursor()

    print('Actualisation')
    for i in range(len(Label)):
        cur.execute("insert into liveAction (idAction,valeur,ouverture,date) values (?,?,?,?)",
                (Label[i], Valeur[i], Valeur[i], date))
        cur.execute("UPDATE action SET PrixAct=:Val,dateAction=:date where idYahoo=:lab ",{"Val":Valeur[i],"date":date,"lab":Label[i]})
        cur.execute(
            "select VolumeAction from portefeuille WHERE IDAction=:iddelaction ",{"iddelaction":Label[i]})
        requete = cur.fetchall()
        if len(requete)>0:
            Volume = int(requete[0][0])
            NouVal=float(Valeur[i])*Volume
            cur.execute("UPDATE portefeuille set Montantptf=:NVal WHERE IDAction=:lab",{"NVal":NouVal,"lab":Label[i]})
    cur.execute("SELECT IdJoueur from joueur")
    requete = cur.fetchall()
    idJoueur=requete[0]
    for id in idJoueur:
        id=int(id)
        cur.execute("select Montantptf,VolumeAction from portefeuille where idJoueur=:ID", {"ID":id})
        listeptf=cur.fetchall()
        montantPTF= sum([listeptf[i][0]*listeptf[i][1] for i in range(len(listeptf))])
        cur.execute("UPDATE joueur set Montantptf=:NVal WHERE IdJ=:lab", {"NVal": NouVal, "lab": Label[i]})

    con.commit()
    con.close()
    return()

def tableauScore():
    # sur la dernière journée
    # retourne les gain des joueurs
    # retourne le compte+portefeuille
    return()



def ReturnPtf(pth,id_joueur):
    con = sqlite3.connect(pth)
    cur = con.cursor()

    cur.execute("select Montantptf,IDAction,VolumeAction FROM portefeuille WHERE idJoueur=:iddujoueur", {"iddujoueur":id_joueur})
    result = cur.fetchall()

    con.commit()
    con.close()
    return(result)

def AcheterAction(pth,Id_joueur,Id_Action,Volume):
    con = sqlite3.connect(pth)
    cur = con.cursor()
    print(Id_Action)
    cur.execute('SELECT PrixAct from action where idYahoo=:iddelaction', {"iddelaction":Id_Action})
    prixAct = cur.fetchall()[0][0]
    print(prixAct)
    print(Id_joueur)
    cur.execute("select compte from joueur where idJoueur=:iddujoueur", {"iddujoueur": Id_joueur})
    Compte = cur.fetchall()[0][0]
    print(Compte)
    if prixAct>Compte:
        con.close()
        print('echec')
        return ('T as pas les sous Voleur')
    else:
        cur.execute("select idportefeuille,VolumeAction from portefeuille WHERE (idJoueur=:iddujoueur) AND IDAction=:iddelaction ", {"iddujoueur": Id_joueur,"iddelaction":Id_Action})
        requete = cur.fetchall()

        if len(requete)==0:
            cur.execute("insert into portefeuille (idJoueur,Montantptf,IDAction,VolumeAction) values (?,?,?,?)",(int(Id_joueur),prixAct*Volume,Id_Action,Volume))
        else:
            print("la requete")
            print(requete)
            id=requete[0][0]
            print(id)
            IDportefeuille=int(id)
            NouVolume=requete[0][1]+int(Volume)
            cur.execute("UPDATE portefeuille SET VolumeAction=:NvVolume  WHERE idportefeuille=:idduptfl ",{"NvVolume": NouVolume,"idduptfl":int(IDportefeuille)})
        cur.execute("UPDATE joueur SET compte=:achat where idJoueur=:iddujoueur", {"achat":Compte-prixAct,"iddujoueur": Id_joueur})
        cur.execute("select MontantPtfTot from joueur where idJoueur=:iddujoueur", {"iddujoueur": Id_joueur})
        ComptePTF = cur.fetchall()[0][0]
        cur.execute("UPDATE joueur SET MontantPtfTot=:achatPTF where idJoueur=:iddujoueur",{"achatPTF":prixAct+ComptePTF, "iddujoueur": Id_joueur})

        con.commit()
        con.close()
        return('L operation a bien été réalisée')


def VenteAction(pth,Id_joueur,Id_Action,Volume):
    con = sqlite3.connect(pth)
    cur = con.cursor()
    print(Id_joueur,Id_Action,Volume)
    cur.execute(
        "select idportefeuille,VolumeAction,Montantptf from portefeuille WHERE (idJoueur=:iddujoueur) AND IDAction=:iddelaction ",
        {"iddujoueur": int(Id_joueur), "iddelaction": Id_Action})
    requete = cur.fetchall()
    print('db requette',requete)
    id = requete[0][0]
    IDportefeuille = int(id)
    AncVolume = int(requete[0][1])
    Montant=float(requete[0][2])
    if AncVolume-Volume<1:
        # tout est vendu
        # Suppression du portfeuille
        cur.execute('DELeTE FROM portefeuille WHERE idportefeuille=:idPTF ', {"idPTF": IDportefeuille})
        cur.execute("UPDATE joueur SET  ")
    else :
        NouVolume=AncVolume-Volume

        cur.execute("UPDATE portefeuille SET VolumeAction=:NvVolume  WHERE idportefeuille=:idduptfl ",
                    {"NvVolume": NouVolume, "idduptfl": int(IDportefeuille)})

    con.commit()
    con.close()
    return()
