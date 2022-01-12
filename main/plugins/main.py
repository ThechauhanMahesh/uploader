#tg:ChauhanMahesh/DroneBots
#github.com/vasusen-code

import os
import time
import asyncio
from .. import Drone
from datetime import datetime
from telethon import events, Button
from main.plugins.external import drive, mfdl, mega_dl
from ethon.uploader import weburl, ytdl, download_from_youtube
from main.plugins.magnet.aria2c import install_aria2c, aria_start, check_progress_for_dl
from main.plugins.utils.utils import get_link, upload_file, force_sub, upload_as_file
from LOCAL.localisation import link_animated, down_sticker, SUPPORT_LINK, forcesubtext

install_aria2c()
aria2p_client = aria_start()

process1 = []
timer = []

async def upload_button(event, data):
    await event.client.send_message(event.chat_id, file=link_animated, reply_to=event.id, buttons=[[Button.inline("Upload.", data=data)]])

@Drone.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def u(event):
    link = get_link(event.text)
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    if 'magnet' == (event.text).split(":")[0]:
        await upload_button(event, 'magnet')
    elif 'drive.google.com' in link: 
        await upload_button(event, 'drive') 
    elif 'playlist' in link:
        return
    elif 'herokuapp' in link:
        return await event.reply("Support of this site is removed to reduce load because of it's slow download speed.")
    elif 'youtube' in link:
        await upload_button(event, 'yt') 
    elif 'youtu.be' in link:
        await upload_button(event, 'yt') 
    elif 'mega' in link:
        await upload_button(event, 'mega') 
    elif 'mediafire' in link:
        await upload_button(event, 'mf')
    else:
        if link:
            await upload_button(event, 'upload')
        else:
            return
        
@Drone.on(events.callbackquery.CallbackQuery(data="drive"))
async def d(event):
    if f'{event.sender_id}' in process1:
        index = process1.index(f'{event.sender_id}')
        last = timer[int(index)]
        present = time.time()
        return await event.answer(f"You have to wait {120-round(present-float(last))} seconds more to start a new process!", alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()
    await event.delete()
    await drive(event, msg) 
    now = time.time()
    timer.append(f'{now}')
    process1.append(f'{event.sender_id}')
    await event.client.send_message(event.chat_id, 'You can start a new process again after 2 minutes.')
    await asyncio.sleep(120)
    timer.pop(int(timer.index(f'{now}')))
    process1.pop(int(process1.index(f'{event.sender_id}')))
    
@Drone.on(events.callbackquery.CallbackQuery(data="yt"))
async def yt(event):
    if f'{event.sender_id}' in process1:
        index = process1.index(f'{event.sender_id}')
        last = timer[int(index)]
        present = time.time()
        return await event.answer(f"You have to wait {120-round(present-float(last))} seconds more to start a new process!", alert=True)
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
        return await edit.edit(f"error: `{e}`\n\ncontact [SUPPORT]({SUPPORT_LINK})")
    await ds.delete()
    await upload_file(file, event, edit) 
    now = time.time()
    timer.append(f'{now}')
    process1.append(f'{event.sender_id}')
    await event.client.send_message(event.chat_id, 'You can start a new process again after 2 minutes.')
    await asyncio.sleep(120)
    timer.pop(int(timer.index(f'{now}')))
    process1.pop(int(process1.index(f'{event.sender_id}')))
    
@Drone.on(events.callbackquery.CallbackQuery(data="mega"))
async def m(event):
    if f'{event.sender_id}' in process1:
        index = process1.index(f'{event.sender_id}')
        last = timer[int(index)]
        present = time.time()
        return await event.answer(f"You have to wait {120-round(present-float(last))} seconds more to start a new process!", alert=True)
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
        await ds.delete()
        return await edit.edit(f"error: `{e}`\n\ncontact [SUPPORT]({SUPPORT_LINK})")
    await ds.delete()
    await upload_as_file(file, event, edit) 
    now = time.time()
    timer.append(f'{now}')
    process1.append(f'{event.sender_id}')
    await event.client.send_message(event.chat_id, 'You can start a new process again after 2 minutes.')
    await asyncio.sleep(120)
    timer.pop(int(timer.index(f'{now}')))
    process1.pop(int(process1.index(f'{event.sender_id}')))

@Drone.on(events.callbackquery.CallbackQuery(data="mf"))
async def mf(event):
    if f'{event.sender_id}' in process1:
        index = process1.index(f'{event.sender_id}')
        last = timer[int(index)]
        present = time.time()
        return await event.answer(f"You have to wait {120-round(present-float(last))} seconds more to start a new process!", alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()
    await event.delete()
    ds = await Drone.send_message(event.chat_id, file=down_sticker, reply_to=msg.id)
    edit = await Drone.send_message(event.chat_id, '**DOWNLOADING**', reply_to=msg.id)
    file = None
    try:
        link = get_link(msg.text)
        file = mfdl(link)
    except Exception as e:
        await ds.delete()
        return await edit.edit(f"error: `{e}`\n\ncontact [SUPPORT]({SUPPORT_LINK})")
    await ds.delete()
    await upload_as_file(file, event, edit) 
    now = time.time()
    timer.append(f'{now}')
    process1.append(f'{event.sender_id}')
    await event.client.send_message(event.chat_id, 'You can start a new process again after 2 minutes.')
    await asyncio.sleep(120)
    timer.pop(int(timer.index(f'{now}')))
    process1.pop(int(process1.index(f'{event.sender_id}')))

@Drone.on(events.callbackquery.CallbackQuery(data="upload"))
async def u(event):
    if f'{event.sender_id}' in process1:
        index = process1.index(f'{event.sender_id}')
        last = timer[int(index)]
        present = time.time()
        return await event.answer(f"You have to wait {120-round(present-float(last))} seconds more to start a new process!", alert=True)
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
    await upload_file(file, event, edit) 
    now = time.time()
    timer.append(f'{now}')
    process1.append(f'{event.sender_id}')
    await event.client.send_message(event.chat_id, 'You can start a new process again after 2 minutes.')
    await asyncio.sleep(120)
    timer.pop(int(timer.index(f'{now}')))
    process1.pop(int(process1.index(f'{event.sender_id}')))

        
@Drone.on(events.callbackquery.CallbackQuery(data="magnet"))
async def magnet(event):
    button = await event.get_message()
    msg = await button.get_reply_message()  
    edit = await event.client.send_message(event.chat_id, "Trying to process.", reply_to=msg.id)
    download = None
    try:
        download = aria2p_client.add_magnet([msg.text], options=None)
    except Exception as e:
        return await edit.edit(str(e))
    gid = download.gid
    await check_progress_for_dl(gid, event, edit, "")
    
    
    
    
    
    
