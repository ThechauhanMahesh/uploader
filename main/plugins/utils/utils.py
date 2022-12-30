#Tg:ChauhanMahesh/DroneBots
#Github.com/Vasusen-code

import re, os, time, requests, subprocess, asyncio
from datetime import datetime as dt
from decouple import config
from telegraph import upload_file as uf

from ... import Drone, BOT_UN, MONGODB_URI, FORCESUB_UN
from main.Database.database import Database
from LOCAL.localisation import SUPPORT_LINK

from telethon import events
from telethon.tl.types import DocumentAttributeVideo
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

from ethon.telefunc import fast_upload
from ethon.pyutils import file_extension
from ethon.pyfunc import video_metadata

db = Database(MONGODB_URI, 'uploaderpro')

def mention(name, id):
    return f'[{name}](tg://user?id={id})'

#uploading---------------------------------------------------------------------------------

async def bash(cmd):
    cmd_ = cmd.split()
    process = await asyncio.create_subprocess_exec(*cmd_, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate() 
    e = stderr.decode().strip()
    o = stdout.decode().strip()
    return o, e

def hhmmss(seconds):
    x = time.strftime('%H:%M:%S',time.gmtime(seconds))
    return x

async def screenshot(video):
    time_stamp = hhmmss(int(duration)/2)
    out = dt.now().isoformat("_", "seconds") + ".jpg"
    cmd = ["ffmpeg",
           "-ss",
           f"{time_stamp}", 
           "-i",
           f"{video}",
           "-frames:v",
           "1", 
           f"{out}",
           "-y"
          ]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    stderr.decode().strip()
    stdout.decode().strip()
    if os.path.isfile(out):
        return out
    else:
        None       
        
#2gb limit

def max_size_error(file):
    if not file == None:
        if os.path.isfile(file) == True:
            size = os.path.getsize(file)/1000000
            if size > 1999:
                os.remove(file)
                return False
        else:
            return True
    else:
        return False

#to get the pmt thumbnail saved by the user

async def thumb(id):
    db = Database(MONGODB_URI, 'uploaderpro')
    T = await db.get_thumb(id)
    if T is not None:
        ext = T.split("/")[4]
        r = requests.get(T, allow_redirects=True)
        path = dt.now().isoformat("_", "seconds") + ext
        open(path , 'wb').write(r.content)
        return path
    else:
        return None

video_mimes = ['mkv', 'mp4']
               
# attrubutes needed to upload video as streaming

def attributes(file):
    metadata = video_metadata(file)
    width = metadata["width"]
    height = metadata["height"]
    duration = metadata["duration"]
    x = [DocumentAttributeVideo(duration=duration, w=width, h=height, supports_streaming=True)]
    return x

#uploads...

async def upload(file, event, edit):
    await edit.edit('preparing to upload...') 
    size = max_size_error(file)
    if size == False:
        await edit.edit("Can't upload files larger than 2GB.")
        return
    text = f'{file}\n\n**UPLOADED by:** {BOT_UN}'
    Drone = event.client
    try:
        T = await thumb(event.sender_id)
    except Exception:
        T = None
    if str(file).split(".")[-1] in video_mimes:
        x = attributes(file) 
        if T is None:
            try:
                T = await screenshot(file)
            except Exception:
                T = None
        try:
            uploader = await fast_upload(file, file, time.time(), event.client, edit, f'**UPLOADING FILE**')
            await Drone.send_file(event.chat_id, uploader, caption=text, thumb=T, attributes=x, force_document=False)
        except Exception:
            try:
                uploader = await fast_upload(file, file, time.time(), event.client, edit, f'**UPLOADING FILE**')
                await Drone.send_file(event.chat_id, uploader, caption=text, thumb=T, force_document=True)
            except Exception as e:
                print(e)
                return await edit.edit("Failed to UPLOAD!")
    else:
        try:
            uploader = await fast_upload(file, file, time.time(), event.client, edit, f'**UPLOADING FILE**')
            await Drone.send_file(event.chat_id, uploader, caption=text, thumb=T, force_document=True)
        except Exception as e:
            print(e)
            return await edit.edit("Failed to UPLOAD!")
    if os.path.isfile(file) == True:
        os.remove(file)
    await edit.delete()
    
#regex-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
    ok = False
    try:
        x = await Drone(GetParticipantRequest(channel=FORCESUB_UN, participant=int(id)))
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
    
