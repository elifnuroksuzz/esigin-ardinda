## BÖLÜM 03 — BEŞ NOKTA

label ch03:
    call chapter_intro(3)

    ## 1. Harita ---------------------------------------------------------------
    scene bg map_table with long_fade
    $ amb("town_night")
    show aras at sil_right
    show mert at sil_left
    with dissolve
    narrator "Aras kasabanın eski belediye haritasını defterin çiziminin yanına açar."
    a "Haritayı tut. Şu beş tepeye bak."
    narrator "Beş tepede de 'bakım yapısı' yazıyor. Boyutları bir trafo için fazla büyük."
    m "Ortadaki çizgi nereye gidiyor?"
    a "Haritada işaretlenmemiş. Bir şey yerin altında birleşiyor."
    narrator "Deniz'in son telefon sinyali, kulelerin kapsama alanlarının kesiştiği noktaya düşüyor: eski servis yolu."
    $ add_note("bes_kule")
    m "Beş kuleyi kimsenin fark etmemesi mümkün mü?"
    a "Fark etmişlerdir. Ama kimse ne işe yaradıklarını bilmiyor olabilir."
    m "Çamlık'ta herkesin bildiği ama kimsenin konuşmadığı şeyler var."

    ## 2. İlk kule -------------------------------------------------------------
    scene bg tower with long_fade
    $ amb("tower_hum")
    show mert at sil_left
    show aras at sil_right
    with dissolve
    narrator "İlk kule. Elektrik kesik görünüyor. Ama metal gövdenin içinden, kemiklere işleyen düşük bir uğultu geliyor."
    m "Bu kule yıllardır burada mıymış?"
    a "Boya yeni değil. Ama kablo hattı kullanılmış."
    narrator "Aras cihazlara dokunmaz. Önce çevreye bakmak gerekiyor."

    call explore("kule")
    scene bg tower with dissolve
    $ amb("tower_hum")
    show mert at sil_left
    show aras at sil_right
    with dissolve
    m "Biri hâlâ çalıştırıyor yani."

    ## 3. Yanlış yankı ---------------------------------------------------------
    $ amb2("wind")
    narrator "Rüzgâr döner. Aras bir an olduğu yerde kalır."
    $ sfx("echo_voice")
    m_fake "Aras! Buraya gel!"
    show aras at sil_right, shake_loop
    a "Mert? Sen… yanımdasın."
    show aras at sil_right
    m "Ben bir şey demedim."
    narrator "Ses yalnızca bir kez gelir. Sonra başka bir ses."
    $ sfx("echo_voice")
    dz_fake "Abi, buradayım."
    m "Deniz!"
    $ sfx("echo_voice")
    dz_fake "Abi, buradayım."
    $ sfx("echo_voice")
    dz_fake "Abi, buradayım."

label .yanki:
    a "Mert. Dur ve düşün. Bu ses neden sahte?"
    menu:
        "Aynı cümle, aynı nefesle, üç kez birebir tekrarlandı.":
            a "Evet. Aynı cümle üçüncü kez, aynı nefesle tekrarlandı."
            if "tekrar_nefes" not in notes:
                $ add_note("tekrar_nefes")
        "Çok uzaktan geliyor; Deniz bu kadar uzakta olamaz.":
            $ stress(8)
            $ sahte_kanma += 1
            a "Uzaklık bir şey kanıtlamaz. Deniz uzakta da olabilir. Başka bir şeye bak."
            jump .yanki
        "Deniz bana böyle seslenmezdi.":
            $ stress(8)
            a "Seslenirdi. Tam da böyle. O şey bunu biliyor, Mert."
            jump .yanki

    m "Bunu duymak kolay değil, Aras."
    narrator "İkisi de aynı şeyi anlar. O şey yalnızca Deniz'i taklit etmiyor."
    narrator "Duyduklarını kullanarak onları birbirinden ayırmaya çalışıyor."
    $ amb2(None)

    ## 4. Merkeze giden çizgi --------------------------------------------------
    scene bg map_table with long_fade
    show aras at sil_right
    show mert at sil_left
    with dissolve
    narrator "Aras haritada kablo güzergâhlarını birleştirir. Beş çizgi tek bir noktada buluşur."
    a "Beş nokta. Tek merkez."
    a "Beş kule bir merkezde birleşiyor."
    m "O merkeze inebilir miyiz?"
    a "Bir servis hattı bulursak. Merkez yüzeyde görünmüyor."
    m "Deniz oradaysa?"
    a "Önce içeri girecek yolu bulmalıyız."
    m "O zaman onu bulacağız."
    return
