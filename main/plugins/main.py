#tg:ChauhanMahesh/DroneBots
#github.com/vasusen-code

import os, time, asyncio
from datetime import datetime

from .. import Drone
from main.plugins.gdown import 
from main.plugins.direct_dl import mega_dl, mediafire, drive
from main.plugins.utils.utils import get_link, force_sub, upload
from LOCAL.localisation import link_animated, down_sticker, SUPPORT_LINK, forcesubtext

from ethon.uploader import weburl, ytdl, download_from_youtube

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
    await asyncio.sleep(600)
    list2.pop(int(timer.index(f'{now}')))
    list1.pop(int(process1.index(f'{event.sender_id}')))
    
#check time left in timer
async def check_timer(event, list1, list2):
    if f'{event.sender_id}' in list1:
        index = list1.index(f'{event.sender_id}')
        last = list2[int(index)]
        present = time.time()
        return False, f"You have to wait {600-round(present-float(last))} seconds more to start a new process!"
    else:
        return True, None
    
# -------------------------------------------------------------------------------------------------------------------------------------------
    
@Drone.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def u(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    link = get_link(event.text)
    if not link:
        return 
    if 'drive.google.com' or 'drive' in link: 
        if 'folder' in link:
            return
        await upload_button(event, 'drive') 
    elif 'playlist' in link:
        return
    elif 'youtube' in link:
        await upload_button(event, 'youtube') 
    elif 'youtu.be' in link:
        await upload_button(event, 'youtube') 
    elif 'mega' in link:
        await upload_button(event, 'mega') 
    elif 'mediafire' in link:
        await upload_button(event, 'mediafire')
    else:
        await upload_button(event, 'upload')
        
#Callbacks-------------------------------------------------------------------------------------------------------------------------------------------
    
@Drone.on(events.callbackquery.CallbackQuery(data="drive"))
async def d(event):
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()
    await event.delete()
    file = None
    try:
        link = get_link(msg.text)
        file = drive(link)
    except Exception as e:
        await ds.delete()
        print(e)
        return await edit.edit(f"**Couldn't download file from link!**\n\ncontact [SUPPORT]({SUPPORT_LINK})")
    await ds.delete()
    if not file == False:
        await upload(file, event, edit)
    else:
        await edit.edit(f"**Couldn't download file from link!**\n\ncontact [SUPPORT]({SUPPORT_LINK})")
    await set_timer(event, process1, timer) 
    
@Drone.on(events.callbackquery.CallbackQuery(data="youtube"))
async def yt(event):
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()
    await event.delete()
    ds = await Drone.send_message(event.chat_id, file=down_sticker, reply_to=msg.id)
    edit = await Drone.send_message(event.chat_id, '**DOWNLOADING**', reply_to=msg.id)
    file = None
    try:
        link = get_link(msg.text)
        file = await download_from_youtube(link)
    except Exception as e:
        await ds.delete()
        print(e)
        return await edit.edit(f"**Couldn't download file from link!**\n\ncontact [SUPPORT]({SUPPORT_LINK})")
    await ds.delete()
    if not file == False:
        await upload(file, event, edit)
    else:
        await edit.edit(f"**Couldn't download file from link!**\n\ncontact [SUPPORT]({SUPPORT_LINK})")
    await set_timer(event, process1, timer) 
    
@Drone.on(events.callbackquery.CallbackQuery(data="mega"))
async def m(event):
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()
    await event.delete()
    ds = await Drone.send_message(event.chat_id, file=down_sticker, reply_to=msg.id)
    edit = await Drone.send_message(event.chat_id, '**DOWNLOADING**', reply_to=msg.id)
    file = None
    try:
        link = get_link(msg.text)
        file = mega_dl(link)
    except Exception as e:
        print(e)
        await ds.delete()
        return await edit.edit(f"**Couldn't download file from link!**\n\ncontact [SUPPORT]({SUPPORT_LINK})")
    await ds.delete()
    if not file == False:
        await upload(file, event, edit)
    else:
        await edit.edit(f"**Couldn't download file from link!**\n\ncontact [SUPPORT]({SUPPORT_LINK})")
    await set_timer(event, process1, timer) 
    
@Drone.on(events.callbackquery.CallbackQuery(data="mediafire"))
async def mf(event):
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()
    await event.delete()
    edit = await Drone.send_message(event.chat_id, '**DOWNLOADING**', reply_to=msg.id)
    file = None
    try:
        link = get_link(msg.text)
        file = mediafire(link)
    except Exception as e:
        print(e)
        return await edit.edit(f"**Couldn't download file from link!**\n\ncontact [SUPPORT]({SUPPORT_LINK})", buttons=None)
    await edit.edit("Download complete.", buttons=None)
    if not file == False:
        await upload(file, event, edit)
    else:
        await edit.edit(f"**Couldn't download file from link!**\n\ncontact [SUPPORT]({SUPPORT_LINK})")
    await set_timer(event, process1, timer) 
 
@Drone.on(events.callbackquery.CallbackQuery(data="upload"))
async def u(event):
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()
    await event.delete()
    ds = await Drone.send_message(event.chat_id, file=down_sticker, reply_to=msg.id)
    edit = await Drone.send_message(event.chat_id, '**DOWNLOADING**', reply_to=msg.id)
    file = None
    try:
        link = get_link(msg.text)
        try:
            x = weburl(link)
            if x is None:
                try:
                    file = await ytdl(link)
                except Exception:
                    await ds.delete()
                    return await edit.edit('Link Not supported.')
            else:
                file = x
        except Exception:
            try:
                file = await ytdl(link)
            except Exception:
                await ds.delete()
                return await edit.edit('Link Not supported.')
    except Exception as e:
        await ds.delete()
        return await edit.edit(f'An error `[{e}]` occured!\n\nContact [SUPPORT]({SUPPORT_LINK})', link_preview=False) 
    await ds.delete()
    if not file == False:
        await upload(file, event, edit)
    else:
        await edit.edit(f"**Couldn't download file from link!**\n\ncontact [SUPPORT]({SUPPORT_LINK})")
    await set_timer(event, process1, timer) 
        
