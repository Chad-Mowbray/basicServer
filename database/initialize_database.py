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
    print(f'{db_name} does not exist yet, creating it now...')
    cursor.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, email TEXT, password TEXT)")
    db.commit()
    cursor.execute("CREATE TABLE posts(id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT, body TEXT, FOREIGN KEY (user_id) REFERENCES users (id))")
    db.commit()

    # , FOREIGN KEY (user_id) REFERENCES users (id)

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


    req2 = requests.get("https://jsonplaceholder.typicode.com/posts")
    posts = req2.json()

    for post in posts:
        user_id = 0
        title = ''
        body = ''
        for k,v in post.items():
            if k == "userId":
                user_id = v
            if k == "title":
                title = v
            if k == "body":
                body = v
        
        cursor = db.cursor()
        cursor.execute("INSERT INTO posts(user_id, title, body)\nVALUES(?,?,?)", (user_id, title, body))

        print('added a new post')
    db.commit()

    db.close()
    print("*********database is populated************")

