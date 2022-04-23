#!/usr/bin/python3
# coding: utf-8

import requests, re, random

from io import BytesIO

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent

bot = Client('bot')

def get_image(url):
    image = BytesIO(requests.get(url).content) 
    image.name = 'image.jpg'
    return image

def get_video(cid):
    url = 'https://'+re.sub(r'\\', '', re.search(r'cc3001.+?.mp4', requests.get("https://www.dmm.co.jp/service/digitalapi/-/html5_player/=/cid={}/mtype=AhRVShI_/service=litevideo/mode=part/width=720/height=480/".format(cid)).text).group())
    res = requests.get(url)
    video = BytesIO(res.content)
    video.name = 'video.mp4'
    return video

@bot.on_message(filters.command('start'))
def welcome(client, message):
    text = '请直接发送番号、番号前缀、女优名（日文/英文）或任何关键字进行搜索'
    bot.send_message(message.chat.id, text)

@bot.on_message(filters.command('random'))
def send_random(client, message):
    bot.send_chat_action(message.chat.id, "upload_photo")
    url = "https://api.dmm.com/affiliate/v3/ItemList?api_id=ezuc1BvgM0f74KV4ZMmS&affiliate_id=sakuradite-999&site=FANZA&service=digital&floor=videoa&hits=50&sort=date&article=genre&article_id=4025&output=json"
    res = random.choice(requests.get(url).json()["result"]["items"])
    image = get_image(res["imageURL"]["large"])
    cid = res["content_id"]
    caption = res["title"]
    javlib_url = 'https://www.javlibrary.com/cn/vl_searchbyid.php?keyword='+re.search(r'[a-zA-Z]+\d+', cid).group()
    if res.get("sampleMovieURL"):
        if message.chat.type == 'private':
            bot.send_photo(message.chat.id, image, caption=caption, reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("预览", callback_data=cid),
            InlineKeyboardButton("Javlibrary", url=javlib_url)
            ]]))
        else:
            preview_url = 'https://'+re.sub(r'\\', '', re.search(r'cc3001.+?.mp4', requests.get("https://www.dmm.co.jp/service/digitalapi/-/html5_player/=/cid={}/mtype=AhRVShI_/service=litevideo/mode=part/width=720/height=480/".format(cid)).text).group())
            bot.send_photo(message.chat.id, image, caption=caption, reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("预览", url=preview_url),
                InlineKeyboardButton("Javlibrary", url=javlib_url)
                ]]))
    else:
        bot.send_photo(message.chat.id, image, caption=caption, reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Javlibrary", url='https://www.javlibrary.com/cn/vl_searchbyid.php?keyword='+cid)
            ]]))


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
    cid = res["content_id"]
    image = get_image(res["imageURL"]["large"])
    caption = res["title"]
    javlib_url = 'https://www.javlibrary.com/cn/vl_searchbyid.php?keyword='+re.search(r'[a-zA-Z]+\d+', cid).group()
    if res.get("sampleMovieURL"):
        preview_url = 'https://'+re.sub(r'\\', '', re.search(r'cc3001.+?.mp4', requests.get("https://www.dmm.co.jp/service/digitalapi/-/html5_player/=/cid={}/mtype=AhRVShI_/service=litevideo/mode=part/width=720/height=480/".format(cid)).text).group())
        bot.send_photo(message.chat.id, image, caption=caption, reply_to_message_id=message.message_id, reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("预览", url=preview_url),
            InlineKeyboardButton("Javlibrary", url=javlib_url)
            ]]))
    else:
        bot.send_photo(message.chat.id, image, caption=caption, reply_to_message_id=message.message_id, reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Javlibrary", url=javlib_url)
            ]]))

