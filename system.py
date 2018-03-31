__author__ = 'jonfun8'
import os
from pykeyboard import PyKeyboard

k = PyKeyboard();
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

def change_volume(threshold):
    volume_bar_amt = 100/16
    threshold = threshold * 100
    volume = int(os.popen('osascript -e \'output volume of (get volume settings)\'').read())
    print(volume)
    diff = abs(round( (volume - threshold) / volume_bar_amt))
    if volume < threshold:
        for i in range (0, diff):
            k.tap_key('KEYTYPE_SOUND_UP')
    elif volume > threshold:
        for i in range (0, diff):
            k.tap_key('KEYTYPE_SOUND_DOWN')

def open_chrome_site(url):
    os.system('open -a "Google Chrome" http://' +  url)
    # # k.press_key('Command')
    # k.press_keys(['Command','t'])
    # time.sleep(2)
    #
    # # k.tap_key('t')
    # # k.release_key('Command')
    # for i in range (0, len(url)):
    #     k.tap_key(url[i])
    # k.tap_key('return')

