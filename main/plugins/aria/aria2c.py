import asyncio, aria2p, logging, os
from telethon.tl.types import KeyboardButtonCallback
from telethon.errors.rpcerrorlist import MessageNotModifiedError
from functools import partial

# referenced from public leech
aloop = asyncio.get_event_loop()

async def aria_start():
    aria2_daemon_start_cmd = []
    # start the daemon, aria2c command
    aria2_daemon_start_cmd.append("aria2c")
    aria2_daemon_start_cmd.append("--allow-overwrite=true")
    aria2_daemon_start_cmd.append("--daemon=true")
    aria2_daemon_start_cmd.append("--enable-rpc")
    aria2_daemon_start_cmd.append("--disk-cache=0")
    aria2_daemon_start_cmd.append("--follow-torrent=false")
    aria2_daemon_start_cmd.append("--max-connection-per-server=10")
    aria2_daemon_start_cmd.append("--min-split-size=10M")
    aria2_daemon_start_cmd.append("--rpc-listen-all=true")
    aria2_daemon_start_cmd.append(f"--rpc-listen-port=8100")
    aria2_daemon_start_cmd.append("--rpc-max-request-size=1024M")
    aria2_daemon_start_cmd.append("--seed-ratio=0.0")
    aria2_daemon_start_cmd.append("--seed-time=1")
    aria2_daemon_start_cmd.append("--split=10")
    aria2_daemon_start_cmd.append(f"--bt-stop-timeout=100")
    aria2_daemon_start_cmd.append(f"--max-tries=10")
    aria2_daemon_start_cmd.append(f"--retry-wait=2")
    process = await asyncio.create_subprocess_exec(
        *aria2_daemon_start_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    print(stdout)
    print(stderr)
    arcli = await aloop.run_in_executor(None, partial(aria2p.Client, host="http://localhost", port=8100, secret=""))
    aria2 = await aloop.run_in_executor(None, aria2p.API, arcli)

    return aria2

async def add_magnet(aria_instance, magnetic_link, c_file_name):
    try:
        download = await aloop.run_in_executor(None, aria_instance.add_magnet, magnetic_link)
    except Exception as e:
        return False, "**FAILED** \n" + str(e) + " \nPlease do not send SLOW links. Read /help"
    return True, "" + download.gid + ""


async def add_torrent(aria_instance, torrent_file_path):
    if torrent_file_path is None:
        return False, "**FAILED** \n\nsomething went wrong when trying to add <u>TORRENT</u> file"
    if os.path.exists(torrent_file_path):
        # Add Torrent Into Queue
        try:

            download = await aloop.run_in_executor(None, partial(aria_instance.add_torrent, torrent_file_path, uris=None, options=None, position=None))

        except Exception as e:
            return False, "**FAILED** \n" + str(e) + " \nPlease do not send SLOW links. Read /help"
        return True, "" + download.gid + ""
    else:
        return False, "**FAILED** \n" + str(e) + " \nPlease try other sources to get workable link"


async def add_url(aria_instance, text_url, c_file_name):
    uris = [text_url]
    # Add URL Into Queue
    try:
        
        download = await aloop.run_in_executor(None, aria_instance.add_uris, uris)

    except Exception as e:
        return False, "**FAILED** \n" + str(e) + " \nPlease do not send SLOW links. Read /help"
    return True, "" + download.gid + ""

async def check_metadata(aria2, gid):
    file = await aloop.run_in_executor(None, aria2.get_download, gid)
    if not file.followed_by_ids:
        return None
    new_gid = file.followed_by_ids[0]
    print("Changing GID " + gid + " to " + new_gid)
    return new_gid

async def remove_dl(gid):
    aria2 = await aria_start()
    try:
        downloads = await aloop.run_in_executor(None, aria2.get_download, gid)
        downloads.remove(force=True, files=True)
    except Exception as e:
        print(e)
        pass
      
      
      
      
