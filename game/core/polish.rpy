## Sunum ve meta sistemler ####################################################
##
## * Konuşan karakter vurgusu (speaking attribute)
## * "Devam" göstergesi (CTC)
## * Sinematik katman: film greni, vinyet, nefes alan kamera
## * Nabız: yüksek gerginlikte kalp atışı ve kırmızı hale
## * Başarımlar
## * Açılış: içerik uyarısı, zorluk seçimi
## * Bölüm sonu özeti ve otomatik kayıt
## * İlk karşılaşmada kısa ipuçları

## Tüm karakterler için ortak temel ##########################################

init -10 python:
    adv = Character(kind=adv, ctc="ctc_blink", ctc_position="nestled-close")

define config.speaking_attribute = "speaking"
define config.say_attribute_transition = Dissolve(0.18)
define config.say_attribute_transition_layer = "master"

image ctc_blink:
    Text(" ▼", size=16, color="#c8a24a")
    alpha 0.0
    linear 0.35 alpha 1.0
    pause 0.5
    linear 0.35 alpha 0.15
    repeat

## Kalıcı ayarlar
default persistent.grain = True
default persistent.camera_drift = True
default persistent.seen_warning = False
default persistent.tips = set()

## Zorluk: "hikaye" veya "gerilim"
default zorluk = "gerilim"
default autotest_zorluk = "gerilim"
default qte_kacan = 0
default chapter_notes_start = 0
default chapter_kanit_start = 0
default chapter_kanma_start = 0
default kirpinti_vuruldu = 0

## Sinematik katman ###########################################################

image fx_grain:
    "images/fx/grain0.png"
    zoom 2.0
    pause 0.06
    "images/fx/grain1.png"
    zoom 2.0
    pause 0.06
    "images/fx/grain2.png"
    zoom 2.0
    pause 0.06
    "images/fx/grain3.png"
    zoom 2.0
    pause 0.06
    repeat

image fx_vignette = "images/fx/vignette.png"

image fx_red:
    "images/fx/vignette_red.png"
    alpha 0.2
    block:
        ease 0.45 alpha 0.5
        ease 0.55 alpha 0.2
        repeat

screen cinematic():
    zorder 30
    if not main_menu:
        add "fx_vignette" alpha 0.55
        if gerginlik >= 75:
            add "fx_red"
    if persistent.grain:
        add "fx_grain" alpha 0.07

init python:
    config.overlay_screens.append("cinematic")

transform cam_drift:
    subpixel True
    zoom 1.015
    xalign 0.5
    yalign 0.5
    block:
        ease 7.0 xoffset 5 yoffset -3
        ease 8.0 xoffset -4 yoffset 3
        ease 6.0 xoffset 2 yoffset -2
        ease 7.0 xoffset 0 yoffset 0
        repeat

transform cam_still:
    zoom 1.0
    xoffset 0
    yoffset 0

init python:
    def apply_camera():
        if persistent.camera_drift:
            renpy.show_layer_at([cam_drift], layer="master", camera=True)
        else:
            renpy.show_layer_at([cam_still], layer="master", camera=True)

    def update_pulse():
        """Gerginlik 70 ve üstündeyken kalp atışı döngüsü."""
        if store.gerginlik >= 70:
            renpy.music.play("audio/sfx/heartbeat.ogg", channel="pulse", loop=True, if_changed=True, fadein=1.0)
        else:
            renpy.music.stop(channel="pulse", fadeout=1.5)

init -4 python:
    renpy.music.register_channel("pulse", mixer="sfx", loop=True)


## Başarımlar #################################################################

init -2 python:
    ACHIEVEMENTS = [
        ("ilk_iz", "İlk İz", "Bölüm 1'i tamamla."),
        ("bir_resim", "Bir Resim", "Hakan'a kızının çizimini sor."),
        ("gozlemci", "Gözlemci", "B2'de camın ardındaki gecikmeyi fark et."),
        ("sessiz_adim", "Sessiz Adım", "Kırpıntı'ları tek mermi harcamadan atlat."),
        ("sogukkanli", "Soğukkanlı", "Hiçbir zamanlı seçimi kaçırmadan oyunu bitir."),
        ("kulak", "Kulak Kabartma", "Hiçbir YANKI taklidine kanmadan oyunu bitir."),
        ("arsivci", "Arşivci", "Altı kanıtın tamamını teslim et."),
        ("tam_defter", "Tam Defter", "Defterdeki bütün girdileri bul."),
        ("son_atis", "Son Atış", "Nöbetçi'yi Rezonans Kesici ile durdur."),
        ("eski_hat", "Eski Hat", "Nöbetçi'yi acil bastırma hattıyla durdur."),
        ("golge", "Gölge", "Bir keşfi hiç fark edilmeden ★★★ ile bitir."),
        ("stratejist", "Stratejist", "Bütün keşiflerde ★★★ al."),
        ("arsiv_faresi", "Arşiv Faresi", "On iki belgenin tamamını bul."),
        ("kabus", "Kâbus", "Oyunu Kâbus zorluğunda bitir."),
        ("esik", "Eşiğin Ardında", "Oyunu bitir."),
    ]
    for _aid, _an, _ad in ACHIEVEMENTS:
        achievement.register(_aid, stat_max=None)

    ACH_NAMES = {a: n for a, n, d in ACHIEVEMENTS}

    def unlock(aid):
        if not achievement.has(aid):
            achievement.grant(aid)
            achievement.sync()
            renpy.show_screen("achievement_toast", name=ACH_NAMES.get(aid, aid))
            renpy.sound.play("audio/sfx/notify.ogg", channel="audio")

