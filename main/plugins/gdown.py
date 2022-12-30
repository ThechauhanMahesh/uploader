#TG:ChauhanMahesh/DroneBots
#Github.com/vasusen-code

import re, os, time, asyncio

from .. import Drone, BOT_UN
from LOCAL.localisation import SUPPORT_LINK
from pathlib import Path
from datetime import datetime as dt

from ethon.pyfunc import bash

from telethon import events, Button

from mega import Mega
import gdown

#Downloaders-------------------------------------------------------------------------------------------------------------

#download mega files
def mega_dl(url):
    try:
        m = Mega().login()
        file = m.download_url(url) 
        return str(Path(str(file)))
    except Exception as e:
        print(e)
        return False

#download files from drive
def drive(link):
    try:
        if 'https://drive.google.com/file/' in link:
            id = (link.split("/"))[5]
            _link = f'https://drive.google.com/uc?id={id}'
            try:
                file = gdown.download(_link, quiet=True)
                return file
            except Exception as e:
                print(e)
                return False 
        elif 'https://drive.google.com/uc?id=' in link:
            try:
                file = gdown.download(link, quiet=True)
            except Exception as e:
                print(e)
                return  False
        elif  'id=' in link:
            try:
                link_ = f'https://drive.google.com/uc?id={(link.split("id="))[1]}'
                file = gdown.download(link_, quiet=True)
                return file
            except Exception as e:
                print(e)
                return False
