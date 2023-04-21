import redis
import json

r = redis.StrictRedis(host="localhost", port=6379, charset="utf-8", decode_responses=True)
with open("trending.json", "r") as f:
    gifs_dict = json.load(f)
for k, v in gifs_dict.items():
    v = v[:v.rfind("?cid")]
    w = r.get(k)
    if w is None:
        r.set(k, v)
    else:
        pass
print("total: ", r.get(tt))
