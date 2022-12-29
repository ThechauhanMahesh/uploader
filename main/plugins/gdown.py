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
import mediafire_dl, gdown

#Downloaders-------------------------------------------------------------------------------------------------------------

#download from mediafire
def mfdl(url, id):
    output = url.split("/")[-1]
    mediafire_dl.download(url, output, sender_id=id, quiet=False)
    return output

#download mega files
def mega_dl(url):
    m = Mega().login()
    file = m.download_url(url) 
    return str(Path(str(file)))

#to upload files from drive folder 
#returns downloaded files path as a list
def drive_folder_download(url):
    output = gdown.download_folder(url, quiet=False)
    return output

#makes error handling handy
async def error(event, error, ps):
    return await event.edit(f"An error [`{error}`] occured while {ps}.\n\nContact [SUPPORT]({SUPPORT_LINK})", link_preview=False, buttons=None)      

#download files frm drive
async def drive(link):
    if 'https://drive.google.com/file/' in link:
        id = (link.split("/"))[5]
        _link = f'https://drive.google.com/uc?id={id}'
        try:
            file = gdown.download(_link, quiet=True, sender_id=event.sender_id)
            return file
        except Exception as e:
            print(e)
            return False 
        folder.append(file)
    elif 'https://drive.google.com/uc?id=' in link:
        try:
            file = gdown.download(link, quiet=True, sender_id=event.sender_id)
        except Exception as e:
            print(e)
            return await error(edit, e, 'downloading') 
        folder.append(file)
    elif  'id=' in link:
        try:
            link_ = f'https://drive.google.com/uc?id={(link.split("id="))[1]}'
            file = gdown.download(link_, quiet=True, sender_id=event.sender_id)
        except Exception as e:
            print(e)
            return await error(edit, e, 'downloading') 
        folder.append(file)
@Drone.on(events.callbackquery.CallbackQuery(data="progress"))
async def status(event):
    st = get_progress(f'GDRIVE FILE DOWN for {event.sender_id}')
    await event.answer(st, alert=True)
    
    
    
