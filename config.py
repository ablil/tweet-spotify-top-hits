#!/usr/bin/env python3

import os

config = {
    'twitter': {
        'consumer_key': os.environ['TWITTER_API_KEY'],
        'consumer_secret': os.environ['TWITTER_API_SECRET_KEY'],
        'access_key': os.environ['TWITTER_API_ACCESS_TOKEN'],
        'access_secret': os.environ['TWITTER_API_ACCESS_TOKEN_SECRET'],
    },
    'spotify': {
        'client_id': os.environ['SPOTIFY_API_CLIENT_ID'],
        'client_secret': os.environ['SPOTIFY_API_CLIENT_SECRET']
    },
    'redis': {
        'host': os.environ['REDIS_HOST'],
        'port': os.environ['REDIS_PORT']
    }
}
