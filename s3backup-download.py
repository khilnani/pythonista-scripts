import requests as r

BASE_DIR = os.path.expanduser('~/Documents')
S3BACKUP_FILE = os.path.join(BASE_DIR, 's3backup.py')

print 'Reading s3backup from github'
file_content = r.get('https://raw.githubusercontent.com/khilnani/pythonista/master/s3backup.py').text

print 'Writing s3backup.py'
s3backup = open(S3BACKUP_FILE, 'w')
s3backup.write(file_content)
s3backup.close()

print 'Done.'
