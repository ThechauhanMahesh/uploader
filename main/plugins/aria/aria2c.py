
import asyncio, aria2p, os, math
from pathlib import Path
from requests import get
from asyncio import sleep
from subprocess import PIPE, Popen
from telethon.tl.types import KeyboardButtonCallback
from telethon.errors.rpcerrorlist import MessageNotModifiedError
from functools import partial
from main.plugins.utils.utils import upload_file

def subprocess_run(cmd):
    subproc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)
    talk = subproc.communicate()
    exitCode = subproc.returncode
    if exitCode != 0:
        return
    return talk

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

def aria_start():
    trackers_list = get(
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt").text.replace("\n\n", ",")
    trackers = f"{trackers_list}"
    cmd = f"aria2c \
          --enable-rpc \
          --rpc-listen-all=false \
          --rpc-listen-port=6800 \
          --max-connection-per-server=10 \
          --rpc-max-request-size=1024M \
          --check-certificate=false \
          --follow-torrent=mem \
          --seed-time=1 \
          --seed-ratio=0.01.\
          --max-overall-upload-limit=2M \
          --max-concurrent-downloads=2 \
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

def add_magnet(aria2, magnet_link):
    try:
        download = aria2.add_magnet(magnet_link, options=None)
        return True, download.gid
    except Exception as e:
        return False, "**FAILED** \n" + str(e) + " \nPlease do not send SLOW links."
      
async def check_progress_for_dl(aria2, gid, event, edit, previous): 
    complete = False
    while not complete:
        try:
            t_file = aria2.get_download(gid)
        except:
            return await edit.edit("Download cancelled by user.")
        complete = t_file.is_complete
        try:
            if t_file.error_message:
                await edit.edit(str(t_file.error_message))
                return
            if not complete and not t_file.error_message:
                if t_file.has_failed:
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
                    f"{prog_str}\n\n"
                    f"GROSS: {humanbytes(downloaded)} ~ {t_file.total_length_string()}\n\n"
                    f"SPEED: {t_file.download_speed_string()}\n\n"
                    f"ETA: {t_file.eta_string()}\n\n"
                )
                if msg != previous:
                    await edit.edit(msg)
                    previous = msg
            else:
                if complete:
                    await upload_file(Path(t_file.name), event, edit) 
        except aria2p.client.ClientException as e:
            if " not found" in str(e) or "'file'" in str(e):
                return edit.edit(f"The Download was canceled.")
            else:
                await edit.edit("Errored due to ta client error.")
            pass
        except MessageNotModifiedError:
            pass
        except RecursionError:
            t_file.remove(force=True)
            return edit.edit("The link is dead.")
        except Exception as e:
            print(str(e))
            if "not found" in str(e) or "'file'" in str(e):
                return await edit.edit("The Download was canceled.")
            else:
                print(str(e))
                return edit.edit(f"Error: {str(e)}")
        
