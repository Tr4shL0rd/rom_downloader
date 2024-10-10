from __future__ import annotations
import sys
import os
import zipfile
import subprocess
import wget
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
load_dotenv()

SERVER = os.getenv("SERVER_IP")
PORT = os.getenv("SERVER_PORT")
URL = f"http://{SERVER}:{PORT}"

DIST = "RetroPie/roms/"
DEBUG = not True
if "v" in sys.argv:
    VERBOSE = True
    print("[WARNING] VERBOSE OUTPUT")
else:
    VERBOSE = False
    
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

    _dirs.pop(_dirs.index("misc/"))
    return _dirs

def get_dir_files(dir_url:str) -> list[str]:
    """Return list of files in dir"""
    _r = requests.get(f"{URL}/{dir_url}", timeout=3)
    _soup = BeautifulSoup(_r.text, 'html.parser')
    _files = [a['href'] for a in _soup.find_all('a', href=True) if not a['href'].endswith('/')]
    return _files

def bar_custom(current, total, width=80):
    print("Downloading: %d%% [%d / %d] Ks" % (current / total * 100, current / 1000, total / 1000), end='\r')

def download_file(files:list[str], directory:str):
    """downloads file from dir"""
    for file in files:
        output = f"{DIST}{directory}{file}"
        wget.download(url=f"{URL}/{directory}{file}", out=output, bar=bar_custom)
    print() # newline for after downloading

def dir_choice(directories: list[str]) -> int:
    """dir selection"""
    menu = {}
    for index, _dir in enumerate(directories, 1):
        menu[index] = _dir
        print(f"[{index}]| {_dir}")
    print("[all] download all ROMs")
    _choice = input("Select a directory by number: ") or None
    if _choice == "all":
        return -1
    else:
        _choice = int(_choice)
    if _choice > index or _choice < 1:
        print(f"please select a valid number between 1 and {index}")
        dir_choice(directories)

    if directories[_choice-1] == "psx/":
        print("[WARNING] PSX DOES NOT WORK IN THE ARCADE")
        yn_choice = input("continue? [y/N]: ").lower() or "n"
        if yn_choice == "n":
            return None

    return None if isinstance(_choice, type(None)) else _choice-1

def unzip_rom_file(file:str, dist:str):
    """
    unzips `file` (`str`) to `dist` (`str`)
    * note: `dist` also means the console that the rom file is for
    """
    with zipfile.ZipFile(file, "r") as zip_file:
        zip_file.extractall(dist)

def bulk_download(dirs: list[str]) -> None:
    """
    Downloads all files from the provided directories.
    """
    for dir in dirs:
        print(f"Downloading files from: {dir}")
        files = get_dir_files(dir)  # Get files in the directory
        if files:
            download_file(files, dir)  # Download the files
        else:
            print(f"No files found in {dir}")

    print("Bulk download complete.")


#def bulk_download(dirs:list[str]):
#    print(dirs)
#    for dir in dirs:

        #for file in get_dir_files(f"{URL}/{dir}"):
        #    print(f"{dir = }")
        #    print(f"{URL}/{dir}{file}")
        #    cmd_str = f"wget -q -O {DIST}{dir}{file} {URL}/{dir}{file}".split(" ")
        #print(dir)
        #print(download_file(get_dir_files(dir)))
        #download_file(get_dir_files(dir))
    

def main():
    """main"""
    dirs = get_dirs()

    choice = dir_choice(dirs)
    if choice == -1:
        print("downloading all")
        bulk_download(get_dirs())
        return
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
