# python
import json
from urllib import parse, request
import redis
from tqdm import tqdm
from loguru import logger
from time import sleep

r = redis.StrictRedis(host="localhost", port=6379, charset="utf-8", decode_responses=True)

url = "http://api.giphy.com/v1/gifs/random"

params = parse.urlencode({
    "api_key": "{KEY}",
})


def get_random() -> dict:
    with request.urlopen("".join((url, "?", params))) as response:
        data = json.loads(response.read())
        k = data["data"]["id"]
        v = data["data"]["images"]["original"]["url"]
        v = v[:v.rfind("?cid")]
    return k, v


def get_total():
    tt = "total"
    w = r.get(tt)
    if w is None:
        return 0
    return int(r.get(tt))


def increase_total():
    tt = "total"
    w = r.get(tt)
    if w is None:
        w = 1
    else:
        w = int(w) + 1
    r.set(tt, w)
    return w

pbar = tqdm()
target = 5000
pbar.update(get_total())
while True:
    try:
        k, v = get_random()
    except Exception as e:
        logger.warning(e)
        sleep(0.1)
        continue
    curr = get_total()
    V = r.get(k)
    if V is None:
        r.set(k, v)
        curr += 1
        increase_total()
        pbar.update()
    else:
        # logger.debug(f"found: {k}: {V}")
        sleep(0.01)
    pbar.total = target
    pbar.set_description(f"{curr}/{target}")
    pbar.refresh()
    if curr >= target:
        break
        
