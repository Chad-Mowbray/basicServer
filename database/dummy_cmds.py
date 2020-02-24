import sqlite3


class Information:

    def __init__(self, db_name="database/users_posts.db"):
        self.db_name = db_name
        self.db = sqlite3.connect(db_name)
        self.cur = self.db.cursor()

    def create_user_add_post(self, user_input_obj):
        # usr = "'" + user_input_obj['username'] + "'"
        usr = user_input_obj['username']
        # try:
        self.cur.execute(f"""SELECT id FROM users WHERE username = {usr} """)  # username" "; UPDATE users SET password = 444 WHERE id = 1"
        userId = self.cur.fetchall()  
        # self.db.commit()
        print(userId)


if __name__ == "__main__":
    x = Information("users_posts.db")

    user_input_obj = {
            "username": "'Bret' UNION SELECT password FROM users--",   #  ' UNION SELECT password FROM users--
            "password": "fefsdf",
            "title": "a title",
            "post": "a post"
        }

    x.create_user_add_post(user_input_obj)


# select username from users where username = "bret" UNION SELECT password FROM users--