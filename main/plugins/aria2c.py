#Tg:ChauhanMahesh/DroneBots
#Github.com/Vasusen-code

from asyncio import sleep
import math
import os
from pathlib import Path
from subprocess import PIPE, Popen
from requests import get
from ethon.pyfunc import bash
from main.plugins.utils.utils import upload_file
from telethon import events
import aria2p

#Maybe this save from suspension of heroku acc
def install_aria2c():
    if not os.path.isdir('aria'):
        os.mkdir('aria') 
        bash('apt update') 
        bash('apt install aria2')
        print('installed aria2c.')
    else:
        pass

def humanbytes(size: float) -> str:
    """ humanize size """
    if not size:
        return ""
    power = 1024
    t_n = 0
    power_dict = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        t_n += 1
    return "{:.2f} {}B".format(size, power_dict[t_n])
   
def subprocess_run(cmd):
    subproc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)
    talk = subproc.communicate()
    exitCode = subproc.returncode
    if exitCode != 0:
        return
    return talk

install_aria2c()
def aria_start():
    trackers_list = get(
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt"
).text.replace("\n\n", ",")
    trackers = f"[{trackers_list}]"
    cmd = f"aria2c \
          --enable-rpc \
          --rpc-listen-all=false \
          --rpc-listen-port=6800 \
          --max-connection-per-server=10 \
          --rpc-max-request-size=1024M \
          --check-certificate=false \
          --follow-torrent=mem \
          --seed-time=0 \
          --max-upload-limit=1K \
          --max-concurrent-downloads=5 \
          --min-split-size=10M \
          --follow-torrent=mem \
          --split=10 \
          --bt-tracker={trackers} \
          --daemon=true \
          --allow-overwrite=true"
    process = subprocess_run(cmd)
    aria2 = aria2p.API(
        aria2p.Client(host="http://localhost", port=6800, secret="")
    )
    return aria2
aria2p_client = aria_start()

async def check_metadata(gid):
    t_file = aria2p_client.get_download(gid)
    if not t_file.followed_by_ids:
        return None
    new_gid = t_file.followed_by_ids[0]
    return new_gid

async def check_progress_for_dl(gid, event, edit, previous): 
    complete = False
    while not complete:
        try:
            t_file = aria2p_client.get_download(gid)
        except:
            return await edit.edit("Download cancelled by user.")
        complete = t_file.is_complete
        is_file = t_file.seeder
        try:
            if t_file.error_message:
                await edit.edit(str(t_file.error_message))
                return
            if not complete and not t_file.error_message:
                percentage = int(t_file.progress)
                downloaded = percentage * int(t_file.total_length) / 100
                prog_str = "**DOWNLOADING FILE:**\n[{0}{1}]".format(
                    "".join(
                        "█"
                        for i in range(math.floor(percentage / 10))
                    ),
                    t_file.progress_string(),
                )
                if is_file is None :
                   info_msg = f"**CONNECTIONS**: {t_file.connections}\n"
                else :
                   info_msg = f"**INFO.**: [ P : {t_file.connections} || S : {t_file.num_seeders} ]\n"
                msg = (
                    f"{prog_str}\n"
                    f"GROSS: {humanbytes(downloaded)} ~ {t_file.total_length_string()}\n\n"
                    f"SPEED: {t_file.download_speed_string()}\n\n"
                    f"ETA: {t_file.eta_string()}\n\n"
                    f"NAME: {t_file.name}\n"
                    f"INFO: {info_msg}\n"
                    f"GID: {gid}\n"
                )
                if msg != previous:
                    await edit.edit(msg)
                    previous = msg
            else:
                await upload_file(t_file.name, event, edit) 
            await sleep(10)
            await check_progress_for_dl(gid, event, edit, previous)
        except Exception as e:
            if "not found" in str(e) or "'file'" in str(e):
                if "Your Torrent/Link is Dead." not in edit.text:
                    await edit.edit(f"**DOWNLOAD CANCELLED :** {t_file.name}")
            elif "depth exceeded" in str(e):
                t_file.remove(force=True)
                await edit.edit(
                    f"**DOWNLOAD AUTO-CANCELLED :** {t_file.name}\nYour Torrent/Link is Dead."
                )
