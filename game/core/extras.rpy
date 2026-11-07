## EK SİSTEMLER ###############################################################
##
## * Belgeler ve Arşiv (Resident Evil tarzı toplanabilir dosyalar)
## * Ses altyazıları (erişilebilirlik)
## * Korkutma anı (yakalanınca)
## * Telsiz ayarlama mini oyunu (Oxenfree esintisi)
## * Ses dalgası analizi bulmacası
## * Fenerle karanlıkta arama
## * Oyun sonu raporu ve Kâbus modu istatistikleri

default persistent.docs = set()
default persistent.captions = False
default persistent.jumpscares = True
default persistent.kabus_done = False

## İstatistikler
default st_caught = 0
default st_bottles = 0
default st_shots = 0
default st_turns = 0
default st_searches = 0
default st_listens = 0


## BELGELER ###################################################################

init -2 python:

    DOCS = [
        ("riza_defter", "RIZA'NIN RÖLE DEFTERİ", "El yazısı · Röle istasyonu",
         "14 Mart\nKule 2 yine sabaha karşı uğuldadı. Sayaç normal.\n\n"
         "2 Nisan\nECHO'dan iki adam geldi. Kayıtları istediler. Vermedim.\nDefteri sobanın arkasına koydum.\n\n"
         "6 Kasım\nSaat 22.40 civarı köpekler havlamaya başladı.\n22.46'da hepsi birden sustu. Aynı dakika elektrik gitti.\n"
         "Kırk yıldır bu vadideyim. Böyle bir sessizlik duymadım.\n\n"
         "Bir de şu: kapının önünden biri 'Rıza amca' diye seslendi.\nRahmetli karımın sesiyle."),
        ("kule_bakim", "KULE 3 · BAKIM KAYDI", "Form BK-07 · Eski bekçi kulübesi",
         "Gövde uğultusu: normal aralıkta (38–55 Hz)\nZ0 bağlantısı: AKTİF\nKablo zırhı: sağlam\n\n"
         "Not: Köyden ses şikâyeti. Bir kadın 'Geceleri adımı çağırıyorlar' diyor.\n"
         "Raporlanmadı. Yönetim: 'Yerel halkla temas asgari tutulacak.'\n\n"
         "Not 2: Tel örgü iki kez kesik bulundu. Biri kuleye ulaşmaya çalışıyor.\nYa da kuleden uzaklaşmaya."),
        ("orman_isaret", "ORMAN MUHAFAZA MEMURU NOTU", "Islak bir not defteri sayfası · Yamaç",
         "Aynı devrik ağaca üç kez çıktım.\nPusula dönüyor. GPS 'konum bulunamadı' diyor.\n\n"
         "Taşa çizik atmayı öğrendim. Çizik değişmiyor.\nBen değişiyorum. Yol değişmiyor, ben yanlış hatırlıyorum.\n\n"
         "Kural: Duyduğuna değil, gördüğüne git.\nKural 2: Gördüğüne de tam güvenme. Eğime güven. Su hep aşağı akar."),
        ("surungen_kayit", "DIŞ KAMERA 4 · OLAY DÖKÜMÜ", "Güvenlik çıktısı · Hendek",
         "02.11  Hareket: servis duvarı, dikey yüzey\n02.11  Hedef boyutu: insan boyunun ~2 katı\n"
         "02.12  Projektör AÇIK → hedef hızlandı, kameraya yöneldi\n02.12  Kamera 4 bağlantısı kesildi\n\n"
         "El yazısı not: Işığı açmayın. Işığa geliyor.\nDar yerlere giremiyor. Kaya yarığı güvenli."),
        ("hakan_vardiya", "VARDİYA DEFTERİ · H. ERSOY", "B3 güvenlik · Malzeme deposu",
         "03.10  B3 tur tamam. Pres hattında sürtünme sesi. Kaynağı bulunamadı.\n"
         "03.40  Ses tekrar. Pres gürlediğinde duruyor, susunca devam ediyor.\n         Bir şey presin sesini dinliyor gibi.\n\n"
         "04.15  Nöbetçi diyorlar ona. Havalandırmaya giremiyor. Not ettim.\n\n"
         "05.00  Kızımın resmini dolabıma astım. Boyumu biraz abartmış.\n         Sabah götüreceğim."),
        ("yanki_siniflandirma", "YANKI SINIFLANDIRMA TABLOSU", "Taslak · Kazan dairesi panosu",
         "TAKLİTÇİ   Ses ve görünüş taklidi. Hareket gecikmeli (~0,4 sn).\n"
         "SÜRÜNGEN   Dikey yüzeylerde hareket. Işığa yönelir. Çok hızlı.\n"
         "GÖZCÜ      Büyük gözlem tehdidi. Ayrıntılar gizli.\n"
         "BOŞLUK     Algı bozulması. Mesafe ve yön yanılsaması.\n"
         "NÖBETÇİ    Ağır, sesle avlanır, normal mühimmata dayanıklı.\n"
         "KIRPINTI   Küçük, kör, sese aşırı duyarlı. Normal mermiyle durur.\n\n"
         "Not: 'Kontrol edilebilir' ibaresi Dr. Demir'in itirazıyla çizildi.\nSonra biri yeniden yazdı."),
        ("kemal_gunluk", "DR. K. DEMİR · KİŞİSEL NOTLAR, 2024", "Katlanmış kâğıt · Atölye",
         "Denek 14 ve Denek 16 ile üçüncü hafta.\nRezonans yönlendirmesi kâğıt üzerinde çalışıyor.\nKâğıt üzerinde.\n\n"
         "Voss sonuçları 'umut verici' diye raporladı.\nBen 'tehlikeli' yazdım. Raporumdan o kelime çıkarıldı.\n\n"
         "Bugün Aras'ın doğum günüydü. Yine aramadım.\nNe diyeceğimi bilmiyorum. 'Babam bir şey saklıyor' diye düşünüyordur.\nHaklı."),
        ("voss_not", "YÖNETİM GENELGESİ · A. VOSS", "Resmî yazı · B2 arşivi",
         "Konu: Karantina protokolleri\n\n"
         "1. Ara Kat D biyolojik tehdit protokolü OTOMATİK kalacaktır.\n   İnsan onayı adımı veri sürekliliğini tehlikeye atar.\n"
         "2. Tahliye talepleri yönetim onayına tabidir.\n"
         "3. Dış temas (sivil) durumunda gözlem önceliklidir.\n\n"
         "Veri sürekliliği her şeyden önce gelir.\n\nA. Voss"),
        ("k2_rapor", "K-2 GÖREV KAYDI (EKSİK)", "Islanmış çıktı · Sifon",
         "22.42  K-2 eski servis yoluna yönlendirildi.\n       Sebep: dış sensör, sivil hareketi.\n"
         "22.43  Sivil görüldü. 16 yaş civarı. Bir varlıktan kaçıyor.\n"
         "22.44  S-17 iç taraftan açıldı. Sivil içeri alındı.\n"
         "22.46  [BAĞLANTI KESİLDİ]\n\n"
         "El yazısı ek: Çocuk güvende. Ailesine haber verilsin.\n"
         "Altında başka bir el yazısı: TAHLİYE EDİLMEYECEK. GÖZLEM. — A.V."),
        ("rezonans_test", "REZONANS KESİCİ · TEST RAPORU", "Prototip 2024-R · Dar boru",
         "Test 1  Kırpıntı sınıfı      Başarılı. Rezonans kesintisi 4,2 sn.\n"
         "Test 2  Kırpıntı sınıfı      Başarılı. Rezonans kesintisi 5,1 sn.\n"
         "Test 3  Büyük varlık         YAPILMADI.\n\n"
         "Gözlem: Kesinti sırasında varlığın göğüs bölgesinde yarık açılıyor.\n"
         "Normal mühimmatın bu aralıkta etkili olup olmadığı bilinmiyor.\n\n"
         "Üretilen mermi: 3. Kalibre: standart tabanca."),
        ("hakan_kizi", "BABAMA", "Pastel boyalı bir not · Hakan'ın masası",
         "Baba,\nsen gece çalışınca ben de uyumuyorum.\nAnnem uyu diyor ama ben kapıyı bekliyorum.\n\n"
         "Resmini yaptım. Boyunu uzun yaptım çünkü sen uzunsun.\n\nErken gel.\n\n— kızın"),
        ("proje_bes", "PROJE BEŞ · DAĞITIM LİSTESİ", "Gizli · Pres hattı dolabı",
         "TESİS 01   ÇAMLIK          DURUM: AKTİF\n"
         "TESİS 02   [GİZLİ]          DURUM: AKTİF\n"
         "TESİS 03   ██████████       DURUM: ██████\n"
         "TESİS 04   ██████████       DURUM: ██████\n"
         "TESİS 05   ██████████       DURUM: ██████\n\n"
         "Bir tesisin kapatılması diğerlerini etkilemez.\nHer tesis kendi merkezine bağlıdır."),
    ]
    DOC_INFO = {d[0]: d for d in DOCS}

    def find_doc(did):
        new = did not in persistent.docs
        persistent.docs.add(did)
        if new:
            renpy.notify("Belge bulundu: " + DOC_INFO[did][1] + "   ·   Arşiv")
            if len(persistent.docs) >= len(DOCS):
                unlock("arsiv_faresi")
        return new


