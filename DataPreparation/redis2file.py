import redis
import json
r = redis.StrictRedis(host="localhost", port=6379, charset="utf-8", decode_responses=True)
items = dict()
for k in r.keys():
    items[k] = r.get(k)


with open('download.json', 'w') as outfile:
    json.dump(items, outfile)

