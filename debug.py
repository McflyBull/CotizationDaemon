import requests
from bs4 import BeautifulSoup


def precioDolar():
    #the fix
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    #response = requests.get(url, headers=headers)
    
    try:
        print("Scrapping bna")
        vgm_url = 'https://www.bna.com.ar/Cotizador/MonedasHistorico'
        print("url for scrap created")
        html_text = requests.get(vgm_url, headers=headers).text
        print("creating html text")
        soup = BeautifulSoup(html_text, 'html.parser')
        print("converting with beatiful soup")
        el = soup.select_one(
            '#cotizacionesCercanas > table.table.table-bordered.cotizador > tbody > tr > td.dest')
        # Dejo solo dos decimales, deberia hacerlo de otra manera
        print("taking value with selector")
        cotizacionDolar = float(el.get_text(strip=True))
        print(cotizacionDolar)
        return (cotizacionDolar)
    except:
        return ("An exception occurred")




def get_new():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    webToScrap = 'https://www.bna.com.ar/Cotizador/MonedasHistorico/'
    asd = BeautifulSoup(requests.get(webToScrap, headers=headers).text, features="html.parser").select_one('#cotizacionesCercanas > table.table.table-bordered.cotizador > tbody > tr > td.dest')
    cotizacionDolar = float(asd.get_text(strip=True))
    
    print(cotizacionDolar)
    return cotizacionDolar

print(precioDolar())
print(get_new())