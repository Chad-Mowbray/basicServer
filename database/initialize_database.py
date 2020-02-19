import requests
import random
import string
import sqlite3

db = sqlite3.connect("user_db.db")
cursor = db.cursor()
cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')

if cursor.fetchone()[0] == 1:
    print('already exists...')
    # db.close()
else:
    print('does not exist yet')
    cursor.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, email TEXT, password TEXT)")
    db.commit()
    # db.close()



    req = requests.get("https://jsonplaceholder.typicode.com/users")

    # password = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
    # print(password)

    # get id, username, email, (password)
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
        
        # print("*" * 40)
        # print(id, username, email, password)
        # db = sqlite3.connect("user_db.db")
        cursor = db.cursor()
        cursor.execute("INSERT INTO users(username, email, password)\nVALUES(?,?,?)", (username, email, password))

        print('added new user')
    db.commit()

