import json
from urllib import parse, request
from typing import List, Dict

from tqdm import tqdm

url = "http://api.giphy.com/v1/gifs/trending"


def get_params(offset: int):
    return parse.urlencode({
        "q": "ryan gosling",
        "api_key": "{KEY}",
        "limit": "50",
        "offset": str(offset)
    })


def main() -> List[Dict[str, str]]:
    results = dict()
    fail_cnt = 0
    offset = 0
    pbar = tqdm()
    while True:
        params = get_params(offset)
        try:
            with request.urlopen("".join((url, "?", params))) as response:
                data = json.loads(response.read())
            if len(data["data"]) == 0:
                break
            for item in data["data"]:
                results[item["id"]] = item["images"]["original"]["url"]
            total_count = data["pagination"]["total_count"]
            pbar.total = total_count
            pbar.update(len(data["data"]))
            pbar.set_description(f"offset: {offset}, total_count: {total_count}")
            pbar.refresh()
            offset += 50
        except Exception as e:
            print(e)
            fail_cnt += 1
            continue
    print(f"fail_cnt: {fail_cnt}")
    return results


results = main()
with open('trending.json', 'w') as outfile:
    json.dump(results, outfile)
