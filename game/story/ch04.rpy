## BÖLÜM 04 — RIZA'NIN RÖLESİ

label ch04:
    call chapter_intro(4)

    ## 1. Eski istasyon --------------------------------------------------------
    scene bg relay_station with long_fade
    $ amb("relay")
    narrator "Kulelerin eski bakım iletişimini yöneten röle istasyonu. Yıllardır terk edilmiş olması gerekiyordu."
    narrator "Ama içeride bir soba yanıyor."
    show riza at sil_center with dissolve
    narrator "Rıza. İstasyonun eski görevlisi. Kimse ona ne zaman emekli olduğunu sormamış."
    show riza at sil_right with move
    show mert at sil_left with dissolve
    rz "O röleye dokunmayın. Son kez çalıştığında bütün vadide ses kesilmişti."
    m "Deniz burada kayboldu."
    rz "O zaman ne aradığınızı anlıyorum. Ama ne bulacağınızı bilmiyorum."
    rz "O gece köpekler sabaha kadar havladı. Sonra birden sustular."
    show aras at sil_left2 with dissolve
    a "Elektrik kesintisiyle aynı saat mi?"
    rz "Aynı dakika. İnsan böyle bir sessizliği unutmaz."
    $ add_note("ruza_sessizlik")
    narrator "Rıza sobanın arkasından yıpranmış bir defter çıkarır."
    rz "Bunu ECHO'nun adamlarına vermedim. Size veriyorum."
    call read_doc("riza_defter")

    narrator "Duvarda düzinelerce kablo, çoğu kesik. Hangi hattın hâlâ yaşadığını bulmak, servis araçlarının hangi yoldan geçtiğini gösterecek."

label .hat:
    a "Üç ana hat var. Hangisi hâlâ çalışıyor?"
    menu:
        "Tozlu, ucu kopuk, etiketi okunmayan kalın hat.":
            $ stress(4)
            narrator "Mert ucu tutar. Hiçbir şey yok. Toz bile yıllardır yerinden oynamamış."
            a "Bu ölü. Yıllardır ölü."
            jump .hat
        "Üzerinde yeni yalıtım bandı olan, hafifçe ılık ve uğuldayan hat.":
            $ sfx("static")
            narrator "Mert elini yaklaştırır. Kablonun içinden bir titreşim geçiyor, kulaklarının arkasında hissediyor."
            a "Bu. Bant en fazla birkaç haftalık. Birisi bu hattı canlı tutuyor."
        "Paslanmış bağlantı kutusuna giden ince sinyal hattı.":
            $ stress(4)
            $ sfx("static")
            narrator "Kutu açılınca içinden kıvılcım değil, sadece pas dökülür."
            rz "O kutu benim zamanımda bile çalışmıyordu."
            jump .hat

    narrator "Canlı hattın izini takip eden Aras, bir servis yolunun haritasını çıkarır. Araçlar eski servis yolundan, ormanın içinden geçiyor."

    ## 2. Kesilmiş uyarı -------------------------------------------------------
    a "Rölenin hafızasında kayıtlı iletimler var. Doğru frekansı bulursak dinleyebiliriz."
    window hide
    $ quick_menu = False
    call screen radio_tune("Rölenin alıcısını ayarla. Parazitin içinde bir insan sesi var.", 63.0, "RÖLE ALICISI")
    $ quick_menu = True
    $ sfx("radio")
    narrator "Parazit çekilir. Rölenin hafızasında yarım kalmış bir mesaj. Gönderen: Dr. Kemal Demir. Alıcı: Adrian Voss."
    k_kayit "…deneyi durdurmamız gerekiyor. Kuleleri aynı anda susturmayın. Tekrar ediyorum, aynı anda değil. Personeli tahliye—"
    $ sfx("static")
    narrator "Kayıt kesilir. Voss'un yanıtı yok."
    $ add_note("kemal_uyari")
    a "Bu uyarıyı kim kesmiş?"
    rz "ECHO'dan gelen adamlar. Başlarında Voss'un ekibi vardı."
    narrator "Kayıt Kemal'i temize çıkarmaz. Yalnızca tehlikeyi bildiğini kanıtlar."
    m "Babası hakkında İdil'e ne söyleyeceğiz?"
    a "Önce gerçeği bulacağız."

    ## 3. Orman hattı ----------------------------------------------------------
    scene bg forest_night with long_fade
    $ amb("forest_night")
    show mert at sil_left
    show aras at sil_right
    with dissolve
    narrator "Eski servis yoluna giden ikinci bir bakım geçidi. Kablo yolu ormanın içine uzanıyor."
    m "Kablo yolu ormana uzanıyor."
    a "Yeraltındaki hatta bağlanıyor olabilir."
    $ sfx("metal_drag")
    narrator "Uzaktan bir ses gelir. Metal üzerinde ağır bir sürtünme."
    m "Bu ses… Deniz'in mesajında da vardı. Rüzgârın arkasında."
    a "Ama burada hoparlör yok."
    narrator "Aras sesin yalnızca bir hoparlörden gelmediğini fark eder. Ormanın içindeki bir şey de aynı sesi çıkarıyor."
    m "Olabilirlerden yoruldum."
    a "Ben de. Ama yanlış kesinlik daha tehlikeli."

    ## 4. Geri dönüşsüz karar ---------------------------------------------------
    scene bg relay_station with dissolve
    $ amb("relay")
    show riza at sil_center with dissolve
    rz "Geri dönmek için hâlâ vaktiniz var."
    show riza at sil_right with move
    show mert at sil_left with dissolve
    m "Deniz'in yok."
    show aras at sil_left2 with dissolve
    a "Biz dikkatli olacağız. Söz veremeyeceğimiz şey bu kadar."

    $ sfx("radio")
    bo_tel "Mert, Aras, duyuyor musunuz? Araçlar hazır. Bir şey olursa biz buradayız."
    m_tel "Duyuyoruz, Bora. Sabaha kadar kanalı açık tut."

    scene bg tower with long_fade
    $ amb("tower_hum")
    narrator "Mert ve Aras kasabadan uzaklaşır."
    narrator "Arkalarında kalan kulelerin ışıkları bir an hep birlikte yanıp söner."
    $ flash("#401010")
    narrator "Sonra her biri farklı bir ritme döner. Sanki birbirleriyle konuşuyorlar."
    return
