## Görsel ve işitsel efektler #################################################

init -4 python:
    renpy.music.register_channel("ambient", mixer="music", loop=True, tight=True)
    renpy.music.register_channel("ambient2", mixer="music", loop=True, tight=True)
    renpy.music.register_channel("sfx2", mixer="sfx", loop=False)

    import os

    ## images/bg/*.jpg dosyalarını "bg <ad>" olarak tanımla.
    for _f in renpy.list_files():
        if _f.startswith("images/bg/") and _f.endswith((".jpg", ".png", ".webp")):
            _n = os.path.splitext(os.path.basename(_f))[0]
            renpy.image(("bg", _n), _f)

    def jolt(strong=False):
        """Ekran sarsıntısı (Ayarlar'dan kapatılabilir)."""
        if persistent.allow_shake:
            renpy.with_statement(vpunch if strong else hpunch)

    def flash(color="#ffffff"):
        """Kısa parlama (Ayarlar'dan kapatılabilir)."""
        if persistent.allow_flash:
            renpy.with_statement(Fade(0.05, 0.0, 0.45, color=color))
        else:
            renpy.with_statement(Dissolve(0.3))

    def sfx(name, channel="audio"):
        renpy.sound.play("audio/sfx/%s.ogg" % name, channel=channel)
        show_caption(name)

    def amb(name, fade=2.0):
        if name is None:
            renpy.music.stop(channel="ambient", fadeout=fade)
        else:
            renpy.music.play("audio/amb/%s.ogg" % name, channel="ambient", fadein=fade, fadeout=fade, if_changed=True)

    def amb2(name, fade=2.0):
        if name is None:
            renpy.music.stop(channel="ambient2", fadeout=fade)
        else:
            renpy.music.play("audio/amb/%s.ogg" % name, channel="ambient2", fadein=fade, fadeout=fade, if_changed=True)

    def bgm(name, fade=2.0):
        if name is None:
            renpy.music.stop(channel="music", fadeout=fade)
        else:
            renpy.music.play("audio/music/%s.ogg" % name, channel="music", fadein=fade, fadeout=fade, if_changed=True)

    def silence(fade=1.5):
        for ch in ("ambient", "ambient2", "music"):
            renpy.music.stop(channel=ch, fadeout=fade)

image black = Solid("#000000")
image white = Solid("#ffffff")
image red_tint = Solid("#5a000040")
image blue_tint = Solid("#00184030")

image fog_overlay:
    "images/fog.png"
    alpha 0.55
    xpos 0
    linear 30.0 xpos -200
    linear 30.0 xpos 0
    repeat

image phone_wave:
    Text("▂▃▅▇▅▃▂▁▂▅▇▅▂", size=60, color="#7aa0c8")
    xalign 0.5
    yalign 0.42
    block:
        linear 0.6 alpha 0.4
        linear 0.6 alpha 1.0
        repeat

## Konumlar ####################################################################

transform sil_left:
    zoom 0.86
    xalign 0.18
    yalign 1.0
    yoffset 30

transform sil_right:
    zoom 0.86
    xalign 0.82
    yalign 1.0
    yoffset 30

transform sil_center:
    zoom 0.86
    xalign 0.5
    yalign 1.0
    yoffset 30

transform sil_far:
    xalign 0.62
    yalign 1.0
    zoom 0.6
    alpha 0.75
    yoffset 10

transform sil_left2:
    xalign 0.02
    yalign 1.0
    zoom 0.92
    yoffset 40

transform sil_right2:
    xalign 0.98
    yalign 1.0
    zoom 0.92
    yoffset 40

transform creature_far:
    xalign 0.5
    yalign 0.85
    zoom 0.45
    alpha 0.0
    linear 1.5 alpha 0.7

transform creature_close:
    xalign 0.5
    yalign 1.0
    zoom 1.0
    alpha 0.0
    linear 0.4 alpha 1.0

transform creature_wall:
    xalign 0.85
    yalign 0.15
    zoom 0.55
    rotate -70
    alpha 0.0
    linear 0.6 alpha 0.9

transform creature_floor:
    xalign 0.3
    yalign 1.0
    zoom 0.6
    alpha 0.0
    linear 0.8 alpha 0.85

## Hareket ve bozulma ##########################################################

transform glitchy:
    alpha 1.0
    block:
        linear 0.04 xoffset -6 alpha 0.7
        linear 0.04 xoffset 4 alpha 1.0
        linear 0.04 xoffset 0
        pause 0.6
        linear 0.03 xoffset 8 alpha 0.5
        linear 0.03 xoffset 0 alpha 1.0
        pause 1.1
        repeat

## Gecikmeli kopya: Taklitçi davranışı (gerçeğin hareketini 0.4 sn geç tekrarlar)
transform delayed_mirror:
    alpha 0.85
    pause 0.4
    linear 0.25 yoffset -18
    linear 0.25 yoffset 0

transform raise_hand:
    linear 0.25 yoffset -18
    linear 0.25 yoffset 0

transform breathe:
    yoffset 30
    block:
        ease 2.2 yoffset 26
        ease 2.2 yoffset 30
        repeat

transform slow_zoom:
    zoom 1.0
    linear 25.0 zoom 1.08

transform shake_loop:
    block:
        linear 0.05 xoffset 3
        linear 0.05 xoffset -3
        repeat

transform flicker_light:
    alpha 1.0
    block:
        pause 2.0
        linear 0.05 alpha 0.4
        linear 0.05 alpha 1.0
        pause 0.3
        linear 0.03 alpha 0.6
        linear 0.03 alpha 1.0
        pause 3.5
        repeat

transform fade_out_slow:
    linear 2.0 alpha 0.0

## Geçişler
define flash_white = Fade(0.05, 0.0, 0.5, color="#ffffff")
define flash_red = Fade(0.05, 0.0, 0.5, color="#600000")
define long_fade = Fade(1.5, 0.5, 1.5)
define slow_dissolve = Dissolve(1.5)
