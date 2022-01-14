#Tg:ChauhanMahesh/DroneBots
#Github.com/Vasusen-code

import asyncio
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

async def aria_start():
    trackers_list = get(
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt"
).text.replace("\n\n", ",")
    trackers = f"[{trackers_list}]"
    cmd = ["aria2c",
           "--enable-rpc",
           " --rpc-listen-all=false",
           "--rpc-listen-port=6800",
           "--max-connection-per-server=10",
           "--rpc-max-request-size=1600M",
           "--check-certificate=false",
           "--follow-torrent=mem",
           "--seed-time=1",
           "--seed-ratio=0.01",
           "--max-overall-upload-limit=2M",
           "--max-concurrent-downloads=2",
           "--min-split-size=10M",
           "--follow-torrent=mem",
           "--split=10",
           f"--bt-tracker={trackers}",
           "--daemon=true",
           "--allow-overwrite=true"]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    aria2 = aria2p.API(
        aria2p.Client(host="http://localhost", port=6800, secret="")
    )
    return aria2

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
                if file.has_failed:
                    return await edit.edit("Download cancelled!\n\nstatus- **FAILED**")
                percentage = int(t_file.progress)
                downloaded = percentage * int(t_file.total_length) / 100
                prog_str = "**DOWNLOADING FILE:**\n\n**[{0}] |** `{1}`".format(
                    "".join(
                        "█"
                        for i in range(math.floor(percentage / 10))
                    ),
                    t_file.progress_string(),
                )
                msg = (
                    f"{prog_str}\n"
                    f"GROSS: {humanbytes(downloaded)} ~ {t_file.total_length_string()}\n\n"
                    f"SPEED: {t_file.download_speed_string()}\n\n"
                    f"ETA: {t_file.eta_string()}\n\n"
                    f"NAME: `{t_file.name}`"
                )
                if msg != previous:
                    await edit.edit(msg)
                    previous = msg
            else:
                if complete:
                    await upload_file(Path(t_file.name), event, edit) 
        except Exception as e:
            if "not found" in str(e) or "'file'" in str(e):
                if "Your Torrent/Link is Dead." not in edit.text:
                    await edit.edit(f"**DOWNLOAD CANCELLED :** {t_file.name}")
            elif "depth exceeded" in str(e):
                t_file.remove(force=True)
                await edit.edit(
                    f"**DOWNLOAD AUTO-CANCELLED :** {t_file.name}\nYour Torrent/Link is Dead."
                )
