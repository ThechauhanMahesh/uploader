# (c) MaheshChauhan
# Github.com/vasusen-code

import asyncio
import heroku3
from mega import Mega
import mediafire_dl
from datetime import datetime as dt
from telethon import events

from ... import HEROKU_API, HEROKU_APP_NAME

#Downloaders-------------------------------------------------------------------------------------------------------------

#download from mediafire
def mfdl(url, id):
    output = url.split("/")[-1]
    mediafire_dl.download(url, output, sender_id=id, quiet=False)
    return output

#download mega files
def mega_dl(url):
    m = Mega().login()
    path = f'./{dt.now().isoformat("_", "seconds")}/'
    os.mkdir(path)
    m.download_url(url, path) 
    file = (os.listdir(path))[0]
    return str(path + '/' + file)

#Progress for ext-dl and gdown--------------------------------------------------------------------------------------------------

""" This is the worst way someone could get a progress bar 
   for progress made by third party packages. """


def get_progress(proc):
    a = []
    app = (heroku3.from_key(HEROKU_API)).app(HEROKU_APP_NAME)
    lines = str(app.get_log()).split(f"{proc}:")
    for line in lines:
        a.append(line)
     
    data =  (str(a.pop(-1))).split("]")[0] 
    
    progress = data.split("|")[1] + "|" + data.split("|")[0]
    gross = (str(data.split("|")[2])).split("[")[0]
    speed =(str(data.split(",")[1])).split("]")[0]

    msg = f"**DOWNLOADING FILE:**\n\n**{progress}**\n\nGROSS: {gross}\n\nSPEED: {speed}\n\nETA: N/A"
    
    return msg

