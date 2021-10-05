#!/usr/bin/python3
# coding: utf-8

import os, requests, urllib.request, shutil, asyncio, re, random, tempfile

from pyrogram import Client, filters
from pyrogram.types import Message

token = os.getenv("TOKEN")
app_id = int(os.getenv("APP_ID"))
app_hash = os.getenv("APP_HASH")

def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename

bot = Client('bot', app_id, app_hash, bot_token=token)

@bot.on_message(filters.command('random'))
def send_randomposter(client, message):
    bot.send_chat_action(message.chat.id, "upload_photo")
    label = ['ssis', 'ssni', 'snis', 'soe', 'oned', 'onsd', 'ebod', 'jufe', 'juy', 'jul', 'mide', 'mifd', 'miaa', 'ipx', 'mird', 'dasd', 'pppd', 'dandy', 'dvdms', 'stars', 'sdmu', 'meyd']
    num = random.choice(label)+'-'+f'{random.randrange(1, 999):03}'
    infopage = requests.get('http://www.javlibrary.com/cn/vl_searchbyid.php?keyword={}'.format(num)).text
    cid = re.search('pics.dmm.co.jp/mono/movie/adult/(\w+)/', infopage).groups()[0]
    picurl = 'https://pics.dmm.co.jp/mono/movie/adult/'+cid+'/'+cid+'pl.jpg'
    image = BytesIO(requests.get(picurl).content)
    image.name = 'image.jpg'
    bot.send_photo(message.chat.id, image, caption=num)


@bot.on_message(filters.command('dmmpic'))
def send_poster(client, message):
    bot.send_chat_action(message.chat.id, "upload_photo")
    num = re.sub(r'/dmmpic\s*', '', message.text)
    infopage = requests.get('http://www.javlibrary.com/cn/vl_searchbyid.php?keyword={}'.format(num)).text
    cid = re.search('pics.dmm.co.jp/mono/movie/adult/(\w+)/', infopage).groups()[0]
    picurl = 'https://pics.dmm.co.jp/mono/movie/adult/'+cid+'/'+cid+'pl.jpg'
    image = BytesIO(requests.get(picurl).content)
    image.name = 'image.jpg'
    bot.send_photo(message.chat.id, image)

@bot.on_message(filters.regex(r'v|V') & filters.reply)
def send_vid(client, message):
    bot.send_chat_action(message.chat.id, "upload_video")
    source_msg = bot.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
    num = re.match(r'.+-\d+', source_msg.caption).group()
    result_page = requests.get('https://www.r18.com/common/search/order=match/searchword='+num+'/', headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"}).text
    try:
        vidurl = re.findall('https://.*\.mp4', result_page)[-1]
        hdvidurl = re.sub('dmb', 'mhb', vidurl)
    except:
        bot.send_message(message.chat.id, '🈚️')
        return
    try:
        video =  download_file(hdvidurl)
    except:
        video = download_file(vidurl)
    bot.send_video(message.chat.id, video, width=720, height=404)
    os.unlink(video)

@bot.on_message(filters.command('dmmvid'))
def send_vid(client, message):
    bot.send_chat_action(message.chat.id, "upload_video")
    num = re.sub(r'/dmmvid\s*', '', message.text)
    result_page = requests.get('https://www.r18.com/common/search/order=match/searchword='+num+'/', headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"}).text     
    try:
        vidurl = re.findall('https://.*\.mp4', result_page)[-1]
        hdvidurl = re.sub('dmb', 'mhb', vidurl)
    except:
        bot.send_message(message.chat.id, '🈚️')
        return
    try:
        video = download_file(hdvidurl)
    except:
        video = download_file(vidurl)
    bot.send_video(message.chat.id, video, width=720, height=404)
    os.unlink(video)

bot.run()
