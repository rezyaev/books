# Project Overview

Hello and welcome! This project is a Flask web application hosted on Heroku, created using HTML, CSS, Bootstrap, Python, PostgreSQL and obviously Flask. You can [find it online](https://rezyayev-cs50w-project1.herokuapp.com/).

Overall, it is a service searching for information about books. When you access the website the first time, you will be asked to log in. You can create a new account and then search in a database with 5000 books. Book page consists of simple info about the book(title, author, publication year and ISBN number), user reviews and a rating from Goodreads.com, which I got using their API. Also, you can create get requests to /api/isbn, where ISBN is 10 or 13 digit number, and information about the book will be returned in JSON format.

## Files

application.py - is a place with all server-side code. It creates a Flask app, sets up the database and adds several routes to be served.

import.py is used to import all information from book.csv to online database.

templates/ and static/ contain all HTML and CSS part of the web app.

All database commands were written with SQLalchemy module for python and raw SQL command.

## How to use Book's API

It's pretty simple. You just make GET request to this address - <https://rezyayev-cs50w-project1.herokuapp.com/api/isbn,> and use needed ISBN number. Example:

~~~python
import requests

res = requests.get("https://rezyayev-cs50w-project1.herokuapp.com/api/1416949658")
return res.json()
~~~

This code will return:

~~~
{
  'title': 'The Dark Is Rising',
  'author': 'Susan Cooper',
  'year': '1973',
  'isbn': '1416949658',
  'review_count': 47614,
  'average_score': '4.07'
}
~~~
