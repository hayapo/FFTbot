import os, boto3
S3_BUCKET = os.environ.get('S3_BUCKET')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS')
AWS_REGION_NAME = os.environ.get('AWS_REGION')
S3_BUCKET = os.environ.get('S3_BUCKET')
logfile = "./tmp/schedule_tweet_log.txt"
save_file_name = "./tmp/schedule_tweet_id.txt"
reply_log = "./tmp/reply_log.txt"

session = boto3.session.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
        )
s3 = session.resource('s3')
bucket = s3.Bucket(S3_BUCKET)
bucket.upload_file(reply_log, 'reply_log.txt')