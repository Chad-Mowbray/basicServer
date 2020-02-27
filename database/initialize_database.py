import requests
import random
import string
import sqlite3


class Initialize_Database:

    def __init__(self, db_name="database/users_posts.db"):
        self.db_name = db_name
        self.db = sqlite3.connect(db_name)
        self.cur = self.db.cursor()

    def create_if_not_there(self):
        self.cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')

        if self.cur.fetchone()[0] == 1:
            print(f'{self.db_name} already exists...')
            return False
        else:
            print(f'{self.db_name} does not exist yet, creating it now...')
            self.cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, email TEXT, password TEXT)")
            self.db.commit()
            self.cur.execute("CREATE TABLE posts(id INTEGER PRIMARY KEY, userId INTEGER, title TEXT, body TEXT, FOREIGN KEY (userId) REFERENCES users (id))")
            self.db.commit()
            return True

    def populate_table(self, url, val_1, val_2, val_3, table_name):
        req = requests.get(url)
        data = req.json()

        for datum in data:
            db_insert_1 = '' 
            db_insert_2 = '' 
            db_insert_3 = '' 

            for k,v in datum.items():
                if k == val_1:
                    db_insert_1 = v
                if k == val_2 and table_name == "users":
                    db_insert_2 = v
                    db_insert_3 += ''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
                if k == val_2 and table_name == "posts":
                    db_insert_2 = v
                if k == val_3 and table_name == "posts":
                    db_insert_3 = v
              
            self.cur.execute(f"INSERT INTO {table_name}('{val_1}', '{val_2}', '{val_3}')\nVALUES(?,?,?)", (db_insert_1, db_insert_2, db_insert_3))
            print('added a new entry')

        self.db.commit()

    def close_db(self):
        self.db.close()
        print("*********database is available************")


class Modify_Database(Initialize_Database):

    def __init__(self, db_name="database/users_posts.db"):
        super().__init__(db_name)
        self.db = sqlite3.connect(db_name)
        self.cur = self.db.cursor()

    def request_posts(self, query):
        self.cur.execute("SELECT title, body, username FROM posts JOIN users WHERE userId = users.id;")
        rows = self.cur.fetchall()
 
        all_posts = ''
        for row in rows:
            all_posts += "<br><h2>Title: {}</h2> <p>Post: {} </p><small>by: {}</small><br><hr><br>".format(row[0], row[1], row[2])

        return all_posts

    def add_user(self, username, password, email="default@default.com"):
        try:
            self.cur.execute("INSERT INTO users(username, email, password)\nVALUES('{}','{}','{}')".format(username, email, password))
            self.db.commit()
        except:
            print("error in add_user")
  
    def just_add_post(self, userId, title, body):
        try: 
            self.cur.execute("INSERT INTO posts(userId, title, body)\nVALUES(?,?,?)", (userId, title, body))
            self.db.commit()
        except:
            print("error in just_add_post")
        
    def create_user_add_post(self, user_input_obj):
        usr = "'" + user_input_obj['username'] + "'"
        try:
            self.cur.executescript(f"""SELECT id FROM users WHERE username = {usr} """)  
            userId = self.cur.fetchone()   
            if not userId:
                self.add_user(user_input_obj["username"], user_input_obj["password"])
                self.cur.execute(f"SELECT id FROM users WHERE username = '{user_input_obj['username']}'")
                userId = self.cur.fetchone()
                self.just_add_post(userId[0], user_input_obj["title"], user_input_obj["post"])
            else:
                self.just_add_post(userId[0], user_input_obj["title"], user_input_obj["post"])
        except:
            print("error in create_user_add_post")


if __name__ == "__main__":

    users_table = ("https://jsonplaceholder.typicode.com/users", 'username', 'email', 'password', 'users')
    posts_table = ("https://jsonplaceholder.typicode.com/posts", 'userId', 'title', 'body', 'posts')
    
    new_db = Initialize_Database("users_posts.db")
    should_continue = new_db.create_if_not_there()
    if should_continue:
        new_db.populate_table(users_table[0], users_table[1], users_table[2], users_table[3], users_table[4])
        new_db.populate_table(posts_table[0], posts_table[1], posts_table[2], posts_table[3], posts_table[4])
    new_db.close_db()

    # x = Information()
    # res = x.request_posts("posts")
