from sqlalchemy import create_engine, text
import mysql.connector

db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="DLwjdghks139@",
        database="miniter"
)
user = { 'name' : 'junghwan', 'email':'123@gmail.com', 'profile':'hola', 'password':'teset12'}
cur = db.cursor()
sql = """insert into users(name,email,profile,hashed_password) values (%s, %s, %s, %s)"""
cur.execute(sql,(
                'junghwan',
                '123@gmail.com',
                'hola',
                'teset12'
        )   
)
