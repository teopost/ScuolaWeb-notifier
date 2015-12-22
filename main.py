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
        bot.sendMessage(chat_id=update.message.chat_id, text="Stai per ricevere le ultime notizie sul tuo registro.")
        updateslist = fetcher.Fetcher.fetchUpdates(schoolcode, user, password)
        messagecontent = ""
        if updateslist:
            for u in updateslist:
                messagecontent+=u
                messagecontent+="\n\n"
            bot.sendMessage(chat_id=update.message.chat_id, text=messagecontent)
        else:
            messagecontent="Errore durante l'autenticazione."
            bot.sendMessage(chat_id=update.message.chat_id, text=messagecontent)
    except Exception:
        bot.sendMessage(chat_id=update.message.chat_id, text="Prima devi creare un utente")
def help(bot, update):
    #   help(), callback per /help; risponde con un messaggio contenente la lista di comandi.
    #print("command /help from:" + update.message["chat"]["username"])
    commandlist = """lista comandi:
/news
/help
/start
/register
/info
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
Progetto OpenSource su: www.github.com/teopost2/ScuolaWeb/
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
    print(text)
    if (len(text) == 4):    # the command needs to have at least 2 arguments
        replymessage = '''Registazione effettuata con successo!
'''
        #  register in db: telegram username, numero registro, password registro
        database.Database.addRecord(text[1], update.message.from_user["id"] , text[2], text[3])
        print(text)
        bot.sendMessage(chat_id=update.message.chat_id, text=replymessage)
    else:
        replymessage = '''Sintassi del comando errata.
/register <codice_scuola> <numero_registro> <password_registro>
'''
        bot.sendMessage(chat_id=update.message.chat_id, text=replymessage)
def start(bot, update):
    #   start(), callback per /start
    #   questo comando informa l'utente sull'utilizzo del bot,
    #   viene eseguito quando per la prima volta un utente avvia la chat con il bot.

    startbanner = '''Per cominciare, registrare un utente con il comando /register
Si consiglia di cambiare la password del registro elettronico con una non usata da nessuna altra parte.
Non mi prendo nessuna responsabilita per eventuale perdita di dati.
'''
    bot.sendMessage(chat_id=update.message.chat_id, text=startbanner)
if __name__ == '__main__':

    updater = Updater(token='TOKEN')
    dispatcher = updater.dispatcher

    #   add telegram messages and commands handlers
    dispatcher.addTelegramMessageHandler(message)
    dispatcher.addTelegramCommandHandler('news', news)
    dispatcher.addTelegramCommandHandler('help', help)
    dispatcher.addUnknownTelegramCommandHandler(unknown)
    dispatcher.addTelegramCommandHandler('info', info)
    dispatcher.addTelegramCommandHandler('register', register)
    dispatcher.addTelegramCommandHandler('start', start)

    updater.start_polling()