screen achievement_toast(name):
    zorder 160
    frame at toast_in:
        xalign 1.0
        ypos 150
        xoffset -20
        padding (18, 10, 22, 12)
        background Solid("#14110ce8")
        hbox:
            spacing 12
            text "◆" size 26 color "#c8a24a" yalign 0.5
            vbox:
                text "BAŞARIM" size 12 color "#8a857c" kerning 3
                text name size 20 color "#e8d08a"
    timer 3.5 action Hide("achievement_toast")

transform toast_in:
    on show:
        xoffset 300 alpha 0.0
        easein 0.4 xoffset -20 alpha 1.0
    on hide:
        easeout 0.5 alpha 0.0

screen achievements():
    tag menu
    use game_menu(_("Başarımlar"), scroll="viewport"):
        vbox:
            spacing 8
            $ got = sum(1 for a, n, d in ACHIEVEMENTS if achievement.has(a))
            text "[got] / [len(ACHIEVEMENTS)] açıldı" size 18 color "#8a857c"
            null height 6
            for aid, aname, adesc in ACHIEVEMENTS:
                $ ok = achievement.has(aid)
                frame:
                    xfill True
                    background Solid("#1a170f" if ok else "#121315")
                    padding (16, 10, 16, 10)
                    hbox:
                        spacing 16
                        text ("◆" if ok else "◇") size 26 color ("#c8a24a" if ok else "#444") yalign 0.5
                        vbox:
                            text aname size 20 color ("#e8d08a" if ok else "#77736b")
                            text adesc size 16 color ("#cfc9bd" if ok else "#55524c")


## Açılış #####################################################################

label splashscreen:
    if renpy.has_label("autotest_run") and autotest_requested():
        jump autotest_run
    scene black
    $ renpy.pause(0.5, hard=True)
    show screen content_warning with Dissolve(1.0)
    $ renpy.pause(6.0 if not persistent.seen_warning else 3.0)
    hide screen content_warning with Dissolve(1.0)
    $ persistent.seen_warning = True
    return

init python:
    import os as _os
    def autotest_requested():
        return bool(_os.environ.get("ESIK_AUTOTEST"))

screen content_warning():
    add Solid("#000000")
    vbox:
        xalign 0.5
        yalign 0.45
        spacing 26
        xsize 760
        text "İÇERİK UYARISI" font "fonts/Oswald-Medium.ttf" size 20 color "#c2302f" kerning 10 xalign 0.5
        text "Bu oyun korku öğeleri, ani sesler, karanlık ortamlar, ölüm ve yas temaları içerir.":
            size 22 color "#cfc9bd" xalign 0.5 text_align 0.5
        null height 10
        text "En iyi deneyim için kulaklıkla, karanlık bir odada oyna.":
            size 20 color "#c8a24a" xalign 0.5 text_align 0.5
        text "Ani korkutmalar, ses altyazıları, ekran sarsıntısı ve zamanlı seçim süresi Ayarlar'dan değiştirilebilir.":
            size 16 color "#77736b" xalign 0.5 text_align 0.5


## Zorluk seçimi ##############################################################

screen difficulty():
    modal True
    add Solid("#050506")
    add "fog_overlay"
    vbox:
        xalign 0.5
        yalign 0.45
        spacing 22
        text "NASIL OYNAMAK İSTERSİN?" font "fonts/Oswald-Medium.ttf" size 34 color "#e6e2da" xalign 0.5 kerning 6
        null height 10
        button:
            xsize 720
            padding (28, 18, 28, 18)
            idle_background Solid("#121315")
            hover_background Solid("#2a2418")
            hover_sound "audio/sfx/ui_hover.ogg"
            activate_sound "audio/sfx/ui_select.ogg"
            action Return("gerilim")
            vbox:
                spacing 6
                text "GERİLİM" font "fonts/Oswald-SemiBold.ttf" size 28 kerning 4 color "#c8a24a"
                text "Önerilen deneyim. Zamanlı seçimler kısa, panik kararların bedeli ağır." size 17 color "#cfc9bd"
        button:
            xsize 720
            padding (28, 18, 28, 18)
            idle_background Solid("#121315")
            hover_background Solid("#1a2024")
            hover_sound "audio/sfx/ui_hover.ogg"
            activate_sound "audio/sfx/ui_select.ogg"
            action Return("hikaye")
            vbox:
                spacing 6
                text "HİKÂYE" font "fonts/Oswald-SemiBold.ttf" size 28 kerning 4 color "#6fa8dc"
                text "Hikâyeye odaklan. Zamanlı seçimlerde iki kat süre, gerginlik yavaş artar." size 17 color "#cfc9bd"
        if persistent.completed:
            button:
                xsize 720
                padding (28, 18, 28, 18)
                idle_background Solid("#160c0c")
                hover_background Solid("#2a1212")
                hover_sound "audio/sfx/ui_hover.ogg"
                activate_sound "audio/sfx/ui_select.ogg"
                action Return("kabus")
                vbox:
                    spacing 6
                    text "KÂBUS" font "fonts/Oswald-SemiBold.ttf" size 28 kerning 4 color "#d04a3a"
                    text "Oyunu bitirenler için. Daha az can, keşif atlanamaz, yaratıklar daha iyi duyar, süreler kısa." size 17 color "#cfc9bd"
        null height 6
        text "Ayarlar'dan istediğin zaman değiştirebilirsin." size 15 color "#666" xalign 0.5


