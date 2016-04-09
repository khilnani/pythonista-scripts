import os, platform, sys, logging, urllib2, zipfile

############################################

GITHUB_MASTER = 'https://raw.githubusercontent.com/khilnani/pythonista-scripts/master/'
GITHUB_ARCHIVE = 'https://github.com/khilnani/pythonista-scripts/archive/master.zip'
ARCHIVE = 'pythonista-scripts.zip'

TOOLS_DIR = 'tools/'
S3BACKUP = 's3backup.py'
S3CONF_SAMPLE = 'sample.aws.conf'
S3CONF = 'aws.conf'

INSTALL_DIR = os.getcwd()

############################################

machine = platform.machine()
print 'Platform system:' + machine

print('Installing to: %s' % INSTALL_DIR)

if 'iP' in machine:
	BASE_DIR = os.path.expanduser('~/Documents')
else
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


def download_file(src, dest):
	logging.info('Downloading %s' % (src))
	file_content = urllib2.urlopen(src).read()
	logging.info('Writing %s' % dest)
	f = open(dest, 'w')
	f.write(file_content)
	f.close()
	logging.info('Done.')

def unzip_file(zip_file, extract_to):
	logging.info('Unzipping %s to %s' % (zip_file, extract_to))
	zip_ref = zipfile.ZipFile(zip_file, 'r')
	zip_ref.extractall(extract_to)
	zip_ref.close()
    logging.info('Done.')

def get_selection():
	sel = None
	if len(sys.argv) > 1:
		sel =sys.argv[1]
	else:
		sel = console.input_alert('''
Select an option:
1. s3backup
''', "", "")
	return sel

############################################

def download_s3backup():
	download_file(GITHUB_MASTER+TOOLS_DIR+S3BACKUP, os.path.join(INSTALL_DIR, S3BACKUP))
	download_file(GITHUB_MASTER+TOOLS_DIR+S3CONF_SAMPLE, os.path.join(INSTALL_DIR, S3CONF))
	print 'Please edit %s and then run: %s' % (S3CONF, S3BACKUP)

def download_archive():
    download_loc = os.path.join(INSTALL_DIR, ARCHIVE)
	download_file(GITHUB_ARCHIVE, download_loc)
    unzip_file(download_loc, INSTALL_DIR)

############################################

def main():
	setup_logging()
	sel = get_selection()

	# tools/s3backup
	if sel == '1':
		download_s3backup()
	elif sel == '2':
		download_archive()

############################################

if __name__ == '__main__':
	main()
