import mechanize
import re
from lxml import html


html_source=file("html_source.txt","r").read()
tree = html.fromstring(html_source)

# Fare l'inspect con chrome e selezionare la tabella
# Fare copy e copiare xpath (copiare la riga con <tbody)
# Togliere a mano il tbody dalla formula

html_data = '//*[@id="ctl00_ContentPlaceHolder1_grdDett_DXMainTable"]/tr'

index = 1
# parto a 1 perche' l'intestazione di della tabella non ha lo
# stesso numero di elementi
for sel in tree.xpath(html_data)[1:6]:
                      
    #   costruisce il messaggio, variando l'indice in td[] si seleziona una diversa colonna della tabella

    print "\nrow: " + str(index)
    print "..col 1: " + sel.xpath('td[1]/text()')[0]
    print "..col 2: " + sel.xpath('td[2]/text()')[0]

    index+=1
   
    



