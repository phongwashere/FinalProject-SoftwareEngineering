"""
functions for grabbing data from spotify
"""
import os
from dotenv import load_dotenv, find_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv(find_dotenv())


def search(title):
    """allows for us to search for an artist id"""
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=os.getenv("client_id"), client_secret=os.getenv("client_secret")
        )
    )
    try:
        query = sp.search(q=title, type="track")
        item = query["tracks"]["items"]
        if len(item) > 0:
            track = item[0]
            a = track["album"]["artists"]
            for dic in a:
                for key in dic:
                    if key == "id":
                        return dic[key]  # returns artist id
    except:
        return "invalid song"


def recommendedartist(id):
    """takes in an artist_id and prints 10 related artists"""
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=os.getenv("client_id"), client_secret=os.getenv("client_secret")
        )
    )
    query = sp.artist_related_artists(artist_id=id)
    item = query["artists"]
    artists = []
    if len(item) > 0:
        for dic in item:
            for i in dic:
                if i == "name":
                    artists.append(dic[i])
    return artists[0:10]  # returns list of 10 related artists


def categoryplaylist(genre):
    """takes a genre and returns the top playlist id for that genre"""
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=os.getenv("client_id"), client_secret=os.getenv("client_secret")
        )
    )
    query = sp.category_playlists(category_id=genre)
    item = query["playlists"]["items"]
    playlist = []
    if len(item) > 0:
        for dic in item:
            for i in dic:
                if i == "id":
                    playlist.append(dic[i])
    id = playlist[0]
    return str(id)  # returns the playlist id


def gettracks(playlist_id):
    """takes the playlist id and returns the top 10 songs within that playlist"""
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=os.getenv("client_id"), client_secret=os.getenv("client_secret")
        )
    )
    tracks = []
    try:
        query = sp.playlist_tracks(playlist_id=playlist_id)
        items = query["items"]
        for dic in items:
            for key in dic:
                if key == "track":
                    songnamedict = dic[key]["name"]
                    tracks.append(songnamedict)
        return tracks[0:10]
    except:
        return "invalid id"
