from downloader import download
from video2flo import Video2flo, check_path
import os


url = "https://www.bilibili.com/video/BV1et411t7Cm"
Path = "./download"
check_path(Path)
title = "test.mp4"
title = os.path.join(Path, title)
download(url, False, 10, name=title)
print("New file: ", title)
Video2flo(url, 0, os.path.join(Path, title))
