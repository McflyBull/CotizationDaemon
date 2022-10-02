import json
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def precioDolar():
    print("Scrapping bna")
    scrapping_url = 'https://www.bna.com.ar/Cotizador/MonedasHistorico'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    try:
        print("converting the site to text")
        html_text = requests.get(scrapping_url, headers=headers).text

        print("Creating html parser")
        soup = BeautifulSoup(html_text, 'html.parser')

        print("Im looking for your selector")
        el = soup.select_one(
            '#cotizacionesCercanas > table.table.table-bordered.cotizador > tbody > tr > td.dest')

        print("taking value with selector")
        cotizacionDolar = float(el.get_text(strip=True))
        
        print(cotizacionDolar)
        return (cotizacionDolar)
    except:
        return ("An exception occurred")

def debug(cont):
    if cont > 99999:
        cont = 1
    print("Running: "+str(cont))
    cont += 1
    time.sleep(1)
    return (cont)

url_api = 'https://hostwebandapps.pythonanywhere.com/cotizacion/Dollar/'
#url_api = 'http://127.0.0.1:8000/cotizacion/Dollar/'
cotizationDidntCheked = True

# Debug
cont = 0

while True:
    # Debug
    cont = debug(cont)

    now = datetime.now()
    dayNow = int(now.strftime("%d"))
    hourNow = int(now.strftime("%H"))

    fechaCobro = 2
    horaCierreCotizacion = 0

    if dayNow == fechaCobro and hourNow >= horaCierreCotizacion and cotizationDidntCheked:

        dollarPrice = precioDolar()
        if dollarPrice != 'An exception occurred':
            print(now)
            r = requests.post(url_api, data={'price': dollarPrice})
            # check status code for response received. Success code - 200. Print content of request
            print(r, r.json())
            # Si ya consulto, evito que se repita
            cotizationDidntCheked = False
        # Bloqueo 2hs por bloqueo de proxy
        else:
            time.sleep(7200)
    # Si ya paso la fecha de cotizacion, reinicio el flag
    elif dayNow > fechaCobro:
        cotizationDidntCheked = True
