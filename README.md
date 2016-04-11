## pythonista scripts

Scripts intended to be used with the iOS [Pythonista](http://omz-software.com/pythonista/) application. In some cases, as noted in the script comments, the scripts can be used on a regular linux/mac osx environment as well.

## Catalog

### `tools/s3backup.py`

- Backup and restore the working directory to a tar zip file in an Amazon S3 bucket.
- Pythonista:
  - Files downloaded to and restored from the `~/Documents` directory
- Linux/mac os:
  - Files downloaded to and restored from the working directory, not the directory containing the script
  - Example: From this directory, run `python tools/s3backup.py`

### `extensions/`

- Pythonista extensions for the iOS homescreen shortcuts and actions

### `samples/`

- Sample scripts designed to work in pythonista and on linux/mac os

### `site-packages/`

- Pythonista specific installed library, contains modules installed via pip and manually

### `thirdparty/`

- Scripts and repos I have downloaded from elsewhere

## Installation

- Pythonista console:
 - Run: `import urllib2; exec urllib2.urlopen('http://khl.io/pythonista-scripts').read()`
- Linux/Mac OS Terminal:
 - Run: `python -c "import urllib2; exec urllib2.urlopen('http://khl.io/pythonista-scripts').read()"`