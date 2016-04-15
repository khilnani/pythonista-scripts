# coding: utf-8

import os
import time
from datetime import datetime
import hashlib
import logging
# boto2
import boto

############################################

# load config

############################################

BASE_DIR = os.path.expanduser('~/Documents')

############################################

def get_hash(file_path):
    # Open,close, read file and calculate MD5 on its contents
    with open(file_path) as file_to_check:
        # pipe contents of the file through
        return hashlib.md5(file_to_check.read()).hexdigest()

############################################

def setup_logging(log_level='INFO'):
    log_format = "%(message)s"
    logging.addLevelName(15, 'FINE')
    logging.basicConfig(format=log_format, level=log_level)

def get_remote_files(s3, bucket, max_files=None):
    remote_files=[]
    sync = s3.get_bucket(bucket)
    for k in sync.get_all_keys(maxkeys=max_files):
        file_hash = hashlib.md5(k.value).hexdigest()
        file_data = {
            'hash': file_hash,
            'rel': k.key}
        remote_files.append(file_data)
    return remote_files


def get_local_files(dir=BASE_DIR, local_files=[], max_files=None):
    dir_rel_path = os.path.relpath(dir, BASE_DIR)
    logging.info('> %s', dir_rel_path )
    files = os.listdir(dir)
    for file in files:
        if max_files and len(local_files) >= max_files:
            return local_files

        file_path = os.path.join(dir, file)
        rel_path = os.path.relpath(file_path, BASE_DIR)

        if not os.path.isdir(file_path) and not file.startswith('.'):
            file_name, file_ext = os.path.splitext(file)
            file_hash = get_hash(file_path)
            file_mod = os.path.getmtime(file_path)
            file_mod_dt = datetime.fromtimestamp(file_mod)
            file_data = {
                'hash': file_hash,
                'mod': file_mod,
                'dt': file_mod_dt,
                'path': file_path,
                'rel': rel_path,
                'name': file_name,
                'ext': file_ext}
            logging.info('  %s (%s)', file , file_mod_dt )
            local_files.append(file_data)
        elif os.path.isdir(file_path) and not file.startswith('.'):
            local_files = get_local_files(file_path, local_files, max_files)

    return local_files

def get_upload_list(local_files, remote_files):
    delta_files = []
    return delta_files

def get_download_list(local_files, remote_files):
    delta_files = []
    return delta_files

############################################

def main():
    setup_logging()

    s3 = boto.connect_s3()

    # check if bucket exists
    bucket_name = os.getenv('AWS_S3_BUCKET', None)
    logging.info("Attempting to sync to: %s" % bucket_name)
    bucket_exists = s3.lookup(bucket_name)
    if bucket_exists is None:
        logging.error("Bucket %s does not exist.", bucket_name)
        logging.info("Following buckets found:")
        for b in s3.get_all_buckets():
            logging.info('  %s' % b.name)
        logging.info("Aborting sync.")
        return False

    # bucket checks out, continue
    max_files = 5

    logging.info('Collecting local info.')
    local_files = get_local_files(max_files=max_files)

    logging.info('Total local files: %i', len(local_files))

    logging.info('Collecting remote info.')
    remote_files = get_remote_files(s3, bucket_name, max_files)
    logging.info('Total remote files: %i', len(remote_files))

############################################

if __name__ == '__main__':
    main()