screen doc_reader(did, called=False):
    modal True
    zorder 180
    $ d = DOC_INFO[did]
    add Solid("#000000c8")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 700
        ysize 640
        background Frame("gui/paper.png", 20, 20)
        padding (54, 46, 54, 36)
        vbox:
            spacing 6
            text d[1] font "fonts/Oswald-SemiBold.ttf" size 26 color "#2a2218" kerning 2 substitute False
            text d[2] font "fonts/DejaVuSansMono.ttf" size 13 color "#6a5a44" substitute False
            null height 4
            add Solid("#6a5a4480", ysize=1)
            null height 10
            viewport:
                ysize 430
                mousewheel True
                scrollbars "vertical"
                text d[3] font "fonts/DejaVuSansMono.ttf" size 16 color "#2a2620" line_spacing 6 substitute False
            null height 8
            textbutton "KAPAT":
                xalign 1.0
                action If(called, Return(), Hide("doc_reader"))
                text_font "fonts/Oswald-Medium.ttf"
                text_size 18
                text_idle_color "#6a5a44"
                text_hover_color "#2a2218"
    key "game_menu" action If(called, Return(), Hide("doc_reader"))
    if autotest_mode:
        timer 0.05 action If(called, Return(), Hide("doc_reader"))

label read_doc(did):
    $ find_doc(did)
    if not autotest_mode:
        call screen doc_reader(did, True)
    return

