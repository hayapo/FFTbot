import os, sys, datetime, re, random
from time import sleep
import numpy as np
import requests,shutil
from logging import Handler, getLogger, StreamHandler, FileHandler, DEBUG, Formatter
from twython import Twython, TwythonError
import src.fourier_transform 
import src.highpass
import src.lowpass

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

IMG_DIR = './images/'
RESULT = './results/figure.png'
keyword = 'https://t.co/'

twitter = Twython(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

logfile = "./records/schedule_tweet_log.txt"
save_file_name = "./records/schedule_tweet_id.txt"
reply_log = "./records/reply_log.txt"

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
    #リプライの画像をダウンロードする

    #変換前画像のpath
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
        #Tweetidの取得
        with open(save_file_name, mode='r') as f:
            tweet_id = f.readline()
        
        #タイムライン上のメンションを取得
        try:
            responses = twitter.get_mentions_timeline(count=20)
        except TwythonError as e:
            logger.error(e.msg)
            sys.exit(1)

        #フォロワーかどうかを判定
        try:
            followers_ids = twitter.get_followers_ids(stringify_ids=True)
        except TwythonError as e:
            logger.error(e.msg)
            sys.exit(1)
        
        #返信リストを取得
        with open(reply_log, mode='r') as f:
            alreadylist = f.readlines()
        alreadylist = [name.rstrip('\n') for name in alreadylist]
        replylist = alreadylist

        #返信処理
        for response in responses:
            #メンションの判定
            if response['in_reply_to_status_id_str'] == tweet_id :
                #名前のセット
                usr = response['user']['id_str']
                #フォロワーであれば返信
                if usr in followers_ids['ids'] :
                    #画像つきの返信か&リプライ済みかの判定
                    if keyword in response['text'] and not usr in replylist:
                        #画像URLの取得
                        source = response['extended_entities']['media'][0]['media_url_https']
                        #ダウンロード関数の呼び出し
                        img_download(source)
                        #変換オプションの判定
                        if 'ハイ' in response['text']:
                            src.highpass.highpass_fft()
                        elif 'ロー' in response['text']:
                            src.lowpass.lowpass_fft()
                        else:
                            src.fourier_transform.fft()
                        #画像をつけて返信する
                        doReply(response,RESULT)

                        #各ディレクトリの初期化
                        shutil.rmtree('images')
                        shutil.rmtree('results')
                        os.mkdir('images')
                        os.mkdir('results')

                        #返信したユーザーをリストに格納
                        replylist.append(usr)
                        
        #返信リストを更新
        with open(reply_log, mode='w') as f:     
            f.write('\n'.join(replylist))
        sleep(100)

def doReply(response,reply_path):
    #リプライ実行関数
    
    #名前の設定
    name = response['user']['name']
    usr_screen_name = response['user']['screen_name']
    if name == "" :
        name = usr_screen_name
    
    #返信のテキスト
    text = "@" + usr_screen_name + "\nフーリエ変換の結果です。"

    try:
        #返信の実行

        #結果画像
        image = open(reply_path, 'rb')

        #画像アップロード
        responseimg = twitter.upload_media(media=image)

        #返信
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