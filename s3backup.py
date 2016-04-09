# coding: utf-8

import platform, os, sys, tarfile, logging, datetime, json

###########################################

machine = platform.machine()
print 'Platform system:' + machine

###########################################

try:
	import boto
	from boto.s3.key import Key
	from boto.s3.bucket import Bucket
except ImportError as ie:
	if 'iP' in machine:
		import requests as r
		print 'Downloading Stash ...'
		exec r.get('http://bit.ly/get-stash').text
		print('In StaSh run: pip install boto')
		print('Restart Pythonista and re-run this script')
	elif 'x86_64' in machine:
		print('Please run: pip install boto')
	sys.exit()

############################################

try:
	import console
	BASE_DIR = os.path.expanduser('~/Documents')
except ImportError:
	BASE_DIR = os.path.dirname(os.path.realpath(__file__))
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
CONF_FILE = os.path.join(BASE_DIR, 'aws.conf')

############################################

def load_config():
	with open(CONF_FILE, 'r') as conf_file:
		try:
			conf = json.load(conf_file)
			for key in conf:
				os.environ[key] = conf[key]
		except Exception as e:
			logging.error('Config load error:')
			logging.error(e)
			sys.exit()

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
backup''', "", "")
	return mode

def bucket_exists(s3, bucket_name):
	logging.info("Connecting to: %s" % bucket_name)
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
		logging.info('No existing archive found.')
	else:
		logging.info('Existing archive removed.')

def tar_exclude(file_path):
	excludes = ['Icon', '.DS_Store', '.Trash', 'Examples', CONF_FILE, BACKUP_NAME]
	for name in excludes:
		if (name in file_path):
			logging.info('Skipping %s' % name)
			return True
	return False

def make_tarfile(filename, source_dir):
	logging.info('Creating archive ...')
	with tarfile.open(filename, "w:bz2") as tar:
		tar.add(source_dir, arcname='.', exclude=tar_exclude)
	sz = os.path.getsize(filename) >> 20
	logging.info('%s created, %iMB' % (filename, sz))

def extract_tarfile(filename, dest_dir):
	logging.info('Extracting ...')
	try:
		fl = tarfile.open(filename, "r:bz2")
		fl.extractall(dest_dir)
		logging.info('Archive extracted.')
	except IOError:
		logging.info('Archive not found.')

def list_tarfile(filename, dest_dir):
	logging.info('Listing ...')
	try:
		fl = tarfile.open(filename, "r:bz2")
		fl.list(verbose=False)
		logging.info('Listing complete.')
	except IOError:
		logging.info('Archive not found.')

def show_progress(num, total):
	per = int(num * 100/total)
	logging.info('  {}% completed'.format(per))

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

	bucket_name = os.getenv('PYTHONISTA_AWS_S3_BUCKET', None)

	if mode == 'list':
		list_tarfile(BACKUP_FILE, BASE_DIR)
	elif mode == 'archive':
		remove_archive(BACKUP_FILE)
		make_tarfile(BACKUP_FILE, BASE_DIR)
	elif mode == 'extract':
		extract_tarfile(BACKUP_FILE, BASE_DIR)
	else:
		s3 = boto.connect_s3()
		# check if bucket exists
		if not bucket_exists(s3, bucket_name):
			sys.exit()
		if mode == 'restore':
			restore(s3, bucket_name)
		elif mode == 'backup':
			backup(s3, bucket_name)


############################################

if __name__ == '__main__':
	main()