screen archive():
    tag menu
    default sel = None
    use game_menu(_("Arşiv"), scroll="viewport"):
        vbox:
            spacing 8
            text "[len(persistent.docs)] / [len(DOCS)] belge bulundu. Keşiflerde ARA eylemiyle ve hikâye sahnelerinde bulunur." size 16 color "#8a857c"
            null height 6
            for did, title, src, body in DOCS:
                if did in persistent.docs:
                    button:
                        xfill True
                        padding (16, 10, 16, 10)
                        idle_background Solid("#1a1810")
                        hover_background Solid("#2e2818")
                        action Show("doc_reader", did=did)
                        hbox:
                            spacing 14
                            text "▤" size 22 color "#c8a24a"
                            vbox:
                                text title font "fonts/Oswald-Medium.ttf" size 19 color "#e8d08a"
                                text src size 13 color "#8a857c"
                else:
                    frame:
                        xfill True
                        padding (16, 10, 16, 10)
                        background Solid("#101113")
                        hbox:
                            spacing 14
                            text "▢" size 22 color "#3a3a3a"
                            text "? ? ?" font "fonts/Oswald-Medium.ttf" size 19 color "#444"


## SES ALTYAZILARI ############################################################

init -3 python:
    CAPTIONS = {
        "metal_drag": "metal üzerinde ağır bir sürtünme", "metal_knock": "metal vuruntular",
        "growl": "derin bir hırıltı", "kirpinti": "tıkırtılar", "crawl": "çok ayaklı bir şey hareket ediyor",
        "echo_voice": "yankılanan bir ses", "whisper": "fısıltı", "door_slam": "kapı çarparak kapanır",
        "door_open": "hidrolik kapı açılır", "gunshot": "silah sesi", "resonance_shot": "rezonans atışı",
        "suppress": "derin bir titreşim dalgası", "alarm": "alarm", "static": "parazit", "radio": "telsiz cızırtısı",
        "phone_beep": "telefon sinyali", "phone_cut": "hat kesilir", "phone_ring": "telefon çalar",
        "birds_stop": "kuşlar birden susar", "footsteps": "ayak sesleri", "thud": "boğuk bir darbe",
        "bottle": "cam kırılır", "fan": "pervane döner", "platform": "platform sarsılarak iner",
        "lever": "kol çekilir", "lock_click": "kilit sesi", "sting": "", "heartbeat": "kalp atışı",
        "jumpscare": "", "flashlight": "fener", "notify": "", "ui_hover": "", "ui_select": "",
        "radio_lock": "sinyal kilitlendi",
    }

    def show_caption(name):
        if not persistent.captions:
            return
        c = CAPTIONS.get(name, "")
        if c:
            renpy.show_screen("caption", msg="[ " + c + " ]")

