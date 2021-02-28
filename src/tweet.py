from logging import Handler, getLogger, StreamHandler, FileHandler, DEBUG, Formatter
from time import sleep
from requests_oauthlib import OAuth1Session
import sys, os
import logging
from datetime import datetime, timedelta, timezone
from twython import Twython, TwythonError

CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

# タイムゾーンの生成
JST = timezone(timedelta(hours=+9), 'JST')

S3_BUCKET = os.environ.get('S3_BUCKET')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS')
AWS_REGION_NAME = os.environ.get('AWS_REGION')
S3_BUCKET = os.environ.get('S3_BUCKET')

twitter = Twython(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

logfile = "./record/schedule_tweet_log.txt"
save_file_name = "./record/schedule_tweet_id.txt"
reply_log = "./record/reply_log.txt"

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
    DIFF_JST_FROM_UTC = 9
    dt_now = datetime.utcnow() + timedelta(hours=DIFF_JST_FROM_UTC)
    dt_now = dt_now.strftime('%Y年%m月%d日 %H:%M')
    text = "【定期投稿】\n{0}\n FFT_botです\nこのアカウントに画像をつけてリプライすると\nフーリエ変換した後の画像を返信します\n文章に「ハイ」を入れるとハイパスフィルタ\n「ロー」を入れるとローパスフィルタ\nそれ以外は普通にフーリエ変換した画像を返信します".format(dt_now)

    try:
        response = twitter.update_status(status=text)
    except TwythonError as e:
        logger.error(e.msg)
        sys.exit(0)
    else:
        logger.info("定期投稿完了: \n{0}".format(text))
        '''
        session = boto3.session.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
        )
        s3 = session.resource('s3')
        bucket = s3.Bucket(S3_BUCKET)
        bucket.download_file('schedule_tweet_id.txt', save_file_name)
        '''
        with open(save_file_name,mode='w') as f:
            f.write(response['id_str'])
        #bucket.upload(save_file_name, 'schedule_tweet_id.txt')
        with open(reply_log, mode='w') as f:
            pass
        #bucket.upload(reply_log, 'reply_log.txt')

if __name__ == '__main__':
    tweet()