## İlk karşılaşma ipuçları ####################################################

screen tip_card(title, body):
    modal True
    zorder 170
    add Solid("#000000a0")
    frame:
        xalign 0.5
        yalign 0.42
        xsize 680
        padding (34, 26, 34, 26)
        background Solid("#14130f")
        vbox:
            spacing 14
            text "İPUCU" size 13 color "#8a857c" kerning 4
            text title font "fonts/Oswald-Medium.ttf" size 28 kerning 2 color "#c8a24a"
            text body size 19 color "#cfc9bd"
            null height 6
            textbutton _("Anladım"):
                xalign 1.0
                action Return()
                text_size 20
                text_idle_color "#cfc9bd"
                text_hover_color "#e8d08a"
    key "dismiss" action Return()

label tip(tid, title, body):
    if autotest_mode or tid in persistent.tips:
        return
    $ persistent.tips.add(tid)
    $ renpy.sound.play("audio/sfx/notify.ogg", channel="audio")
    call screen tip_card(title, body)
    return


## Bölüm sonu özeti ###########################################################

screen chapter_summary(num, title, yeni_not, yeni_kanit, kanma):
    modal True
    zorder 120
    add Solid("#000000")
    vbox:
        xalign 0.5
        yalign 0.42
        spacing 10
        text "BÖLÜM [num] TAMAMLANDI" font "fonts/Oswald-Medium.ttf" size 20 color "#c8a24a" kerning 8 xalign 0.5
        text "[title]" size 64 color "#e6e2da" font "fonts/Oswald-SemiBold.ttf" kerning 10 xalign 0.5
        null height 30
        grid 4 1:
            xalign 0.5
            spacing 50
            vbox:
                text "[yeni_not]" size 40 color "#e6e2da" xalign 0.5
                text "yeni ipucu" size 15 color "#8a857c" xalign 0.5
            vbox:
                text "[yeni_kanit]" size 40 color "#d06050" xalign 0.5
                text "kanıt" size 15 color "#8a857c" xalign 0.5
            vbox:
                text "[kanma]" size 40 color ("#8a949c" if kanma else "#e6e2da") xalign 0.5
                text "YANKI'ya kanma" size 15 color "#8a857c" xalign 0.5
            vbox:
                text "[gerginlik]" size 40 color ("#c2302f" if gerginlik >= 60 else "#e6e2da") xalign 0.5
                text "nabız" size 15 color "#8a857c" xalign 0.5
        null height 40
        text "Otomatik kaydedildi" size 14 color "#55524c" xalign 0.5
        null height 8
        textbutton _("Devam ▸"):
            xalign 0.5
            action Return()
            text_size 24
            text_idle_color "#cfc9bd"
            text_hover_color "#e8d08a"
    if autotest_mode:
        timer 0.1 action Return()
    key "dismiss" action Return()

label chapter_outro(num):
    $ chap_info = CHAPTERS[num - 1]
    $ silence(1.5)
    $ renpy.music.stop(channel="pulse", fadeout=1.0)
    window hide
    scene black with Dissolve(1.2)
    if num == 1:
        $ unlock("ilk_iz")
    $ renpy.force_autosave(take_screenshot=False)
    $ quick_menu = False
    call screen chapter_summary(str(num).zfill(2), chap_info[1], len(notes) - chapter_notes_start, len(kanit) - chapter_kanit_start, sahte_kanma - chapter_kanma_start)
    $ quick_menu = True
    return


## Final başarımları ##########################################################

label final_achievements:
    $ unlock("esik")
    if zorluk == "kabus":
        $ unlock("kabus")
        $ persistent.kabus_done = True
    if sahte_kanma == 0:
        $ unlock("kulak")
    if qte_kacan == 0:
        $ unlock("sogukkanli")
    if len(kanit) >= len(EVIDENCE):
        $ unlock("arsivci")
    if len(notes) >= len(JOURNAL):
        $ unlock("tam_defter")
    if kirpinti_atlatma >= 1 and kirpinti_vuruldu == 0:
        $ unlock("sessiz_adim")
    return
