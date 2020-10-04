from credential import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import os, sys, datetime, re, random
from time import sleep
import numpy as np
import requests,shutil
from logging import Handler, getLogger, StreamHandler, FileHandler, DEBUG, Formatter
from twython import Twython, TwythonError
from fourier_transform import fft
from highpass import highpass_fft
from lowpass import lowpass_fft

IMG_DIR = './images/'
RESULT = './results/figure.png'
keyword = 'https://t.co/'

twitter = Twython(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

logfile = "./schedule_tweet_log.txt"
save_file_name = "schedule_tweet_id.txt"
reply_log = "reply_log.txt"

logger = getLogger(__name__)
handler1 = StreamHandler()
handler1.setFormatter(Formatter("%(asctime)s %(levelname)8s %(message)s"))
handler2 = FileHandler(logfile)
handler2.setLevel(DEBUG)
handler2.setFormatter(Formatter("%(asctime)s %(levelname)8s %(message)s"))
logger.setLevel(DEBUG)
logger.addHandler(handler1)
logger.addHandler(handler2)
logger.propagate = False

def img_download(url):
    path = IMG_DIR + 'before.png'
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                f.write(r.content)
    except:
        print("Downloading Error")
        sys.exit(1)
    return path

def main():
    while True:
        with open(save_file_name, mode='r') as f:
            tweet_id = f.readline()
        try:
            responses = twitter.get_mentions_timeline(count=20)
        except TwythonError as e:
            logger.error(e.msg)
            sys.exit(1)

        try:
            followers_ids = twitter.get_followers_ids(stringify_ids=True)
        except TwythonError as e:
            logger.error(e.msg)
            sys.exit(1)
        with open(reply_log, mode='r') as f:#返信リストを取得
            alreadylist = f.readlines()
        alreadylist = [name.rstrip('\n') for name in alreadylist]
        replylist = alreadylist

        for response in responses:
            if response['in_reply_to_status_id_str'] == tweet_id :
                usr = response['user']['id_str']
                if usr in followers_ids['ids'] :
                    if keyword in response['text'] and not usr in replylist:
                        source = response['extended_entities']['media'][0]['media_url_https']
                        print(source)
                        img_download(source)
                        if 'ハイ' in response['text']:
                            highpass_fft()
                        elif 'ロー' in response['text']:
                            lowpass_fft()
                        else:
                            fft()
                        doReply(response,RESULT)
                        shutil.rmtree('images')
                        shutil.rmtree('results')
                        os.mkdir('images')
                        os.mkdir('results')
                        replylist.append(usr)
        with open(reply_log, mode='w') as f:     #返信リストのファイルを更新
            f.write('\n'.join(replylist))
        sleep(100)

def doReply(response,reply_path):
    name = response['user']['name']
    usr_screen_name = response['user']['screen_name']
    if name == "" :
        name = usr_screen_name
    text = "@" + usr_screen_name + "\nフーリエ変換の結果です。"
    try:
        image = open(reply_path, 'rb')
        responseimg = twitter.upload_media(media=image)
        twitter.update_status(status=text, in_reply_to_status_id=response['id'], auto_populate_reply_metadata=True, media_ids=[responseimg['media_id']])
        logger.info("返信しました: \n{0}\n添付画像: {1}".format(text, reply_path))
    except TwythonError as te:
        logger.error(te.msg)
        sys.exit(1)
    except FileNotFoundError as fe:
        logger.error(fe)
        sys.exit(1)

if __name__ == '__main__':
    main()