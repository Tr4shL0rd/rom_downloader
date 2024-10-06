"""asd"""
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
    """asd"""
    for _i,file in enumerate(files,0):
        command_str = f"wget -O {DIST}{directory}{file} {URL}/{directory}{file}".split(" ")
        subprocess.run(command_str)

#print(get_dirs())
download_file(files=get_dir_files(get_dirs()[3]), directory=get_dirs()[3])
