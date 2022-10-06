import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from threading import Thread
import pytz

class WorkerThread(Thread):
    def __init__(self, value=0):
        super(WorkerThread, self).__init__()
        self.value = value
    def run(self):
        while self.value < 1000:
            self.value += 1
            time.sleep(1)

class ProgressThread(Thread):
    def __init__(self, worker):
        super(ProgressThread, self).__init__()
        self.worker = worker
    def run(self):
        while True:
            if not self.worker.is_alive():
                print('Worker is done')
                return True
            print('Worker is at', self.worker.value)
            time.sleep(1)
countWorker = WorkerThread()            # Alive Counter declaration
progress = ProgressThread(countWorker)  # Alive Counter progress|

def timeArgNow():
    u = datetime.utcnow()
    u = u.replace(tzinfo=pytz.utc) #NOTE: it works only with a fixed utc offset
    return (u.astimezone(pytz.timezone("America/Argentina/Buenos_Aires")))


def precioDolar():
    print("Scrapping bna")
    scrapping_url = 'https://www.bna.com.ar/Cotizador/MonedasHistorico'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
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
        return ("Web Blocked by firewall")

def postApi(url_api, dollarPrice):
    r = requests.post(url_api, data={'price': dollarPrice})
    if (r.ok):
        print(r.ok)     # Debug
        print(r.json()) # Debug
        return True
    return False

def main(cotizationDidntChecked):
    countWorker.start()     # Alive Counter
    progress.start()        # Alive Counter

    now = timeArgNow()
    today = int(now.strftime("%d"))
    hourNow = int(now.strftime("%H"))

    if today == fechaCotizacion and hourNow >= horaCierreCotizacion and cotizationDidntChecked:
            dollarPrice = precioDolar()
            if type(dollarPrice) == float:
                cotizationDidntChecked = postApi(url_api, dollarPrice) #Prevent new request to server the same day
            elif dollarPrice == "Web Blocked by firewall": time.sleep(7200) 
    
    if today > fechaCotizacion: cotizationDidntChecked = True #Reinicio flag si paso fecha de cotizacion

    progress.join()# Alive Counter

url_api = 'https://hostwebandapps.pythonanywhere.com/cotizacion/Dollar/'
#url_api = 'http://127.0.0.1:8000/cotizacion/Dollar/'  # Local api
cotizationDidntChecked = True
fechaCotizacion = 25
horaCierreCotizacion = 16

while True:
    if __name__ == "__main__":
        main(cotizationDidntChecked)
