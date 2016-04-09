# Save the text of the current the Pythonista Editor into a
# separate file with a similar name with a timestamp added.
# It is meant to be added to the editor's action menu.
# inspired by: http://omz-forums.appspot.com/pythonista/post/5903756180848640

import datetime, editor, os, sys, console
text = editor.get_text()
if not text:
    sys.exit('No text in the Editor.')
root, ext = os.path.splitext(editor.get_path())
filename = '{}_{:%Y%m%d_%H%M%S}{}'.format(root, datetime.datetime.now(), ext)
with open(filename, 'w') as out_file:
    out_file.write(text)
console.hud_alert('Saved to {}.'.format(os.path.basename(filename)))