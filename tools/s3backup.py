# coding: utf-8

import platform, os, sys, tarfile, logging
import datetime, json, urllib2

###########################################

if os.environ.get('LC_CTYPE', '') == 'UTF-8':
    os.environ['LC_CTYPE'] = 'en_US.UTF-8'

machine = platform.machine()
print 'Platform system:' + machine

###########################################

def install_stash():
    try:
        from stash import stash
        return True
    except ImportError:
        import requests as r
        print 'Downloading Stash ...'
        exec r.get('http://bit.ly/get-stash').text
    try:
        from stash import stash
        return True
    except ImportError:
        return False
    
    return False

def install_boto():
    try:
        import boto
        from boto.s3.key import Key
        from boto.s3.bucket import Bucket
        return True
    except ImportError:
        if install_stash():
            _stash = stash.StaSh()
            print('StaSh version: ' + str(stash.__version__))
            print('Installing AWS boto library ...')
            _stash('pip install boto')
            print('AWS boto library installed.')
            print('Please restart Pythonista and re-run this script') 
    try:
        import boto
        from boto.s3.key import Key
        from boto.s3.bucket import Bucket
        return True
    except ImportError:
        return False

def install_awscli():
    try:
        import awscli.clidriver
        return True
    except ImportError:
        if install_stash():
            _stash = stash.StaSh()
            print('StaSh version: ' + str(stash.__version__))
            print('Installing AWS CLI library ...')
            _stash('pip install awscli')
            print('AWS CLI installed.')
            print('Please restart Pythonista and re-run this script') 
    try:
        import awscli.clidriver
        return True
    except ImportError:
        return False        

try:
    import boto
    from boto.s3.key import Key
    from boto.s3.bucket import Bucket
except ImportError as ie:
    if 'iP' in machine:
        install_boto()
    elif 'x86_64' in machine:
        print('Please run: pip install boto awscli')
    sys.exit()

############################################

try:
    import console
    BASE_DIR = os.path.expanduser('~/Documents')
except ImportError:
    BASE_DIR = os.getcwd()
    class console (object):
        @staticmethod
        def hud_alert(message, icon=None, duration=None):
            print message

        @staticmethod
        def input_alert(title, message=None, input=None, ok_button_title=None, hide_cancel_button=False):
            message = '' if message == None else message
            ret = input
            try:
                ret = raw_input(title + '' + message + ' :')
            except Exception as e:
                print e
            return ret

############################################

BACKUP_NAME = 'pythonista_backup.tar.bz2'
BACKUP_COPY = 'pythonista_backup.{:%Y%m%d_%H%M%S}.tar.bz2'.format(datetime.datetime.now())
BACKUP_FILE = os.path.join(BASE_DIR, BACKUP_NAME)
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CONF_NAME = 's3backup.conf'
CONF_FILE = os.path.join(SCRIPT_DIR, CONF_NAME)
TEST_NAME = '.s3test'
TEST_ARCHIVE_NAME = TEST_NAME+'.tar.bz2'
TEST_ARCHIVE = os.path.join(BASE_DIR, TEST_ARCHIVE_NAME)

GITHUB_MASTER = 'https://raw.githubusercontent.com/khilnani/pythonista/master/tools/'
S3BACKUP_FILE = 's3backup.py'

print 'BASE_DIR: %s' % BASE_DIR

############################################

def load_config():
    try:
        with open(CONF_FILE, 'r') as conf_file:
            conf = json.load(conf_file)
            for key in conf:
                os.environ[key] = conf[key]
            logging.info('%s loaded to environment.' % CONF_NAME)
    except Exception as e:
        logging.warning('No %s, using AWS Credentials/Config' % CONF_NAME)

def aws_configure():
    install_awscli()
    import awscli.clidriver
    sys.argv.append('configure')
    return awscli.clidriver.main()    
    
def setup_logging(log_level='INFO'):
    log_format = "%(message)s"
    logging.addLevelName(15, 'FINE')
    logging.basicConfig(format=log_format, level=log_level)

def get_mode():
    mode = None
    if len(sys.argv) > 1:
        mode =sys.argv[1]
    else:
        mode = console.input_alert('''
Select an option:
list
archive
extract
restore
backup
configure
dry run
update script
''', "", "")
    return mode

def get_bucket_name():
    bucket_name = os.getenv('PYTHONISTA_AWS_S3_BUCKET', '')
    if not bucket_name:
        bucket_name = console.input_alert('S3 bucket name: ', '', bucket_name)
    return bucket_name

def friendly_path(name):
    if BASE_DIR in name:
        return name.split(BASE_DIR)[-1]
    return name

def download_file(src, dest):
    logging.info('Reading %s' % (src))
    file_content = urllib2.urlopen(src).read()
    logging.info('Writing %s' % dest)
    f = open(dest, 'w')
    f.write(file_content)
    f.close()
    logging.info('Done.')

def update_script():
    download_file(GITHUB_MASTER+S3BACKUP_FILE, os.path.join(SCRIPT_DIR, S3BACKUP_FILE))

def bucket_exists(s3, bucket_name):
    logging.info("Connecting to S3: %s" % bucket_name)
    bucket_exists = s3.lookup(bucket_name)
    if bucket_exists is None:
        logging.error("Bucket %s does not exist.", bucket_name)
        logging.info("Following buckets found:")
        for b in s3.get_all_buckets():
            logging.info('  %s' % b.name)
        logging.info("Aborting sync.")
        return False
    return True

