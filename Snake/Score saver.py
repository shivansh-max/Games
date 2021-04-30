import mysql.connector as mc
import pygame

mydb = mc.connect(host="localhost", user="root", passwd="Qwaszx@123", database="snake",
                  auth_plugin='mysql_native_password')

m = mydb.cursor()

score = 0

# m.execute("CREATE TABLE scores (name VARCHAR(1000), year int not null, score int not null);")

