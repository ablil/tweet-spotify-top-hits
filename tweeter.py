#!/usr/bin/env python3

import logging
import random
from typing import Dict

import redis
import tweepy

from config import config


def bold(input_text):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    bold_chars = "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"
    output = ""

    for character in input_text:
        output += bold_chars[chars.index(character)] if character in chars else character

    return output


class Tweeter:
    def __init__(self, consumer_key, consumer_secret, access_key, access_secret):
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_key, access_secret)
        self.api = tweepy.API(auth)

    def tweet(self, content: str):
        try:
            self.api.update_status(content.strip())
        except Exception as e:
            logging.error("Failed to tweet, reason: ", e)


class Store:
    def __init__(self, host='localhost', port=6379):
        self.__redis = redis.Redis(host=host, port=int(port), db=0)

    def fetch_hit(self, rank: int) -> Dict:
        return self.__redis.hgetall(f"hit:{rank}")

    def close(self):
        self.__redis.close()


def main():
    """Read data from redis storage and tweet"""
    tweeter = Tweeter(**config['twitter'])
    store = Store(**config['redis'])

    rank = random.randint(1, 40)
    hit = store.fetch_hit(rank)
    if hit:
        tweet = f"Today's top #{rank} hit on @Spotify \n"
        tweet += f"{bold(hit[b'name'].decode())} by {bold(hit[b'artist'].decode())}"
        tweet += "\n\n"
        tweet += f"listen right now {hit[b'url'].decode()}"
        tweeter.tweet(tweet)

    store.close()


if __name__ == '__main__':
    main()
