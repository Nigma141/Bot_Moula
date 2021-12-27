import datetime
import yfinance as yf
import db


## definition des liste d' actif
listeCac=["VIE.PA","SGO.PA","SU.PA","ORA.PA","DG.PA","ATO.PA","AIR.PA","OR.PA","ML.PA","HO.PA","CA.PA","AI.PA","ENGI.PA","EN.PA","AC.PA","MC.PA","KER.PA","BN.PA","CAP.PA","VIV.PA","SAN.PA","LR.PA","ACA.PA","BNP.PA","RI.PA","WLN.PA","GLE.PA","SW.PA"]
NomCac=['VEOLIA ENVIRON.', 'SAINT GOBAIN', 'SCHNEIDER ELECTRIC SE', 'ORANGE', 'VINCI', 'ATOS', 'AIRBUS SE', "L'OREAL", 'MICHELIN', 'THALES', 'CARREFOUR', 'AIR LIQUIDE', 'ENGIE', 'BOUYGUES', 'ACCOR', 'LVMH', 'KERING', 'DANONE', 'CAPGEMINI', 'VIVENDI SE', 'SANOFI', 'LEGRAND', 'CREDIT AGRICOLE', 'BNP PARIBAS ACT.A', 'PERNOD RICARD', 'WORLDLINE', 'SOCIETE GENERALE', 'SODEXO']
Devise=["EURUSD=X"]
NomDevise=["EUR/USD"]
listeDowJ=[]
NomDowJ=[]
listeCripto=["BTC-EUR","ETH-EUR",'BNB-EUR',"SOL1-EUR","USDT-EUR"]
NomCripto=["Bitcoin","Ethereum","Solana","Tether"]

ListeActif=listeCac+Devise+listeCripto
NomActif=NomCac+NomDevise+NomCripto

ListeListeActif=[[listeCac],[Devise],[listeCripto]]
NomListeListe=["Cac-40","Devise","Cripto"]


def init(liste,nom,pth):
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
        print(idx)
        req = yf.Ticker(idx)
        name += [req.info['shortName']]

    now = datetime.datetime.now()
    date=now.strftime("%d/%m/%Y %H:%M:%S")
    db.initAction(pth,Label,name,Valeur,date)
    return()

def Actu(liste,pth):
    Valeur=[]
    Label=[]
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=1)
    tomorrow = now + datetime.timedelta(days=1)
    dateYes = yesterday.strftime("%Y-%m-%d")
    dateTom = tomorrow.strftime("%Y-%m-%d")
    for elm in liste:
        print(elm)
        aapl = yf.Ticker(elm)
        aapl_historical = aapl.history(end=dateTom, start=dateYes, interval="1m")
        Valeur+=[aapl_historical.Close.values[-1]]
        Label+=[elm]
    #data = yf.download(tickers=liste,period='3d',intervals='1m',threads=True)
    #Valeur = data.Close.values[0]
    #Label = data.Close.columns

    name = []
    for idx in Label:
        name += [NomCac[listeCac.index(idx)]]
    #    print(idx)
    #    req = yf.Ticker(idx)
    #    name += [req.info['shortName']]

    now = datetime.datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")
    db.Actualisation(pth,Label,Valeur,date)
    return ()