screen caption(msg):
    zorder 150
    frame:
        xpos 40
        ypos 455
        padding (12, 4, 12, 4)
        background Solid("#000000b0")
        text msg size 16 color "#d8d2c6" italic True substitute False
    timer 2.6 action Hide("caption")


## KORKUTMA ANI ###############################################################

transform js_slam:
    xalign 0.5 yalign 0.62
    zoom 0.9 alpha 0.0
    linear 0.06 zoom 1.5 alpha 1.0
    ease 0.14 zoom 1.35
    block:
        linear 0.04 xoffset 14
        linear 0.04 xoffset -14
        repeat

screen jumpscare_scr(kind):
    zorder 200
    add Solid("#000000")
    add ("images/char/%s.png" % kind) at js_slam
    add "fx_red"

label jumpscare(kind):
    if not persistent.jumpscares or autotest_mode:
        $ sfx("growl")
        return
    $ sfx("jumpscare")
    show screen jumpscare_scr(kind)
    $ renpy.pause(0.85, hard=True)
    hide screen jumpscare_scr
    return


## TELSİZ AYARLAMA ############################################################
## Kaydırıcıyı sinyalin en güçlü olduğu frekansa getir ve 1,5 saniye tut.

init python:
    def radio_volume(sig):
        renpy.music.set_volume(max(0.08, 1.0 - sig), delay=0.1, channel="ambient2")

