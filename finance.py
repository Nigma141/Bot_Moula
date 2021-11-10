import yfinance as yf

listePays=["^FCHI","^STOXX50E","^DJI","DAX","^FTSE","000001.SS","NIY=F"]
listeEntreprise=["SAF.PA","MSFT","AAPL","TSLA","BA","AIR.PA","HO.PA","EADSY","CAP.PA","ATE.PA","ENR.DE","GOOG","STLA.PA","DSY.PA","TTE"]

class action:
    def __init__(self,nom,ouverture,fermeture,avg200,avg50d,devise):
        self.name = nom
        self.ouverture = ouverture
        self.fermeture=fermeture
        self.avg200=avg200
        self.avg50d=avg50d
        self.devise=devise

    def MAJ(self,nom,ouverture,fermeture,avg200,avg50d,devise):
        self.name = nom
        self.ouverture = ouverture
        self.fermeture=fermeture
        self.avg200=avg200
        self.avg50d=avg50d
        self.devise=devise
        return(self)

listeAction=[]
# get stock info


listeActionEntre=[]
listeActionPays=[]
for index in listePays:
    req=yf.Ticker(index)
    print(req.info['shortName'])
    listeActionPays += [action(req.info['shortName'],req.info['open'],req.info['previousClose'],req.info['twoHundredDayAverage'],req.info['fiftyDayAverage'],req.info['currency'])]

for index in listeEntreprise:
    req=yf.Ticker(index)
    print(req.info['shortName'])
    listeActionPays += [action(req.info['shortName'],req.info['open'],req.info['previousClose'],req.info['twoHundredDayAverage'],req.info['fiftyDayAverage'],req.info['currency'])]
