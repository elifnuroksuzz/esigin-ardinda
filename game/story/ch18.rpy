## BÖLÜM 18 — SON GEÇİT

label ch18:
    call chapter_intro(18)

    ## 1. 05.18–05.33 — Cam ve kilit -------------------------------------------
    scene bg isolation with long_fade
    $ amb("z0")
    centered "{size=+4}05.18{/size}"
    show kemal at sil_right
    show mert at sil_left
    with dissolve
    k "Deniz'i merkezden ayırmak için yardımcı denge halkasını kapatmalıyız."
    m "O bir enerji kaynağı değil."
    k "Hayır. Ölçtükleri bir insandı."
    show aras at sil_center with dissolve
    a "Yönetim kilidi nerede?"
    k "Taklitçi'nin bulunduğu çekirdekte. Fiziksel bir anahtar. Konsolun altında."

    scene bg core_room with dissolve
    show mert at sil_left
    show aras at sil_right
    with dissolve
    narrator "Çekirdeğin bakım hattı. Perdenin öbür tarafında Taklitçi bekliyor."
    $ sfx("echo_voice")
    k_fake1 "Aras, buraya. Sağdaki kapı."
    narrator "Sonra ses değişir."
    $ sfx("echo_voice")
    dz_fake "Abi! Buradayım, sağdaki kapı! Lütfen!"
    $ stress(8)