def remove_archive(archive_file):
    try:
        os.remove(archive_file)
    except:
        logging.info('No local archive %s found.' % friendly_path(archive_file))
    else:
        logging.info('Local archive %s removed.' % friendly_path(archive_file))

def tar_exclude(file_path):
    excludes = ['/Icon', '/.DS_Store', '/.Trash', '/Examples', '/.git', '/'+TEST_NAME, '/'+TEST_ARCHIVE_NAME, '/'+BACKUP_NAME]
    friendly_file_path = friendly_path(file_path)
    for name in excludes:
        if (name == friendly_file_path):
            logging.info('Skipping %s' % friendly_file_path)
            return True
    return False

def make_tarfile(filename, source_dir):
    logging.info('Creating %s ...' % friendly_path(filename))
    with tarfile.open(filename, "w:bz2") as tar:
        tar.add(source_dir, arcname='.', exclude=tar_exclude)
    sz = os.path.getsize(filename) >> 20
    logging.info('Created %iMB %s' % (sz, friendly_path(filename) ))

def extract_tarfile(filename, dest_dir):
    logging.info('Extracting %s to %s...' % (friendly_path(filename), friendly_path(dest_dir)))
    try:
        fl = tarfile.open(filename, "r:bz2")
        fl.extractall(dest_dir)
        logging.info('Archive extracted.')
    except IOError:
        logging.error('Archive extraction error.')
        logging.error(e)

def list_tarfile(filename, dest_dir):
    logging.info('Listing % ...' % friendly_path(filename))
    try:
        fl = tarfile.open(filename, "r:bz2")
        fl.list(verbose=False)
        logging.info('Listing complete.')
    except IOError:
        logging.info('Archive not found.')

def show_progress(num, total):
    per = int(num * 100/total)
    logging.info('  {}% completed'.format(per))

def test_upload(s3, bucket_name):
    logging.info('Testing upload of %s to S3 ...' % TEST_NAME)
    bucket = s3.get_bucket(bucket_name)
    k = bucket.get_key(TEST_NAME, validate=False)
    k.set_contents_from_string(TEST_NAME, replace=True, cb=show_progress, num_cb=200)
    logging.info('Upload test complete.')

def test_download(s3, bucket_name):
    logging.info('Testing download of %s from S3 ...' % TEST_NAME)
    bucket = s3.get_bucket(bucket_name)
    k = bucket.get_key(TEST_NAME, validate=True)
    content = k.get_contents_as_string(cb=show_progress, num_cb=200)
    if content != TEST_NAME:
        logging.error('Test file %s read from S3 is not the one created.' % TEST_NAME)
    logging.info('Download test complete.')

def upload_archive(s3, bucket_name, key, fl):
    logging.info('Uploading to S3 ...')
    bucket = s3.get_bucket(bucket_name)
    k = bucket.get_key(key , validate=False)
    k.set_contents_from_filename(fl, replace=True, cb=show_progress, num_cb=200)
    logging.info('Upload complete.')

def duplicate_key(s3,bucket_name, key, dest_key):
    logging.info('Creating backup copy ...')
    bucket = s3.get_bucket(bucket_name)
    k = bucket.get_key(key, validate=True)
    k.copy(bucket_name, dest_key)
    logging.info('Backup copy created.')

def download_archive(s3, bucket_name, key, fl):
    logging.info('Downloading from S3 ...')
    bucket = s3.get_bucket(bucket_name)
    k = bucket.get_key(key , validate=True)
    k.get_contents_to_filename(fl, cb=show_progress, num_cb=200)
    logging.info('Download complete.')

def dry_run(s3, bucket_name):
    remove_archive(TEST_ARCHIVE)
    make_tarfile(TEST_ARCHIVE, BASE_DIR)
    extract_tarfile(TEST_ARCHIVE, os.path.join(BASE_DIR, TEST_NAME))
    test_upload(s3, bucket_name)
    test_download(s3, bucket_name)

def restore(s3, bucket_name):
    remove_archive(BACKUP_FILE)
    download_archive(s3, bucket_name, BACKUP_NAME, BACKUP_FILE)
    extract_tarfile(BACKUP_FILE, BASE_DIR)
    #remove_archive(BACKUP_FILE)

def backup(s3, bucket_name):
    remove_archive(BACKUP_FILE)
    make_tarfile(BACKUP_FILE, BASE_DIR)
    upload_archive(s3, bucket_name, BACKUP_NAME, BACKUP_FILE)
    duplicate_key(s3, bucket_name, BACKUP_NAME, BACKUP_COPY)
    #remove_archive(BACKUP_FILE)

############################################

def main():
    setup_logging()
    load_config()
    mode = get_mode()

    if mode == 'update script':
        update_script()
    elif mode == 'list':
        list_tarfile(BACKUP_FILE, BASE_DIR)
    elif mode == 'archive':
        remove_archive(BACKUP_FILE)
        make_tarfile(BACKUP_FILE, BASE_DIR)
    elif mode == 'extract':
        extract_tarfile(BACKUP_FILE, BASE_DIR)
    elif mode == 'configure':
        aws_configure()
    else:
        s3 = boto.connect_s3()
        # check if bucket exists
        bucket_name = get_bucket_name()
        if not bucket_exists(s3, bucket_name):
            sys.exit()
        if mode == 'dry run':
            dry_run(s3, bucket_name)
        elif mode == 'restore':
            restore(s3, bucket_name)
        elif mode == 'backup':
            backup(s3, bucket_name)


############################################

if __name__ == '__main__':
    main()