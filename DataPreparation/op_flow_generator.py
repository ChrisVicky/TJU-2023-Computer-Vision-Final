import cv2
from mmflow.apis import init_model, inference_model
from mmflow.datasets import write_flow
import os
from tqdm import tqdm
import numpy as np
import json
import torch
from loguru import logger
from PIL import Image, ImageSequence
import numpy as np


#  mim download mmflow --config raft_8x2_100k_mixed_368x768 --dest ./checkpoints
Config = "./checkpoints/raft_8x2_100k_mixed_368x768.py"
Checkpoint = "./checkpoints/raft_8x2_100k_mixed_368x768.pth"
Device = "cuda:0" if torch.cuda.is_available() else "cpu"
Video = "./download/cxk.mp4"
Gif = "./download/test.gif"
# Base = "/root/autodl-fs/CV/results"
Base = "/root/autodl-fs/CV/4300"
Mode = 5
DN = 2 # How many frames for one dataset
Model = init_model(Config, Checkpoint, Device)
target = 512.0 # 512 x 512


def check_path(p):
    if os.path.exists(p):
        pass
    else:
        os.makedirs(p)


check_path(Base)


def flow2rgb2(flow: np.ndarray) -> np.ndarray:
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv = np.zeros((flow.shape[0], flow.shape[1], 3), dtype=np.uint8)
    hsv[..., 0] = ang * 180 / np.pi / 2  # hue is the direction
    hsv[..., 1] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX) # saturation is the magnitude
    hsv[..., 2] = 255  # not used
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)


def imgs2flo(imgs: [], source: str):
    global Model
    base = os.path.join(Base, source)
    result = inference_model(Model, imgs[0], imgs[1])
    cv2.imwrite(os.path.join(base, f"flow.jpg"), flow2rgb2(result))
    metadata = {
        "source": source,
        "min": np.min(result),
        "max": np.max(result),
    }
    json_str = json.dumps(metadata, indent=4)
    with open(os.path.join(base, "metadata.json"), 'w') as json_file:
        json_file.write(json_str)


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


def Video2flo(url: str, vid: int = None, video: str = Video):
    global Base
    if vid is None:
        numbs = [int(i) for i in os.listdir(Base)]
        vid = max(numbs) + 1
    print(f"Current Video: {video}, started with {vid}")
    cap = cv2.VideoCapture(video)
    assert cap.isOpened()
    fps = cap.get(cv2.CAP_PROP_FPS)
    mode = max(int(fps / 6), Mode)
    # length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    imgs = []
    datas = []
    data = {}
    cnt = 0
    cnt_i = 0
    while (cap.isOpened()):
        flag, img = cap.read()
        if not flag:
            break
        # Store the [0] and [fps] figures
        if cnt == 0:
            imgs.append(img)
        if cnt == fps:
            imgs.append(img)
        # Choose Images 2 minutes later
        if cnt == fps * 60 * 2:
            data["video_id"] = str(vid)
            vid += 1
            data["imgs"] = imgs
            imgs = []
            data["source"] = url
            data["start_frame"] = cnt_i * fps * 60 * 2
            datas.append(data)
            data = {}
            cnt_i += 1
            cnt = 0
        cnt += 1
    cap.release()

    if len(imgs) == 2:
        data["video_id"] = str(vid)
        vid += 1
        data["imgs"] = imgs
        imgs = []
        data["source"] = url
        data["start_frame"] = cnt_i * fps * 60 * 2
        datas.append(data)
        data = {}
        cnt_i += 1
        cnt = 0
    imgs2flo(datas)
    return vid


def Gif2flo(url: str, vid: int = None, gif: str = Gif):
    global Base
    if vid is None:
        numbs = [int(i) for i in os.listdir(Base)]
        vid = max(numbs) + 1
    print(f"Current Gif: {gif}, started with {vid}")
    _gif = Image.open(gif)
    i = 0
    imgs = []
    datas = []
    data = {}
    img_list = []
    for frame in ImageSequence.Iterator(_gif):
        frame = frame.convert('RGB')
        cv_img = np.array(frame, dtype=np.uint8)
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGBA2BGRA)
        img_list.append(cropimg(cv_img))

    imgs.append(img_list[0])
    imgs.append(img_list[-1])
    data["video_id"] = str(vid)
    vid += 1
    data["imgs"] = imgs
    data["start_frame"] = 0
    data["source"] = url
    datas.append(data)
    imgs2flo(datas)
    return vid

Gif2flo("test", 12)
