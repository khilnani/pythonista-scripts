This directory is included in the default import path of the Python 2.7 interpreter, so that you can put reusable modules here.

Please note that site packages will *not* be reloaded automatically when you run a script. This is different from modules in other user directories, so you should typically only put modules here that you don't intend to change.

If you create a module named `pythonista_startup` in this directory, it will automatically be executed when the Python 2.7 interpreter is initialized (shortly after the app launches).