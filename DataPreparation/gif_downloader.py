import concurrent.futures as futures
from typing import Iterable, Set, List, Dict
from pathlib import Path
import time
from dataclasses import dataclass
import json

from loguru import logger
import requests
from tqdm import tqdm


@dataclass
class Gif:
    hash_id: str
    url: str

    def __hash__(self):
        return (self.hash_id + self.url).__hash__()


class Downloader:
    def __init__(self, n_thread: int = 4, output_dir: Path = Path.cwd(), proxy_pool: List[Dict] = None):
        self.gif_group: Set[Gif] = set()
        self.n_thread = n_thread
        self.output_dir = output_dir
        self.proxy_pool = proxy_pool or []

    def add(self, gifs: Iterable[Gif]):
        for gif in gifs:
            self.gif_group.add(gif)
        logger.info(f"added {len(gifs)} gifs, total {len(self.gif_group)}")

    def download_single(self, gif: Gif, proxies=None, overwrite=False, retries=5) -> bool:
        image_name = f"{gif.hash_id}.gif"
        image_path = self.output_dir / image_name
        if image_path.exists() and not overwrite:
            return False
        for n in range(retries):
            try:
                if n == retries - 1:
                    proxies = None  # last retry without proxy
                response = requests.get(gif.url, proxies=proxies)
                if response.status_code == 200:
                    with open(image_path, "wb") as f:
                        f.write(response.content)
                    return True
            except Exception as e:
                logger.warning(f"fail to download {image_name}, retrying, Exception: {e}")
                time.sleep(3)
        logger.error(f"fail to download {image_name}")
        return False

    def download(self):
        logger.info(f"===== downloader start with {self.n_thread} threads =====")
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True)

        # balance proxy pool
        if self.proxy_pool:
            proxy_pool = self.proxy_pool * (len(self.gif_group) // len(self.proxy_pool) + 1)
        else:
            proxy_pool = [None] * len(self.gif_group)

        with futures.ThreadPoolExecutor(self.n_thread) as executor:
            with tqdm(total=len(self.gif_group), desc="downloading") as pbar:
                for _ in executor.map(self.download_single, self.gif_group, proxy_pool):
                    pbar.update(1)
        logger.info("===== downloader end =====")


# test
if __name__ == "__main__":
    # redis 2 file
    with open("4309.json", "r") as f:
        gifs_dict = json.load(f)
    downloader = Downloader(n_thread=4, output_dir=Path.cwd() / "gifs")
    downloader.add([Gif(k, v) for k, v in gifs_dict.items()])
    downloader.download()