@bot.on_message()
def private(client, message):
    if message.chat.type != "private":
        return
    bot.send_chat_action(message.chat.id, "upload_photo")
    input = message.text or message.caption
    if re.match(r'\w+-\d+', input):
        keyword = re.sub('-', '00', re.match(r'\w+-\d+', input).group())
    else:
        keyword = message.text
    url = "https://api.dmm.com/affiliate/v3/ItemList?api_id=ezuc1BvgM0f74KV4ZMmS&affiliate_id=sakuradite-999&site=FANZA&service=digital&floor=videoa&keyword={}&sort=date&output=json".format(keyword)
    res = requests.get(url).json()["result"]["items"]
    if not res:
        bot.send_message(message.chat.id, '🈚️', reply_to_message_id=message.message_id)
        return
    info = res[0]
    image = get_image(info["imageURL"]["large"])
    cid = info["content_id"]
    caption = info["title"]
    javlib_url = 'https://www.javlibrary.com/cn/vl_searchbyid.php?keyword='+re.search(r'[a-zA-Z]+\d+', cid).group()
    extra = {}
    for i in res[1:5]:
        c = i["content_id"]
        num = re.sub(r'([a-zA-Z]+)00', r'\1-', re.search(r'[a-zA-Z]+\d+', c).group())
        extra[c] = num
    button = []
    if info.get("sampleMovieURL"):
        button.append(InlineKeyboardButton("预览", callback_data=cid))
    button.append(InlineKeyboardButton("Javlib", url=javlib_url))
    buttonlist = [button]
    if extra:
        for i in extra:
            buttonlist.append([InlineKeyboardButton(extra[i], callback_data='cid:'+i)])
    bot.send_photo(message.chat.id, image, caption=caption, reply_to_message_id=message.message_id, reply_markup=InlineKeyboardMarkup(buttonlist))

@bot.on_callback_query(filters.regex(r'^cid'))
def extra(client, callback_query):
    bot.send_chat_action(callback_query.message.chat.id, "upload_photo")
    cid = re.search(r'\w+\d+', callback_query.data).group()
    url = "https://api.dmm.com/affiliate/v3/ItemList?api_id=ezuc1BvgM0f74KV4ZMmS&affiliate_id=sakuradite-999&site=FANZA&service=digital&floor=videoa&cid={}&output=json".format(cid)
    res = requests.get(url).json()["result"]["items"][0]
    image = get_image(res["imageURL"]["large"])
    cid = res["content_id"]
    caption = res["title"]
    javlib_url = 'https://www.javlibrary.com/cn/vl_searchbyid.php?keyword='+re.search(r'[a-zA-Z]+\d+', cid).group()
    button = []
    if res.get("sampleMovieURL"):
        button.append(InlineKeyboardButton("预览", callback_data=cid))
    button.append(InlineKeyboardButton("Javlib", url=javlib_url))
    bot.send_photo(callback_query.message.chat.id, image, caption=caption, reply_markup=InlineKeyboardMarkup([button]))
    bot.answer_callback_query(callback_query.id)

@bot.on_callback_query()
def send_video(client, callback_query):
    sending = bot.send_message(callback_query.message.chat.id, "发送中。。。")
    cid = callback_query.data
    video = get_video(cid)
    bot.send_chat_action(callback_query.message.chat.id, "upload_video")
    bot.send_video(callback_query.message.chat.id, video, width=720, height=404, reply_to_message_id=callback_query.message.message_id)
    bot.delete_messages(callback_query.message.chat.id, sending.message_id)
    bot.answer_callback_query(callback_query.id)
    del video

@bot.on_inline_query()
def answer(client, inline_query):
    if not inline_query.query:
        return
    keyword = inline_query.query
    url = "https://api.dmm.com/affiliate/v3/ItemList?api_id=ezuc1BvgM0f74KV4ZMmS&affiliate_id=sakuradite-999&site=FANZA&service=digital&floor=videoa&keyword={}&sort=date&output=json".format(keyword)
    res = requests.get(url).json()["result"]["items"]
    results=[]
    for i in res[:5]:
        img = i["imageURL"]["large"]
        title = i["title"]
        url = i["URL"]
        cid = i["content_id"]
        genre = [g["name"] for g in i["iteminfo"]["genre"]]
        genres = ' '.join(genre)
        javlib_url = 'https://www.javlibrary.com/cn/vl_searchbyid.php?keyword='+re.search(r'[a-zA-Z]+\d+', cid).group()
        if i.get("sampleMovieURL"):
            preview_url = 'https://'+re.sub(r'\\', '', re.search(r'cc3001.+?.mp4', requests.get("https://www.dmm.co.jp/service/digitalapi/-/html5_player/=/cid={}/mtype=AhRVShI_/service=litevideo/mode=part/width=720/height=480/".format(cid)).text).group())
            reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("预览", url=preview_url),
            InlineKeyboardButton("Javlibrary", url=javlib_url)
            ]])
        else:
            reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Javlibrary", url=javlib_url)
            ]])
        results.append(InlineQueryResultArticle(title=title, description=genres, input_message_content=InputTextMessageContent(title+'\n'+url), thumb_url=img, reply_markup=reply_markup))
    inline_query.answer(results=results)


bot.run()
