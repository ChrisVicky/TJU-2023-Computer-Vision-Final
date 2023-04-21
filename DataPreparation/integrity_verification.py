"""
This script is used for data integrity check.
collect -> download -> CHECK -> flow extraction -> CHECK -> text annotation -> CHECK -> restructure -> DONE
"""

from pathlib import Path
import time
import json
from typing import Union

import cv2
from loguru import logger

################# params ####################
data_root = './GIF'

auto_delete: bool = False

check_frames: bool = True
check_flow: bool = True
check_text: bool = True
#############################################

logger.remove()
logger.add("integrity_verif.log", level="INFO")
logger.add(sink="stderr", level="INFO")


class CheckFramesException(Exception):
    pass


class CheckFlowException(Exception):
    pass


class CheckTextException(Exception):
    pass


def gif_dir_generator(data_root: Union[str, Path]) -> Path:
    data_root = Path(data_root)
    for gif_dir in data_root.iterdir():
        if not gif_dir.is_dir():
            continue
        yield gif_dir


if __name__ == '__main__':
    for gif_dir in gif_dir_generator(data_root):
        if not gif_dir.is_dir():
            continue
        try:
            time.sleep(0.1)
            if check_frames:
                try:
                    frame_0 = cv2.imread(str(gif_dir / '0.jpg'))
                    frame_1 = cv2.imread(str(gif_dir / '1.jpg'))
                    if frame_0 is None or frame_1 is None:
                        raise CheckFramesException(f'frame 0 or 1 is corrupted')
                    cv2.imshow('frame_0', frame_0)
                    cv2.imshow('frame_1', frame_1)
                except:
                    raise CheckFramesException(f'frame 0 or 1 is corrupted')

            if check_flow:
                try:
                    flow = cv2.imread(str(gif_dir / 'flow.jpg'))
                    if flow is None:
                        raise CheckFlowException(f'flow is corrupted')
                    cv2.imshow('flow', flow)
                    with open('metadata.json', 'r') as f:
                        metadata = json.load(f)
                    if not metadata['source']:
                        raise CheckFlowException(f'flow is corrupted, metadata is empty')
                    flow_max = int(metadata['max'])
                    flow_min = int(metadata['min'])
                except:
                    raise CheckFlowException(f'flow is corrupted')
            if check_text:
                try:
                    with open('metadata.json', 'r') as f:
                        metadata = json.load(f)
                    if not metadata['prompt']:
                        raise CheckTextException(f'text is corrupted, prompt is empty')
                except:
                    raise CheckTextException(f'text is corrupted')
        except Exception as e:
            logger.error(f"gif {gif_dir} is corrupted, Exception: {e}")
            if auto_delete:
                logger.info(f"deleting {gif_dir}")
                for file in gif_dir.iterdir():
                    file.unlink()
                gif_dir.rmdir()
