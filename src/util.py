from src.constants import Constants
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from multiprocessing.pool import Pool
from src.chapter import Chapter
from src.image import Image
from pathlib import Path
from PIL import Image as PilImage
import os
import platform
import subprocess
import json



def clear_terminal() -> None:    
    if platform.system() == "Windows":        
        subprocess.run("cls", shell=True)
    else:        
        subprocess.run("clear", shell=True)         


def read_json(path: Path | str, default = None):
    if isinstance(path, str):
        path = Path(path)
    
    try:
        with open(path, "r") as file:
            return json.load(file)
    except Exception:
        return default


def save_json(obj, path: Path) -> None:
    if isinstance(path, str):
        path = Path(path)
    
    with open(path, "w+") as file:
        json.dump(obj, file, indent=4, sort_keys=True, check_circular=True)

    
def clear_dir(dir: Path) -> None:
    [os.remove(i) for i in dir.iterdir()]    


def compress_to_cbr(dest: Path) -> None:
    clear_terminal()
    src = Constants.tmp_dir
    dest = dest.with_suffix(".cbr")    
    command = f'zip -r -j -q "{dest}" "{src}"' ;
    print(f"[COMPRESSING {src} into {dest}. Command: {command}]")
    os.system(command)


def convert_image_to_jpg(path: Path) -> None:
    PilImage.open(path).convert("RGB").save(path.with_suffix(".jpeg"))

