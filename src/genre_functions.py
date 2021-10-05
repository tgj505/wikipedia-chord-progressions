import spotipy as sp

def get_spotify_genres(x):
    result0 = sp.artist(x)

    try:
        artist_1_genre = result0['genres']
    except IndexError:
        artist_1_genre = ['Index Error None']

    return artist_1_genre


