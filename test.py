from sqlalchemy import create_engine, text

db = {
        'user' : 'root',
        'password' : 'test1234',
        'host' : 'localhost',
        'port' : 3306,
        'database' : 'miniter'
}

db_url = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}?charset=utf8"
db = create_engine(db_url, encoding = 'utf-8', max_overflow = 0)

params = {'name' : '이정환'}
rows = db.execute(text("SELECT * FROM users WHERE name = :name"),params).fetchall()

for row in rows:
    print(f"name : {row['name']}")
    print(f"email : {row['email']}")