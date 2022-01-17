# (c) MaheshChauhan
# Github.com/vasusen-code

from mega import Mega
import mediafire_dl

#download from mediafire
def mfdl(url):
    output = url.split("/")[-1]
    mediafire_dl.download(url, output, quiet=False)
    return output

#download mega files
def mega_dl(url):
    m = Mega().login()
    s, o = m.download_url(url) 
    return s, o


