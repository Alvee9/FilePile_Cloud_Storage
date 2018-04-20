from django.db import models
import mysql.connector

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

