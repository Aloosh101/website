import sqlite3 as sql
con = sql.connect("./thistube.db")
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS Videos(id integer NOT NULL,Video text NOT NULL,photo text NOT NULL,nameVideo text NOT NULL,Description txet not NULL,IdTheUser integer NOT NULL)""")
cur.execute("""CREATE TABLE IF NOT EXISTS Users(id integer NOT NULL,email text NOT NULL,username text NOT NULL,password BLOB NOT NULL)""")
cur.execute("""CREATE TABLE IF NOT EXISTS devices(idUser integer NOT NULL,device text NOT NULL,ip_addr integer NOT NULL)""")
#cur.execute("""SELECT DISTINCT Video FROM Videos""")