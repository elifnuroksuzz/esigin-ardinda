## EŞİĞİN ARDINDA — Arayüz ekranları
## Görsel dosyası gerektirmeyen, renk tabanlı karanlık arayüz.

init offset = -1

################################################################################
## Stiller
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")

style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5

style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")

style bar:
    ysize gui.bar_size
    left_bar Solid("#c8a24a")
    right_bar Solid("#2a2620")

style vbar:
    xsize gui.bar_size
    top_bar Solid("#2a2620")
    bottom_bar Solid("#c8a24a")

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Solid("#1c1a17")
    thumb Solid("#6a5a3a")

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Solid("#1c1a17")
    thumb Solid("#6a5a3a")

style slider:
    ysize gui.slider_size
    base_bar Solid("#2a2620")
    thumb Solid("#c8a24a")
    thumb_offset 0

style vslider:
    xsize gui.slider_size
    base_bar Solid("#2a2620")
    thumb Solid("#c8a24a")

style frame:
    padding gui.frame_borders.padding
    background Solid("#121315ee")

################################################################################
## Oyun içi ekranlar
################################################################################

## Diyalog ####################################################################

screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        if who is not None:
            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"

    ## Yan görüntü (kullanılmıyor ama standart destek)
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label

style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    background Fixed(
        Solid("#050607d8"),
        Solid("#c8a24a40", ysize=1),
        )

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    ypos gui.name_ypos
    ypadding 14
    background None

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5
    outlines [(2, "#000000aa", 0, 0)]

style say_dialogue:
    properties gui.text_properties("dialogue")
    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos
    adjust_spacing False
    line_spacing 4
    outlines [(1, "#00000088", 0, 0)]

## Girdi ######################################################################

screen input(prompt):
    style_prefix "input"

    window:
        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width

## Seçim ######################################################################

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action

style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 300
    yanchor 0.5
    spacing gui.choice_spacing

style choice_button:
    xsize gui.choice_button_width
    xalign 0.5
    padding (40, 12, 40, 12)
    idle_background Solid("#0b0c0ecc")
    hover_background Solid("#3a2f18ee")
    insensitive_background Solid("#0b0c0e88")
    hover_sound "audio/sfx/ui_hover.ogg"
    activate_sound "audio/sfx/ui_select.ogg"

style choice_button_text:
    properties gui.text_properties("choice_button")
    xalign 0.5
    text_align 0.5

## Hızlı menü #################################################################

screen quick_menu():
    zorder 100

    if quick_menu:
        hbox:
            style_prefix "quick"
            xalign 0.5
            yalign 1.0

            textbutton _("Geri") action Rollback()
            textbutton _("Geçmiş") action ShowMenu('history')
            textbutton _("Defter") action ShowMenu('journal')
            textbutton _("Atla") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Oto") action Preference("auto-forward", "toggle")
            textbutton _("Kaydet") action ShowMenu('save')
            textbutton _("H.Kayıt") action QuickSave()
            textbutton _("H.Yükle") action QuickLoad()
            textbutton _("Ayarlar") action ShowMenu('preferences')

init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")
    padding (10, 4, 10, 4)

style quick_button_text:
    properties gui.text_properties("quick_button")

################################################################################
## Ana ve oyun menüsü
################################################################################

screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.5

        spacing gui.navigation_spacing

        if main_menu:
            if renpy.newest_slot() is not None:
                textbutton _("Devam Et") action FileLoad(renpy.newest_slot(), slot=True)
            textbutton _("Yeni Oyun") action Start()
            if persistent.max_chapter > 1:
                textbutton _("Bölüm Seç") action ShowMenu("chapter_select")
        else:
            textbutton _("Geçmiş") action ShowMenu("history")
            textbutton _("Defter") action ShowMenu("journal")
            textbutton _("Kaydet") action ShowMenu("save")

        textbutton _("Yükle") action ShowMenu("load")
        textbutton _("Ayarlar") action ShowMenu("preferences")

        if _in_replay:
            textbutton _("Tekrarı Bitir") action EndReplay(confirm=True)
        elif not main_menu:
            textbutton _("Ana Menü") action MainMenu()

        textbutton _("Başarımlar") action ShowMenu("achievements")
        textbutton _("Hakkında") action ShowMenu("about")
        textbutton _("Yardım") action ShowMenu("help")

        if renpy.variant("pc"):
            textbutton _("Çıkış") action Quit(confirm=not main_menu)

