#TG:ChauhanMahesh/DroneBots
#Github.com/vasusen-code

import re
import gdown
from mega import Mega
from requests import get
from bs4 import BeautifulSoup

#Downloaders-------------------------------------------------------------------------------------------------------------

#download from mediafire
def mediafire(url):
    try:
        link = re.findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
    except IndexError:
        return False
    page = BeautifulSoup(get(link).content, 'lxml')
    info = page.find('a', {'aria-label': 'Download file'})
    real_link = info.get('href')
    try:
        file = weburl(real_link)
        if file is not None:
            return file
        else:
            return None
    except Exception as e:
        print(e)
        return False

#download mega files
def mega_dl(url):
    try:
        m = Mega().login()
        file = m.download_url(url) 
        return str(Path(str(file)))
    except Exception as e:
        print(e)
        return False

#download files from drive
def drive(link):
    try:
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
    except Exception as e:
        print(e)
        return False
