import logging
import boto3
from botocore.exceptions import ClientError
import os
import sys
import threading


class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
#    s3_client = boto3.client('s3')

    s3_client = boto3.client(
            service_name='s3',
            region_name='eu-west-2',
            aws_access_key_id='MY_ACCESS_KEY_ID',
            aws_secret_access_key='MY_SECRET_ACCESS_KEY',
            )

    try:
        response = s3_client.upload_file(file_name, bucket, object_name, Callback=ProgressPercentage(file_name))
    except ClientError as e:
        logging.error(e)
        return False
    return True


if __name__ == '__main__':
    assert(len(sys.argv) == 3), \
            'Usage: python upload_to_s3.py [BUCKET_NAME] [SOURCE_DIRECTORY]'
    bucket_name = sys.argv[1]
    src_dir = sys.argv[2]
    assert(os.path.exists(src_dir)), \
            f'Source directory {src_dir} not found!'
    
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            upload_file(os.path.join(root,file), bucket_name)

    '''
    upload_file('../data/youtube_bb_test.zip', 'youtube-bb-videos')
    upload_file('../data/youtube_bb_train.zip', 'youtube-bb-videos')
    upload_file('../data/youtube_bb_trainval.zip', 'youtube-bb-videos')
    #upload_file('../data/class-decodes-absents.tar.gz', 'youtube-bb-videos')
    #upload_file('../data/class-decodes.tar.gz', 'youtube-bb-videos')
    #upload_file('../youtubebb2017voc.tar.gz', 'youtube-bb-videos')
    '''