style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    padding (6, 6, 6, 6)
    hover_sound "audio/sfx/ui_hover.ogg"

style navigation_button_text:
    size 26
    idle_color "#8f8a80"
    hover_color "#e8d08a"
    selected_color "#ffffff"
    insensitive_color "#44444480"


screen main_menu():
    tag menu

    add gui.main_menu_background
    add "fog_overlay"

    frame:
        style "main_menu_frame"

    use navigation

    vbox:
        xalign 0.95
        yalign 0.88
        spacing 4
        text "EŞİĞİN ARDINDA":
            size 64
            color "#e6e2da"
            font "DejaVuSans-Bold.ttf"
            xalign 1.0
            outlines [(3, "#000000", 0, 0)]
            at title_flicker
        text "Çamlık Kasabası  •  ECHO  •  YANKI":
            size 20
            color "#c8a24a"
            xalign 1.0
        text "[config.version]":
            size 14
            color "#666"
            xalign 1.0

style main_menu_frame:
    xsize 300
    yfill True
    background Solid("#000000a0")

transform title_flicker:
    alpha 1.0
    pause 4.0
    linear 0.05 alpha 0.55
    linear 0.05 alpha 1.0
    pause 0.2
    linear 0.04 alpha 0.7
    linear 0.04 alpha 1.0
    pause 7.0
    repeat


screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":
                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True
                        side_yfill True
                        vbox:
                            spacing spacing
                            transclude

                elif scroll == "vpgrid":
                    vpgrid:
                        cols 1
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True
                        side_yfill True
                        spacing spacing
                        transclude
                else:
                    transclude

    use navigation

    textbutton _("Geri"):
        style "return_button"
        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")

style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar
style game_menu_label is gui_label
style game_menu_label_text is gui_label_text
style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 30
    top_padding 120
    background Solid("#0b0c0e")

style game_menu_navigation_frame:
    xsize 280
    yfill True

style game_menu_content_frame:
    left_margin 40
    right_margin 20
    top_margin 10

style game_menu_viewport:
    xsize 920

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 10

style game_menu_label:
    xpos 50
    ysize 120

style game_menu_label_text:
    size gui.title_text_size
    color "#c8a24a"
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -30

## Hakkında ###################################################################

screen about():
    tag menu
    use game_menu(_("Hakkında"), scroll="viewport"):
        style_prefix "about"
        vbox:
            label "[config.name!t]"
            text _("Sürüm [config.version!t]\n")
            if gui.about:
                text "[gui.about!t]\n"
            text _("[renpy.version_only] sürümlü {a=https://www.renpy.org/}Ren'Py{/a} ile yapıldı.\n\n[renpy.license!t]")

style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size

## Kaydet / Yükle #############################################################

screen save():
    tag menu
    use file_slots(_("Kaydet"))

screen load():
    tag menu
    use file_slots(_("Yükle"))

screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Sayfa {}"), auto=_("Otomatik"), quick=_("Hızlı"))

    use game_menu(title):

        fixed:
            order_reverse True

            button:
                style "page_label"
                key_events True
                xalign 0.5
                action page_name_value.Toggle()
                input:
                    style "page_label_text"
                    value page_name_value

            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"
                xalign 0.5
                yalign 0.5
                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):
                    $ slot = i + 1
                    button:
                        action FileAction(slot)
                        has vbox
                        add FileScreenshot(slot) xalign 0.5
                        text FileTime(slot, format=_("{#file_time}%d.%m.%Y, %H:%M"), empty=_("boş yuva")):
                            style "slot_time_text"
                        text FileSaveName(slot):
                            style "slot_name_text"
                        key "save_delete" action FileDelete(slot)

            vbox:
                style_prefix "page"
                xalign 0.5
                yalign 1.0
                hbox:
                    xalign 0.5
                    spacing gui.page_spacing
                    textbutton _("<") action FilePagePrevious()
                    textbutton _("{#auto_page}O") action FilePage("auto")
                    textbutton _("{#quick_page}H") action FilePage("quick")
                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)
                    textbutton _(">") action FilePageNext()

style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text
style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 50
    ypadding 3

style page_label_text:
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    padding (10, 4, 10, 4)

style page_button_text:
    idle_color gui.idle_color
    hover_color gui.hover_color
    selected_color gui.selected_color

style slot_button:
    xsize gui.slot_button_width
    ysize gui.slot_button_height
    padding (10, 10, 10, 10)
    idle_background Solid("#16171a")
    hover_background Solid("#2a2418")

style slot_button_text:
    size gui.slot_button_text_size
    xalign 0.5
    idle_color gui.idle_small_color
    hover_color gui.hover_color

## Ayarlar ####################################################################

screen preferences():
    tag menu

    use game_menu(_("Ayarlar"), scroll="viewport"):

        vbox:
            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):
                    vbox:
                        style_prefix "radio"
                        label _("Ekran")
                        textbutton _("Pencere") action Preference("display", "window")
                        textbutton _("Tam ekran") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "check"
                    label _("Atla")
                    textbutton _("Okunmamış metin") action Preference("skip", "toggle")
                    textbutton _("Seçimden sonra") action Preference("after choices", "toggle")
                    textbutton _("Geçişler") action InvertSelected(Preference("transitions", "toggle"))

                vbox:
                    style_prefix "check"
                    label _("Erişilebilirlik")
                    textbutton _("Ekran sarsıntısı") action ToggleField(persistent, "allow_shake")
                    textbutton _("Yanıp sönme") action ToggleField(persistent, "allow_flash")
                    textbutton _("Zamanlı seçimde 2× süre") action ToggleField(persistent, "qte_relaxed")

                vbox:
                    style_prefix "check"
                    label _("Görüntü")
                    textbutton _("Film greni") action ToggleField(persistent, "grain")
                    textbutton _("Nefes alan kamera") action [ToggleField(persistent, "camera_drift"), Function(apply_camera)]
                    if not main_menu:
                        textbutton _("Hikâye modu") action ToggleVariable("zorluk", "hikaye", "gerilim")

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:
                    label _("Metin hızı")
                    bar value Preference("text speed")
                    label _("Oto ilerleme süresi")
                    bar value Preference("auto-forward time")

                vbox:
                    label _("Müzik / Ambiyans")
                    hbox:
                        bar value Preference("music volume")
                    label _("Efekt sesi")
                    hbox:
                        bar value Preference("sound volume")
                        if config.sample_sound:
                            textbutton _("Dene") action Play("sound", config.sample_sound)
                    null height gui.pref_spacing
                    textbutton _("Tümünü sustur"):
                        action Preference("all mute", "toggle")
                        style "mute_all_button"

style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox
style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox
style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox
style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox
style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0
    size 22

style pref_vbox:
    xsize 300

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    padding (24, 4, 4, 4)
    selected_background Solid("#c8a24a30")

style radio_button_text:
    properties gui.text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    padding (24, 4, 4, 4)
    selected_background Solid("#c8a24a30")

style check_button_text:
    properties gui.text_properties("check_button")

style slider_slider:
    xsize 350

style slider_button:
    yalign 0.5
    left_margin 10

style slider_vbox:
    xsize 450

## Geçmiş #####################################################################

