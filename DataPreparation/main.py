from downloader import download
from video2flo import video2flo
import os


url = "https://www.bilibili.com/video/BV1et411t7Cm"
Path = "./download"
files0 = os.listdir(Path)
title = download(url, False, 10, path=Path)
print("New file: ", title)
video2flo(url, 0)
