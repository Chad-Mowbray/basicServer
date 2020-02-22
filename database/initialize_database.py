import requests
import random
import string
import sqlite3
import time


class Initial_Database:

    def __init__(self, db_name):
        self.db_name = db_name
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()
    
    
    def create_if_not_there(self):
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')

        if self.cursor.fetchone()[0] == 1:
            print(f'{self.db_name} already exists...')
            return False
        else:
            print(f'{self.db_name} does not exist yet, creating it now...')
            self.cursor.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, email TEXT, password TEXT)")
            self.db.commit()
            self.cursor.execute("CREATE TABLE posts(id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT, body TEXT, FOREIGN KEY (user_id) REFERENCES users (id))")
            self.db.commit()
            return True

    def populate_users_table(self):
        req = requests.get("https://jsonplaceholder.typicode.com/users") #url

        users = req.json()

        for user in users:
            password = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
            username = '' # val 1
            email = '' # val 2
            for k,v in user.items():
                if k == 'username':
                    username = v
                if k == 'email':
                    email = v
            
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO users(username, email, password)\nVALUES(?,?,?)", (username, email, password))

            print('added a new user')
        self.db.commit()


    def populate_posts_table(self):

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
            
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO posts(user_id, title, body)\nVALUES(?,?,?)", (user_id, title, body))

            print('added a new post')
        self.db.commit()

    def close_db(self):
        self.db.close()
        print("*********database is populated************")



class Information:

    # def __init__(self, db_name="users_posts.db"):
    #     self.db_name = db_name
    #     self.db = sqlite3.connect(db_name)
    #     self.cursor = self.db.cursor()

    def request_posts(self, query):
        
        conn = sqlite3.connect("database/users_posts.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM posts")
 
        rows = cur.fetchall()
 
        all_posts = ''
        for row in rows:
            all_posts += f"<h2>Title: {row[2]}</h2> <p>Post: {row[3]} </p><br/>"

        return all_posts



    def add_user(self, username, password, email="default@default.com"):
        conn = sqlite3.connect("database/users_posts.db")
        cursor = conn.cursor()
        # cur.execute(f"INSERT INTO users VALUES('{username}', '{email}', '{password}')")
        cursor.execute("INSERT INTO users(username, email, password)\nVALUES(?,?,?)", (username, email, password))
        conn.commit()
        cursor.close()
  


    def add_post_and_title(self, user_id, title, body):
        conn = sqlite3.connect("database/users_posts.db")
        cursor = conn.cursor()
        # cur.execute(f"INSERT INTO users VALUES('{username}', '{email}', '{password}')")
        cursor.execute("INSERT INTO posts(user_id, title, body)\nVALUES(?,?,?)", (user_id, title, body))
        conn.commit()
        cursor.close()


    def add_post(self, user_input_obj):
        conn = sqlite3.connect("database/users_posts.db")
        cur = conn.cursor()
        cur.execute(f"SELECT id FROM users WHERE username = '{user_input_obj['username']}'")

        user_id = cur.fetchone()
        if not user_id:
            conn.close()
            self.add_user(user_input_obj["username"], user_input_obj["password"])
            time.sleep(1)
            conn = sqlite3.connect("database/users_posts.db")
            cur = conn.cursor()
            cur.execute(f"SELECT id FROM users WHERE username = '{user_input_obj['username']}'")
            user_id = cur.fetchone()
            self.add_post_and_title(user_id[0], user_input_obj["title"], user_input_obj["post"])

        else:
            self.add_post_and_title(user_id[0], user_input_obj["title"], user_input_obj["post"])








if __name__ == "__main__":

    # users_table = ("https://jsonplaceholder.typicode.com/users", 'id', 'username', 'email' )
    # posts_table = ("https://jsonplaceholder.typicode.com/posts", 'userId', 'title', 'body')
    
    new_db = Initial_Database("users_posts.db")
    should_continue = new_db.create_if_not_there()
    if should_continue:
        new_db.populate_users_table()
        new_db.populate_posts_table()
    new_db.close_db()











# import requests
# import random
# import string
# import sqlite3


# class Initial_Database:

#     def __init__(self, db_name):
#         self.db_name = db_name
#         self.db = sqlite3.connect(db_name)
#         self.cursor = self.db.cursor()
    
    
#     def create_if_not_there(self):
#         self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')

#         if self.cursor.fetchone()[0] == 1:
#             print(f'{self.db_name} already exists...')
#         else:
#             print(f'{self.db_name} does not exist yet, creating it now...')
#             self.cursor.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, email TEXT, password TEXT)")
#             self.db.commit()
#             self.cursor.execute("CREATE TABLE posts(id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT, body TEXT, FOREIGN KEY (user_id) REFERENCES users (id))")
#             self.db.commit()


#     def populate_table(self, chunk):
#         print(len(chunk), type(chunk))
#         for chn in chunk:
#             print(chn)

#         url, val_id, val_1, val_2, table_name = chunk[0], chunk[1], chunk[2], chunk[3], chunk[4]

#         req = requests.get(url) 
#         users = req.json()
#         three = ''

#         for user in users:
            
#             for k,v in user.items():
#                 if k == val_1:
#                     one = v
#                 if k == val_2:
#                     two = v
#                 if table_name == 'users':
#                     password = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
#                     three == password
#                 else:
#                     if k == val_id:
#                         three = v


#             cursor = self.db.cursor()
#             if table_name == "users":
#                 cursor.execute(f"INSERT INTO {table_name}(username, email, password)\nVALUES(?,?,?)", (one, two, three))
#             else:
#                 cursor.execute(f"INSERT INTO {table_name}(user_id, title, body)\nVALUES(?,?,?)", (one, two, three))


#             print('added a new user')
#         self.db.commit()


#     def close_db(self):
#         self.db.close()
#         print("*********database is populated************")




# if __name__ == "__main__":

#     users_table = ("https://jsonplaceholder.typicode.com/users", 'id', 'username', 'email', 'users')
#     posts_table = ("https://jsonplaceholder.typicode.com/posts", 'userId', 'title', 'body', "posts")
    
#     new_db = Initial_Database("users_and_posts.db")
#     new_db.create_if_not_there()
#     new_db.populate_table(users_table)
#     new_db.populate_table(posts_table)
#     new_db.close_db()

