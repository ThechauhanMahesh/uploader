#tg:ChauhanMahesh/DroneBots
#github.com/vasusen-code

from pathlib import Path
from requests import get
from asyncio import sleep
import aria2p, os, math, subprocess, asyncio
from telethon.errors.rpcerrorlist import MessageNotModifiedError

from main.plugins.utils.utils import upload_file
from .aria2c_conf import conf

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

os.system(conf)

def aria_start():  
    aria2 = aria2p.API(
        aria2p.Client(host="http://localhost", port=6800, secret="")
    )
    return aria2

def add_magnet(aria2, magnet_link):
    try:
        download = aria2.add_magnet(magnet_link, options=None)
        return True, download.gid
    except Exception as e:
        return False, "**FAILED** \n" + 'ERROR:' + str(e) + " \nPlease do not send SLOW links."

def get_new_gid(aria2, gid):
    file = aria2.get_download(gid)
    new_gid = file.followed_by_ids[0]
    print("Changing GID "+gid+" to "+new_gid)
    return new_gid
    
async def check_progress_for_dl(aria2, gid, event, edit, previous): 
    complete = False
    while not complete:
        try:
            t_file = aria2.get_download(gid)
        except:
            return False , "Download cancelled by user."
        complete = t_file.is_complete
        try:
            if t_file.error_message:
                return False, str(t_file.error_message)
            if not complete and not t_file.error_message:
                if t_file.has_failed:
                    return False, "Download cancelled!\n\nstatus- **FAILED**"
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
                    return True, Path(str(t_file.name))
                
        except aria2p.client.ClientException as e:
            if " not found" in str(e) or "'file'" in str(e):
                return False, "The Download was canceled."
            else:
                await False, "Errored due to ta client error."
            pass
        except MessageNotModifiedError:
            pass
        except RecursionError:
            t_file.remove(force=True)
            return False, "The link is dead."
        except Exception as e:
            print(str(e))
            if "not found" in str(e) or "'file'" in str(e):
                return False, "The Download was canceled."
            else:
                print(str(e))
                return False, f"Error: {str(e)}"
        
