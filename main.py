#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'lorenzo'
import fetcher
from telegram import Updater
import database


"""
#   scuolaweb functions
def getnews(schoolcode, user, password):
    #   getnews() ha la funzione di scaricare gli aggiornamenti dal sito della scuola specificato come terzo primo.
    #   ogni novita viene poi scritta su disco in modo da poter effetuare il compare() in futuro e per mantensi aggiornati sulle modifiche.
    f = open("latest.bck","w")
    updates = fetcher.Fetcher.fetchUpdates(schoolcode, user, password)
    for u in updates:
        #print(u)
        f.write(u)
        f.write('\n')
    f.close()
    return updates
def compare(schoolcode, user, password):
    #   compare() compara la modifiche scaricate dall sito della scuola con quelle su disco
    #   per determinare se vi sono state delle modifiche (es: aggiunta di un nuovo voto).
    #   viene ritornata una stringa contenente l'ultimo voto aggiunto nel caso ce ne sia,
    #   altrimenti viene ritornata una stringa per avvertire che non ci sono voti nuovi.

    #   count lines in latest.bck
    count = 0
    y=[]
    with open("latest.bck","r") as f:
        for line in f:
            y.append(line)
            #print(line)
        f.close()
        x=getnews(schoolcode, user, password)
        print(x)
        if x:   # se x e una lista vuota, invia un messaggio di errore di autenticazione, altrimenti manda gli aggiornamenti.
            print(x[0])
            print(y)
            if(x[0] != y[0][:-1]):
                return x[0] #   new updates
            else:
                return "Nessun nuovo voto."
        else:
            return  "Errore durante l'autenticazione"
"""


#   telegram commands
def message(bot, update):
    #   message() fa da callback nel caso un messaggio (NON comando come: /help, /start...)
    #   viene inviato al bot
    print("message from:" + update.message["chat"]["username"])
def news(bot, update):
    #   news(), callback del comando /news.
    #   news() scarica gli aggiornamenti con genews(), fa il confronto con compare();
    #   infine un messaggio contenente gli aggiornamenti, viene inviato all'utente che ne ha fatto richiesta.
    try:
        user = database.Database.getField(update.message.from_user["id"], "username_registro")
        password = database.Database.getField(update.message.from_user["id"], "pass")
        schoolcode = database.Database.getField(update.message.from_user["id"], "school_code")
        bot.sendMessage(chat_id=update.message.chat_id, text="Stai per ricevere aggiornamenti sul tuo registro.")
        updateslist = fetcher.Fetcher.fetchUpdates(schoolcode, user, password)
        messagecontent = ""
        if updateslist:
            for u in updateslist:
                messagecontent+=u
                messagecontent+="\n\n"
            bot.sendMessage(chat_id=update.message.chat_id, text=messagecontent)
        else:
            messagecontent="Errore durante l'autenticazione, verificare le credenziali d'accesso e registrare un nuovo utente."
            bot.sendMessage(chat_id=update.message.chat_id, text=messagecontent)
    except Exception:
        bot.sendMessage(chat_id=update.message.chat_id, text="Creare un utente con /register, prima di poter richiedere notifiche sul registro.")
def help(bot, update):
    #   help(), callback per /help; risponde con un messaggio contenente la lista di comandi.
    #print("command /help from:" + update.message["chat"]["username"])
    commandlist = """lista comandi:
/news       ricevi aggiornamenti
/help       mostra lista comandi
/start      mostra guida del bot
/register   registra un utente
/info       informazioni sul bot
    """
    bot.sendMessage(chat_id=update.message.chat_id, text=commandlist)
def unknown(bot, update):
    #   callback per comando sconosciuto, um messaggio di errore viene inviato all'utente per avvisarlo
    #print("unkown command from:" + update.message["chat"]["username"])
    commandlist = """Il comando non esiste.
usa /help per mostrare la lista comandi.
"""
    bot.sendMessage(chat_id=update.message.chat_id, text=commandlist)
