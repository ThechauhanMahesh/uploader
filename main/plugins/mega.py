#tg:ChauhanMahesh/DroneBots
#Github.com/vasusen-code

from mega import Mega 

#download mega files
def mega_dl(url):
    m = Mega().login()
    file = m.download_url(url)
    return file


    
    
