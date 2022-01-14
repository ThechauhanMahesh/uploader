# (c) MaheshChauhan
# Github.com/vasusen-code

from zippyshare_downloader import extract_info, extract_info_coro

#download from mediafire
def mfdl(url):
    output = url.split("/")[-1]
    mediafire_dl.download(url, output, quiet=False)
    return output

#download mega files
def mega_dl(url):
    m = Mega().login()
    path = f'./{dt.now().isoformat("_", "seconds")}/'
    os.mkdir(path)
    m.download_url(url, path) 
    file = (os.listdir(path))[0]
    return str(path + '/' + file)

def zippy_dl(url):
    # by default, parameter download is True
    file = extract_info(url, download=True)
    return file
