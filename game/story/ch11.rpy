## BÖLÜM 11 — YALNIZLIK

label ch11:
    call chapter_intro(11)

    ## 1. Kendi sesi -----------------------------------------------------------
    scene bg b3_dark with long_fade
    $ amb("b3")
    show mert at sil_center with dissolve
    narrator "B3'ün arka koridorları. Işıkların yarısı sönük. Fener ışığı duvarlarda titriyor."
    $ drain_pil(6)
    $ sfx("echo_voice")
    m_fake "Buraya gel."
    m "Bu benim sesim."
    $ sfx("echo_voice")
    m_fake "Buraya gel."
    narrator "Ses iki ayrı yönden geliyor. Sol koridorda tavana asılı bir ECHO hoparlörü var. Sağ koridor karanlık."
    m "Kendi sesim bana bir kapının ardından cevap veriyor."

    menu:
        "Sol koridordaki hoparlörün kablosunu çek.":
            $ sfx("static")
            narrator "Kablo çıkınca sol taraftaki ses kesilir."
        "Bekle ve iki sesi karşılaştır.":
            $ stress(5)
            narrator "İkisi de aynı cümleyi söylüyor. Ama sol taraftakinde hafif bir elektronik cızırtı var."
            narrator "Mert sonunda hoparlörün kablosunu çeker. Sol taraf susar."

    $ sfx("echo_voice")
    m_fake "Buraya gel."
    m "Hoparlörü kapattım. İkincisi hâlâ konuşuyor."
    m "Hoparlör sustu ama o susmadı. Demek burada iki ayrı şey var."
    $ add_note("hoparlor_yanki")

    menu:
        "Sağ koridordan, sesin geldiği yerden geç.":
            $ stress(15)
            $ sahte_kanma += 1
            narrator "Mert sağa birkaç adım atar. Karanlıkta bir şey kıpırdar. Ses birden kesilir."
            $ sfx("growl")
            narrator "Geri çekilir. Kalbi kulaklarında atıyor."
            m "Aptal. Sesi duyunca gidilmez."
        "Sol koridordan, susturduğun hoparlörün altından geç.":
            narrator "Sessiz koridordan geçer. Arkasında, sağdaki karanlık bir süre daha 'Buraya gel' der. Sonra susar."

    ## 2. Kırpıntı -------------------------------------------------------------
    scene bg b3_corridor with dissolve
    show mert at sil_left with dissolve
    $ sfx("kirpinti")
    narrator "Metal zeminde tıkırtılar. Küçük, soluk, gözsüz bir şey bir boru yığınının altından çıkıyor."
    show kirpinti at creature_floor
    kirp "(Metal üzerinde tıkırtı.)"
    m "{size=-4}Kıpırdama… sesime geliyorlar.{/size}"
    narrator "Yerde boş bir cam şişe var. Tabancada [mermi] mermi."

    call screen qte("Kırpıntı yaklaşıyor", [("Şişeyi uzağa fırlat", "sise"), ("Ateş et", "ates"), ("Geri çekil", "geri")], 5.0, "fark")
    if _return == "sise":
        $ sfx("bottle")
        thought "Önce şişeyi uzağa at. Sonra geç."
        narrator "Cam koridorun öbür ucunda kırılır. Kırpıntı o yöne atılır. Mert yanından süzülür."
        $ kirpinti_atlatma += 1
    elif _return == "ates":
        if use_bullet():
            $ sfx("gunshot")
            $ flash("#fff4d0")
            narrator "Tek atış. Küçük gövde yere yığılır. Kulakları çınlıyor."
            narrator "Silah sesi koridorlarda yankılanır. Uzakta bir şey bu sesi duymuştur."
            $ stress(5)
        else:
            $ sfx("lock_click")
            narrator "Tetik boşa düşer. Mermi yok."
            $ stress(15)
            narrator "Kırpıntı ses yönüne atılır. Mert son anda bir dolabın arkasına kaçar."
    elif _return == "geri":
        narrator "Mert yavaşça, topuklarını kaldırarak geri çekilir. Kırpıntı bir süre havayı koklar, sonra başka yöne döner."
        $ kirpinti_atlatma += 1
    else:
        $ stress(15)
        narrator "Kırpıntı ayak sesini duyar. Çarpar. Mert onu tekmeleyip uzaklaştırır, bir kapının arkasına kaçar."
        if ilkyardim > 0:
            $ ilkyardim -= 1
            narrator "Bileğinde ince bir kesik. İlk yardım paketinden bir sargı harcar."
    hide kirpinti with dissolve
    $ add_note("kirpinti")
    narrator "Silah sınırsız üstünlük sağlamıyor. Büyük YANKI'lara karşı ise hiç güvenilir değil."

    ## 3. Ses izi --------------------------------------------------------------
    scene bg control_room with dissolve
    show mert at sil_left with dissolve
    narrator "Küçük bir kontrol odası. Ekranlardan biri hâlâ açık: DIŞ MİKROFON ARŞİVİ."
    narrator "Mert 6 Kasım gecesini bulur. 22.41."
    $ sfx("phone_beep")
    dz_kayit "Abi… eski servis yolundayım."
    m "Rüzgâr aynı. Bu, oradaki gerçek kayıt."
    narrator "Hemen ardından aynı tonla ikinci bir çağrı. Ama arkasında rüzgâr yok."
    m "Deniz gerçekten oradaydı. Ama ardından duyulan her ses ona ait değildi."
    m "Birileri seni dinlemiş, Deniz."
    $ add_evidence("deniz_ses")
    m "Deniz'in sesini duyarsam önce nereden geldiğini anlayacağım."

    ## 4. Aras'a söz -----------------------------------------------------------
    $ sfx("radio")
    narrator "Mert bozuk telsizi açar."
    m_tel "Aras, beni duyuyorsan… vazgeçmedim."
    $ sfx("static")
    a_tel "{size=-6}…buradayım…{/size}"
    m_tel "Dayan. Geliyorum."
    narrator "Aras'ın öldüğüne dair bir kanıt yok. Bu yeter."
    narrator "Bir sonraki kapının ardında soğuk, mavi ışıklı araştırma katı uzanıyor."
    call pil_check
    return
