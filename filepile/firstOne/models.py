from django.db import models
import mysql.connector
import os
from pathlib import Path

# Create your models here.


class ConnectDB:
    def __init__(self):
        self.conn = mysql.connector.connect(host='localhost', database='file_pile', user='root', password='')

    def DBVar(self):
        return self.conn


class ValidateUser:
    def __init__(self):
        a = 10

    def check(self, username, password):
        # print(username, password)
        conn = ConnectDB()
        conn = conn.DBVar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USERS")
        rows = cursor.fetchall()
        for row in rows:
            #print(row)
            if row[1] == username and row[3] == password:
                conn.close()
                return int(row[0])
        conn.close()
        return -1


class Register:
    def __init__(self):
        a=10

    def register(self, email, name, password):
        conn = ConnectDB()
        conn = conn.DBVar()
        cursor = conn.cursor()

        v = ValidateUser()

        if v.check(email, password) != -1:
            print(name, " registration unsuccesful")
            return

        cursor.execute("SELECT COUNT(*) FROM DIRECTORIES")
        rows = cursor.fetchall()
        tmp1 = 0
        if int(rows[0][0]) > 0:
            cursor.execute("SELECT MAX(DIRECTORYID) FROM DIRECTORIES")
            rows = cursor.fetchall()
            tmp1 = rows[0][0]




        tmp1 = int(tmp1)

        query = "INSERT INTO USERS(EMAIL,NAME,PASSWORD,ROOT) "\
                "VALUES(%s,%s,%s, %s);"
        args = (email, name, password, tmp1+1)
        cursor.execute(query, args)
        conn.commit()

        d = str(Path().resolve().parents[1])
        d += "/usdir/" + str(tmp1+1)
        print( "the directory address is ", d)

        os.makedirs(d)

        print(name, " registered successfully")

        cursor.execute("SELECT COUNT(*) FROM USERS")
        rows = cursor.fetchall()
        print("table size = ", rows[0][0])
        tableSize = rows[0][0]

        cursor.execute("SELECT ID FROM USERS")
        rows = cursor.fetchall()
        tmp2 = rows[tableSize-1][0]

        query = "INSERT INTO DIRECTORIES(DIRECTORYID,OWNER,PARENTID,Address)"\
                "VALUES(%s, %s, %s, %s);"
        args = (tmp1+1, tmp2 , -1, d)

        cursor.execute(query, args)
        conn.commit()

        conn.close()
