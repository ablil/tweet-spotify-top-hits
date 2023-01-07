#!/usr/bin/env python3

from typing import List, Dict

import redis
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from config import config


class Spotify:
    playlist_id = '37i9dQZF1DXcBWIGoYBM5M'  # Today's top hit playlist id

    def __init__(self, client_id, client_secret):
        self.api = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                                         client_secret=client_secret))

    def fetch_today_top_hits(self) -> List[Dict]:
        data = self.api.playlist(playlist_id=self.playlist_id)
        return list(map(lambda item: item['track'], data['tracks']['items']))


class Store:
    def __init__(self, host='localhost', port=6379):
        self.__redis = redis.Redis(host=host, port=int(port), db=0)

    def store(self, rank: int, track: dict):
        identifier = f"hit:{rank}"

        self.__redis.hset(identifier, key='artist', value=track['artists'][0]['name'])
        self.__redis.hset(identifier, key='url', value=track['external_urls']['spotify'])
        self.__redis.hset(identifier, key='name', value=track['name'])
        self.__redis.hset(identifier, key='rank', value=rank)

    def close(self):
        self.__redis.close()


def main():
    """Fetch today's top hits and push to redis storage"""
    spotify = Spotify(**config['spotify'])
    store = Store(**config['redis'])

    today_hits = spotify.fetch_today_top_hits()
    today_hits.sort(key=lambda item: int(item['popularity']), reverse=True)  # sort by popularity

    for index, hit in enumerate(today_hits):
        store.store(index + 1, hit)
    else:
        store.close()


if __name__ == '__main__':
    main()
