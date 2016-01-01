# -*- coding: utf-8 -*-
__author__ = 'lorenzo'

import mechanize
import re

class Fetcher:

    @staticmethod
    def fetchUpdates(schoolcode, user, password):
        try:
            updatesregex = '<td align="Left" width="600">.*<\/td>'
            dateregex = '<td align="Left" width="80">.*<\/td>'      #   regex user to get dates

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
