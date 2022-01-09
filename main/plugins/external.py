#TG:ChauhanMahesh/DroneBots
#Github.com/vasusen-code

import re
import os
import time
import gdown
import asyncio
import mediafire_dl 
from mega import Mega 
from datetime import datetime as dt
from .. import Drone, BOT_UN
from telethon import events
from ethon.telefunc import fast_upload
from ethon.pyfunc import bash
from LOCAL.localisation import SUPPORT_LINK, down_sticker
from telethon.tl.types import MessageMediaWebPage
from main.plugins.utils.utils import get_link, upload_folder

#to upload files from drive folder 
#returns downloaded files path as a list
def drive_folder_download(url):
    output = gdown.download_folder(url, quiet=True)
    return output

#makes error handling handy
async def error(event, error, ps):
    return await event.edit(f"An error [`{error}`] occured while {ps}.\n\nContact [SUPPORT]({SUPPORT_LINK})", link_preview=False)        

#download files frm drive
async def drive(event, msg):
    folder = []
    Drone = event.client
    link = get_link(msg.text)
    ds = await Drone.send_file(event.chat_id, file=down_sticker, reply_to=msg.id)
    edit = await Drone.send_message(event.chat_id, "**DOWNLOADING**", reply_to=msg.id)
    if 'folder' in link:
        try:
            output = drive_folder_download(link)
        except Exception as e:
            print(e)
            await ds.delete()
            return await error(edit, e, 'downloading')
        if output is None:
            await ds.delete()
            return await edit.edit("Could not Download!")
        index = len(output)
        for i in range(int(index)):
            folder.append((output)[i])
    elif 'folders' in link:
        try:
            output = drive_folder_download(link)
        except Exception as e:
            print(e)
            await ds.delete()
            return await error(edit, e, 'downloading') 
        if output is None:
            await ds.delete()
            return await edit.edit("Could not Download!")
        index = len(output)
        for i in range(int(index)):
            folder.append((output)[i])
    elif 'https://drive.google.com/file/' in link:
        id = (link.split("/"))[5]
        _link = f'https://drive.google.com/uc?id={id}'
        try:
            file = gdown.download(_link, quiet=True)
        except Exception as e:
            await ds.delete()
            print(e)
            return await error(edit, e, 'downloading') 
        folder.append(file)
    elif 'https://drive.google.com/uc?id=' in link:
        try:
            file = gdown.download(link, quiet=True)
        except Exception as e:
            print(e)
            await ds.delete()
            return await error(edit, e, 'downloading') 
        folder.append(file)
    elif 'id=' in link:
        try:
            link_ = f'https://drive.google.com/uc?id={(link.split("id="))[1]}'
            file = gdown.download(link_, quiet=True)
        except Exception as e:
            print(e)
            await ds.delete()
            return await error(edit, e, 'downloading') 
        folder.append(file)
    else:
        await ds.delete()
        return await edit.edit(f'Link support not added.\n\ncontact [SUPPORT]({SUPPORT_LINK})', link_preview=False)
    await ds.delete()
    await upload_folder(folder, event, edit) 

#download from mediafire
def mfdl(url):
    output = url.split("/")[-1]
    mediafire_dl.download(url, output, quiet=False)
    return output

#download mega files
def mega_dl(url):
    m = Mega().login()
    file = m.download_url(url)
    return file
