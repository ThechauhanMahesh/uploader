
from telethon import errors, events

# Forcesub
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

async def force_sub(id):
    try:
        x = await bot(GetParticipantRequest(channel=FSUB, participant=int(id)))
        left = x.stringify()
        if 'left' in left:
            ok = True
        else:
            ok = False
    except UserNotParticipantError:
        ok = True 
    return ok   
