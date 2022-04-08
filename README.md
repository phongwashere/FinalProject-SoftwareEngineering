# Tunes Final Project 

## Creators
* Ashwini Aphalee
* Humaira Ridi
* Phong Vu

Application can be found at: 

## Description of Project

Tunes is a web application created for a fun way to explore new music. It contains features like a login/register page, 
a landing page, a recommmendations page, a favorites page. This web application is served via the flask framework and deployed on Heroku. 

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
and after logging in to the web application, more features are available to the user. 

### Favorites Page

The user might be interested in keeping a list of their favorite song or artist. The favorites page takes in the information stored in the Heroku DB
and allows the user to add and delete a favorite song/artist to the webpage. The functions that deal with this process are save_fav_song(), 
del_fav_song(), save_fav_artist(), del_fav_artist(), and favorites() within app.py. 

## How to run locally?
