## Oyun sistemleri: HUD, zamanlı seçim, defter, bölüm kartı, bölüm seçme ######

init -2 python:

    CHAPTERS = [
        (1, "KAYIP", "6–9 Kasım 2026 · Çamlık Kasabası"),
        (2, "KARA DOSYA", "9 Kasım · Akşam"),
        (3, "BEŞ NOKTA", "9 Kasım · Gece"),
        (4, "RIZA'NIN RÖLESİ", "9 Kasım · Gece"),
        (5, "YANLIŞ SES", "9 Kasım · Gece"),
        (6, "SÜRÜNGEN", "10 Kasım · Şafak öncesi"),
        (7, "GİZLİ GİRİŞ", "10 Kasım · Sabah"),
        (8, "ECHO", "10 Kasım · 12.07–13.30 · B3 ve güvenlik girişi"),
        (9, "BİR RESİM", "10 Kasım · 13.30–15.02 · Güvenlik bölümü"),
        (10, "D-14", "10 Kasım · 15.03–18.21 · Ara Kat D"),
        (11, "YALNIZLIK", "10 Kasım · 18.34–20.12 · B3/B2 geçişi"),
        (12, "GÖZLEM", "10 Kasım · 20.24–22.31 · B2"),
        (13, "DERİNLİK", "10 Kasım 22.34 – 11 Kasım 01.02 · B2 servis arşivi"),
        (14, "KAYIT DIŞI", "11 Kasım · 01.09–02.43 · Güvenlik yönlendirme"),
        (15, "YENİDEN", "11 Kasım · 02.47–03.46 · Transfer Odası 03"),
        (16, "MERKEZ", "11 Kasım · 03.49–04.38 · Z0"),
        (17, "EŞİK", "11 Kasım · 04.39–05.17 · Z0 yönetim çekirdeği"),
        (18, "SON GEÇİT", "11 Kasım · 05.18–07.30 · Z0'dan Çamlık'a"),
    ]

    MAP_CHAPTER = {"kule": 3, "orman": 5, "servis": 6, "b3": 8, "gecis": 11, "drenaj": 13, "tahliye": 18}

    def chapter_label(n):
        return "ch%02d" % n

    def qte_time(sec):
        k = 2.0 if (persistent.qte_relaxed or store.zorluk == "hikaye") else 1.0
        if store.zorluk == "kabus" and not persistent.qte_relaxed:
            k = 0.75
        return sec * k


default autotest_mode = False

## Bölüm kartı ################################################################

screen chapter_card(num, title, sub):
    zorder 120
    add Solid("#000000")
    vbox:
        xalign 0.5
        yalign 0.45
        spacing 14
        text "BÖLÜM [num]":
            xalign 0.5
            font "fonts/Oswald-Medium.ttf"
            size 22
            color "#c8a24a"
            kerning 10
        text "[title]":
            xalign 0.5
            size 84
            font "fonts/Oswald-SemiBold.ttf"
            kerning 12
            color "#e6e2da"
            at glitchy
        null height 6
        text "[sub]":
            xalign 0.5
            size 20
            color "#8a857c"

label chapter_intro(num):
    $ chap_info = CHAPTERS[num - 1]
    $ current_chapter = num
    $ persistent.max_chapter = max(persistent.max_chapter, num)
    $ stress(-25)
    $ chapter_notes_start = len(notes)
    $ chapter_kanit_start = len(kanit)
    $ chapter_kanma_start = sahte_kanma
    $ save_name = "Bölüm %02d — %s" % (num, chap_info[1])
    $ apply_camera()
    $ silence(1.0)
    window hide
    scene black with Dissolve(1.0)
    $ sfx("sting")
    $ quick_menu = False
    show screen chapter_card(str(num).zfill(2), chap_info[1], chap_info[2]) with Dissolve(0.8)
    $ renpy.pause(3.2)
    hide screen chapter_card with Dissolve(0.8)
    $ quick_menu = True
    return


## HUD ########################################################################

screen hud():
    zorder 40
    $ minigame = any(renpy.get_screen(n) for n in ("radio_tune", "waveform_puzzle", "flashlight_search", "end_report", "loadout", "doc_reader"))
    if show_hud and not main_menu and not minigame:
        frame:
            xalign 1.0
            xoffset -14
            ypos 14
            xsize 214
            padding (14, 10, 14, 12)
            background Solid("#05070acc")
            vbox:
                spacing 5
                hbox:
                    xfill True
                    text "FENER" style "hud_label"
                    text "[pil]%" style "hud_value" xalign 1.0 color ("#e05040" if pil < 25 else "#e6e2da")
                bar:
                    value StaticValue(pil, 100)
                    xfill True
                    ysize 4
                    left_bar Solid("#e05040" if pil < 25 else "#c8a24a")
                    right_bar Solid("#1c1a16")
                hbox:
                    xfill True
                    text "NABIZ" style "hud_label"
                    text "[gerginlik]" style "hud_value" xalign 1.0 color ("#e05040" if gerginlik >= 70 else "#e6e2da")
                bar:
                    value StaticValue(gerginlik, 100)
                    xfill True
                    ysize 4
                    left_bar Solid("#c2302f")
                    right_bar Solid("#1c1a16")
                null height 2
                grid 3 2:
                    xfill True
                    spacing 2
                    text "● [mermi]" style "hud_item"
                    text "◍ [sise]" style "hud_item"
                    text "✚ [ilkyardim]" style "hud_item"
                    text "▮ [yedek_pil]" style "hud_item"
                    text "◉ [kaydedici]" style "hud_item"
                    if rezonans_alindi:
                        text "◆ [rezonans]" style "hud_item" color "#b0a8ff"
                    else:
                        null

