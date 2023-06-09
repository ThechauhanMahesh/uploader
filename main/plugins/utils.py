import re
from telethon import errors, events
from telegraph import upload_file as uf
from LOCAL.localisation import SUPPORT_LINK
from main.Database.database import Database

from .. import MONGODB_URI, Drone, FORCESUB_UN
db = Database(MONGODB_URI, 'uploaderpro')

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
    
#regex-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#to get the url from event

def get_link(string):
    try:
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex,string)   
        link = [x[0] for x in url][0]
        if link:
            return link
        else:
            return False
    except Exception as e:
        print(e)
        return False
    
# Forcesub
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest


async def force_sub(id):
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
