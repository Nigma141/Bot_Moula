import datetime
import yfinance as yf
import db


listeCac=["VIE.PA","SGO.PA","SU.PA","ORA.PA","DG.PA","ATO.PA","AIR.PA","OR.PA","ML.PA","HO.PA","CA.PA","AI.PA","ENGI.PA","EN.PA","AC.PA","MC.PA","KER.PA","BN.PA","CAP.PA","VIV.PA","SAN.PA","LR.PA","ACA.PA","BNP.PA","RI.PA","WLN.PA","GLE.PA","SW.PA"]
NomCac=['VEOLIA ENVIRON.', 'SAINT GOBAIN', 'SCHNEIDER ELECTRIC SE', 'ORANGE', 'VINCI', 'ATOS', 'AIRBUS SE', "L'OREAL", 'MICHELIN', 'THALES', 'CARREFOUR', 'AIR LIQUIDE', 'ENGIE', 'BOUYGUES', 'ACCOR', 'LVMH', 'KERING', 'DANONE', 'CAPGEMINI', 'VIVENDI SE', 'SANOFI', 'LEGRAND', 'CREDIT AGRICOLE', 'BNP PARIBAS ACT.A', 'PERNOD RICARD', 'WORLDLINE', 'SOCIETE GENERALE', 'SODEXO']
listeDowJ=[]
Cripto=[]

def init(liste,pth):
    data = yf.download(
        tickers=liste,
        period='5d',
        intervals='1m',
        threads=True)
    Valeur = data.Close.values[0]
    Label = data.Close.columns
    print(Valeur, Label)
    name=[]
    for idx in Label:
        name+=[NomCac[listeCac.index(idx)]]
    #    print(idx)
    #    req = yf.Ticker(idx)
    #    name += [req.info['shortName']]

    now = datetime.datetime.now()
    date=now.strftime("%d/%m/%Y %H:%M:%S")
    db.initAction(pth,Label,name,Valeur,date)
    return()

def Actu(liste,pth):
    data = yf.download(
        tickers=liste,
        period='1m',
        intervals='1m',
        threads=True)
    Valeur=data.Close.values[0]
    Label=data.Close.columns
    print(Valeur,Label)
    h=datetime.datetime
    date=str(h.year)+"-"+str(h.month)+"-"+str(h.day)+" "+str(h.hour)+":"+str(h.minute)+":"+str(h.second)
    bd.Actualisation(pth,Valeur,Label,date)


    return ()


def Historique(action,temps):
    # creer le graphe en fonction de l action et du temps
    return()

