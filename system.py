__author__ = 'jonfun8'
import os
from pykeyboard import PyKeyboard
app = 'dictate'
k = PyKeyboard();
if app == 'spotify':
    os.system('open /Applications/Spotify.app/')
    k.tap_key('KEYTYPE_PLAY')
    k.tap_key('KEYTYPE_NEXT')

    # KEYTYPE_PREVIOUS
    # KEYTYPE_ILLUMINATION_UP
    # KEYTYPE_ILLUMINATION_DOWN
    # KEYTYPE_BRIGHTNESS_UP
    # KEYTYPE_BRIGHTNESS_DOWN
    # KEYTYPE_SOUND_UP
    # KEYTYPE_SOUND_DOWN
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
    k.tap_key('command')
    k.tap_key('command')
