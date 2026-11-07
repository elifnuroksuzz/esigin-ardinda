## BÖLÜM 10 — D-14

label ch10:
    call chapter_intro(10)

    ## 1. Yanlış güvenlik ------------------------------------------------------
    scene bg d_corridor with long_fade
    $ amb("quarantine")
    show hakan at sil_center
    show mert at sil_left
    show aras at sil_right
    with dissolve
    narrator "Ara Kat D. Kırmızı ışık. Her yüzeyde karantina şeritleri."
    narrator "Hava burada farklı kokuyor. Metal ve dezenfektan. Altında başka bir şey."
    $ sfx("alarm")
    centered "{color=#ff4030}BİYOLOJİK TEHDİT ALGILANDI\nKARANTİNA PROTOKOLÜ BAŞLATILDI{/color}"
    $ sfx("door_slam")
    $ jolt(True)
    a "Kapı kendi kendine kilitlendi!"
    h "Biyolojik karantina. Ben başlatmadım."
    narrator "Sistem insan onayı beklemiyor. Yıllar önce böyle kurulmuş, böyle bırakılmış."
    $ add_note("d14_otomatik")

    ## 2. Ayrılma --------------------------------------------------------------
    $ sfx("metal_drag")
    show nobetci at creature_far
    narrator "Koridorun öbür ucunda Nöbetçi belirir. Kırmızı ışık gövdesinde kayıyor."
    h "Mert, yan geçide! Aras, yaralı personel kapısını tut!"
    $ bgm("chase", 0.3)

    call screen qte("Çelik paneller düşüyor!", [("Yan geçide atla", "yan"), ("Aras'a doğru koş", "aras")], 3.0, "dur")
    if _return == "yan":
        narrator "Mert yan geçide atılır. Arkasında çelik paneller sırayla iner."
    elif _return == "aras":
        $ stress(15)
        narrator "Mert Aras'a doğru koşar. Bir panel tam önüne iner. Omzu çeliğe çarpar."
        $ jolt(True)
        if ilkyardim > 0:
            $ ilkyardim -= 1
            narrator "Kolundan kan sızıyor. Paketi açıp sargıyı sıkıca sarar. Bir paket eksildi."
        else:
            $ stress(10)
            narrator "Kolundan kan sızıyor. Sarabilecek bir şey yok."
    else:
        $ stress(10)
        narrator "Mert bir an donar. Hakan onu yan geçide iter."
    hide nobetci
    $ sfx("door_slam")
    scene bg d_corridor with flash_red
    show mert at sil_center with dissolve
    narrator "Mert başka tarafta kalır. Aras ve Hakan, D-14'ün içinde."
    $ sfx("radio")
    m_tel "Aras, buradan geçemiyorum."
    a_tel "Sen ilerle. Ben Hakan'la başka kapıya bakacağım."
    m_tel "Seni burada bırakmam."
    a_tel "Deniz'i bul. Sonra beni bul."
    $ bgm(None, 1.0)

    ## 3. Hakan'ın sonu --------------------------------------------------------
    scene bg d14 with long_fade
    $ amb("quarantine")
    narrator "Telsiz açık kalır. Mert, kapının öbür tarafında olanları yalnızca duyabilir."
    $ sfx("metal_drag")
    h "Aras, yere yat. Ses çıkarma."
    a_tel "Sen de gel!"
    $ sfx("growl")
    h "Kapıyı tutacağım. Git!"

    menu:
        "Panele vur, kapıyı aç!":
            $ sfx("metal_knock")
            narrator "Mert yumruklarıyla panele vurur. Kilit ekranı kırmızı kalır: KARANTİNA — ERİŞİM YOK."
        "Telsize bağır: 'Hakan, çık oradan!'":
            m_tel "Hakan! Çık oradan!"
            narrator "Cevap yok. Sadece metal sesi."
        "Sessizce dinle.":
            narrator "Mert telsizi kulağına bastırır. Ellerinin titrediğini fark etmez."

    $ sfx("thud")
    a_tel "Hakan! Hayır!"
    $ sfx("static")
    narrator "Sonra sessizlik."
    narrator "Hakan Aras'ı güvenlik nişine itmiş, Nöbetçi'yi kendi üzerine çekmişti. Bunu Mert ancak sonra öğrenecekti."
    narrator "Hızlı bir kahramanlık gösterisi değildi. Sadece bir adamın, korkarken bile yaptığı şeydi."
    $ stress(20)

    ## 4. İki yalnızlık --------------------------------------------------------
    scene bg d_corridor with long_fade
    show mert at sil_center with dissolve
    m_tel "Aras? Cevap ver."
    $ renpy.pause(1.5, hard=True)
    $ sfx("radio")
    a_tel "{size=-4}Buradayım…{/size}"
    m_tel "Hakan?"
    a_tel "Mert… Hakan öldü."
    narrator "Uzun bir sessizlik."
    m_tel "Seni çıkaracağım. Söz."
    a_tel "Nefesini duyabiliyorum, Mert. Bağlantı kopmadan konuş."
    m_tel "Buradayım. Sen de konuş."
    a_tel "Hakan'ın ayak sesini artık duymuyorum."
    m_tel "Seni oradan çıkarana kadar hattı açık tutacağım."
    $ sfx("static")
    narrator "Hat cızırdar. Sonra kopar."
    narrator "Aras karantinadan çıkamıyor. Hakan'ın bedeni D-14'te kalıyor."
    narrator "Mert'in elinde Bora'nın tabancası, [mermi] mermi ve giderek azalan bir fener var. Ve yalnız."
    return
