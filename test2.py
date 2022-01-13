from sqlalchemy.engine import create_engine



from sqlalchemy import create_engine, text
from sqlalchemy.sql import text
import mysql.connector

db = {
        'user' : 'junghwan',
        'password' : '1234',
        'host' : 'localhost',
        'port' : 3306,
        'database' : 'miniter'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
db = create_engine(DB_URL, encoding = 'utf-8', max_overflow = 0)


sql = """insert into users(name,email,profile,hashed_password) values (%s, %s, %s, %s)"""
db.execute(sql,(
                'junghwan',
                '123gmail.com',
                'hola',
                'teset12'
        )   
)

