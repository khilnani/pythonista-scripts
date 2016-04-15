import os, shutil, platform, sys, logging, urllib2, zipfile

############################################

INSTALL_DIR = os.getcwd()

GITHUB_MASTER = 'https://raw.githubusercontent.com/khilnani/pythonista-scripts/master/'
GITHUB_ARCHIVE = 'https://github.com/khilnani/pythonista-scripts/archive/master.zip'

ARCHIVE_DIR_PARTIAL = 'pythonista-scripts-master/'
ARCHIVE_DIR = os.path.join(INSTALL_DIR, ARCHIVE_DIR_PARTIAL)
ARCHIVE_NAME = 'pythonista-scripts.zip'
ARCHIVE_PATH = os.path.join(INSTALL_DIR, ARCHIVE_NAME)

TOOLS_DIR = 'tools/'
S3BACKUP = 's3backup.py'
S3CONF_SAMPLE = 's3backup.sample.conf'
S3CONF = 's3backup.conf'

EXCLUDE_FILES = ['/.gitignore', '/download.py', '/README.md']

############################################

machine = platform.machine()
print 'Platform system:' + machine

print('Installing to: %s' % INSTALL_DIR)

if 'iP' in machine:
    BASE_DIR = os.path.expanduser('~/Documents')
else:
    BASE_DIR = os.getcwd()

############################################

try:
    import console
except ImportError:
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

def setup_logging(log_level='INFO'):
    log_format = "%(message)s"
    logging.addLevelName(15, 'FINE')
    logging.basicConfig(format=log_format, level=log_level)

def friendly_path(name):
    if ARCHIVE_DIR_PARTIAL in name:
        return name.split(ARCHIVE_DIR_PARTIAL)[-1]
    if INSTALL_DIR in name:
        return name.split(INSTALL_DIR)[-1]
    return name

def move_files(from_dir, to_dir, dry_run=False):
    pre_msg = 'DRY RUN: ' if dry_run else ''
    logging.info('%sMoving files from %s to %s' % (pre_msg, from_dir, to_dir))
    for dirpath, dirnames, filenames in os.walk(from_dir):
        dir_partial = dirpath.split(ARCHIVE_DIR)[-1]
        dest_dir = os.path.join(to_dir, dir_partial)
        if not os.path.exists(dest_dir):
            if not dry_run:
                os.makedirs(dest_dir)
        for f in filenames:
            from_file = os.path.join(dirpath, f)
            to_file = os.path.join(dest_dir, f)
            if friendly_path(to_file) in EXCLUDE_FILES:
                logging.info('  %sSkipping %s' % (pre_msg, friendly_path(to_file)))
            elif os.path.exists(to_file):
                logging.info('  %sEXISTS %s' % (pre_msg, friendly_path(to_file)))
            else:
                logging.info('  %s%s' % (pre_msg, friendly_path(to_file)))
            try:
                if not dry_run:
                    shutil.copyfile(from_file, to_file)
            except IOError as ioe:
                logging.error(ioe)
            except shutil.Error as e:
                logging.warn(e)
            except Exception as e:
                logging.error(e)

def download_file(src, dest):
    logging.info('Downloading %s' % (src))
    file_content = urllib2.urlopen(src).read()
    logging.info('Writing %s' % dest)
    f = open(dest, 'w')
    f.write(file_content)
    f.close()

def delete_archive_dir():
    logging.info('Deleting downloaded archive content')
    shutil.rmtree(ARCHIVE_DIR)

def delete_archive():
    logging.info('Deleting downloaded archive')
    os.remove(ARCHIVE_PATH)

def list_zip(zip_file):
    logging.info('Lising zip %s' % (zip_file))
    zip_ref = zipfile.ZipFile(zip_file, 'r')
    for name in zip_ref.namelist():
        print '  %s' % (friendly_path(name))
    zip_ref.close()

def unzip_file(zip_file, extract_to):
    logging.info('Unzipping %s to %s' % (zip_file, extract_to))
    zip_ref = zipfile.ZipFile(zip_file, 'r')
    zip_ref.extractall(extract_to)
    zip_ref.close()

def get_selection():
    sel = None
    if len(sys.argv) > 1:
        sel =sys.argv[1]
    else:
        sel = console.input_alert('''
Select an option:
1. S3 backup/restore script
2. List all files
3. Download all files
''', "", "")
    return sel

############################################

def download_s3backup():
    download_file(GITHUB_MASTER+TOOLS_DIR+S3BACKUP, os.path.join(INSTALL_DIR, S3BACKUP))
    download_file(GITHUB_MASTER+TOOLS_DIR+S3CONF_SAMPLE, os.path.join(INSTALL_DIR, S3CONF))
    logging.info('Done.')
    print 'Please edit %s and then run: %s' % (S3CONF, S3BACKUP)


def download_archive():
    download_file(GITHUB_ARCHIVE, ARCHIVE_PATH)
    unzip_file(ARCHIVE_PATH, INSTALL_DIR)
    move_files(ARCHIVE_DIR, INSTALL_DIR, dry_run=False)
    delete_archive_dir()
    delete_archive()
    logging.info('Done.')

def review_archive():
    download_file(GITHUB_ARCHIVE, ARCHIVE_PATH)
    unzip_file(ARCHIVE_PATH, INSTALL_DIR)
    move_files(ARCHIVE_DIR, INSTALL_DIR, dry_run=True)
    delete_archive_dir()
    delete_archive()
    logging.info('Done.')

############################################

def main():
    setup_logging()
    sel = get_selection()

    # tools/s3backup
    if sel == '1':
        download_s3backup()
    elif sel == '2':
        review_archive()
    elif sel == '3':
        download_archive()

############################################

if __name__ == '__main__':
    main()