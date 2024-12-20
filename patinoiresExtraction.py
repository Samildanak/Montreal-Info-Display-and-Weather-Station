import os
import requests
from bs4 import BeautifulSoup

def extractPage(url, pagepath='page'):
    session = requests.Session()
    #... whatever other requests config you need here
    response = session.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    path, _ = os.path.splitext(pagepath)
    site_conteneur = soup.find("div", id="site_conteneur")
    arrondissementTuples = []
    for arr in site_conteneur.find_all("h2"):
        arrondissementTuples.append((arr.get("id"), arr.text))
    return site_conteneur, arrondissementTuples
    
def getArrondissement(site_conteneur, arrondissement):
    patinoiresArrondissement = site_conteneur.find("h2", id= arrondissement)
    return patinoiresArrondissement.parent

def beautifyDict(patinoiresArrondissementHtml):
    patinoiresArrondissementDict = {}
    
    for pat in patinoiresArrondissementHtml.table:
        try:
            completeName = pat.td.text
            patinoiresArrondissementDict[completeName] = []
            for state in pat:
                if state.text == completeName:
                    continue
                patinoiresArrondissementDict[completeName].append(state.text)
        except:
            pass
    return patinoiresArrondissementDict

def extractInfo(patinoiresArrondissement):
    infoList = []
    for info in patinoiresArrondissement.find_all("span"):
        infoList.append(info.text)
    return infoList
    



url = 'https://montreal2.qc.ca/ski/conditions_patinoires_arr.php'
site, arrondissementTuples = extractPage(url)
patinoiresArrondissement = getArrondissement(site, 'vsp')
patinoiresDict = beautifyDict(patinoiresArrondissement)
extractInfo(patinoiresArrondissement)