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


def getSongArtist(song_title):
    """takes the song title and returns artist name"""
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=os.getenv("client_id"), client_secret=os.getenv("client_secret")
        )
    )
    query = sp.search(q=song_title, type="track")
    item = query["tracks"]["items"]
    if len(item) > 0:
        track = item[0]
        a = track["album"]["artists"]
        for dic in a:
            for key in dic:
                if key == "name":
                    return dic[key]  # returns artist name


def getSongName(song_title):
    """takes the song title and returns song name"""
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=os.getenv("client_id"), client_secret=os.getenv("client_secret")
        )
    )
    query = sp.search(q=song_title, type="track")
    song_name = query["tracks"]["items"][0]["name"]
    return song_name  # returns song name


def getSongCover(song_title):
    """takes the song title and returns album cover"""
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=os.getenv("client_id"), client_secret=os.getenv("client_secret")
        )
    )
    query = sp.search(q=song_title, type="track")
    item = query["tracks"]["items"]
    if len(item) > 0:
        track = item[0]
        a = track["album"]["images"]
        for dic in a:
            for key in dic:
                if key == "url":
                    return dic[key]  # returns artist name


def getAlbum(song_title):
    """takes the song title and returns album name"""
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=os.getenv("client_id"), client_secret=os.getenv("client_secret")
        )
    )
    query = sp.search(q=song_title, type="track")
    item = query["tracks"]["items"]
    if len(item) > 0:
        track = item[0]
        album_name = track["album"]["name"]
        return album_name


def getReleaseDate(song_title):
    """takes the song title and returns release date"""
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=os.getenv("client_id"), client_secret=os.getenv("client_secret")
        )
    )
    query = sp.search(q=song_title, type="track")
    item = query["tracks"]["items"]
    if len(item) > 0:
        track = item[0]
        release_date = track["album"]["release_date"]
        return release_date


# {
#   "tracks": {
#     "href": "https://api.spotify.com/v1/search?query=as+it+was&type=track&locale=en-US%2Cen%3Bq%3D0.9&offset=0&limit=20",
#     "items": [
#       {
#         "album": {
#           "album_type": "single",
#           "artists": [
#             {
#               "external_urls": {
#                 "spotify": "https://open.spotify.com/artist/6KImCVD70vtIoJWnq6nGn3"
#               },
#               "href": "https://api.spotify.com/v1/artists/6KImCVD70vtIoJWnq6nGn3",
#               "id": "6KImCVD70vtIoJWnq6nGn3",
#               "name": "Harry Styles",
#               "type": "artist",
#               "uri": "spotify:artist:6KImCVD70vtIoJWnq6nGn3"
#             }
#           ],
#           "available_markets": [
#             "AD",
#             "AE",
#             "AG",
#             "AL",
#             "AM",
#             "AO",
#             "AR",
#             "AT",
#             "ZM",
#             "ZW"
#           ],
#           "external_urls": {
#             "spotify": "https://open.spotify.com/album/2pqdSWeJVsXAhHFuVLzuA8"
#           },
#           "href": "https://api.spotify.com/v1/albums/2pqdSWeJVsXAhHFuVLzuA8",
#           "id": "2pqdSWeJVsXAhHFuVLzuA8",
#           "images": [
#             {
#               "height": 640,
#               "url": "https://i.scdn.co/image/ab67616d0000b273b46f74097655d7f353caab14",
#               "width": 640
#             },
#             {
#               "height": 300,
#               "url": "https://i.scdn.co/image/ab67616d00001e02b46f74097655d7f353caab14",
#               "width": 300
#             },
#             {
#               "height": 64,
#               "url": "https://i.scdn.co/image/ab67616d00004851b46f74097655d7f353caab14",
#               "width": 64
#             }
#           ],
#           "name": "As It Was",
#           "release_date": "2022-03-31",
#           "release_date_precision": "day",
#           "total_tracks": 1,
#           "type": "album",
#           "uri": "spotify:album:2pqdSWeJVsXAhHFuVLzuA8"
#         },
#         "artists": [
#           {
#             "external_urls": {
#               "spotify": "https://open.spotify.com/artist/6KImCVD70vtIoJWnq6nGn3"
#             },
#             "href": "https://api.spotify.com/v1/artists/6KImCVD70vtIoJWnq6nGn3",
#             "id": "6KImCVD70vtIoJWnq6nGn3",
#             "name": "Harry Styles",
#             "type": "artist",
#             "uri": "spotify:artist:6KImCVD70vtIoJWnq6nGn3"
#           }
#         ],
#         "available_markets": [
#           "AD",
#           "ZA",
#           "ZM",
#           "ZW"
#         ],
#         "disc_number": 1,
#         "duration_ms": 167303,
#         "explicit": false,
#         "external_ids": {
#           "isrc": "USSM12200612"
#         },
#         "external_urls": {
#           "spotify": "https://open.spotify.com/track/4LRPiXqCikLlN15c3yImP7"
#         },
#         "href": "https://api.spotify.com/v1/tracks/4LRPiXqCikLlN15c3yImP7",
#         "id": "4LRPiXqCikLlN15c3yImP7",
#         "is_local": false,
#         "name": "As It Was",
#         "popularity": 100,
#         "preview_url": "https://p.scdn.co/mp3-preview/e9216304e6456a9015ac2054692fd4f0135d8aa9?cid=774b29d4f13844c495f206cafdad9c86",
#         "track_number": 1,
#         "type": "track",
#         "uri": "spotify:track:4LRPiXqCikLlN15c3yImP7"
#       },
