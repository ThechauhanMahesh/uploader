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
def mega_dl(url, sender_id):
    m = Mega().login()
    path = f'./{dt.now().isoformat("_", "seconds")}/'
    os.mkdir(path)
    m.download_url(url, path, sender_id=sender_id) 
    file = (os.listdir(path))[0]
    return str(path + '/' + file)
