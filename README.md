# pythonista

Scripts intended to be used with the iOS [Pythonista](http://omz-software.com/pythonista/) application. In some cases, as noted in the script comments, the scripts can be used on a regular linux/mac osx environment as well.

### tools/s3backup.py

- Backup and restore the working directory to a tar zip file in an Amazon S3 bucket
- Installation:
  - Pythonista console:
    - Run: `import urllib2; exec urllib2.urlopen('http://khl.io/s3backupv1').read()`
  - Linux/Mac OS Terminal:
    - Run: `python -c "import urllib2; exec urllib2.urlopen('http://khl.io/s3backupv1').read()"`
- AWS Config: `aws.conf` (Template created by the installer)

### extensions

- Pythonista extensions for the iOS homescreen shortcuts and actions
- Installation:
  - Pythonista console:
    - Run: `import urllib2; exec urllib2.urlopen('http://khl.io/extensionsv1').read()`
  - Linux/Mac OS Terminal:
    - Run: `python -c "import urllib2; exec urllib2.urlopen('http://khl.io/extensionsv1').read()"`

### samples

- Sample scripts designed to work in pythonista and on linux/mac os
- Installation:
  - Pythonista console:
    - Run: `import urllib2; exec urllib2.urlopen('http://khl.io/samplesv1').read()`
  - Linux/Mac OS Terminal:
    - Run: `python -c "import urllib2; exec urllib2.urlopen('http://khl.io/samplesv1').read()"`
