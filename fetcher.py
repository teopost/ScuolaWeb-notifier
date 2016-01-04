# -*- coding: utf-8 -*-
__author__ = 'lorenzo'

import mechanize
import re
from lxml import html

class Fetcher:

    @staticmethod
    def fetchUpdates(schoolcode, user, password):
        try:
            updatesregex = '<td align="Left" width="600">.*<\/td>'
            #   regex usato per ottenere le date
            dateregex = '<td align="Left" width="80">.*<\/td>'

            url = "https://www.scuolawebromagna.it/scuolawebfamiglie/src/login.aspx?Scuola=" + schoolcode

            browser = mechanize.Browser()
            browser.open(url)
            browser.select_form(name="ctl06")

            browser.form["LoginControl1$txtCodUser"] = user
            browser.form["LoginControl1$txtPassword"] = password

            page = browser.submit()
            text = page.read()

            #   trova tutte le occorrenze nella pagina secondo la espressione regolare
            fetcheddata=[]
            updatedates=[]
            for d in re.findall(dateregex, text):
                tmp = d[29:]
                updatedates.append(tmp[:-5])

            index = 0
            for r in re.findall(updatesregex, text):
                temp = updatedates[index]
                temp+="\n"
                temp+=r[29:]
                fetcheddata.append(temp[:-5])
                index+=1
            return fetcheddata
        except mechanize.ControlNotFoundError:
            return []
    @staticmethod
    def fetchHomeworks(schoolcode, user, password):
        try:
            url = "https://www.scuolawebromagna.it/scuolawebfamiglie/src/login.aspx?Scuola=" + schoolcode
            urlhomeworkspage = "https://www.scuolawebromagna.it/scuolawebfamiglie/src/FMp05.aspx"

            #   effettua il login, apre la pagina urlhomeworkspage, visualizza i compiti
            browser = mechanize.Browser()
            browser.open(url)
            browser.select_form(name="ctl06")

            browser.form["LoginControl1$txtCodUser"] = user
            browser.form["LoginControl1$txtPassword"] = password
            browser.submit()

            #   effettuato il login, si sposta sulla pagina per visualizzare i compiti: come cliccare su: Studente->Visualizzazioni/Richieste
            browser.open(urlhomeworkspage)
            #   selezione il form principale in cui sono contenuti tutti i controlli
            browser.select_form(name="aspnetForm")
            #   va nel menu a tendina e sceglie Compiti assegnati
            browser.form["ctl00$ContentPlaceHolder1$lstArchivio"] = ["Compiti assegnati"]
            #   preme il pulsante Visualizza
            page = browser.submit(name="ctl00$ContentPlaceHolder1$btnVisualizza")
            #   scarica la pagina ottenuta
            text = page.read()




            #   costruisce albero rappresentante pagina html usando la pagina appena scaricata
            tree = html.fromstring(text)

            #   oggetto da ritornare
            fetchedhomeworks=[]
            #   indice usato nel ciclo; in for(int x=0;x<k;x++) equivalente a x. evita di usare la funzione python enumerate
            index = 0
            #   cicla tra le righe prime 6 della tabella dei compiti, saltando la prima
            for sel in tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_tblStud"]/tr')[1:6]:
                #   costruisce il messaggio, variando l'indice in td[] si seleziona una diversa colonna della tabella
                fetchedhomeworks.append(sel.xpath('td[5]/text()')[0])   # aggiunge la materia
                fetchedhomeworks[index]+="\n"
                fetchedhomeworks[index]+=sel.xpath('td[2]/text()')[0]   # aggiunge il corpo
                fetchedhomeworks[index]+="\nDa consegnare entro: "
                fetchedhomeworks[index]+=sel.xpath('td[3]/text()')[0]   # aggiunge la data di consegna
                index+=1
            return fetchedhomeworks

        except mechanize.ControlNotFoundError:
            return []