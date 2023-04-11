import cv2
import os
from tqdm import tqdm
import numpy as np
from PIL import Image, ImageSequence


def check_path(p):
    if os.path.exists(p):
        return 1
    else:
        os.makedirs(p)
        return 0


Base = "./gifs"
FigBase = "./figures"
target = 256


def cropimg(img):
    global target
    h = img.shape[0]
    w = img.shape[1]
    if h > w:
        Size = (int(target), int(h*(target/w)))
        img = cv2.resize(img, Size)
    else:
        Size = (int(w*(target/h)), int(target))
        img = cv2.resize(img, Size)
    img = img[0:int(target), 0:int(target)]
    return img


def Gif2figure(gif: str):
    global Base
    _gif = Image.open(os.path.join(Base, gif+".gif"))
    img_list = []
    for frame in ImageSequence.Iterator(_gif):
        frame = frame.convert('RGB')
        cv_img = np.array(frame, dtype=np.uint8)
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGBA2BGRA)
        img_list.append(cropimg(cv_img))

    base = os.path.join(FigBase, gif)
    if check_path(base):
        return
    i = 0
    j = -1
    if len(img_list) >= 4:
        i = 0
        j = 2
    cv2.imwrite(os.path.join(base, "0.jpg"), img_list[i])
    cv2.imwrite(os.path.join(base, "1.jpg"), img_list[j])


def main():
    gifs = os.listdir(Base)
    for g in tqdm(gifs):
        if '.gif' not in g:
            continue
        g = g[:g.rfind(".gif")]
        Gif2figure(g)


main()
