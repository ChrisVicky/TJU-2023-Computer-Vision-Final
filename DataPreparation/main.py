from downloader import download
from video2flo import Video2flo, check_path
import os


# url = "https://www.bilibili.com/video/BV1et411t7Cm"
# Path = "./download"
# check_path(Path)
# title = "test"
# download(url, False, 10, path=Path, name=title)
# title += ".mp4"
# print("New file: ", title)
# Video2flo(url, 0, os.path.join(Path, title))
url = [
        "https://www.bilibili.com/video/BV1i441187Vj",  # 藤原书记
        "https://www.bilibili.com/video/BV1ct4y1n7t9"   # 蔡徐坤
        ]
Video2flo("localhost", 0, os.path.join("./download", "ndmz.flv"))
