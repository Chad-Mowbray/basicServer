import requests
import random
import string
import sqlite3

db_name = "users.db"
db = sqlite3.connect(db_name)
cursor = db.cursor()
cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')

if cursor.fetchone()[0] == 1:
    print(f'{db_name} already exists...')
else:
    print(f'{db_name}does not exist yet, creating it now...')
    cursor.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, email TEXT, password TEXT)")
    db.commit()

    req = requests.get("https://jsonplaceholder.typicode.com/users")

    users = req.json()

    for user in users:
        password = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
        id = 0
        username = ''
        email = ''
        for k,v in user.items():
            if k == 'id':
                id = v
            if k == 'username':
                username = v
            if k == 'email':
                email = v
        
        cursor = db.cursor()
        cursor.execute("INSERT INTO users(username, email, password)\nVALUES(?,?,?)", (username, email, password))

        print('added a new user')
    db.commit()
    db.close()
    print("*********database is populated************")

