from .. import Drone, ACCESS_CHANNEL, AUTH_USERS
from telethon import events, Button
from LOCAL.localisation import START_TEXT as st
from LOCAL.localisation import DEV, info_text, spam_notice, SUPPORT_LINK
from main.plugins.utils import set_thumbnail, rem_thumbnail

@Drone.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    await event.reply(st, buttons=[[Button.inline("Menu.", data="menu")]])
    
@Drone.on(events.callbackquery.CallbackQuery(data="menu"))
async def menu(event):
    await event.edit("**📑MENU.**",
                    buttons=[[
                         Button.inline("info.", data="info"),
                         Button.inline("Help", data="help")],
                         [
                         Button.inline("NOTICE.", data="notice"),
                         Button.inline("SETTINGS.", data="settings")],
                         [
                         Button.url("DEVELOPER", url=f"{DEV}")]])
    
@Drone.on(events.callbackquery.CallbackQuery(data="info"))
async def info(event):
    await event.edit(f'**ℹ️NFO:**\n\n{info_text}',
                    buttons=[[
                         Button.inline("Menu.", data="menu")]])
@Drone.on(events.callbackquery.CallbackQuery(data="notice"))
async def notice(event):
    await event.answer(spam_notice, alert=True)
    
@Drone.on(events.callbackquery.CallbackQuery(data="help"))
async def help(event):       
    await event.edit(f"Send me any kind of 🔗, and i'll try to upload it on telegram.",
                    buttons=[[
                         Button.url("SUPPORT.", url=SUPPORT_LINK)],
                         [
                         Button.inline("Menu.", data="menu")]])
    
@Drone.on(events.callbackquery.CallbackQuery(data="settings"))
async def help(event):
    await event.edit('**🛠SETTINGS.**',
                    buttons=[[
                         Button.inline("set THUMBNAIL", data="sett"),
                         Button.inline("rem THUMBNAIL", data='remt')],
                         [
                         Button.inline("restart", data="restart")],
                         [
                         Button.inline("Menu.", data="menu")]])
                    
#-----------------------------------------------------------------------------------------------                            
    
@Drone.on(events.callbackquery.CallbackQuery(data="sett"))
async def sett(event):    
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    async with Drone.conversation(event.chat_id) as conv: 
        xx = await conv.send_message("Send me any image for thumbnail.")
        try:
            x = await conv.get_response()
            if not x.media:
                return await xx.edit("No media found.")
            mime = x.file.mime_type
            if not 'png' in mime:
                if not 'jpg' in mime:
                    if not 'jpeg' in mime:
                        return await xx.edit("No image found.")
            await set_thumbnail(event, x.media)
            await xx.delete()
        except Exception:
            await xx.edit("An error occured while waiting for the response.")
        
        
@Drone.on(events.callbackquery.CallbackQuery(data="remt"))
async def remt(event):  
    await event.delete()
    await rem_thumbnail(event)
    