label .anahtar:
    menu:
        "Deniz'in sesinin geldiği sağdaki kapıya koş.":
            $ stress(12)
            $ sahte_kanma += 1
            $ sfx("growl")
            show taklitci at creature_close
            narrator "Kapının ardında Deniz yok. Kapının ardında Deniz'in sesini kullanan bir şey var."
            if rezonans > 0:
                menu:
                    "Bir Rezonans Kesici ateşle.":
                        $ rezonans -= 1
                        $ sfx("resonance_shot")
                        $ flash("#a090ff")
                        narrator "Mor bir titreşim. Taklitçi'nin gövdesi bir an bulanıklaşır, geri savrulur."
                        narrator "Bir mermi gitti. Ama yol açıldı."
                    "Geri çekil, perdeyi kullan.":
                        $ sfx("door_slam")
                        narrator "Aras perdeyi indirir. Çelik, yaratığın önüne düşer."
            else:
                $ sfx("door_slam")
                narrator "Aras perdeyi indirir. Çelik, yaratığın önüne düşer."
            hide taklitci with dissolve
            m "Deniz camın arkasında. Ben bunu biliyorum. O ses başka bir şey."
            jump .anahtar
        "Sesi duyma. Hareketin gecikmesini izle, perdeyi onun önüne indir.":
            narrator "Taklitçi'nin gölgesi sese doğru kıpırdar. Bir an sonra."
            $ sfx("door_slam")
            narrator "Aras tam o boşlukta perdeyi indirir. Mert konsolun altına uzanır."
            $ sfx("lock_click")
            narrator "Soğuk, ağır bir metal anahtar. YÖNETİM — Z0."
    narrator "Taklitçi içeride kalır."

    ## 2. 05.33–05.42 — Adrian Voss --------------------------------------------
    scene bg z0_core with dissolve
    $ sfx("door_open")
    narrator "Z0'ın B1 yönetim hattına bağlanan tahliye geçidi açılır."
    show adrian at sil_center with dissolve
    narrator "Takım elbiseli, düzgün taranmış saçlı bir adam. Elinde taşınabilir bir yönetim kontrolü. Adrian Voss."
    adr "Siz buraya kadar geldiniz. Demek sistem hâlâ işe yarıyor."
    show adrian at sil_right with move
    show mert at sil_left with dissolve
    m "Deniz'i beş gündür burada tutuyorsun."
    adr "Onları kontrol edebiliriz."
    show kemal at sil_left2 with dissolve
    k "Yalnızca nereye gideceklerini değiştiriyorsun."
    adr "Farkı ne?"
    k "Bir gün gidecekleri yer sen olana kadar farkı anlayamazsın."
    if hakan_resmi:
        m "Hakan Ersoy öldü. Masasında kızının çizdiği bir resim vardı. Sabah eve götürecekti."
    else:
        m "Hakan Ersoy öldü. D-14'te."
    adr "Karantina protokolü otomatiktir. Sistemin bir sonucu."
    m "O protokolü kim burada tuttu?"
    narrator "Voss yanıt vermez."

    ## 3. 05.42–05.53 — Kapıyı kapatmak ----------------------------------------
    scene bg z0_collapse with flash_white
    $ amb("z0")
    $ bgm("chase", 0.5)
    narrator "Voss kontrol cihazıyla merkez hatlarını zorlar. Beş kulenin aynı anda susması için."
    $ sfx("suppress")
    $ jolt(True)
    narrator "Merkezin ortasında bir şey açılır. Bir geçiş. Karanlığın içinden fiziksel bir baskı."
    narrator "Kontrol cihazı Voss'un elinde parçalanır."
    show adrian at sil_right with dissolve
    show aras at sil_left with dissolve
    a "Yönetim geçidine kaçıyor!"
    show mert at sil_center with dissolve
    m "Bırak. Önce Deniz."
    hide adrian with dissolve
    narrator "Voss panikle B1–Z0 özel tahliye koridoruna kaçar."
    a "Beş hattı aynı anda kapatırsak geçit açık kalabilir."
    show kemal at sil_left2 with dissolve
    k "Tek tek ayır. Yardımcı halkayı dengele."
    narrator "Dev bir mekanik halka merkezin çevresinde dönüyor. Her hat, halka dengelendiği anda ayrılabilir."

    $ halka = 1
    $ cokus = False
    while halka <= 5:
        $ hat_adi = "ECHO-%d" % halka
        call screen qte("[hat_adi] dengede — ŞİMDİ AYIR!", [("Ayır", "ayir"), ("Hepsini birden kes", "hepsi")], 3.0, "kacti")
        if _return == "ayir":
            $ sfx("lever")
            narrator "[hat_adi] ayrıldı. Kanallardan biri sönerek susar."
            $ halka += 1
        elif _return == "hepsi":
            $ stress(10)
            $ sfx("suppress")
            k "Hayır! Aynı anda değil! Kapı açık kalır!"
            narrator "Aras elini çeker. Halka sarsılır, ama hâlâ dönüyor."
        else:
            $ stress(5)
            narrator "Halka denge noktasını geçer. Bir tur daha beklemek gerek."
        if halka == 4 and not cokus:
            $ cokus = True
            $ jolt()
            m "Merkez çöküyor!"

    a "Biraz daha. Son hat… tamam!"
    $ bgm(None, 2.0)
    $ sfx("thud")
    scene bg z0_core with long_fade
    k "Çamlık hattı ayrıldı. Geçit kapanıyor."
    narrator "Merkezdeki karanlık içine çöker. Beş kanaldan gelen uğultu birer birer söner."
    narrator "Çamlık'ın yerel ECHO bağlantısı güvenli biçimde kesildi."

    ## 4. 05.53–06.01 — Deniz ---------------------------------------------------
    scene bg isolation with dissolve
    $ amb("tension")
    $ sfx("door_open")
    narrator "Merkez kilitleri çözülür. İzolasyon kapısı açılır."
    show deniz at sil_right with dissolve
    show mert at sil_left with dissolve
    narrator "Mert Deniz'e yaklaşır. Sonra bir an duraksar."
    narrator "Taklitçi'nin seslerini hatırlıyor. Gecikme var mı? Aynı nefes mi?"
    dz "Abi? Gerçekten sen misin?"
    m "Sen hâlâ kulaklığını bozduğumu kabul etmedin."
    dz "Sen bozdun."
    m "O kulaklık zaten bozuktu."
    dz "Yalancısın."
    narrator "Gecikme yok. Bu Deniz."
    show deniz at sil_center
    show mert at sil_center
    with move
    narrator "İki kardeş sarılır."
    narrator "Deniz'in yorgunluğu ve korkusu silinmiyor. Kurtulmuş olması her şeyin bittiği anlamına gelmiyor."
    m "Hadi eve gidelim."
    dz "Dışarı çıktığımızda ilk ne yapacağız?"
    m "Seni doktora götüreceğiz. Sonra eve."
    dz "Evde hâlâ o eski kupa var mı?"
    m "Var. Seni bekliyor."
    dz "O zaman acele edelim."

    ## 5. 06.01–06.13 — Kemal'in bedeli ----------------------------------------
    scene bg b3_corridor with dissolve
    $ amb("b3")
    show aras at sil_left
    show kemal at sil_right
    with dissolve
    narrator "Tahliye. Yukarı, B3'e. Servis korkulukları gevşemiş, merkezin çöküşüyle titreşiyor."
    $ sfx("metal_drag")
    a "Baba, çekil!"
    k "Önce sen geç!"
    $ sfx("thud")
    $ jolt(True)
    narrator "Bir korkuluk kopar. Kemal Aras'ı iterek düşen parçanın altından çıkarır. Kendi bacağı sıkışır."
    show mert at sil_center with dissolve
    m "Bacağı sıkıştı. Bakım krikosunu getir."
    show deniz at sil_left2 with dissolve
    dz "İlk yardım çantası burada. Ben yolu açarım."
    if ilkyardim > 0:
        $ ilkyardim -= 1
        narrator "Mert son ilk yardım paketini Kemal'in bacağına sarar. Kanama yavaşlar."
    narrator "Mert ve Aras krikoyla parçayı kaldırır. Deniz servis kapısının sürgüsünü açar."
    k "Aras…"
    a "Konuşma. Seni çıkarıyoruz."
    narrator "Kemal tekerlekli bakım sedyesine alınır. Elektrik kesik; ama yük platformunun mekanik acil indirme kolu çalışıyor."

    ## 6. 06.13–06.28 — Son geçit ----------------------------------------------
    scene bg b3_dark with dissolve
    $ bgm("chase", 0.5)
    show deniz at sil_left
    show mert at sil_center
    show aras at sil_right
    with dissolve
    dz "Metal üzerinde bir şey sürükleniyor."
    $ sfx("metal_drag")
    m "Nöbetçi."
    narrator "Deniz sesi herkesten önce duydu. Bu bir yetenek değil. Beş günlük korkunun bıraktığı tetiklik."
    a "B3 servis rampasına. Koşmayın; kapıya kadar sessiz."

    k "Panellerdeki mekanik sürgüler. Geçtiğiniz yolu kapatın."
    $ bgm(None, 1.0)
    call explore("tahliye")
    scene bg b3_exit with dissolve
    $ sfx("door_slam")
    show deniz at sil_left
    show mert at sil_center
    show aras at sil_right
    with dissolve
    narrator "Kapılar onu sonsuza kadar durdurmaz. Yalnızca dışarı çıkacak zaman kazandırır."

    ## 7. 06.28–06.39 — Son nöbet ----------------------------------------------
    scene bg forest_dawn with long_fade
    $ amb("dawn")
    centered "{size=+4}06.28{/size}"
    narrator "Dışarıda gün ağarıyor."
    show mert at sil_left
    show aras at sil_right
    with dissolve
    $ sfx("door_slam")
    $ jolt(True)
    narrator "Arkalarında servis kapısı patlar. Nöbetçi orman yoluna çıkar."
    show nobetci at creature_close
    $ sfx("growl")
    a "Tüfek dolabı açılmış. Merkezi kilitler düşmüş."
    narrator "Merkez kilitleri çözülünce Bölüm 8'deki güvenlik dolabı da açılmıştı. Aras çıkarken tüfeği almıştı."
    m "Özel mermi kaldıysa ben vururum. Yoksa acil bastırma hattını çalıştır."

    if rezonans > 0:
        menu:
            "Rezonans Kesici'yi ateşle (kalan: [rezonans]).":
                $ final_yontem = "rezonans"
                $ rezonans -= 1
                $ sfx("resonance_shot")
                $ flash("#a090ff")
                narrator "Mert nefesini verir. Tetiği çeker. Mor bir dalga yaratığın göğsüne çarpar."
            "Aras'a bağır: 'Bastırma hattı!'":
                $ final_yontem = "bastirma"
    else:
        $ final_yontem = "bastirma"
        narrator "Mert'in elinde özel mermi kalmamış."

    if final_yontem == "bastirma":
        narrator "Girişteki eski acil rezonans bastırma hattı. Merkez kapanınca ayrı acil beslemesi yeniden devreye girmişti."
        narrator "Deniz panele en yakın olan. Kolu indirir."
        $ sfx("suppress")
        $ flash("#a090ff")
        narrator "Tek seferlik manuel test. Hava bir an kulakları tıkayacak kadar yoğunlaşır."

    if final_yontem == "rezonans":
        $ unlock("son_atis")
    else:
        $ unlock("eski_hat")
    a "Rezonans kesildi! Göğsündeki yarık açıldı!"
    m "Şimdi, Aras!"
    $ sfx("gunshot")
    $ flash("#fff4d0")
    narrator "İlk atış onu durdurur."
    $ sfx("gunshot")
    narrator "Sonrakiler yere serer."
    $ jolt(True)
    narrator "Nöbetçi bir süre yeniden kalkmaya çalışır. Sonra tamamen hareketsiz kalır."
    hide nobetci with fade_out_slow
    $ bgm(None, 3.0)
    a "Bu Hakan için."
    show deniz at sil_center with dissolve
    dz "Hareket etmiyor."
    m "Bitti."

    ## 8. 06.39–06.45 — Ses geri geliyor ---------------------------------------
    $ sfx("phone_ring")
    narrator "Telefonlar çekmeye başlar. Bir çubuk. İki."
    hide aras
    hide deniz
    with dissolve
    bo_fon "Mert! Neredesiniz?"
    m "Eski servis yolundayız. Deniz yanımda."
    bo_fon "Deniz mi?"
    show deniz at sil_right with dissolve
    narrator "Mert telefonu Deniz'e uzatır."
    dz "Bora abi… Ben iyiyim… galiba."
    narrator "Hattın öbür ucunda konuşmalar, ağlama, araç kapılarının kapanma sesleri."
    bo_fon "Geliyoruz. Ambulansı da yönlendirdik."

    ## 9. 07.05–07.15 — Geldiniz -----------------------------------------------
    scene bg forest_dawn with long_fade
    centered "{size=+4}07.05{/size}"
    narrator "Araçlar gelir. Arkalarından acil yardım ekipleri."
    show bora at sil_left with dissolve
    show mert at sil_right with dissolve
    narrator "Bora, Mert'i görünce bir şey demeden sarılır."
    bo "Bir daha böyle kaybolursan seni ben öldüreceğim."
    m "Sıraya gir."
    hide bora
    hide mert
    with dissolve
    show duru at sil_left
    show aras at sil_right
    with dissolve
    du "Aras!"
    a "Buradayım."
    narrator "Duru ağabeyine koşar. Sonra sedyedeki babasını görür."
    du "Babam?"
    show kemal at sil_center with dissolve
    k "Buradayım, kızım. Anlatmam gereken çok şey var."
    du "Anlatacaksın."
    narrator "Elif ve Emir battaniye ve su getirir. Kaan sağlık görevlilerini Kemal'e yönlendirir."

    ## 10. 07.15 — Babam nerede? -----------------------------------------------
    hide duru
    hide kemal
    with dissolve
    show idil at sil_left with dissolve
    narrator "İdil, Aras'a yaklaşır."
    idl "Babamı gördün mü?"
    a "Evet."
    idl "Yaşıyor mu?"
    a "Son gördüğümde yaşıyordu."
    narrator "İdil kısa bir süre rahatlar. Sonra Aras'ın yüzüne bakar."
    idl "Ne yaptı?"
    a "Deniz'i bırakmadı. Merkezi yeniden çalıştırmaya kalktı."
    idl "Neden?"
    a "Bilmiyorum. Ama ne yaptığını anlatmak zorundayız."
    idl "Anlatın."
    narrator "İdil babasının suçlarından sorumlu tutulmayacak. Ama gerçekle yüzleşecek."

    ## 11. 07.15–07.30 — Kanıt -------------------------------------------------
    scene bg forest_dawn with dissolve
    show aras at sil_left with dissolve
    narrator "Polis ve sağlık görevlileri bölgeyi güvenceye alır."
    $ kanit_sayisi = len(kanit)
    narrator "Aras ve Mert, topladıkları kayıtları bir görevliye teslim eder. Görevli her birinin saatini ve kaynağını not alır."
    if kanit_sayisi >= 6:
        narrator "S-17, K-2, D-14, Voss'un ret notu, yönetim komutu, Deniz'in gerçek ses kaydı. Hepsi. Eksiksiz bir zaman çizelgesi."
        narrator "Görevli bir süre sessiz kalır. 'Bu dosyayla kimse bunu örtbas edemez.'"
    elif kanit_sayisi >= 3:
        narrator "Elde [kanit_sayisi] kayıt var. Zaman çizelgesinde boşluklar kalıyor ama soruşturmayı başlatmaya yetecek kadar."
    else:
        narrator "Kayıtların çoğu içeride kaldı. Kemal'in ifadesi ve tesisin mühürlenmesi şimdilik en güçlü kanıt."
    narrator "Kemal tedaviye alınır ve ifade vermeyi kabul eder."
    narrator "D-14'te kalan Hakan'ın bedeni için, tesis güvenli hâle geldiğinde adli kurtarma planlanır."
    narrator "Voss'un B1–Z0 özel geçidine kaçtığı biliniyor. Dışarı çıkıp çıkmadığı bilinmiyor."
    narrator "ECHO mühürlenir."

    ## 12. 2 Aralık — Eve dönüş -----------------------------------------------
    $ silence(2.0)
    scene black with long_fade
    $ show_hud = False
    centered "{size=+6}2 Aralık{/size}\n\n{size=-2}Üç hafta sonra{/size}"
    scene bg kitchen with long_fade
    $ amb("kitchen")
    $ bgm("epilogue", 3.0)
    show deniz at sil_right
    show mert at sil_left
    with dissolve
    narrator "Aydınların mutfağı. Mert ve Deniz kahvaltı hazırlıyor. Masada o eski kupa."
    dz "Bazen sessizlikte bile ses gelecekmiş gibi bekliyorum."
    m "Ben de."
    $ sfx("lock_click")
    show aras at sil_center with dissolve
    narrator "Aras ziyarete gelir."
    narrator "Kemal tedavi sonrası soruşturmada ifade veriyor. Adrian Voss hâlâ aranıyor."
    a "Hakan'ın ailesini ziyaret ettim."
    a "Eşi bana aile fotoğrafının bir kopyasını verdi. 'Onu sadece öldüğü günkü hâliyle hatırlamamanı istiyorum' dedi."
    a "Kızı da… 'Babam korktuğunda da yardım ederdi' dedi."
    narrator "Mert fotoğrafa bakar. Üç kişi. Babası, annesi ve kendisi."
    m "Haklı."
    narrator "Deniz reçelli ekmeğini uzatır."
    a "Bunun adı kahvaltı mı?"
    dz "Hayatta kaldık, şikâyet etme."
    narrator "Kısa bir sessizlik olur."
    narrator "Bu kez kimse ondan kaçmaz."

    $ renpy.pause(2.0)
    call final_achievements
    scene black with long_fade
    call screen credits
    jump .post_credits

