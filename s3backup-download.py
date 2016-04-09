import os, platform, sys, urllib2

machine = platform.machine()
print 'Platform system:' + machine

if 'iP' in machine:
  BASE_DIR = os.path.expanduser('~/Documents')
else:
  BASE_DIR = os.getcwd()

GITHUB_MASTER = 'https://raw.githubusercontent.com/khilnani/pythonista/master/'
S3BACKUP_FILE = 's3backup.py'
S3CONF_FILE = 'sample.aws.conf'
S3CONF_DEST_FILE = 'aws.conf'

def download_file(src, dest):
  print 'Reading %s from %s' % (src, GITHUB_MASTER + src)
  file_content = urllib2.urlopen(GITHUB_MASTER + src).read()
  print 'Writing %s' % dest
  file_path = os.path.join(BASE_DIR, dest)
  f = open(file_path, 'w')
  f.write(file_content)
  f.close()
  print 'Done.'

download_file(S3BACKUP_FILE, S3BACKUP_FILE)
download_file(S3CONF_FILE, S3CONF_DEST_FILE)

print 'Please edit %s and then run: %s' % (S3CONF_DEST_FILE, S3BACKUP_FILE)
