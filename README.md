# pythonista

Scripts intended to be used with the iOS [Pythonista](http://omz-software.com/pythonista/) application. In some cases, as noted in the script comments, the scripts can be used on a regular linux/mac osx environment as well.

## Key scripts

- s3backup.py
  - Backup and restore the working directory to a tar zip file in an Amazon S3 bucket
  - Requires: `aws.conf` (created by the installer below)
  - Installation
    - Pythonista console: 
      - Run: `import urllib2; exec urllib2.urlopen('http://khl.io/s3backup').read()`
    - Linux/Mac OS Terminal:
      - Run: `python -c "import urllib2; exec urllib2.urlopen('http://khl.io/s3backup').read()"`