screen radio_tune(prompt, target, label_text="TELSİZ"):
    modal True
    default freq = 12.0
    default hold = 0.0
    default tick = 0
    $ diff = abs(freq - target)
    $ sig = max(0.0, 1.0 - diff / 22.0)
    $ locked = diff <= 2.5

    timer 0.1 repeat True action [Function(radio_volume, sig), SetScreenVariable("tick", tick + 1), If(locked, SetScreenVariable("hold", hold + 0.1), SetScreenVariable("hold", 0.0))]
    if hold >= 1.5:
        timer 0.01 action [Play("audio", "audio/sfx/radio_lock.ogg"), Return(True)]

    on "show" action Play("ambient2", "audio/amb/static_loop.ogg")
    on "hide" action Stop("ambient2", fadeout=0.5)

    add Solid("#05070a")
    add "fx_vignette"

    vbox:
        xalign 0.5
        yalign 0.42
        spacing 18
        text label_text font "fonts/Oswald-Medium.ttf" size 18 color "#8a857c" kerning 8 xalign 0.5
        text prompt size 20 color "#cfc9bd" xalign 0.5 text_align 0.5 xmaximum 900

        frame:
            xalign 0.5
            xsize 860
            padding (30, 24, 30, 24)
            background Solid("#0c1014")
            vbox:
                spacing 14
                hbox:
                    xfill True
                    text ("%.1f MHz" % (140.0 + freq * 0.3)) font "fonts/Oswald-SemiBold.ttf" size 46 color ("#9ec0a0" if locked else "#e8d08a")
                    vbox:
                        xalign 1.0
                        yalign 0.5
                        text "SİNYAL" font "fonts/Oswald-Medium.ttf" size 13 color "#8a857c" kerning 3 xalign 1.0
                        hbox:
                            spacing 3
                            xalign 1.0
                            for i in range(10):
                                add Solid("#9ec0a0" if (i < int(sig * 10) and locked) else ("#c8a24a" if i < int(sig * 10) else "#1c2228"), xsize=14, ysize=8 + i * 3) yalign 1.0
                ## Dalga
                hbox:
                    spacing 2
                    xalign 0.5
                    for i in range(64):
                        $ hgt = int(4 + abs(((i * 37 + tick * 13) % 29) - 14) * (0.4 + (1.0 - sig) * 2.2) + sig * 30 * abs(((i * 7) % 11) - 5) / 5.0)
                        add Solid("#9ec0a0" if locked else "#5a6a70", xsize=9, ysize=hgt) yalign 0.5
                bar value ScreenVariableValue("freq", 100) xsize 800 ysize 26 xalign 0.5 left_bar Solid("#3a3220") right_bar Solid("#151a1f") thumb Solid("#e8d08a") thumb_offset 4
                hbox:
                    xfill True
                    text "140.0" size 13 color "#55524c"
                    text ("KİLİTLENİYOR…" if locked else "Kaydırıcıyı sürükle  ·  ← → tuşları") size 13 color ("#9ec0a0" if locked else "#77736b") xalign 0.5
                    text "170.0" size 13 color "#55524c" xalign 1.0

    key "K_LEFT" action SetScreenVariable("freq", max(0.0, freq - 1.0))
    key "K_RIGHT" action SetScreenVariable("freq", min(100.0, freq + 1.0))
    if autotest_mode:
        timer 0.05 action Return(True)


## SES DALGASI ANALİZİ ########################################################

