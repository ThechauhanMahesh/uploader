#TG:ChauhanMahesh/DroneBots
#Github.com/vasusen-code

import re, asyncio, os
import gdown
import yt_dlp
from mega import Mega
from requests import get
from bs4 import BeautifulSoup

#Downloaders

#download from mediafire-----------------------------------------------------------------------------------------
def mediafire(url):
    try:
        link = re.findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
    except IndexError:
        return False
    page = BeautifulSoup(get(link).content, 'lxml')
    info = page.find('a', {'aria-label': 'Download file'})
    real_link = info.get('href')
    weburl(real_link)
 
#download mega files------------------------------------------------------------------------------------
def mega_dl(url):
    m = Mega().login()
    file = m.download_url(url) 
    return str(Path(str(file)))

#download files from drive---------------------------------------------------------------------------------------
def drive(link):
    if 'https://drive.google.com/file/' in link:
        file = gdown.download(link, quiet=True, fuzzy=True)
        return file
    elif 'https://drive.google.com/uc?id=' in link:
        file = gdown.download(link, quiet=True)
        return file
    elif 'id=' in link:
        new_link = f'https://drive.google.com/uc?id={(link.split("id="))[1]}'
        file = gdown.download(new_link, quiet=True)
        return file
    else:
        return None
        
#Download videos from youtube-------------------------------------------------------------------------------------------
async def download_from_youtube(url):
    await bash(f'yt-dlp -f best --no-warnings --prefer-ffmpeg {url}')
    o, e = await bash(f'yt-dlp -f best --get-filename {url}')
    with yt_dlp.YoutubeDL({'format': 'best'}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None) 
        video_ext = info_dict.get('ext', None) 
        file = f"{video_title}.{video_ext}"
        os.rename(f"{o}", file) 
        return file
    
#for ytdlp supported sites ------------------------------------------------------------------------------------------
async def bash(cmd):
    cmd_ = cmd.split()
    process = await asyncio.create_subprocess_exec(*cmd_, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate() 
    e = stderr.decode().strip()
    o = stdout.decode().strip()
    return o, e

async def ytdl(url):
    if 'HLS' in url:
        await bash(f'yt-dlp -f best --no-warnings --hls-prefer-ffmpeg {url}')
    elif 'm3u8' in url:
        await bash(f'yt-dlp -f best --no-warnings --hls-prefer-ffmpeg {url}')
    else:
        await bash(f'yt-dlp -f best --prefer-ffmpeg --no-warnings {url}')
    o, e = await bash(f'yt-dlp -f best --get-filename {url}')
    with yt_dlp.YoutubeDL({'format': 'best'}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', None) 
        extension = info_dict.get('ext', None) 
        file = f"{title}.{extension}"
        os.rename(f"{o}", file) 
        return file
    
#weburl download------------------------------------------------------------------------------
#Does the url contain a downloadable resource
def is_downloadable(url):
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

#Get filename from content-disposition
def get_filename_from_cd(cd):
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]
  
def weburl(url):
    x = is_downloadable(url)
    if x is False:
        return None
    elif x is True:
        pass
    else:
        return None
    r = requests.get(url, allow_redirects=True)
    filename = get_filename_from_cd(r.headers.get('content-disposition'))
    open(filename, 'wb').write(r.content)
    return filename
