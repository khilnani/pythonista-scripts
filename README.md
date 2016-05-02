## pythonista scripts

Scripts intended to be used with the iOS [Pythonista](http://omz-software.com/pythonista/) application. In some cases, as noted in the script comments, the scripts can be used on a regular linux/mac osx environment as well.

> - s3sync.py - Amazon S3 Backup/Restore script - moved to its own repo:  [https://github.com/khilnani/s3sync.py](https://github.com/khilnani/s3sync.py)
> - jira.py - CLI/iOS access to Jira issue summary - moved to its own repo [https://github.com/khilnani/jira.py](https://github.com/khilnani/jira.py)
> - hipchat.py - CLI/iOS access to unread messages - moved to its own repo [https://github.com/khilnani/hipchat.py](https://github.com/khilnani/hipchat.py)

## Catalog

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