screen history():
    tag menu
    predict False

    use game_menu(_("Geçmiş"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing):

        style_prefix "history"

        for h in _history_list:
            window:
                has fixed:
                    yfit True
                if h.who:
                    label h.who:
                        style "history_name"
                        substitute False
                        if "color" in h.who_args:
                            text_color h.who_args["color"]
                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("Henüz diyalog geçmişi yok.")

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art", "i", "b" }

style history_window is empty
style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text
style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    text_align gui.history_name_xalign
    size 20

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    text_align gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")
    size 20

style history_label:
    xfill True

style history_label_text:
    xalign 0.5

## Yardım #####################################################################

screen help():
    tag menu

    use game_menu(_("Yardım"), scroll="viewport"):
        style_prefix "help"
        vbox:
            spacing 12
            text _("{b}Nasıl oynanır{/b}") color "#c8a24a"
            text _("Tıkla / Boşluk / Enter: ilerle.   Fare tekerleği yukarı: geri sar.")
            text _("J: Defter (ipuçları ve kanıtlar).   Esc / sağ tık: menü.   Ctrl: atla.")
            text _("H: arayüzü gizle.   S: ekran görüntüsü.")
            null height 10
            text _("{b}Hayatta kalma{/b}") color "#c8a24a"
            text _("• Duyduğun her sesi takip etme. Tekrar eden nefes, gecikme ve yön değişimi YANKI'nın işaretidir.")
            text _("• Kırmızı çubuklu seçimler zamanlıdır. Süre biterse karar senin yerine verilir.")
            text _("• Normal mermi büyük YANKI'lara işlemez. Rezonans Kesici mermileri değerlidir.")
            text _("• Fener pili azalırsa karanlık bölümler zorlaşır. Gerginlik yükseldikçe algın bozulur.")
            text _("• Hata yapmak oyunu bitirmez: bir bedeli olur ya da yeniden denersin.")

style help_text is gui_text
style help_text:
    size 20

################################################################################
## Ek ekranlar
################################################################################

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    style_prefix "confirm"

    add Solid("#000000c0")

    frame:
        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100
                textbutton _("Evet") action yes_action
                textbutton _("Hayır") action no_action

    key "game_menu" action no_action

style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Solid("#121315f4")
    padding (40, 40, 40, 40)
    xalign .5
    yalign .5

style confirm_prompt_text:
    text_align 0.5
    layout "subtitle"

style confirm_button:
    padding (10, 6, 10, 6)

style confirm_button_text:
    idle_color gui.idle_color
    hover_color gui.hover_color


screen skip_indicator():
    zorder 100
    style_prefix "skip"

    frame:
        hbox:
            spacing 6
            text _("Atlanıyor")
            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"

transform delayed_blink(delay, cycle):
    alpha .5
    pause delay
    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat

style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Solid("#000000a0")
    padding (16, 5, 30, 5)

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    font "DejaVuSans.ttf"


screen notify(message):
    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')

transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0

style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos
    background Solid("#1a160ee8")
    padding (16, 6, 30, 6)

style notify_text:
    size gui.notify_text_size
    color "#e8d08a"


## NVL (yedek; oyun NVL kullanmıyor) ##########################################

screen nvl(dialogue, items=None):
    window:
        style "nvl_window"
        has vbox:
            spacing gui.nvl_spacing
        use nvl_dialogue(dialogue)
        for i in items or []:
            textbutton i.caption:
                action i.action
                style "nvl_button"
    add SideImage() xalign 0.0 yalign 1.0

screen nvl_dialogue(dialogue):
    for d in dialogue:
        window:
            id d.window_id
            fixed:
                yfit gui.nvl_height is None
                if d.who is not None:
                    text d.who:
                        id d.who_id
                text d.what:
                    id d.what_id

define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default
style nvl_label is say_label
style nvl_dialogue is say_dialogue
style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True
    background Solid("#000000c0")
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    text_align gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    text_align gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign
