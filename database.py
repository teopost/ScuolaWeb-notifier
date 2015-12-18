__author__ = 'lorenzo'
import sqlite3
class Database:

    databasepath = "users.db"

    #   DATABASE MANAGEMENT
    @staticmethod
    def addRecord(username_telegram, username_registro, password):
        #   open db connection
        conn = sqlite3.connect(Database.databasepath, detect_types=sqlite3.PARSE_COLNAMES)
        c = conn.cursor()
        #   put the values into the db
        values = "('%s', '%s', '%s')" % (username_telegram, username_registro, password)
        command = "INSERT into users(username_telegram, username_registro, pass) VALUES" + values
        print(command)
        c.execute("delete from users where username_telegram='%s'" % (username_telegram))   #   if the user already made an accout, overwrite
        c.execute(command)
        conn.commit()


    @staticmethod
    def checkField(key, field):
        #   open db connection
        conn = sqlite3.connect(Database.databasepath, detect_types=sqlite3.PARSE_COLNAMES)
        c = conn.cursor()

        command = "SELECT '%s' FROM users WHERE id='%s'" % (field, str(key))
        c.execute(command)
        if c.fetchone() == None:
            return False
        return True

    @staticmethod
    def updateField(key, field, value):
        #   open db connection
        conn = sqlite3.connect(Database.databasepath, detect_types=sqlite3.PARSE_COLNAMES)
        c = conn.cursor()

        command = "UPDATE users SET '%s'='%s' WHERE id='%s'" % (field, str(value), str(key))
        c.execute(command)
        conn.commit()

    @staticmethod
    def getField(key, field):
        #   open db connection
        conn = sqlite3.connect(Database.databasepath, detect_types=sqlite3.PARSE_COLNAMES)
        c = conn.cursor()

        command = "SELECT " + field + " FROM users WHERE chatid=" + str(key)
        c.execute(command)
        return Database.c.fetchone()[0]

    @staticmethod
    def deleteRecord(key):
        #   open db connection
        conn = sqlite3.connect(Database.databasepath, detect_types=sqlite3.PARSE_COLNAMES)
        c = conn.cursor()

        command = "DELETE FROM users WHERE chatid='%s';" % str(key)
        print(command)
        c.execute(command)
        conn.commit()