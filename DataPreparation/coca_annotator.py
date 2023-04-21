from typing import List, Union, Tuple
from pathlib import Path
from tqdm import tqdm
import open_clip
import torch
from PIL import Image
import json

device = "cuda" if torch.cuda.is_available() else "cpu"

model, _, transform = open_clip.create_model_and_transforms(
    model_name="coca_ViT-L-14",
    device=device,
    pretrained="mscoco_finetuned_laion2B-s13B-b90k",
    cache_dir='/root/autodl-tmp/huggingface_cachedir'
)


class Timer:
    def __init__(self, name, end="\n"):
        """
        Timer for measuring the time of a block of code
        Args:
            name (str): the name of the timer, used for printing
            end (str): the end of the print statement, default to "\n"
        """
        self.name = name
        self.end = end

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # keep 2 decimal places
        print(f"[{self.name}] {time.time() - self.tstart:.2f}s", end=self.end)


def gif_dir_generator(data_root: Union[str, Path]) -> Path:
    data_root = Path(data_root)
    for gif_dir in data_root.iterdir():
        if not gif_dir.is_dir():
            continue
        yield gif_dir


def batch_generator(data_root: Union[str, Path], batch_size=100) -> Tuple[List[str], List[Path]]:
    """

    Args:
        data_root:
        batch_size:

    Returns:
        the list of image_paths and the list of gif_dirs
    """
    image_paths = []
    gif_dirs = []
    for gif_dir in gif_dir_generator(data_root):
        image_paths.append(str(gif_dir / '0.jpg'))
        gif_dirs.append(gif_dir)
        if len(image_paths) == batch_size:
            yield image_paths, gif_dirs
            image_paths = []
            gif_dirs = []
    if len(image_paths) != 0:  # the last batch
        yield image_paths, gif_dirs


def get_prompts(image_paths: List[str]) -> List[str]:
    images = []
    for image_path in image_paths:
        im = Image.open(image_path).convert("RGB")
        im = transform(im).unsqueeze(0)
        images.append(im)
    images = torch.cat(images, dim=0)
    images = images.to(device)
    with torch.no_grad(), torch.cuda.amp.autocast():
        generated = model.generate(images, num_beams=3)
    return [open_clip.decode(generated[i]).split("<end_of_text>")[0].replace("<start_of_text>", "") for i in
              range(len(generated))]


if __name__ == '__main__':
    for image_paths, gif_dirs in tqdm(batch_generator('/root/autodl-fs/CV/results/')):
        with Timer(f"get prompts for {len(image_paths)} images"):
            prompts = get_prompts(image_paths)
        for prompt, gif_dir in zip(prompts, gif_dirs):
            with open(gif_dir / 'metadata.json', 'w') as f:
                original = json.load(f)
                original['prompt'] = prompt
                json.dump(original, f)