"""
Copyright (C) 2019 The Raphielscape Company LLC.

Licensed under the Raphielscape Public License, Version 1.c (the "License");
you may not use this file except in compliance with the License.

Helper Module containing various sites direct links generators. This module is copied and modified as per need
from https://github.com/AvinashReddy3108/PaperplaneExtended . I hereby take no credit of the following code other
than the modifications. See https://github.com/AvinashReddy3108/PaperplaneExtended/commits/master/userbot/modules/direct_links.py
for original authorship. """

from os import popen
import re
import urllib.parse
import json
from random import choice
import requests
from bs4 import BeautifulSoup
from humanize import naturalsize

def zippy_share(link):
    """ ZippyShare direct links generator
    Based on https://github.com/LameLemon/ziggy"""
    dl_url = ''
    session = requests.Session()
    base_url = re.search('http.+.com', link).group()
    response = session.get(link)
    page_soup = BeautifulSoup(response.content, "lxml")
    scripts = page_soup.find_all("script", {"type": "text/javascript"})
    for script in scripts:
        if "getElementById('dlbutton')" in script.text:
            url_raw = re.search(r'= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);',
                                script.text).group('url')
            math = re.search(r'= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);',
                             script.text).group('math')
            dl_url = url_raw.replace(math, '"' + str(eval(math)) + '"')
            break
    dl_url = base_url + eval(dl_url)
    return dl_url


def yandex_disk(link):
    """ Yandex.Disk direct links generator
    Based on https://github.com/wldhx/yadisk-direct"""
    api = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'
    dl_url = requests.get(api.format(link)).json()['href']
    return dl_url


def mega_dl(link):
    """ MEGA.nz direct links generator
    Using https://github.com/tonikelope/megadown"""
    command = f'bin/megadown -q -m {link}'
    result = popen(command).read()
    data = json.loads(result)
    print(data)
    dl_url = data['url']
    return dl_url


def cm_ru(url: str) -> str:
    """ cloud.mail.ru direct links generator
    Using https://github.com/JrMasterModelBuilder/cmrudl.py"""
    command = f'bin/cmrudl -s {link}'
    result = popen(command).read()
    result = result.splitlines()[-1]
    data = json.loads(result)
    dl_url = data['download']
    return dl_url


def mediafire(url: str) -> str:
    """ MediaFire direct links generator """
    page = BeautifulSoup(requests.get(link).content, 'lxml')
    info = page.find('a', {'aria-label': 'Download file'})
    dl_url = info.get('href')
    return dl_url


def sourceforge(url: str) -> str:
    """ SourceForge direct links generator """
    dl_url = ''
    file_path = re.findall(r'files(.*)/download', link)[0]
    project = re.findall(r'projects?/(.*?)/files', link)[0]
    mirrors = f'https://sourceforge.net/settings/mirror_choices?' \
        f'projectname={project}&filename={file_path}'
    page = BeautifulSoup(requests.get(mirrors).content, 'html.parser')
    info = page.find('ul', {'id': 'mirrorList'}).findAll('li')
    for mirror in info[1:]:
        dl_url = f'https://{mirror["id"]}.dl.sourceforge.net/project/{project}/{file_path}'
        return dl_url


def osdn(url: str) -> str:
    """ OSDN direct links generator """
    osdn_link = 'https://osdn.net'
    page = BeautifulSoup(
        requests.get(link, allow_redirects=True).content, 'lxml')
    info = page.find('a', {'class': 'mirror_link'})
    link = urllib.parse.unquote(osdn_link + info['href'])
    mirrors = page.find('form', {'id': 'mirror-select-form'}).findAll('tr')
    for data in mirrors[1:]:
        mirror = data.find('input')['value']
        dl_url = re.sub(r'm=(.*)&f', f'm={mirror}&f', link)
        return dl_url


def github(url: str) -> str:
    """ GitHub direct links generator """
    dl_url = ''
    download = requests.get(url, stream=True, allow_redirects=False)
    dl_url = download.headers["location"]
    return dl_url


def androidfilehost(url: str) -> str:
    """ AFH direct links generator """
    fid = re.findall(r'\?fid=(.*)', link)[0]
    session = requests.Session()
    user_agent = useragent()
    headers = {'user-agent': user_agent}
    res = session.get(link, headers=headers, allow_redirects=True)
    headers = {
        'origin': 'https://androidfilehost.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': user_agent,
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-mod-sbb-ctype': 'xhr',
        'accept': '*/*',
        'referer': f'https://androidfilehost.com/?fid={fid}',
        'authority': 'androidfilehost.com',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'submit': 'submit',
        'action': 'getdownloadmirrors',
        'fid': f'{fid}'
    }
    mirrors = None
    error = "`Error: Can't find Mirrors for the link`\n"
    req = session.post(
        'https://androidfilehost.com/libs/otf/mirrors.otf.php',
        headers=headers,
        data=data,
        cookies=res.cookies)
    mirrors = req.json()['MIRRORS']
    for item in mirrors:
        dl_url = item['url']
        return dl_url

