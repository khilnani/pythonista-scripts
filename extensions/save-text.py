# coding: utf-8

import clipboard, datetime, console, appex
import json, os, sys, shutil

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
            sys.exit()
    return save_dir

###########################################

def main():
    # get text from app share or clipboard
    if appex.is_running_extension():
        text = appex.get_text()
    else:
        text = clipboard.get()

    # get file save info
    save_dir_name = get_save_dir()
    file_name = 'txt-{:%Y%m%d-%H%M%S}.txt'.format(datetime.datetime.now())
    save_dir = os.path.join(BASE_DIR, save_dir_name)
    file_path = os.path.join(save_dir, file_name)

    # check dirs and save
    if not os.path.exists(save_dir ):
        os.makedirs(save_dir)
    with open(file_path, 'w') as f:
        f.write(text)
        f.close()

    # wrapup
    console.hud_alert('Saved to: ' + os.path.join(save_dir_name, file_name))
    if appex.is_running_extension():
        appex.finish()

###########################################

if __name__ == '__main__':
    main()