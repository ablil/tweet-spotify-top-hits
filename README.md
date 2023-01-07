# Tweet spotify hit tracks

Tweet spotify's top hits each day.

# How it works ?

`spotify.py` fetch top hits and save them to a Redis store.

`tweeter.py` read from the Redis store, and tweet one random track.

Each of the above scripts can be run independently of each other, but all of them read the config/credentials
from `config.py`.

# Get started

1. Install necessary dependencies

```shell
pip3 install -r requirements.txt
```

2. Create a redis store to hold the data

```shell
$ docker pull redis && docker run -d --name mystore -p 6379:6379 redis
```

3. Set a cronjob to fetch spotify hits daily

```
0 0 * * * python3 /path/to/spotify.py
```

4. Set cronjob to tweet his each one or two hours.

```
0 */1 * * * python3 /path/to/tweeter.py
```
