#!/usr/bin/python3
# coding: utf-8

import os, requests, urllib.request, shutil, asyncio, re, random, tempfile

from io import BytesIO

from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeFilename, DocumentAttributeVideo, DocumentAttributeImageSize
from telethon.utils import get_input_media

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from hachoir.metadata.video import MP4Metadata

from FastTelethon.FastTelethon import upload_file

token = os.getenv("TOKEN")
app_id = int(os.getenv("APP_ID"))
app_hash = os.getenv("APP_HASH")

bot = TelegramClient('bot', app_id, app_hash).start(bot_token=token)

def get_metadata(save_path):
    metadata = extractMetadata(createParser(save_path))
    if isinstance(metadata, MP4Metadata):
        return dict(
            duration=metadata.get('duration').seconds,
            w=metadata.get('width'),
            h=metadata.get('height')
        ), metadata.get('mime_type')
    else:
        return dict(
            w=metadata.get('width'),
            h=metadata.get('height')
        ), metadata.get('mime_type')

@bot.on(events.NewMessage(pattern='/random'))
async def send_pic(event):
    chat_id = event.message.chat_id
    label = ['ssis', 'ssni', 'snis', 'soe', 'oned', 'onsd', 'ebod', 'jufe', 'juy', 'jul', 'mide', 'mifd', 'miaa', 'ipx', 'mird', 'dasd', 'pppd', 'dandy', 'dvdms', 'stars', 'sdmu', 'meyd']
    num = random.choice(label)+'-'+f'{random.randrange(1, 999):03}'
    infopage = requests.get('http://www.javlibrary.com/cn/vl_searchbyid.php?keyword={}'.format(num)).text
    cid = re.search('pics.dmm.co.jp/mono/movie/adult/(\w+)/', infopage).groups()[0]
    picurl = 'https://pics.dmm.co.jp/mono/movie/adult/'+cid+'/'+cid+'pl.jpg'
    image = BytesIO(requests.get(picurl).content)
    await bot.send_file(chat_id, image, caption=num)


@bot.on(events.NewMessage(pattern=r'/dmmpic\s*.*-\d*'))
async def send_pic(event):
    chat_id = event.message.chat_id
    num = re.sub(r'/dmmpic\s*', '', event.message.text)
    infopage = requests.get('http://www.javlibrary.com/cn/vl_searchbyid.php?keyword={}'.format(num)).text
    cid = re.search('pics.dmm.co.jp/mono/movie/adult/(\w+)/', infopage).groups()[0]
    picurl = 'https://pics.dmm.co.jp/mono/movie/adult/'+cid+'/'+cid+'pl.jpg'
    image = BytesIO(requests.get(picurl).content)
    await bot.send_file(chat_id, image)

@bot.on(events.NewMessage(pattern=r'V|v'))
async def send_vid(event):
    chat_id = event.message.chat_id
    reply_msg = await event.get_reply_message()
    num = re.match(r'.+-\d+', reply_msg.text).group()
    infopage = requests.get('http://www.javlibrary.com/cn/vl_searchbyid.php?keyword={}'.format(num)).text
    cid = re.search('pics.dmm.co.jp/mono/movie/adult/(\w+)/', infopage).groups()[0]
    cidp = cid[0]+'/'+cid[0:3]+'/'+cid
    vidurl = 'https://cc3001.dmm.co.jp/litevideo/freepv/'+cidp+'/'+cid+'_mhb_w.mp4'
    if requests.get(vidurl).status_code == 404:
        vidurl = 'https://cc3001.dmm.co.jp/litevideo/freepv/'+cidp+'/'+cid+'_dmb_w.mp4'
        if requests.get(vidurl).status_code == 404:
            cid = cid[:-5]+cid[-3:]
            cidp = cid[0]+'/'+cid[0:3]+'/'+cid
            vidurl = 'https://cc3001.dmm.co.jp/litevideo/freepv/'+cidp+'/'+cid+'_mhb_w.mp4'
            if requests.get(vidurl).status_code == 404:
                vidurl = 'https://cc3001.dmm.co.jp/litevideo/freepv/'+cidp+'/'+cid+'_dmb_w.mp4'
    temp_dir = tempfile.TemporaryDirectory()
    save_path = temp_dir.name+'/'+cid+'.mp4'
    with urllib.request.urlopen(vidurl) as response, open(save_path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    metadata, mime_type = get_metadata(save_path)
    with open(save_path, 'rb') as f:
        input_file = await upload_file(bot, f)
    input_media = get_input_media(input_file)
    input_media.attributes = [
        DocumentAttributeVideo(round_message=False, supports_streaming=True, **metadata),
        DocumentAttributeFilename(os.path.basename(save_path)),
    ]
    input_media.mime_type = mime_type
    await bot.send_file(chat_id, input_media)
    temp_dir.cleanup()

@bot.on(events.NewMessage(pattern=r'/dmmvid\s*.+-\d+'))
async def send_vid(event):
    chat_id = event.message.chat_id
    num = re.sub(r'/dmmvid\s*', '', event.message.text)
    infopage = requests.get('http://www.javlibrary.com/cn/vl_searchbyid.php?keyword={}'.format(num)).text
    cid = re.search('pics.dmm.co.jp/mono/movie/adult/(\w+)/', infopage).groups()[0]
    cidp = cid[0]+'/'+cid[0:3]+'/'+cid
    vidurl = 'https://cc3001.dmm.co.jp/litevideo/freepv/'+cidp+'/'+cid+'_mhb_w.mp4'
    if requests.get(vidurl).status_code == 404:
        vidurl = 'https://cc3001.dmm.co.jp/litevideo/freepv/'+cidp+'/'+cid+'_dmb_w.mp4'
        if requests.get(vidurl).status_code == 404:
            cid = cid[:-5]+cid[-3:]
            cidp = cid[0]+'/'+cid[0:3]+'/'+cid
            vidurl = 'https://cc3001.dmm.co.jp/litevideo/freepv/'+cidp+'/'+cid+'_mhb_w.mp4'
            if requests.get(vidurl).status_code == 404:
                vidurl = 'https://cc3001.dmm.co.jp/litevideo/freepv/'+cidp+'/'+cid+'_dmb_w.mp4'
    temp_dir = tempfile.TemporaryDirectory()
    save_path = temp_dir.name+'/'+cid+'.mp4'
    with urllib.request.urlopen(vidurl) as response, open(save_path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    metadata, mime_type = get_metadata(save_path)
    with open(save_path, 'rb') as f:
        input_file = await upload_file(bot, f)
    input_media = get_input_media(input_file)
    input_media.attributes = [
        DocumentAttributeVideo(round_message=False, supports_streaming=True, **metadata),
        DocumentAttributeFilename(os.path.basename(save_path)),
    ]
    input_media.mime_type = mime_type
    await bot.send_file(chat_id, input_media)
    temp_dir.cleanup()

if __name__ == '__main__':
    bot.start()
    bot.run_until_disconnected()
