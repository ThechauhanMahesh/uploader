#Tg:ChauhanMahesh/DroneBots
#Github.com/Vasusen-code

import os, time, subprocess, asyncio, requests
from datetime import datetime as dt
from telegraph import upload_file as uf

from ... import Drone, BOT_UN, MONGODB_URI
from main.Database.database import Database
from LOCAL.localisation import SUPPORT_LINK

from ethon.telefunc import fast_upload
from ethon.pyfunc import video_metadata

video_mimes = ['mkv', 'mp4', 'MKV', 'Mkv', 'Mp4', 'MP4']

# check size 
def max_size_error(file):
    if not file == None:
        if os.path.isfile(file) == True:
            size = os.path.getsize(file)/1000000
            if size > 2000:
                os.remove(file)
                return False
        else:
            return True
    else:
        return False

# permanent thumbnail
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

# set attributes of a video file
def attributes(file):
    metadata = video_metadata(file)
    width = metadata["width"]
    height = metadata["height"]
    duration = metadata["duration"]
    if not None in [width, height, duration]:
        return [DocumentAttributeVideo(duration=duration, w=width, h=height, supports_streaming=True)]
    else:
        return [DocumentAttributeVideo(duration=0, w=1280, h=720, supports_streaming=True)]

# generate a screenshot of video

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
    metadata = video_metadata(file)
    duration = metadata["duration"]' 
    if duration == None:
        duration = 0
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
        return None       
        
# Upload a file to telegram
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
        attr = attributes(file) 
        if T is None:
            try:
                T = await screenshot(file)
            except Exception:
                T = None
        try:
            uploader = await fast_upload(file, file, time.time(), event.client, edit, f'**UPLOADING FILE**')
            await Drone.send_file(event.chat_id, uploader, caption=text, thumb=T, attributes=attr, force_document=False)
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
    try:
        os.remove(file)
    except Exception as e:
        print(e)
    await edit.delete()
    
