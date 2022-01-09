#tg:ChauhanMahesh/DroneBots
#Github.com/vasusen-code

#download mega files
def mega_dl(url):
    from datetime import datetime as dt
    from mega import Mega as x
    d = dt.now().isoformat("_", "seconds")
    xx = x()
    m = xx.login()
    file = m.download_url(url)
    return file


    
    
