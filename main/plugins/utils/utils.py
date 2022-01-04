#Tg:ChauhanMahesh/DroneBots
#Github.com/Vasusen-code

import re
import os
import time
import heroku3
import requests
from datetime import datetime as dt
from ... import Drone, BOT_UN, MONGODB_URI
from main.Database.database import Database
from telethon import events
from decouple import config
from ethon.telefunc import fast_upload
from telethon.tl.types import DocumentAttributeVideo
from ethon.pyutils import file_extension
from ethon.pyfunc import video_metadata
from LOCAL.localisation import SUPPORT_LINK
from telegraph import upload_file as uf
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

db = Database(MONGODB_URI, 'videoconvertor')

#uploading---------------------------------------------------------------------------------

async def thumb(id):
    db = Database(MONGODB_URI, 'videoconvertor')
    T = await db.get_thumb(id)
    if T is not None:
        ext = T.split("/")[4]
        r = requests.get(T, allow_redirects=True)
        path = dt.now().isoformat("_", "seconds") + ext
        open(path , 'wb').write(r.content)
        return path
    else:
        return None

video_mimes = ['.mp4',
               '.mkv', 
               '.webm']

#attrubutes needed to upload video as streaming
def attributes(file):
    metadata = video_metadata(file)
    width = metadata["width"]
    height = metadata["height"]
    duration = metadata["duration"]
    x = [DocumentAttributeVideo(duration=duration, w=width, h=height, supports_streaming=True)]
    return x

#uploads video in streaming form
async def upload_video(file, event, edit):
    T = await thumb(event.sender_id)
    text = f'{file}\n\n**UPLOADED by:** {BOT_UN}'
    Drone = event.client
    try:
        x = attributes(file)
        uploader = await fast_upload(file, file, time.time(), event.client, edit, f'**UPLOADING FILE**')
        await Drone.send_file(event.chat_id, uploader, caption=text, thumb=T, attributes=x, force_document=False)
        os.remove(file)
    except Exception:
        False    

async def upload_file(file, event, edit):
    T = await thumb(event.sender_id)
    text = f'{file}\n\n**UPLOADED by:** {BOT_UN}'
    Drone = event.client
    try:
        extension = file_extension(file)
        if extension in video_mimes:
            result = await upload_video(file, event, edit) 
            if result is False:
                uploader = await fast_upload(file, file, time.time(), event.client, edit, f'**UPLOADING FILE:**')
                await Drone.send_file(event.chat_id, uploader, caption=text, thumb=T, force_document=True)
                os.remove(file)
        else:
            uploader = await fast_upload(file, file, time.time(), event.client, edit, f'**UPLOADING FILE:**')
            await Drone.send_file(event.chat_id, uploader, caption=text,thumb=T, force_document=True)
            os.remove(file)
    except Exception as e:
        return await edit.edit(f"An error `[{e}]` occured while uploading.\n\nContact [SUPPORT]({SUPPORT_LINK})", link_preview=False)
    await edit.delete()
        
#uploads a folder 
#Note:Here folder is a list of all contents in a folder
async def upload_folder(folder, event, edit):
    T = await thumb(event.sender_id)
    Drone = event.client
    index = len(folder)
    for i in range(int(index)):
        try:
            file = folder[int(i)]
            text = f'{file}\n\n**UPLOADED by:** {BOT_UN}'
            extension = file_extension(file)
            if extension in video_mimes:
                result = await upload_video(file, event, edit) 
                if result is False:
                    uploader = await fast_upload(file, file, time.time(), event.client, edit, f'**UPLOADING FILE:**')
                    await Drone.send_file(event.chat_id, uploader, caption=text, thumb=T, force_document=True)
                    os.remove(file)
            else:
                uploader = await fast_upload(file, file, time.time(), event.client, edit, f'**UPLOADING FILE:**')
                await Drone.send_file(event.chat_id, uploader, caption=text, thumb=T, force_document=True)
                os.remove(file)
        except Exception as e:
            print(e)
            return await edit.edit(f"An error `[{e}]` occured while uploading.\n\nContact [SUPPORT]({SUPPORT_LINK})", link_preview=False)
        await edit.delete()
        folder.pop(i)
       
#to get the url from event
def get_link(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)   
    try:
        link = [x[0] for x in url][0]
        if link:
            return link
        else:
            return False
    except Exception:
        return False
    
#Forcesub-----------------------------------------------------------------------------------

async def force_sub(id):
    FORCESUB = config("FORCESUB", default=None)
    if not str(FORCESUB).startswith("-100"):
        FORCESUB = int("-100" + str(FORCESUB))
    ok = False
    try:
        x = await Drone(GetParticipantRequest(channel=int(FORCESUB), participant=int(id)))
        left = x.stringify()
        if 'left' in left:
            ok = True
        else:
            ok = False
    except UserNotParticipantError:
        ok = True 
    return ok   
    
#Thumbnail--------------------------------------------------------------------------------------------------------------

async def set_thumbnail(event, img):
    edit = await event.client.send_message(event.chat_id, 'Trying to process.')
    try:
        path = await event.client.download_media(img)
        meta = uf(path)
        link = f'https://telegra.ph{meta[0]}'
    except Exception as e:
        print(e)
        return await edit.edit("Failed to Upload on Tgraph.")
    await db.update_thumb_link(event.sender_id, link)
    await edit.edit("Done!")
    
async def rem_thumbnail(event):
    edit = await event.client.send_message(event.chat_id, 'Trying.')
    T = await db.get_thumb(event.sender_id)
    if T is None:
        return await edit.edit('No thumbnail saved!')
    await db.rem_thumb_link(event.sender_id)
    await edit.edit('Removed!')
    
#Heroku--------------------------------------------------------------------------------------------------------------
   
async def heroku_restart():
    HEROKU_API = config("HEROKU_API", default=None)
    HEROKU_APP_NAME = config("HEROKU_APP_NAME", default=None)
    x = None
    if not HEROKU_API and HEROKU_APP_NAME:
        x = None
    else:
        try:
            acc = heroku3.from_key(HEROKU_API)
            bot = acc.apps()[HEROKU_APP_NAME]
            bot.restart()
            x = True
        except Exception as e:
            print(e)
            x = False
    return x
    