style hud_label is default:
    font "fonts/Oswald-Medium.ttf"
    size 13
    kerning 3
    color "#8a857c"

style hud_value is default:
    font "fonts/Oswald-Medium.ttf"
    size 14
    color "#e6e2da"

style hud_item is default:
    size 14
    color "#cfc9bd"

init python:
    config.overlay_screens.append("hud")


## Zamanlı seçim ##############################################################
##
## call screen qte("Ne yapacaksın?", [("Seçenek", "deger"), ...], 5.0, "zaman_asimi")
## Süre dolarsa timeout değeri döner.

screen qte(prompt, options, seconds=5.0, timeout=None):
    modal True
    zorder 150

    default total = qte_time(seconds)
    default remaining = qte_time(seconds)

    timer 0.05 repeat True action If(remaining > 0.05, SetScreenVariable("remaining", remaining - 0.05), [SetVariable("qte_kacan", qte_kacan + 1), Return(timeout)])

    ## Yalnızca otomatik testte (autotest_mode) rastgele seçim yapar.
    if autotest_mode:
        timer 0.25 action Return(renpy.random.choice(options)[1])

    add Solid("#1a000055")

    vbox:
        xalign 0.5
        ypos 170
        spacing 18

        text prompt:
            xalign 0.5
            size 28
            color "#ffdddd"
            outlines [(2, "#000000", 0, 0)]

        bar:
            value StaticValue(remaining, total)
            xalign 0.5
            xsize 620
            ysize 8
            left_bar Solid("#c2302f")
            right_bar Solid("#2a1212")

        null height 10

        for cap, val in options:
            textbutton cap:
                style "choice_button"
                text_style "choice_button_text"
                action Return(val)

    on "show" action Play("sfx2", "audio/sfx/heartbeat.ogg")
    on "hide" action Stop("sfx2")


## Defter #####################################################################

screen journal():
    tag menu

    use game_menu(_("Defter"), scroll="viewport"):

        style_prefix "journal"

        vbox:
            spacing 10

            if show_hud:
                $ rt = ("   ·   Rezonans %d" % rezonans) if rezonans_alindi else ""
                text "Fener [pil]%   ·   Mermi [mermi]   ·   İlk yardım [ilkyardim][rt]" size 16 color "#8a857c"
                null height 6

            label _("İpuçları")
            if not notes:
                text _("Henüz bir şey yazılmadı.") color "#666"
            for nid in reversed(notes):
                $ t, body = JOURNAL[nid]
                frame:
                    xfill True
                    background Solid("#16171a")
                    padding (16, 10, 16, 12)
                    vbox:
                        spacing 4
                        text t size 19 color "#c8a24a"
                        text body size 17 color "#cfc9bd"

            if kanit:
                null height 14
                label _("Kanıtlar")
                for eid in kanit:
                    $ t, body = EVIDENCE[eid]
                    frame:
                        xfill True
                        background Solid("#1a1214")
                        padding (16, 10, 16, 12)
                        vbox:
                            spacing 4
                            text t size 19 color "#d06050"
                            text body size 17 color "#cfc9bd"

    key "K_j" action Return()

style journal_label_text:
    size 24
    color "#e6e2da"

style journal_text:
    size 17


## Bölüm seç ##################################################################

screen chapter_select():
    tag menu

    use game_menu(_("Bölüm Seç"), scroll="viewport"):
        vbox:
            spacing 6
            text _("Ulaştığın bölümlerden başlayabilirsin. Kaynaklar o bölüme göre ayarlanır.") size 17 color "#8a857c"
            null height 8
            for num, title, sub in CHAPTERS:
                $ cmaps = [k for k, v in MAP_CHAPTER.items() if v == num]
                $ cst = "".join(("★" * persistent.map_stars.get(k, 0)).ljust(3, "☆") for k in cmaps)
                if num <= persistent.max_chapter:
                    textbutton "{:02d}  ·  {}   {}".format(num, title, cst):
                        action Start("sel_%02d" % num)
                        text_size 22
                        text_idle_color "#cfc9bd"
                        text_hover_color "#e8d08a"
                else:
                    textbutton "{:02d}  ·  ? ? ?".format(num):
                        action NullAction()
                        sensitive False
                        text_size 22


## Fener kontrolü #############################################################
## Karanlık bölümlerden sonra çağrılır: call pil_check

label pil_check:
    if pil <= 30 and yedek_pil:
        $ sfx("flashlight")
        menu:
            "Fener titriyor (kalan pil: [pil]). Yedek pili tak.":
                $ pil = 100
                $ yedek_pil -= 1
                narrator "Yeni pil yerine oturur. Işık yeniden beyazlaşır."
            "Şimdilik idare et.":
                pass
    elif pil == 0:
        $ stress(10)
        narrator "Fener tamamen söndü. Telefonun ekran ışığıyla ilerlemek zorundasın."
    elif pil <= 20:
        $ stress(5)
        narrator "Fenerin ışığı sararıyor. Karanlık, ışığın kenarından içeri sızıyor."
    return
