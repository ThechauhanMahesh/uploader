import os, time, asyncio, traceback
from datetime import datetime

from .. import Drone
from main.plugins.downloaders import mega_dl, mediafire, drive
from main.plugins.downloaders import download_from_youtube, ytdl, weburl
from main.plugins.uploader import upload
from main.plugins.utils import get_link, force_sub
from LOCAL.localisation import link_animated, down_sticker, SUPPORT_LINK, forcesubtext

from telethon import events, Button

process1 = []
timer = []

#Handy candy-------------------------------------------------------------------------------------------------------------------------------------------

async def upload_button(event, data):
    await event.client.send_message(event.chat_id, file=link_animated, reply_to=event.id, buttons=[[Button.inline("Upload.", data=data)]])

#Set timer to avoid spam
async def set_timer(event, list1, list2):
    now = time.time()
    list2.append(f'{now}')
    list1.append(f'{event.sender_id}')
    await event.client.send_message(event.chat_id, 'You can start a new process again after 10 minutes.')
    await asyncio.sleep(10)
    list2.pop(int(timer.index(f'{now}')))
    list1.pop(int(process1.index(f'{event.sender_id}')))
    
#check time left in timer
async def check_timer(event, list1, list2):
    if f'{event.sender_id}' in list1:
        index = list1.index(f'{event.sender_id}')
        last = list2[int(index)]
        present = time.time()
        return False, f"You have to wait {10-round(present-float(last))} seconds more to start a new process!"
    else:
        return True, None
    
# -------------------------------------------------------------------------------------------------------------------------------------------
    
def download(link):
    link_ = link.lower()
    if 'drive.google.com' or 'drive' in link_: 
        if 'folder' in link_:
            return
        else:
            return drive(link)
    elif 'playlist' in link_:
        return
    elif 'youtube' in link_ or 'youtu.be' in link_:
        return download_from_youtube(link)
    elif 'mega' in link_:
        return mega_dl(link)
    elif 'mediafire' in link_:
        return mediafire(link)
    else:
        'unkown'

async def unkown_download(link):
    file = None
    try:
        x = weburl(link)
        if x is None:
            return await ytdl(link)
        else:
            return x
    except:
        traceback.print_exc()
        return await ytdl(link)
              
#Callbacks-------------------------------------------------------------------------------------------------------------------------------------------
    
@Drone.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def u(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    link = get_link(event.text)
    if not link:
        return 
    await upload_button(event, "run")

@Drone.on(events.callbackquery.CallbackQuery(data="run"))
async def down_load(event):
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()
    await event.delete()
    ds = await Drone.send_message(event.chat_id, file=down_sticker, reply_to=msg.id)
    edit = await Drone.send_message(event.chat_id, '**DOWNLOADING**', reply_to=msg.id)
    file = None
    link = msg.text
    try:
        file = download(link)
        if file == "unkown":
            file = await unkown_download(link)
    except:
        traceback.print_exc()
        await ds.delete()
        return await edit.edit(f"**Couldn't download file from link!**\n\ncontact [SUPPORT]({SUPPORT_LINK})")
    await ds.delete()
    if file == None:
        return await edit.edit(f"**Couldn't download file from link!**\n\ncontact [SUPPORT]({SUPPORT_LINK})")
    else:
        try:
            await upload(file, event, edit)
        except:
            traceback.print_exc()
    await set_timer(event, process1, timer) 
    
