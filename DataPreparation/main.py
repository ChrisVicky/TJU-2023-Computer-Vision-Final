from downloader import download
from video2flo import Video2flo, check_path
import os


Path = "./download"
check_path(Path)

url = [
        # "https://www.bilibili.com/video/BV1i441187Vj",  # 藤原书记
        # "https://www.bilibili.com/video/BV1ct4y1n7t9"   # 蔡徐坤
        ]
for u in url:
    title = u[u.rfind("/")+1:]
    download(u, False, 10, path=Path, name=title)
    title += ".mp4"
    print("New file: ", title)
    vid = Video2flo(url, vid, os.path.join(Path, title))

local = [
#         "BV1ct4y1n7t9.mp4", # 蔡徐坤
#         "BV1i441187Vj.mp4", # 藤原书记
#         "ndmz_0.mp4",     # 你的名字
#         "ndmz_1.mp4",     # 你的名字
        ]

vid = 0
while True:
    item = ""
    with open("todolist", "r+") as f:
        todoList = f.read().splitlines()
        if len(todoList) == 0:
            break
        item = todoList[0].strip()
    if item != "":
        vid = Video2flo(item, vid, os.path.join(Path, item))
    with open("todolist", "w") as f:
        f.seek(0)
        for i in range(len(todoList)-1):
            t = todoList[i+1]
            f.write(t+'\n')
    with open("donelist", "a") as f:
        f.write(item + "\n")
