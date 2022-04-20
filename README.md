# Tunes Final Project 

## Creators
* Ashwini Aphale
* Humaira Ridi
* Phong Vu

Application can be found at: 
  
  Sprint 1:
  https://guarded-lowlands-27554.herokuapp.com/
  
  Sprint 2:
  https://tunes-music.herokuapp.com/

Kanban board can be found at: https://github.com/phongwashere/FinalProject-SoftwareEngineering/projects/1

## Description of Project

Tunes is a web application created for a fun way to explore new music. It contains features like a login/register page, 
a landing page, a recommmendations page, and a favorites page. This web application is served via the flask framework and deployed on Heroku. 

## Layout of Project

The contents of this web application include "static" and "templates" directories. The CSS components are found within the static directory. 
The templated directory now contains 6 HTML pages: login.html, register.html, favorites.html, recommendations.html, main.html, landing.html. 
In addition, the project directory includes app.py, spotifyapi.py, a Procfile, requirements.txt, a .env file, and a .gitignore file. The flask 
framework is running in app.py, and the API fetching is done in spotifyapi.py. In addition, we use flask SQLALCHEMY in order to connect to our Heroku Database. 

### Heroku
The application is deployed on Heroku. We created a heroku database in order to store information for the application. 

### Database 
We created 3 separate tables: a User table (for storing username information), a favorite songs table (for storing a song and the current user), and a 
favorite artists table (for storing an artist and the current user).

### SpotifyAPI.py

Within this file we had a few functions that helped shape the recommendations page. The user is prompted with an HTML form and asked to enter a song
title upon loading. After hitting submit the page should show 10 related artists the user might like 
based on the entered song. Each of these artists are hyperlinked to specific YouTube covers based on that artist. For example, 
clicking Taylor Swift will send you to YouTube covers of Taylor Swift. 

We contain functions such as search(), recommendedArtist(), categoryPlaylist(), and getTracks(). The search() function takes
a song title and returns an artist ID. We query the Spotipy API which gets information from Spotify. Using the client_id and client_server we 
are granted authentication to view Spotify information. recommendedArtist() takes in an artist ID and returns 10 related artists. 
categoryPlaylist() takes in a genre and returns the top playlist ID from that genre. getTracks() takes in a playlist ID 
and returns the 10 top tracks from that playlist. 

### Landing Page

As shown above, the landing page takes in the 2 functions: categoryPlaylist() and getTracks() to display the top
10 tracks from a genre the user might be interested in. The landing page is first shown to those who load the site
and after logging in to the web application, more features are available to the user. Each song is a hyperlink that redirects the user to a page with song information and a link to listen to YouTube covers of the song. 

### Favorites Page

The user might be interested in keeping a list of their favorite song or artist. The favorites page takes in the information stored in the Heroku DB
and allows the user to add and delete a favorite song/artist to the webpage. The functions that deal with this process are save_fav_song(), 
del_fav_song(), save_fav_artist(), del_fav_artist(), and favorites() within app.py. 

### Randomize Page

The user might be interested in finding a completely random song to listen to in a new genre! This page uses the Spotipy API and searches for a random song within a list of genres provided, returning the user a random song to listen to. 

## How to run locally?
#### Install general libraries(use pip or pip3)
1. pip install python-dotenv
2. pip install requests
3. pip install flask
5. pip install flask_bcrypt
6. pip install flask_wtf
7. pip install flask_sqlalchemy
8. pip install flask_login
9. pip install spotipy
#### PostgreSQL Setup
5. brew install postgresql (if on mac)
6. brew services start postgresql (if on mac)
7. psql -h localhost  # this is just to test out that postgresql is installed okay - type "\q" to quit
8. pip install psycopg2-binary
9. pip install Flask-SQLAlchemy==2.1
10. pip install flask-login
#### Heroku Setup
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)  # install Homebrew
brew tap heroku/brew && brew install heroku  # install Heroku CLI
#### Adding to the .env file
You would need to create a .env file within the project and add
* export db_url="name of your url" change the url to say postgresql!
* export secretKey="secret key"
* export client_id="client id obtained from Spotify"
* export client_secret="client secret key obtained from Spotify"
* export redirect_uri="redirect url" and whitelist this on Spotify dashboard 
#### How to make database
* git init, add + commit all changed files with git
* heroku login -i
* heroku create
* heroku addons:create heroku-postgresql:hobby-dev
* heroku config
#### How to run app
Type python or python3 app.py into your terminal once you are within the correct directory
