__author__ = 'lorenzo'
import sqlite3
import time
import sys

class Database:

    databasepath = "users.db"

    #   DATABASE MANAGEMENT
    @staticmethod
    def addRecord(school_code, username_telegram, username_registro, password):
        #   open db connection
        conn = sqlite3.connect(Database.databasepath, detect_types=sqlite3.PARSE_COLNAMES)
        c = conn.cursor()
        #   put the values into the db
        values = "('%s', '%s', '%s', '%s')" % (school_code, username_telegram, username_registro, password)
        command = "INSERT into users(school_code, username_telegram, username_registro, pass) VALUES" + values
        #   write that to stdout so that nohup can save it into log file: nohup.out
        sys.stdout.write("added user: ")
        sys.stdout.write(str(school_code) + " ")
        sys.stdout.write(str(username_telegram) + " ")
        sys.stdout.write(str(username_registro))
        sys.stdout.write("\t")
        sys.stdout.write(time.strftime("%Y:%m:%d %H:%M:%S"))
        c.execute("delete from users where username_telegram='%s'" % (username_telegram))   #   if the user already made an accout, overwrite
        c.execute(command)
        conn.commit()
        conn.close()

    @staticmethod
    def checkField(key, field):
        #   open db connection
        conn = sqlite3.connect(Database.databasepath, detect_types=sqlite3.PARSE_COLNAMES)
        c = conn.cursor()

        command = "SELECT '%s' FROM users WHERE username_telegram='%s'" % (field, str(key))
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
        try:
        #   open db connection
            conn = sqlite3.connect(Database.databasepath, detect_types=sqlite3.PARSE_COLNAMES)
            c = conn.cursor()

            command = "SELECT " + field + " FROM users WHERE username_telegram=" + str(key)
            c.execute(command)
            toret = c.fetchone()[0]
            return toret
        except Exception:
            raise Exception

    @staticmethod
    def deleteRecord(key):
        #   open db connection
        conn = sqlite3.connect(Database.databasepath, detect_types=sqlite3.PARSE_COLNAMES)
        c = conn.cursor()

        command = "DELETE FROM users WHERE chatid='%s';" % str(key)
        print(command)
        c.execute(command)
        conn.commit()