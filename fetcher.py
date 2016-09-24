# -*- coding: utf-8 -*-
__author__ = 'lorenzo'

'''
Errori di mechanize:

AmbiguityError
BrowserStateError
ContentTooShortError
ControlNotFoundError
FormNotFoundError
HTTPDefaultErrorHandler
HTTPError
HTTPErrorProcessor
ItemCountError
ItemNotFoundError
LinkNotFoundError
LoadError
LocateError
ParseError
RobotExclusionError
URLError
'''

import mechanize
import re
from lxml import html

class Fetcher:

    #   ottiene la pagina home, effettuato il login in html
    @staticmethod
    def login(schoolcode, user, password):

        #url = "https://www.scuolawebromagna.it/scuolawebfamiglie/src/login.aspx?Scuola=" + schoolcode
	url = "https://registro.itis-cesena.it/scuolawebfamiglie/src/login.aspx?Scuola=" + schoolcode
        browser = mechanize.Browser()
        browser.open(url)
        browser.select_form(name="ctl06")

        browser.form["LoginControl1$txtCodUser"] = user
        browser.form["LoginControl1$txtPassword"] = password

        page = browser.submit()
        text = page.read()
        return text

    #   ottiene la pagina Visualizza->studenti in html
    @staticmethod
    def students(schoolcode, user, password, droplistitem):

        #url = "https://www.scuolawebromagna.it/scuolawebfamiglie/src/login.aspx?Scuola=" + schoolcode
        url = "https://registro.itis-cesena.it/scuolawebfamiglie/src/login.aspx?Scuola=" + schoolcode
        urlhomeworkspage = "https://registro.itis-cesena.it/scuolawebfamiglie/src/FMp05.aspx"

        #   effettua il login, apre la pagina Studenti->Visualizza, visualizza i compiti
        browser = mechanize.Browser()
        browser.open(url)
        #   se il codice scuola è sbagliato, il form 'ctl06' non viene trovato e un errore viene lanciato
        browser.select_form(name="ctl06")
        browser.form["LoginControl1$txtCodUser"] = user
        browser.form["LoginControl1$txtPassword"] = password
        #   fai il submit, non controlla se il login vada a buon fine (e che quindi ritorni la pagina home del registro)
        browser.submit()

        #   effettuato il login, si sposta sulla pagina per visualizzare i compiti: come cliccare su: Studente->Visualizzazioni/Richieste
        browser.open(urlhomeworkspage)
        #   seleziona il form principale in cui sono contenuti tutti i controlli
        #   se il form 'aspenetForm' non esiste, il login è fallito, e broswer.open() ritorna una pagina diversa da quella aspettata quindi le credenziali sono errate
        browser.select_form(name="aspnetForm")
        #   va nel menu a tendina e sceglie Compiti assegnati
        #browser.form["ctl00$ContentPlaceHolder1$lstArchivio"] = [droplistitem]
        browser.form["ctl00$ContentPlaceHolder1$lstGruppo"] = [droplistitem]
        #   preme il pulsante Visualizza
        page = browser.submit(name="ctl00$ContentPlaceHolder1$btnVisualizza")
        #   scarica la pagina ottenuta
        text = page.read()
        return text

    @staticmethod
    def fetchHomeworks(schoolcode, user, password):

        #   scarica html
        page = Fetcher.students(schoolcode, user, password, "Compiti assegnati")

        #   costruisce albero rappresentante pagina html usando la pagina appena scaricata
        tree = html.fromstring(page)

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

    @staticmethod
    def fetchMarks(schoolcode, user, password):

        #   scarica html
        page = Fetcher.students(schoolcode, user, password, "Voti")

        #   costruisce albero rappresentante pagina html usando la pagina appena scaricata
        tree = html.fromstring(page)

        #   oggetto da ritornare
        fetchedmarks=[]
        #   indice usato nel ciclo; in for(int x=0;x<k;x++) equivalente a x. evita di usare la funzione python enumerate
        index = 0
        #   cicla tra le righe prime 6 della tabella dei compiti, saltando la prima
        for sel in tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_tblStud"]/tr')[1:6]:
            #   costruisce il messaggio, variando l'indice in td[] si seleziona una diversa colonna della tabella
            fetchedmarks.append("materia: "+sel.xpath('td[2]/text()')[0])   # aggiunge la materia
            fetchedmarks[index]+="\ndata: "
            fetchedmarks[index]+=sel.xpath('td[1]/text()')[0]   # aggiunge il corpo
            fetchedmarks[index]+="\ntipo: "
            fetchedmarks[index]+=sel.xpath('td[3]/text()')[0]
            fetchedmarks[index]+="\nvoto: "
            fetchedmarks[index]+=sel.xpath('td[4]/text()')[0]   # aggiunge il voto
            fetchedmarks[index]+="\npeso: "
            fetchedmarks[index]+=sel.xpath('td[5]/text()')[0]   # aggiunge il voto
            index+=1
        return fetchedmarks

    @staticmethod
    def fetchCommunications(schoolcode, user, password):
        #   scarica html
        page = Fetcher.students(schoolcode, user, password, "Comunicazioni")

        #   costruisce albero rappresentante pagina html usando la pagina appena scaricata
        tree = html.fromstring(page)

        #   oggetto da ritornare
        fetchedaCommunications=[]
        #   indice usato nel ciclo; in for(int x=0;x<k;x++) equivalente a x. evita di usare la funzione python enumerate
        index = 0
        #   cicla tra le righe prime 6 della tabella dei compiti, saltando la prima
        for sel in tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_tblStud"]/tr')[1:8]:
            #   costruisce il messaggio, variando l'indice in td[] si seleziona una diversa colonna della tabella
            fetchedaCommunications.append(sel.xpath('td[1]/text()')[0])
            fetchedaCommunications[index]+="\n"
            fetchedaCommunications[index]+=sel.xpath('td[2]/text()')[0]
            fetchedaCommunications[index]+="\ndata evento: "
            evtdata = sel.xpath('td[3]/text()')[0]
            if evtdata == "&nbsp":
                evtdata = "---"
            fetchedaCommunications[index]+=evtdata
            index+=1
        return fetchedaCommunications

    @staticmethod
    def fetchArguments(schoolcode, user, password):
        '''
        scarica la tabella degli argomenti svolti
        '''
        #   scarica html
        page = Fetcher.students(schoolcode, user, password, "Argomenti svolti")

        #   costruisce albero rappresentante pagina html usando la pagina appena scaricata
        tree = html.fromstring(page)

        #   oggetto da ritornare
        fetchedarguments=[]
        #   indice usato nel ciclo; in for(int x=0;x<k;x++) equivalente a x. evita di usare la funzione python enumerate
        index = 0
        #   cicla tra le righe prime 6 della tabella dei compiti, saltando la prima
        for sel in tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_tblStud"]/tr')[1:6]:
            #   costruisce il messaggio, variando l'indice in td[] si seleziona una diversa colonna della tabella
            fetchedarguments.append(sel.xpath('td[5]/text()')[0])   # aggiunge la materia
            fetchedarguments[index]+="\n"
            fetchedarguments[index]+=sel.xpath('td[2]/text()')[0]   # aggiunge il corpo del messaggio
            fetchedarguments[index]+="\nSvolto in data: "
            fetchedarguments[index]+=sel.xpath('td[1]/text()')[0]   # aggiunge la data di consegna
            index+=1
        return fetchedarguments
