__author__ = 'lorenzo'
import fetcher
from telegram import Updater
import database


#   scuolaweb functions
def getnews():
    f = open("latest.bck","w")
    updates = fetcher.Fetcher.fetchUpdates()
    for u in updates:
        #print(u)
        f.write(u)
        f.write('\n')
    return updates
def compare():
    #   count lines in latest.bck
    count = 0
    y=[]
    with open("latest.bck","r") as f:
        for line in f:
            y.append(line)
            #print(line)
        x=getnews()
    if(len(x)> len(y) or x[0] != y[0][:-1]):
        return x[0] #   new updates
    else:
        return "Nessun nuovo voto."


#   telegram commands
def message(bot, update):
    print("message received from:" + str(update.message.chat_id))

def news(bot, update):
    print("news from:" + str(update.message.chat_id))
     #if(compare()):
     #    message = "Aggiunto un nuovo voto!"
     #   print(message)
    #else:
    #    message = "Nessun nuovo voto."
    bot.sendMessage(chat_id=update.message.chat_id, text=compare())
def help(bot, update):
    commandlist = """lista comandi:
/news
/help
    """
    bot.sendMessage(chat_id=update.message.chat_id, text=commandlist)
def unknown(bot, update):
    commandlist = """Il comando non esiste.
usa /help per mostrare la lista comandi.
"""
    bot.sendMessage(chat_id=update.message.chat_id, text=commandlist)
def info(bot, update):
    infotext="""ScuolaWeb Notifyer by:
Lorenzo Teodorani, l.teodorani@gmail.com
Progetto OpenSource su: www.github.com/teopost2/ScuolaWeb/
"""
    bot.sendMessage(chat_id=update.message.chat_id, text=infotext)
def register(bot, update):
    text = update.message["text"].split(" ") #  parse arguments using the space as separator
    if (len(text) == 3): # the command needs to have at least 2 arguments
        replymessage = '''Registazione effettuata con successo!
        '''
        #print(update.message["chat"]["username"])
        #print(text[1])#  register in db: telegram username, numero registro, password registro
        database.Database.addRecord(update.message["chat"]["username"], text[1], text[2])
        bot.sendMessage(chat_id=update.message.chat_id, text=replymessage)
    else:
        replymessage = '''Sintassi del comando errata.
/register <numero_registro> <password_registro>
'''
        bot.sendMessage(chat_id=update.message.chat_id, text=replymessage)

if __name__ == '__main__':
    updater = Updater(token='154791779:AAECjweY4rBcr2YxUP5Eksqa4rLAR0YlXkk')
    dispatcher = updater.dispatcher

    #   add telegram messages and commands handlers
    dispatcher.addTelegramMessageHandler(message)
    dispatcher.addTelegramCommandHandler('news', news)
    dispatcher.addTelegramCommandHandler('help', help)
    dispatcher.addUnknownTelegramCommandHandler(unknown)
    dispatcher.addTelegramCommandHandler('info', info)
    dispatcher.addTelegramCommandHandler('register', register)

    updater.start_polling()
