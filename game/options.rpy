## EŞİĞİN ARDINDA — oyun ayarları

define config.name = _("EŞİĞİN ARDINDA")
define gui.show_name = True
define config.version = "1.0.0"

define gui.about = _p("""
Çamlık Kasabası'nda geçen, tek gecelik bir korku/gizem hikâyesi.

Deniz Aydın 6 Kasım gecesi eski servis yolunda kayboldu.
Telefonunda son bir sesli mesaj kaldı. Ve o mesajın arkasında,
ona benzeyen ama ona ait olmayan bir ses.

Görseller ve sesler tools/gen_assets.py ile prosedürel üretilmiştir.
""")

define build.name = "EsiginArdinda"

## Ses kanalları ##############################################################

define config.has_sound = True
define config.has_music = True
define config.has_voice = False

define config.main_menu_music = "audio/music/theme.ogg"

## Geçişler ###################################################################

define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.intra_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = fade

## Pencere ####################################################################

define config.window = "auto"
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)

## Varsayılan tercihler #######################################################

default preferences.text_cps = 45
default preferences.afm_time = 15
default preferences.music_volume = 0.7
default preferences.sfx_volume = 0.9

## Kayıt dizini ###############################################################

define config.save_directory = "EsiginArdinda-1731000000"

## Simge ######################################################################

define config.window_icon = "gui/window_icon.png"

## Build ######################################################################

init python:

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
    build.classify('docs/**', None)
    build.classify('tools/**', None)
    build.classify('.github/**', None)
    build.classify('README.md', None)
    build.classify('lint.txt', None)
    build.classify('renpy-sdk/**', None)
    build.classify('*.zip', None)
    build.classify('*.tar.bz2', None)
    build.classify('game/dev_autotest.rpy*', None)

    build.documentation('*.txt')

## Klavye kısayolu: J = Defter
init python:
    config.keymap['open_journal'] = ['K_j']
    config.underlay.append(renpy.Keymap(open_journal=ShowMenu("journal")))
define config.check_conflicting_properties = True
