import os
import time
from pykeyboard import PyKeyboard
import pyautogui

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

volumes = [0, 6, 13, 19, 25, 31, 38, 44, 50, 56, 62, 68, 75, 81, 88, 94, 100]

def change_volume(target):
    volume = volumes.index(int(os.popen('osascript -e "output volume of (get volume settings)"').read()))
    diff = abs(volume - target)
    if volume < target:
        for i in range (0, diff):
            k.tap_key('KEYTYPE_SOUND_UP')
    elif volume > target:
        for i in range (0, diff):
            k.tap_key('KEYTYPE_SOUND_DOWN')

def play():
    k.tap_key('KEYTYPE_PLAY')

def dictation():
    pyautogui.press('f1')

def open_chrome_site(url):
    os.system('open -a "Google Chrome" http://%s' % url)

