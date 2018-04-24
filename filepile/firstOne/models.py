from django.db import models
import mysql.connector
import os
from pathlib import Path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.http import FileResponse
from django.utils.encoding import smart_str

# Create your models here.


class ConnectDB:
    conn = None

    def __init__(self):
        self.conn = mysql.connector.connect(host='localhost', database='file_pile', user='root', password='')

    @classmethod
    def getDB(cls):
        if cls.conn is None:
            cls.conn =  mysql.connector.connect(host='localhost', database='file_pile', user='root', password='')
        return cls.conn



class ValidateUser:
    def __init__(self):
        a = 10

    def usernameExists(self,username):
        conn = ConnectDB.getDB()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USERS")
        rows = cursor.fetchall()
        for row in rows:
            # print(row)
            if row[1] == username:
                conn.close()
                return True

        return False

    def check(self, username, password):
        # print(username, password)
        conn = ConnectDB.getDB()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USERS")
        rows = cursor.fetchall()
        for row in rows:
            #print(row)
            if row[1] == username and row[3] == password:
                return int(row[0])

        return -1


class Register:
    def __init__(self):
        a=10



    def register(self, email, name, password):
        conn = ConnectDB.getDB()
        cursor = conn.cursor()

        v = ValidateUser()

        if v.usernameExists(email) == True:
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

        query = "INSERT INTO DIRECTORIES(DIRECTORYID,OWNER,PARENTID,ADDRESS, DIRECTORYNAME, ISSHARED)"\
                "VALUES(%s, %s, %s, %s, %s, %s);"
        args = (tmp1+1, tmp2 , -1, d, "ROOT", 0)

        cursor.execute(query, args)
        conn.commit()


class CloudStorageOperations:
    this = None
    user = -1
    currentFolder = -1
    def __init__(self):
        a = 10


    def setCurrentFolder(self):
        conn = ConnectDB.getDB()
        cursor = conn.cursor()
        cursor.execute("SELECT ROOT FROM USERS WHERE ID = "+str(self.user))
        rows = cursor.fetchall()
        self.currentFolder = int(rows[0][0])
        print("user = ", self.user)
        print("current folder = ", self.currentFolder)

    @classmethod
    def getInstance(cls, userID):

        if cls.this is None:
            cls.this = CloudStorageOperations()

        cls.user = userID
        cls.this.setCurrentFolder()
        return cls.this


    def uploadFile(self, request):
        if 'fileToUpload' not in request.FILES:
            return
        f = request.FILES['fileToUpload']

        conn = ConnectDB.getDB()
        cursor = conn.cursor()
        cursor.execute("SELECT ADDRESS FROM DIRECTORIES WHERE DIRECTORYID = " + str(self.currentFolder))
        rows = cursor.fetchall()

        address = rows[0][0]+'/'+f.name

        if os.path.exists(address):
            return

        with open(address, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        query = "INSERT INTO FILES (DIRECTORYID, FILENAME, ISSHARED) VALUES(%s, %s, %s)"
        args = (self.currentFolder, f.name, 0)

        cursor.execute(query, args)
        conn.commit()


    def downloadFile(self, filename):
        conn = ConnectDB.getDB()
        cursor = conn.cursor()
        cursor.execute("SELECT ADDRESS FROM DIRECTORIES WHERE DIRECTORYID = " + str(self.currentFolder))
        rows = cursor.fetchall()

        address = rows[0][0] + '/' + filename


        print("path ", address)
        response = FileResponse(open('manage.py'), 'rb')
        if os.path.exists(address):
            response = HttpResponse(content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
            response['X-Sendfile'] = smart_str(address)
        return response


    def viewFiles(self):
        conn = ConnectDB.getDB()
        cursor = conn.cursor()
        cursor.execute("SELECT* FROM FILES ")
        rows = cursor.fetchall()
        fileList = []
        for row in rows:
            if row[1] == self.currentFolder:
                fileList.append(row)
        return fileList


    def deleteFile(self, filename):
        conn = ConnectDB.getDB()
        cursor = conn.cursor()
        cursor.execute("SELECT ADDRESS FROM DIRECTORIES WHERE DIRECTORYID = " + str(self.currentFolder))
        rows = cursor.fetchall()

        address = rows[0][0] + '/' + filename
        query = 'DELETE FROM FILES '\
                'WHERE FILENAME = "' + filename + '" AND DIRECTORYID = ' + str(self.currentFolder)
        cursor.execute(query)
        conn.commit()
        if os.path.exists(address):
            os.remove(address)


