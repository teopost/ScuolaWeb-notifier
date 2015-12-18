__author__ = 'lorenzo'

import mechanize
import re

class Fetcher:

    @staticmethod
    def fetchUpdates():

        regex = '<td align="Left" width="600">.*<\/td>'
        url = "https://www.scuolawebromagna.it/scuolawebfamiglie/src/login.aspx?Scuola=FOTF010008"
        user = "00692"
        password = "----"

        browser = mechanize.Browser()
        browser.open(url)
        browser.select_form(name="ctl06")

        browser.form["LoginControl1$txtCodUser"] = user
        browser.form["LoginControl1$txtPassword"] = password

        page = browser.submit()
        text = page.read()

        #trova tutte le occorrenze nella pagina secondo la espressione regolare
        toret=[]
        for r in re.findall(regex,text):
            temp = r[29:]
            toret.append(temp[:-5])
        return toret