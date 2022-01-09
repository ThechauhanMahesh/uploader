#tg:ChauhanMahesh/DroneBots
#Github.com/vasusen-code

from datetime import datetime as dt
from mega import Mega as x

#download mega files
def mega_dl(url):
    d = dt.now().isoformat("_", "seconds")
    xx = x()
    m = xx.login()
    file = m.download_url(url)
    return file
    
    
