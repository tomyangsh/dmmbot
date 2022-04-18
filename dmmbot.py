#!/usr/bin/python3
# coding: utf-8

import os, requests, json, re, random, ffmpeg

from io import BytesIO

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

token = os.getenv("TOKEN")
app_id = int(os.getenv("APP_ID"))
app_hash = os.getenv("APP_HASH")

bot = Client('bot', app_id, app_hash, bot_token=token)

def get_image(url):
    image = BytesIO(requests.get(url).content) 
    image.name = 'image.jpg'
    return image

def get_video(cid):
    url = "https://cc3001.dmm.co.jp/litevideo/freepv/{}/{}/{}/{}_mhb_w.mp4".format(cid[0], cid[:3], cid, cid)
    res = requests.get(url)
    if res.status_code == 404:
        url = re.sub(r'([a-z])00', r'\1', url)
        res = requests.get(url)
    video = BytesIO(res.content)
    video.name = 'video.mp4'
    return video

def get_metadata(video_path):
    width, height, duration = 1920, 1080, 0
    try:
        video_streams = ffmpeg.probe(video_path, select_streams="v")["streams"][0]
        height = video_streams["height"]
        width = video_streams["width"]
        duration = int(float(video_streams["duration"]))
    except Exception as e:
        print(e)
    return dict(height=height, width=width, duration=duration)


def get_thumbnail(video_path):
    thumbnail = os.path.dirname(__file__)+'/thumbnail.png'
    ff =    (
            ffmpeg
            .input(video_path, ss='1')
            .output(thumbnail, vframes=1)
            .overwrite_output()
            .run()
        )
    return thumbnail


@bot.on_message(filters.command('random'))
def send_random(client, message):
    bot.send_chat_action(message.chat.id, "upload_photo")
    url = "https://api.dmm.com/affiliate/v3/ItemList?api_id=ezuc1BvgM0f74KV4ZMmS&affiliate_id=sakuradite-999&site=FANZA&service=digital&floor=videoa&hits=50&sort=date&article=genre&article_id=4025&output=json"
    res = random.choice(requests.get(url).json()["result"]["items"])
    image = get_image(res["imageURL"]["large"])
    cid = res["content_id"]
    caption = res["title"]
    if res.get("sampleMovieURL"):
        if message.chat.type == 'private':
            bot.send_photo(message.chat.id, image, caption=caption, reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("预览", callback_data=cid)
            ]]))
        else:
            preview_url = res["sampleMovieURL"][list(res["sampleMovieURL"])[-3]]
            bot.send_photo(message.chat.id, image, caption=caption, reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("预览", url=preview_url)
                ]]))
    else:
        bot.send_photo(message.chat.id, image, caption=caption)


@bot.on_message(filters.command('dmm'))
def send_info(client, message):
    if not re.match(r'/dmm\s+.+', message.text):
            return None
    bot.send_chat_action(message.chat.id, "upload_photo")
    if re.match(r'/dmm\s+\w+-\d+', message.text):
        keyword = re.sub(r'/dmm\s+(\w+)-(\d+)', r'\g<1>00\2', message.text)
    else:
        keyword = re.sub(r'/dmm\s+(\w+)', r'\1', message.text)
    url = "https://api.dmm.com/affiliate/v3/ItemList?api_id=ezuc1BvgM0f74KV4ZMmS&affiliate_id=sakuradite-999&site=FANZA&service=digital&floor=videoa&keyword={}&sort=date&output=json".format(keyword)
    res = requests.get(url).json()["result"]["items"]
    if not res:
        bot.send_message(message.chat.id, '🈚️', reply_to_message_id=message.message_id)
        return
    res = res[0]
    image = get_image(res["imageURL"]["large"])
    caption = res["title"]
    if res.get("sampleMovieURL"):
        preview_url = res["sampleMovieURL"][list(res["sampleMovieURL"])[-3]]
        bot.send_photo(message.chat.id, image, caption=caption, reply_to_message_id=message.message_id, reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("预览", url=preview_url)
            ]]))
    else:
        bot.send_photo(message.chat.id, image, caption=caption, reply_to_message_id=message.message_id)

@bot.on_message(filters.chat(384635476))
def private(client, message):
    bot.send_chat_action(message.chat.id, "upload_photo")
    if re.match(r'\w+-\d+', message.text):
        keyword = re.sub(r'(\w+)-(\d+)', r'\g<1>00\2', message.text)
    else:
        keyword = message.text
    url = "https://api.dmm.com/affiliate/v3/ItemList?api_id=ezuc1BvgM0f74KV4ZMmS&affiliate_id=sakuradite-999&site=FANZA&service=digital&floor=videoa&keyword={}&sort=date&output=json".format(keyword)
    res = requests.get(url).json()["result"]["items"]
    if not res:
        bot.send_message(message.chat.id, '🈚️', reply_to_message_id=message.message_id)
        return
    res = res[0]
    image = get_image(res["imageURL"]["large"])
    cid = res["content_id"]
    caption = res["title"]
    if res.get("sampleMovieURL"):
        bot.send_photo(message.chat.id, image, caption=caption, reply_to_message_id=message.message_id, reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("预览", callback_data=cid)
            ]]))
    else:
        bot.send_photo(message.chat.id, image, caption=caption, reply_to_message_id=message.message_id)

@bot.on_callback_query()
def send_video(client, callback_query):
    cid = callback_query.data
    video = get_video(cid)
    bot.send_chat_action(callback_query.message.chat.id, "upload_video")
    bot.send_video(callback_query.message.chat.id, video, width=720, height=404, reply_to_message_id=callback_query.message.message_id)

bot.run()
