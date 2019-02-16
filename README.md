# Project Overview

Hello and welcome! This project is a Flask web application hosted on Heroku, created using html, css, Bootstrap, Python, PostreSQL and obviosly Flask. You can [find it online](https://rezyayev-cs50w-project1.herokuapp.com/).

Overall, it is a service for searching information about the books. When you access website first time, you will be asked to login. You can create new account and then search in a database with 5000 books. Book page consists of simple info about book(title, author, publication year and ISBN number), user reviews and a rating from Goodreads.com, which I got using their API. Also, you can create get requests to /api/isbn, where isbn is 10 or 13 digit number, and information about book will be returned in JSON format.

## Files

application.py - is a place with all server-side code. It creates Flask app, sets up database and adds several routes to be served.

import.py was used to import all information from book.csv to online database.

templates/ and static/ contain all html and css part of web app.

All database commands were written with SQLalchemy module for python and raw SQL command.

## How to use Book's API

It's pretty simple. You just make GET request to this address - <https://rezyayev-cs50w-project1.herokuapp.com/api/isbn,> and use needed isbn number. Example:

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
