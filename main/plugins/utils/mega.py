#tg:ChauhanMahesh/DroneBots
#Github.com/vasusen-code

from datetime import datetime as dt
from mega import Mega as x
import os

#download mega files
#return the name of files as list
def mega_dl():
    d = dt.now().isoformat("_", "seconds")
    xx = x()
    m = xx.login()
    m.download_url(url, f'./{d}/')
    content = os.listdir(f'./{d}/')
    return content
    
    
