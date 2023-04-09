from downloader import download
from video2flo import Video2flo, check_path
import os


Path = "./download"
check_path(Path)

url = [
        "https://www.bilibili.com/video/BV1i441187Vj",  # 藤原书记
        "https://www.bilibili.com/video/BV1ct4y1n7t9"   # 蔡徐坤
        ]
vid = 0
for u in url:
    title = u[u.rfind("/")+1:]
    download(u, False, 10, path=Path, name=title)
    title += ".mp4"
    print("New file: ", title)
    vid = Video2flo(url, vid, os.path.join(Path, title))

local = [
        "ndmz.flv",     # 你的名字
        "sq.mp4"        # 沙丘
        ]

for t in local:
    vid = Video2flo("localhost", vid, os.path.join(Path, t))
