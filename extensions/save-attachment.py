# coding: utf-8

# Make a local copy of the text file passed in via a share sheet.
# See: https://forum.omz-software.com/topic/2637/is-it-possible-to-read-a-file-say-txt-file-from-other-app

###########################################

import sys
import os
import appex
import datetime
import console
import json
import clipboard

###########################################

# share safe documents dir location
BASE_DIR = os.getcwd().split('Documents')[0] + 'Documents'
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CONF_FILE = os.path.join(SCRIPT_DIR, 'save.conf')

###########################################

def get_save_dir():
    save_dir = ''
    with open(CONF_FILE, 'r') as conf_file:
        try:
            config = json.load(conf_file)
            save_dir = config['TEXT']
            return save_dir
        except Exception as e:
            print('Config load error:')
            print(e)
            sys.exit(e)
    return save_dir

###########################################

def main():
    if appex.is_running_extension():
        content = None
        attachments = appex.get_attachments()
        filepaths = appex.get_file_path()
        
        if attachments and attachments[0].rstrip() and appex.get_file_path():
            with open(attachments[0], 'r') as f:
                content = f.read()
            attachment_name = filepaths.split(os.sep)[-1]
        else:
            print('No attachment found.')
            sys.exit(1)
        
        sel = console.alert('Save: %s' % attachment_name, button1='File', button2='Clipboard')

        if sel == 1:
            file_name = '{:%Y%m%d-%H%M%S}_{}'.format(datetime.datetime.now(), attachment_name)
            save_dir_name = get_save_dir()
            save_dir_path = os.path.join(BASE_DIR, save_dir_name)
            save_file_rel_path = os.path.join(save_dir_name, file_name)
            save_file_path = os.path.join(BASE_DIR, save_file_rel_path)
            
            try:
                # check dirs and save
                if not os.path.exists(save_dir_path):
                    os.makedirs(save_dir_path)
                with open(save_file_path, 'w') as f:
                    f.write(content)
                # wrapup
                msg = 'Saved: %s' % save_file_rel_path
            except Exception as e:
                msg = str(e)
            console.alert(msg, button1='OK', hide_cancel_button=True)
        elif sel == 2:
            clipboard.set(content)
    
        if appex.is_running_extension():
            appex.finish()

###########################################

if __name__ == '__main__':
    main()