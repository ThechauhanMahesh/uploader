#tg:chauhanMahesh/DroneBots
#github.com/vasusen-code

import heroku3 
from .. import Drone, AUTH_USERS, ACCESS_CHANNEL, MONGODB_URI
from telethon import events 
from decouple import config
from main.Database.database import Database
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telegraph import upload_file

def mention(name, id):
    return f'[{name}](tg://user?id={id})'

#Database command handling--------------------------------------------------------------------------

db = Database(MONGODB_URI, 'uploaderpro')

@Drone.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def incomming(event):
    await event.forward_to(int(ACCESS_CHANNEL))
    if not await db.is_user_exist(event.sender_id):
        await db.add_user(event.sender_id)
    
@Drone.on(events.NewMessage(incoming=True, from_users=AUTH_USERS , pattern="/users"))
async def listusers(event):
    xx = await event.reply("Counting total users in Database.")
    x = await db.total_users_count()
    await xx.edit(f"Total user(s) {int(x)}")
    
@Drone.on(events.NewMessage(incoming=True, from_users=AUTH_USERS , pattern="^/disallow (.*)" ))
async def bban(event):
    c = event.pattern_match.group(1)
    if not c:
        await event.reply("Disallow who!?")
    AUTH = config("AUTH_USERS", default=None)
    admins = []
    admins.append(f'{int(AUTH)}')
    if c in admins:
        return await event.reply("I cannot ban an AUTH_USER")
    xx = await db.is_banned(int(c))
    if xx is True:
        return await event.reply("User is already disallowed!")
    else:
        await db.banning(int(c))
        await event.reply(f"{c} is now disallowed.")
    admins.remove(f'{int(AUTH)}')
    
@Drone.on(events.NewMessage(incoming=True, from_users=AUTH_USERS , pattern="^/allow (.*)" ))
async def unbban(event):
    xx = event.pattern_match.group(1)
    if not xx:
        await event.reply("Allow who?")
    xy = await db.is_banned(int(xx))
    if xy is False:
        return await event.reply("User is already allowed!")
    await db.unbanning(int(xx))
    await event.reply(f"{xx} Allowed! ")
   
@Drone.on(events.NewMessage(incoming=True, from_users=AUTH_USERS, pattern="^/msg (.*)"))
async def msg(event):
    ok = await event.get_reply_message()
    if not ok:
        await event.reply("Reply to the message you want to send!")
    user = event.pattern_match.group(1)
    if not user:
        await event.reply("Give the user id you want me to send message. ")
    await Drone.send_message(int(user) , ok )
    await event.reply("Messsage sent.")
    
#Listing--------------------------------------------------------------------------------------------------------------

#Not in use
def one_trial_queue(id, List1):
    if f'{id}' in List1:
        return False
    
#Not in use
def two_trial_queue(id, List1, List2):
    if not f'{id}' in List1:
        List1.append(f'{id}')
    else:
        if not f'{id}' in List2:
            List2.append(f'{id}')
        else:
            return False

#Not in use        
def ps_queue(id, media, List1, List2):
    List1.append(f'{id}')
    List2.append(media)
    if not len(List1) < 2:
        return 'EMPTY'
    if len(List1) > 2:
        return 'FULL'

    

   
    
