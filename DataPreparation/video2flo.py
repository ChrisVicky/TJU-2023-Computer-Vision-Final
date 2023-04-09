import cv2
from mmflow.apis import init_mode, inference_model
from mmflow.datasets import visualize_flow, write_flow
import os


#  mim download mmflow --config raft_8x2_100k_mixed_368x768 --dest ./checkpoints
Config = "./checkpoints/raft_8x2_100k_mixed_368x768.py"
Checkpoint = "./checkpoints/raft_8x2_100k_mixed_368x768.pth"
Device = "cpu"
Video = "./download/cxk.mp4"
Base = "./results"
Mode = 5


model = init_mode(Config, Checkpoint, Device)
cap = cv2.VideoCapture(Video)
assert cap.isOpen()
size = (
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )

fps = cap.get(cv2.CAP_PROP_FPS)

imgs = []
cnt = 0
while (cap.isOpen()):
    flag, img = cap.read()
    if not flag:
        break
    if cnt % Mode == 0:
        imgs.append(img)
        cnt = 0
    cnt += 1

for i in range(len(imgs) - 1):
    img1 = imgs[i]
    img2 = imgs[i+1]
    result = inference_model(model, img1, img2)
    visualize_flow(result, os.path.join(Base, f"{i}.jpg"))
    write_flow(result, os.path.join(Base, f"{i}.flo"))

cap.release()
