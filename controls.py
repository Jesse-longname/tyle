import os
import time
from pykeyboard import PyKeyboard
import pyautogui
import auto_correct

k = PyKeyboard();

apps = {
    'Chrome': 'Google Chrome',
    'Word': 'Microsoft Word',
    'Spotify': 'Spotify',
}

app_names = {'Chrome', 'Word', 'Spotify'}

def open_app(app_name):
    os.system('open -a "%s".app' % app_name)

def align_left():
    k.press_keys(['Control','Alternate','a'])

def align_right():
    k.press_keys(['Control','Alternate','d'])

def do_app_action(app):
    if app == 'spotify':
        os.system('open /Applications/Spotify.app/')
        k.tap_key('KEYTYPE_PLAY')
        k.tap_key('KEYTYPE_NEXT')
    elif app == 'mute':
        k.tap_key('KEYTYPE_MUTE')
    elif app == 'vol up':
        k.tap_key('KEYTYPE_SOUND_UP')
        k.tap_key('KEYTYPE_SOUND_UP')
        k.tap_key('KEYTYPE_SOUND_UP')
    elif app == 'bright':
        k.tap_key('KEYTYPE_BRIGHTNESS_UP')
        k.tap_key('KEYTYPE_BRIGHTNESS_UP')
        k.tap_key('KEYTYPE_BRIGHTNESS_UP')
    elif app == 'mute':
        k.tap_key('KEYTYPE_MUTE')
    elif app == 'dictate':
        # Note must set the shortcut on mac to activate from this
        k.tap_key('command')
        k.tap_key('command')

for i in range(15):
    k.tap_key('KEYTYPE_SOUND_DOWN')
cur_vol = 0
# os.popen('osascript -e "set Volume 0"')

def change_volume(target):
    global cur_vol
    diff = abs(cur_vol - target)
    if cur_vol < target:
        for i in range (0, diff):
            k.tap_key('KEYTYPE_SOUND_UP')
    elif cur_vol > target:
        for i in range (0, diff):
            k.tap_key('KEYTYPE_SOUND_DOWN')
    cur_vol = target

def play():
    k.tap_key('KEYTYPE_PLAY')

def dictation():
    pyautogui.press('f1')

def open_chrome_site(url):
    os.system('open -a "Google Chrome" http://%s' % auto_correct.auto_correct(url))

