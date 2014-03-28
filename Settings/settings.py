from Settings.defaultSettings import *


##Create a unique secret key for the project
try:
    from Settings.secret_key import *
except ImportError:
    from django.utils.crypto import get_random_string
    SETTINGS_DIR=os.path.abspath(os.path.dirname(__file__))
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(50, chars)

    secretfile = open(SETTINGS_DIR+"/secret_key.py", 'w')
    secretfile.write("SECRET_KEY = \'"+secret_key+"\'\n")
    secretfile.close()
    from Settings.secret_key import *

''''
Production enviroment settings overrides. You can override Settings/defaultSettings.py settings from here.

If you're a developer, you want to be editing the defaultSettings file instead.

Only edit this file if you're deploying it. And make sure it's not being updated by typing "git update-index --assume-unchanged Settings/settings.py"

'''''