label .post_credits:
    ## Kredi sonrası — Proje Beş -----------------------------------------------
    $ silence(1.0)
    scene black with Dissolve(1.0)
    $ renpy.pause(1.5, hard=True)
    scene bg archive_unknown with long_fade
    $ amb("b2")
    narrator "Bilinmeyen bir arşiv odası. Yalnızca iki dosya sayfası görünüyor."
    centered "TESİS 01 — ÇAMLIK / KAPATILDI\n\n{color=#c03020}TESİS 02 — KONUM GİZLİ / AKTİF{/color}"
    narrator "Diğer üç tesisin durumu açıklanmıyor."
    $ sfx("radio")
    gorevli "İkinci tesis aktif."
    $ renpy.pause(1.0, hard=True)
    $ sfx("echo_voice")
    uzak "İkinci tesis aktif."
    narrator "Aynı cümle bir an sonra tekrar ediliyor. Ama bu kez telsizden değil."
    narrator "Görevlinin hemen arkasından."
    $ silence(0.1)
    scene black with Dissolve(0.15)
    $ renpy.pause(2.0, hard=True)
    centered "{size=+10}EŞİĞİN ARDINDA{/size}\n\n{size=-4}Çamlık'ın hikâyesi tamamlandı.\nDünyanın tüm sırları çözülmedi.{/size}"
    $ persistent.completed = True
    return

