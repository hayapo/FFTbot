from logging import Handler, getLogger, StreamHandler, FileHandler, DEBUG, Formatter
from time import sleep
from requests_oauthlib import OAuth1Session
import sys
import logging
import datetime
from twython import Twython, TwythonError
from credential import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

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

def tweet():
    '''
    10:00と19:30に定期投稿する
    reply_bot.pyで呼び出される
    '''
    dt_now = datetime.datetime.now()
    dt_now = dt_now.strftime('%Y年%m月%d日 %H:%M')
    text = "【定期投稿】\n{0}\n FFT_botです\nこのアカウントに画像をつけてリプライすると\nフーリエ変換した後の画像を返信します\n文章に「ハイ」を入れるとハイパスフィルタ\n「ロー」を入れるとローパスフィルタ\nそれ以外は普通にフーリエ変換した画像を返信します".format(dt_now)
    try:
        response = twitter.update_status(status=text)
    except TwythonError as e:
        logger.error(e.msg)
        sys.exit(0)
    else:
        logger.info("定期投稿完了: \n{0}".format(text))
        with open(save_file_name,mode='w') as f:
            f.write(response['id_str'])
        with open(reply_log, mode='w') as f:
            pass

if __name__ == '__main__':
    tweet()