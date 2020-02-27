# Cross-site Scripting and SQL Injection










## Challenges


### Setup
The challenges for today will require a little bit of setup.  

1. Clone this repo and cd into the base directory.
2. Create a virtual environment

```bash
python -m venv venv
```

3. Activate your virtual environment

```bash
source venv/bin/activate
```

4. Install the necessary Python module(s)

```bash
pip install -r requirements.txt
```

Run the bash script:
```bash
./start.sh
```
It will populate the database, and start the server.

Go to localhost:2222/ and see what you can do.

### Challenge 1: Little Bobby Tables
Some people just want to watch the world burn.  Today you'll get to sample that delicious nihilism as you (relatively) easily break things that other people spent so much more time making.  

Don't get me wrong, hackers aren't all bleakness and evil--they also love a good laugh.  In the dark corners of the internet, where everyone types with a hoodie on, there's a well-known internet comic.

[Here is one of his comics](https://xkcd.com/327/)

Unfortunately, I'm not sure I get the joke.  What could it mean?  

Note: Your database might become corrupted as you work through this challenge.  If so, simply start fresh by deleting users_posts.db, and running the start script.  When you do figure it out, you'll definitely have to re-create the database.










Once you figure out how to break it, what would you do to prevent such attacks?
Change the source code so that your attack doesn't work anymore.