# pythonista

Scripts intended to be used with the iOS [Pythonista](http://omz-software.com/pythonista/) application. In some cases, as noted in the script comments, the scripts can be used on a regular linux/mac osx environment as well.

## Key scripts

- s3backup.py
  - Backup the Documents directory to a tar zip file in an Amazon S3 bucket
  - Requires: `aws.conf` (created by the installer below)
  - To install, run: `import requests as r; exec r.get('http://khl.io/s3backup').text`
