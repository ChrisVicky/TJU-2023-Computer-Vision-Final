import cv2
import imageio
import os

Base = "./download"

def frame_to_gif(frame_list, filename):
    d = 2.0 / len(frame_list)
    imageio.mimsave(
            os.path.join(Base, filename),
            frame_list,
            'GIF',
            duration=d
            )
    # duration 表示图片间隔


def read_video(video_path: str, seconds: int = 4):
    video_cap = cv2.VideoCapture(video_path)
    # 视频平均帧率
    fps = int(video_cap.get(cv2.CAP_PROP_FPS))
    total_frames = fps * seconds
    cnt = 0
    gif = 0
    all_frames = []
    total_gif = 1000
    while True:
        ret, frame = video_cap.read()
        if ret is False:
            break
        if cnt % 5 == 0:
            frame = frame[..., ::-1]   # opencv读取BGR，转成RGB
            all_frames.append(frame)
        if cnt > total_frames:
            frame_to_gif(all_frames, f"result_{gif}.gif")
            all_frames.clear()
            gif += 1
            print('===>', gif, "/", total_gif)
            cnt = 0
        if gif >= total_gif:
            break
        cnt += 1
    video_cap.release()
    print('===>', gif)
    return all_frames


if __name__ == "__main__":
    frame_list = read_video(os.path.join(Base, "【1080p 自制中日字幕 nced】辉夜大小姐想让我告白第3话ED「チカっとチカ千花っ♡」 P1 中日字幕.mp4"))