init python:
    class Waveform(renpy.Displayable):
        """Ses kaydını çubuk grafik olarak çizer. kind: real | copy | cut"""

        def __init__(self, kind, seed, color="#8fb0c8", **kw):
            super(Waveform, self).__init__(**kw)
            r = __import__("random").Random(seed)
            n = 110
            floor = [0.12 + r.random() * 0.12 for _ in range(n)]
            vals = list(floor)
            if kind == "real":
                for i in range(30, 80):
                    vals[i] = floor[i] + abs(r.gauss(0, 0.35)) * (1 - abs(i - 55) / 30.0)
            elif kind == "copy":
                word = [abs(r.gauss(0, 0.4)) * (1 - abs(j - 10) / 12.0) for j in range(22)]
                for j, v in enumerate(word):
                    vals[18 + j] = floor[18 + j] + v
                    vals[66 + j] = floor[18 + j] + v
                    floor[66 + j] = floor[18 + j]
                for j in range(22):
                    vals[66 + j] = vals[18 + j]
            elif kind == "cut":
                for i in range(40, 72):
                    vals[i] = abs(r.gauss(0, 0.3)) * (1 - abs(i - 56) / 18.0)
                    if vals[i] < 0.02:
                        vals[i] = 0.0
            self.vals = vals
            self.color = renpy.easy.color(color)

        def render(self, width, height, st, at):
            w, h = 720, 90
            rv = renpy.Render(w, h)
            c = rv.canvas()
            col = (int(self.color.rgb[0] * 255), int(self.color.rgb[1] * 255), int(self.color.rgb[2] * 255), 255)
            c.line((40, 50, 60, 255), (0, h // 2), (w, h // 2), 1)
            bw = w / float(len(self.vals))
            for i, v in enumerate(self.vals):
                bh = max(1, int(min(1.0, v) * (h - 6)))
                c.rect(col, (int(i * bw), h // 2 - bh // 2, max(1, int(bw) - 2), bh))
            return rv

screen waveform_puzzle():
    modal True
    default hint = False
    add Solid("#05070a")
    add "bg depot" alpha 0.12
    vbox:
        xalign 0.5
        ypos 50
        spacing 14
        text "SES ANALİZİ" font "fonts/Oswald-SemiBold.ttf" size 40 color "#e6e2da" kerning 8 xalign 0.5
        text "Üç kayıt. Biri gerçekten Deniz. Hangisi?" size 19 color "#a9a295" xalign 0.5
        null height 8
        for wkey, wlabel, kind, seed in (("A", "A · Sesli mesaj: 'Abi, eski servis yolundayım.'", "real", 3), ("B", "B · Ormandaki kayıt: 'Abi?' (iki kez)", "copy", 7), ("C", "C · Mesajın sonu: 'Deniz…'", "cut", 11)):
            frame:
                xsize 980
                xalign 0.5
                padding (18, 12, 18, 12)
                background Solid("#0c1014")
                hbox:
                    spacing 18
                    vbox:
                        spacing 6
                        text wlabel font "fonts/Oswald-Medium.ttf" size 17 color "#cfc9bd"
                        add Waveform(kind, seed)
                    textbutton "GERÇEK BU":
                        yalign 0.5
                        style "ex_btn"
                        text_style "ex_btn_text"
                        xsize 170
                        action Return(wkey)
        null height 4
        if hint:
            text "Gerçek bir kayıtta arka plan gürültüsü (rüzgâr) hiç sıfıra inmez. Bir insan aynı kelimeyi iki kez birebir aynı söyleyemez." size 16 color "#e8d08a" xalign 0.5 text_align 0.5 xmaximum 900
        else:
            textbutton "İPUCU" xalign 0.5 action SetScreenVariable("hint", True) text_size 16 text_idle_color "#77736b" text_hover_color "#e8d08a"
    if autotest_mode:
        timer 0.05 action Return(renpy.random.choice(["A", "B", "C"]))


## FENERLE ARAMA ##############################################################

init python:
    class Flashlight(renpy.Displayable):
        """Fareyi izleyen fener ışığı: ekranın geri kalanı karanlık."""

        def __init__(self, **kw):
            super(Flashlight, self).__init__(**kw)
            self.x, self.y = 640, 360
            self.mask = renpy.displayable("gui/flashlight_mask.png")

        def event(self, ev, x, y, st):
            if (x, y) != (self.x, self.y) and 0 <= x <= 1280 and 0 <= y <= 720:
                self.x, self.y = x, y
                renpy.redraw(self, 0)
            return None

        def render(self, width, height, st, at):
            rv = renpy.Render(1280, 720)
            m = renpy.render(self.mask, 2560, 1440, st, at)
            rv.blit(m, (int(self.x - 1280), int(self.y - 720)))
            return rv


screen flashlight_search(bg, items, title, drain=False):
    modal True
    default found = []
    default fl = Flashlight()
    $ done = len(found) >= len(items)

    add ("bg " + bg)
    for iid, ilabel, icon, x, y in items:
        if iid not in found:
            button:
                pos (x, y)
                anchor (0.5, 0.5)
                xysize (130, 110)
                background None
                action [SetScreenVariable("found", found + [iid]), Play("audio", "audio/sfx/notify.ogg")]
                vbox:
                    xalign 0.5
                    yalign 0.5
                    text icon size 44 color "#d8cfb8" xalign 0.5
                    text ilabel size 13 color "#d8cfb8" xalign 0.5
    add fl
    for iid, ilabel, icon, x, y in items:
        if iid in found:
            text ("✓ " + ilabel) pos (x, y) anchor (0.5, 0.5) size 15 color "#9ec0a0" outlines [(2, "#000", 0, 0)]

    if drain:
        timer 1.5 repeat True action Function(drain_pil, 1)

    frame:
        xalign 0.5
        ypos 18
        padding (24, 10, 24, 10)
        background Solid("#000000c0")
        vbox:
            spacing 4
            text title font "fonts/Oswald-Medium.ttf" size 22 color "#e8d08a" xalign 0.5 kerning 2
            text ("Feneri fareyle gezdir. Bulduklarına tıkla.  (%d / %d)" % (len(found), len(items))) size 14 color "#a9a295" xalign 0.5
            if drain:
                text ("Fener pili: %d%%" % pil) size 13 color ("#e05040" if pil < 25 else "#77736b") xalign 0.5
    if done or (drain and pil <= 0):
        textbutton "DEVAM":
            xalign 0.5
            yalign 0.94
            style "ex_btn"
            text_style "ex_btn_text"
            xsize 240
            text_xalign 0.5
            action Return(found)
    if autotest_mode:
        timer 0.05 action Return([i[0] for i in items])


## OYUN SONU RAPORU ###########################################################

init python:
    def end_rank():
        if st_caught == 0 and sahte_kanma == 0:
            return ("GÖLGE", "Seni hiçbir şey duymadı. Hiçbir ses seni kandırmadı.")
        if len(kanit) >= len(EVIDENCE) and len(persistent.docs) >= 9:
            return ("ARŞİVCİ", "ECHO'nun sakladığı her şeyi gün ışığına çıkardın.")
        if st_shots == 0:
            return ("SESSİZ ADIM", "Tek kurşun atmadan çıktın.")
        if st_caught >= 5:
            return ("İNATÇI", "Defalarca yakalandın. Her seferinde yeniden kalktın.")
        return ("HAYATTA KALAN", "Çamlık'tan çıktın. Deniz yanında.")

    def fmt_time(sec):
        sec = int(sec)
        return "%d sa %02d dk" % (sec // 3600, (sec % 3600) // 60) if sec >= 3600 else "%d dk %02d sn" % (sec // 60, sec % 60)

screen end_report():
    modal True
    add Solid("#05070a")
    add "fx_vignette"
    $ rank, rdesc = end_rank()
    $ stars = sum(persistent.map_stars.values())
    vbox:
        xalign 0.5
        yalign 0.45
        spacing 10
        text "DOSYA KAPANDI" font "fonts/Oswald-Medium.ttf" size 20 color "#8a857c" kerning 10 xalign 0.5
        text rank font "fonts/Oswald-SemiBold.ttf" size 72 color "#e8d08a" kerning 12 xalign 0.5
        text rdesc size 18 color "#cfc9bd" xalign 0.5
        null height 26
        grid 4 2:
            xalign 0.5
            spacing 40
            for val, lab in ((fmt_time(renpy.get_game_runtime()), "oyun süresi"), ("%d / %d" % (stars, len(MAPS) * 3), "keşif yıldızı"),
                             ("%d / %d" % (len(kanit), len(EVIDENCE)), "kanıt"), ("%d / %d" % (len(persistent.docs), len(DOCS)), "belge"),
                             (str(st_caught), "kez yakalandın"), (str(sahte_kanma), "YANKI'ya kandın"),
                             (str(st_bottles), "şişe attın"), (str(st_shots), "kurşun sıktın")):
                vbox:
                    xsize 190
                    text val font "fonts/Oswald-Medium.ttf" size 30 color "#e6e2da" xalign 0.5
                    text lab size 14 color "#8a857c" xalign 0.5
        null height 26
        text ("Zorluk: " + {"hikaye": "Hikâye", "gerilim": "Gerilim", "kabus": "Kâbus"}.get(zorluk, zorluk)) size 15 color "#77736b" xalign 0.5
        null height 10
        textbutton "DEVAM" style "ex_btn" text_style "ex_btn_text" xsize 240 xalign 0.5 text_xalign 0.5 action Return()
    if autotest_mode:
        timer 0.05 action Return()
