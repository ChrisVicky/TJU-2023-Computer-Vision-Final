import cv2
from mmflow.apis import init_model, inference_model
from mmflow.datasets import write_flow
import os
from tqdm import tqdm
import numpy as np
import json
import torch


#  mim download mmflow --config raft_8x2_100k_mixed_368x768 --dest ./checkpoints
Config = "./checkpoints/raft_8x2_100k_mixed_368x768.py"
Checkpoint = "./checkpoints/raft_8x2_100k_mixed_368x768.pth"
Device = "cuda:0" if torch.cuda.is_available() else "cpu"
Video = "./download/cxk.mp4"
Base = "./results"
Mode = 5
DN = 30  # How many frames for one dataset
Model = init_model(Config, Checkpoint, Device)


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


def imgs2flo(datas: []):
    global Model
    for data in datas:
        base = os.path.join(Base, data["video_id"])
        check_path(base)

        imgs = data["imgs"]
        metadata = {
                "video_id":     data["video_id"],
                "source":       data["source"],
                "start_frame":  data["start_frame"],
                "dynamic":      "0",
                }
        json_str = json.dumps(metadata, indent=4)
        with open(os.path.join(base, "metadata.json"), 'w') as json_file:
            json_file.write(json_str)

        for i in tqdm(range(len(imgs) - 1)):
            img1 = imgs[i]
            img2 = imgs[i+1]

            result = inference_model(Model, img1, img2)

            p = os.path.join(base, "flow_rgb")
            check_path(p)
            cv2.imwrite(os.path.join(p, f"{i:04d}.jpg"), flow2rgb2(result))

            p = os.path.join(base, "flow")
            check_path(p)
            write_flow(result, os.path.join(p, f"{i:04d}.flo"))

            p = os.path.join(base, "target")
            check_path(p)
            cv2.imwrite(os.path.join(p, f"{i:04d}.jpg"), img1)
        cv2.imwrite(os.path.join(p, f"{i+1:04d}.jpg"), imgs[-1])


def Video2flo(url: str, vid: int, video: str = Video):
    cap = cv2.VideoCapture(video)
    assert cap.isOpened()
    # fps = cap.get(cv2.CAP_PROP_FPS)
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
        if cnt % Mode == 0:
            imgs.append(img)
            cnt_i += 1
        if cnt_i % DN == (DN - 1):
            data["video_id"] = str(vid)
            vid += 1
            data["imgs"] = imgs
            imgs = []
            data["source"] = url
            data["start_frame"] = cnt_i - DN + 1
            datas.append(data)
            data = {}
        cnt += 1
    cap.release()

    imgs2flo(datas)
    return vid
