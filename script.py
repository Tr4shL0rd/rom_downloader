from __future__ import annotations
import os
import pathlib
import zipfile
import subprocess
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
load_dotenv()

SERVER = os.getenv("SERVER_IP")
PORT = os.getenv("SERVER_PORT")
URL = f"http://{SERVER}:{PORT}"

DIST = "RetroPie/roms/"
DEBUG = not True

def test_connect():
    """tests connection"""
    _r = requests.get(URL, timeout=3)
    return _r.status_code

def clear(n:int) -> None:
    """clears screen by `n` (`int`) lines"""
    print("\n"*n)

def server_info():
    """displays server info"""
    print("||==========================")
    print(f"||SERVER ADDRESS: {SERVER}")
    print(f"||SERVER PORT   : {PORT}")
    print(f"||URL           : {URL}")
    print("||==========================\n")
    
def get_dirs() -> list[str]:
    """returns only dirs from SERVER"""
    _r = requests.get(URL, timeout=3)
    _soup = BeautifulSoup(_r.text, 'html.parser')
    _dirs = [a['href'] for a in _soup.find_all('a', href=True) if a['href'].endswith('/')]
    return _dirs

def get_dir_files(dir_url:str) -> list[str]:
    """Return list of files in dir"""
    _r = requests.get(f"{URL}/{dir_url}", timeout=3)
    _soup = BeautifulSoup(_r.text, 'html.parser')
    _files = [a['href'] for a in _soup.find_all('a', href=True) if not a['href'].endswith('/')]
    return _files

def download_file(files:list[str], directory:str):
    """downloads file from dir"""
    for _i, file in enumerate(files,0):
        command_str = f"wget -q -O {DIST}{directory}{file} {URL}/{directory}{file}".split(" ")
        if not DEBUG:
            print(f"[{_i}/{len(directory)}]", end="\r")
            subprocess.run(command_str)
        else:
            print(command_str)

def dir_choice(directories: list[str]) -> int:
    """dir selection"""
    menu = {}
    for index, _dir in enumerate(directories, 1):
        menu[index] = _dir
        print(f"[{index}]| {_dir}")

    _choice = int(input("Select a directory by number: ")) or None
    if _choice >= index or _choice <= 1:
        print(f"please select a valid number between 1 and {index}")
        dir_choice(directories)
    return None if isinstance(_choice, type(None)) else _choice-1

def unzip_rom_file(file:str, dist:str):
    """unzips `file` (`str`) to `dist` (`str`)"""
    here = pathlib.Path(__name__).parent.resolve()
    with zipfile.ZipFile("Contra (USA).zip", "r") as zip_file:
        zip_file.extractall(here)


def main():
    """main"""
    dirs = get_dirs()
    dirs.pop(dirs.index("zipped_roms/"))

    choice = dir_choice(dirs)
    if choice <= len(dirs):
        print(f"show files in \"{get_dirs()[choice].replace('/','')}\"?", end="")
        if input(" [y/N] ").lower() == "y":
            print(get_dir_files(get_dirs()[choice]))
    download_file(files=get_dir_files(get_dirs()[choice]), directory=get_dirs()[choice])

if __name__ == "__main__":
    try:
        test_connect()
        if not os.path.exists(DIST):
            print(f"[WARNING] Path \"{DIST}\" not found!")
            continued = input("continue? [y/N] ").lower() or "n"
            if continued == "n":
                raise FileNotFoundError
            else:
                clear(10)
        server_info()
        main()
    except KeyboardInterrupt:
        print("\n")
    except requests.exceptions.ConnectionError as e:
        print(f"could not connect to \"{e.request.url}\"")
    except FileNotFoundError:
        print("path not found.\nexiting...")
    #finally:
    #    exit()