default halka = 1
default cokus = False
default hat_adi = ""
default kanit_sayisi = 0


## Kredi ekranı ################################################################

screen credits():
    modal True
    add Solid("#000000")
    timer 34.0 action Return()
    key "dismiss" action NullAction()
    key "game_menu" action Return()

    vbox:
        xalign 0.5
        ypos 760
        spacing 22
        at credits_scroll

        text "EŞİĞİN ARDINDA" size 54 color "#e6e2da" xalign 0.5 font "DejaVuSans-Bold.ttf"
        text "Çamlık Kasabası • ECHO • YANKI" size 20 color "#c8a24a" xalign 0.5
        null height 50
        text "Mert Aydın · Deniz Aydın · Aras Demir" size 22 color "#cfc9bd" xalign 0.5
        text "Dr. Kemal Demir · Duru Demir" size 22 color "#cfc9bd" xalign 0.5
        text "Adrian Voss · İdil Voss" size 22 color "#cfc9bd" xalign 0.5
        text "Rıza · Bora · Kaan · Elif · Emir" size 22 color "#cfc9bd" xalign 0.5
        null height 30
        text "Hakan Ersoy'un anısına" size 24 color "#7aa0c0" xalign 0.5
        text "Korktuğunda da yardım ederdi." size 18 color "#8a857c" xalign 0.5 italic True
        null height 50
        text "Hikâye ve kanon" size 18 color "#8a857c" xalign 0.5
        text "EŞİĞİN ARDINDA hikâye dosyası" size 22 color "#cfc9bd" xalign 0.5
        null height 20
        text "Motor" size 18 color "#8a857c" xalign 0.5
        text "Ren'Py Visual Novel Engine" size 22 color "#cfc9bd" xalign 0.5
        null height 20
        text "Görsel ve sesler" size 18 color "#8a857c" xalign 0.5
        text "tools/gen_assets.py ile prosedürel üretildi" size 22 color "#cfc9bd" xalign 0.5
        null height 60
        text "Oynadığın için teşekkürler." size 24 color "#e6e2da" xalign 0.5

    text "Esc: geç" size 14 color "#444" xalign 0.98 yalign 0.98

transform credits_scroll:
    ypos 760
    linear 32.0 ypos -1100