def info(bot, update):
    #   callback per /info.
    #   invia un mesasggio informativo sul progetto.
    #print("command /info from:" + update.message["chat"]["username"])
    infotext="""ScuolaWeb Notifyer by:
Lorenzo Teodorani, l.teodorani@gmail.com
Progetto OpenSource su: www.github.com/teopost2/ScuolaWeb-notifier/
"""
    bot.sendMessage(chat_id=update.message.chat_id, text=infotext)
def register(bot, update):
    #   register(), callback per /register.
    #   il comando register, registra un nuovo utente del db.
    #   per ogni utente viene salvata password e numero di accesso al sito del registro.
    #   questi dati sono ottenuti quando l'utente scrice il comando secondo la sintassi:
    #   /register <numero_registro> <password>
    #   nel caso la del comando non sia rispettata, viene inviato un messaggio di errore.


    #print("command /register from:" + '%s') % (str(update.message.from_user["id"]))
    text = update.message["text"].split(" ") #  parse arguments using the space as separator
    if (len(text) == 4):    # the command needs to have at least 2 arguments
        replymessage = '''Registazione effettuata con successo!
'''
        #  register in db: telegram username, numero registro, password registro
        database.Database.addRecord(text[1], update.message.from_user["id"] , text[2], text[3])

        bot.sendMessage(chat_id=update.message.chat_id, text=replymessage)
    else:
        replymessage = '''Sintassi del comando errata.
/register <codice_scuola> <utente> <password>
Nota: Il codice della scuola lo trovi nella pagina principale di https://www.scuolawebromagna.it.
Ad esempio, per l'ITT Pascal di Cesena il codice è: FOIC81600G.
'''
        bot.sendMessage(chat_id=update.message.chat_id, text=replymessage)
def start(bot, update):
    #   start(), callback per /start
    #   questo comando informa l'utente sull'utilizzo del bot,
    #   viene eseguito quando per la prima volta un utente avvia la chat con il bot.

    startbanner = '''ScuolaWeb Notifier ti permette di consultare i voti del registro elettronico di https://www.scuolawebromagna.it.
La prima volta devi registrare il tuo utente con il comando /register, specificando il codice della scuola, lo username e la password.
In seguito, con il comando /news potrai ricevere gli aggiornamenti dei voti pubblicati sul sito.

Attenzione: Il bot, per recuperare i dati, deve eseguire il login sul sito scuolawebromagna.
Ciò significa che l'utente e la password che registrerai saranno memorizzati sui nostri server.
Non è possibile fare diversamente perchè scuolawebromagna non dispone di servizi dedicati per la consultazione dei dati.
Ti suggeriamo di non usare password già usate per altri servizi (es. posta elettronica).
'''
    bot.sendMessage(chat_id=update.message.chat_id, text=startbanner)
def homeworks(bot, update):
    user = database.Database.getField(update.message.from_user["id"], "username_registro")
    password = database.Database.getField(update.message.from_user["id"], "pass")
    schoolcode = database.Database.getField(update.message.from_user["id"], "school_code")
    homeworkslist = fetcher.Fetcher.fetchHomeworks(schoolcode, user, password)
    messagecontent = ""
    if homeworkslist:
        for u in homeworkslist:
            messagecontent+=u
            messagecontent+="\n\n"
        bot.sendMessage(chat_id=update.message.chat_id, text=messagecontent)
    else:
        messagecontent="sono qui"
        bot.sendMessage(chat_id=update.message.chat_id, text=messagecontent)



if __name__ == '__main__':

    updater = Updater(token='154791779:AAHX0HPCe2lmdLRotxB7k2O1hC2J71bpjhs')
    dispatcher = updater.dispatcher

    #   add telegram messages and commands handlers
    dispatcher.addTelegramMessageHandler(message)
    dispatcher.addTelegramCommandHandler('news', news)
    dispatcher.addTelegramCommandHandler('help', help)
    dispatcher.addUnknownTelegramCommandHandler(unknown)
    dispatcher.addTelegramCommandHandler('info', info)
    dispatcher.addTelegramCommandHandler('register', register)
    dispatcher.addTelegramCommandHandler('start', start)
    dispatcher.addTelegramCommandHandler('homeworks', homeworks)

    updater.start_polling()
