from __future__ import annotations
import os
from bs4 import BeautifulSoup
import requests
import subprocess
from dotenv import load_dotenv
load_dotenv()

SERVER = os.getenv("SERVER_IP")
PORT = os.getenv("SERVER_PORT")
URL = f"http://{SERVER}:{PORT}"

DIST = "RetroPie/roms/"
DEBUG = not True

def clear(n:int) -> None:
    """clears screen by `n` (`int`) lines"""
    print("\n"*n)

def INFO():
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

def download_file(files:str, directory:str):
    """downloads file from dir"""
    for file in files:
        command_str = f"wget -O {DIST}{directory}{file} {URL}/{directory}{file}".split(" ")
        if not DEBUG:
            subprocess.run(command_str)
        else:
            print(command_str)

def dir_choice(directories: list[str]) -> int:
    """dir selection"""
    menu = {}
    for _i, _dir in enumerate(directories, 1):
        menu[_i] = _dir
        print(f"[{_i}]| {_dir}")

    _choice = int(input("Select a directory by number: ")) or None
    return None if isinstance(_choice, type(None)) else _choice-1


def main():
    """main"""
    dirs = get_dirs()
    choice = dir_choice(dirs)
    if choice <= len(dirs):
        print(f"show files in \"{get_dirs()[choice].replace('/','')}\"?", end="")
        if input(" [y/N] ").lower() == "y":
            print(get_dir_files(get_dirs()[choice]))
    download_file(files=get_dir_files(get_dirs()[choice]), directory=get_dirs()[choice])

if __name__ == "__main__":
    try:
        if not os.path.exists(DIST):
            print(f"[WARNING] Path \"{DIST}\" not found!")
            if input("continue? [y/N] ").lower() == "n":
                exit()
        clear(10)
        INFO()
        main()
    except KeyboardInterrupt:
        exit()
