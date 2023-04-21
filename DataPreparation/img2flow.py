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

Config = "./checkpoints/raft_8x2_100k_mixed_368x768.py"
Checkpoint = "./checkpoints/raft_8x2_100k_mixed_368x768.pth"
Device = "cuda:0" if torch.cuda.is_available() else "cpu"
Model = init_model(Config, Checkpoint, Device)
Base = "/root/autodl-fs/CV/4300"


def img2flow(img1, img2, source: str):
    global Model
    base = os.path.join(Base, source)
    result = inference_model(Model, img1, img2)
    cv2.imwrite(os.path.join(base, f"flow.jpg"), flow2rgb2(result))
    metadata = {
        "source": source,
        "min": np.min(result),
        "max": np.max(result),
    }
    json_str = json.dumps(metadata, indent=4)
    with open(os.path.join(base, "metadata.json"), 'w') as json_file:
        json_file.write(json_str)


hashs = os.listdir(Base)

for h in tqdm(hashs):
    base = os.path.join(Base, h)
    img1 = cv2.imread(os.path.join(base, "0.jpg"))
    img2 = cv2.imread(os.path.join(base, "1.jpg"))
    # img2flow(img1, img2, h)
