## BÖLÜM 01 — KAYIP

label ch01:
    call chapter_intro(1)

    ## 1. Son telefon ----------------------------------------------------------
    scene bg phone_dark with long_fade
    $ amb("wind")
    centered "{size=+6}6 Kasım 2026 — 22.41{/size}\n\n{size=-2}Çamlık Kasabası, eski servis yolu{/size}"

    narrator "Deniz, Çamlık'ın eski servis yolunda tek başınaydı."
    narrator "Mert'in telefonuna bıraktığı sesli mesaj, sonradan defalarca dinlenecek kadar kısaydı."

    $ sfx("phone_beep")
    show phone_wave
    dz_tel "Abi… eski servis yolundayım. Bir şey gördüm…"
    dz_tel "Biri var sandım ama… hayır, o insan değil."
    dz_tel "Abi, lütfen telefonu aç!"
    $ sfx("whisper")
    uzak "Deniz…"
    dz_tel "Kim o?"
    $ sfx("phone_cut")
    hide phone_wave
    with Dissolve(0.3)
    $ add_note("sesli_mesaj")

    narrator "Polis telefonu ertesi sabah buldu. Deniz'i bulamadı."

    scene bg mert_room with long_fade
    $ amb("wind")
    centered "{size=+4}9 Kasım{/size}"
    show mert at sil_center, breathe with dissolve
    m_mesaj "Deniz, aç şu telefonu. Ne olur aç."
    narrator "Üç gün. Mert'in telefonunda aynı mesaj, aynı rüzgâr, aynı kesik."

    menu:
        "Mesajı bir kez daha dinle.":
            $ sfx("phone_beep")
            narrator "Mert kulaklığı takar. Sesi sonuna kadar açar."
            narrator "Deniz'in sesi gelirken arkada rüzgâr uğulduyor. Yapraklar, uzakta bir tel."
            narrator "Sonra o ikinci ses: {i}Deniz…{/i}"
            narrator "Ve o an rüzgâr yok. Hiç yok. Sanki ses başka bir yerden kesilip buraya yapıştırılmış."
            $ sfx("phone_cut")
            $ add_note("ikinci_ses")
            $ stress(5)
        "Telefonu ters çevirip masaya bırak.":
            narrator "Ekran karardığında oda daha da karanlık görünür."
            narrator "Mert telefonu ters çevirir. Ama mesaj kafasında çalmaya devam eder."
            $ stress(-5)

    ## 2. Aras'ın dönüşü --------------------------------------------------------
    $ sfx("lock_click")
    narrator "Kapı çalınır. Mert açmadan önce bekler; kim olduğunu bilmek ister gibi."
    show mert at sil_left with move
    show aras at sil_right with dissolve
    narrator "Aras Demir, Çamlık'a üç gün sonra dönebilmişti. Mert'i günlerdir uyumamış hâlde bulur."

    m "Polis telefonunu buldu. Deniz'i bulamadı. Bunun nasıl mümkün olduğunu anlat bana."
    m "Eski servis yolunu soruyorum, kimse cevap vermiyor. Sanki o yol haritada yokmuş gibi."
    a "Anlatabileceğim tek şey var: Babamın çalıştığı tesis bu ormana yakın."
    m "…"
    m "Bunu neden şimdi söylüyorsun?"
    a "Çünkü babamın ne sakladığını ben de bilmiyorum. Ama birlikte öğrenebiliriz."
    narrator "Aras'ın babası Dr. Kemal Demir. Yıllardır Çamlık'ın çevresindeki bir araştırma tesisinde çalışıyor. Ne yaptığını evde hiç anlatmamış."

    m "Son mesajını defalarca dinledim. Arka planda rüzgâr var, sonra o ses geliyor."
    a "Korktuğun için ayrıntıları kaçırman normal. Beraber dinleriz."
    m "Bir daha dinlemeye dayanabilir miyim, bilmiyorum."
    if "ikinci_ses" in notes:
        m "Ama bir şey fark ettim. O ikinci seste rüzgâr yok."
        a "…Emin misin?"
        m "Hayır. Ama yok."

    ## 3. İlk iz ---------------------------------------------------------------
    scene bg service_road with long_fade
    $ amb("forest_night")
    narrator "İkili, Deniz'in son görüldüğü noktaya gider."
    show mert at sil_left
    show aras at sil_right
    with dissolve
    narrator "Orman alışıldık seslerini taşır. Çekirgeler, rüzgâr, uzakta bir baykuş."
    $ amb(None, 0.2)
    $ sfx("birds_stop")
    narrator "Sonra bir anda hepsi susar."
    narrator "Bütün sesler aynı anda kesilir. Sanki biri düğmeye basmış gibi."
    $ renpy.pause(1.5, hard=True)
    $ amb("forest_night", 3.0)
    $ add_note("kus_sesi")
    a "Duydun mu? …Yani, duymadın mı?"
    m "Kuşlar sustu. Hepsi birden."

    narrator "Bir çit direğinde eskimiş bir işaret var. Boyası dökülmüş harfler: {b}ECHO{/b}."
    $ add_note("echo_isareti")
    a "Babamın kartvizitinde bu logo vardı."

    $ sfx("echo_voice")
    dz_fake "Abi?"
    with hpunch
    m "Deniz? Beni duyuyor musun?"

    menu:
        "Sesin geldiği ağaçlara koş.":
            $ sahte_kanma += 1
            $ stress(15)
            $ sfx("footsteps")
            narrator "Mert iki adım atamadan Aras kolunu yakalar."
            a "Dur!"
            $ jolt()
        "Olduğun yerde kal ve dinle.":
            $ stress(-5)
            narrator "Mert nefesini tutar. Ses yeniden gelir. Ama bu kez başka bir yerden."

    $ sfx("echo_voice")
    dz_fake "Abi?"
    a "Dur. Aynı ses sağımızdan da geliyor."
    m "Ya gerçekten oysa?"
    a "O zaman bile körlemesine koşarsak ikimizi de kaybeder."
    narrator "İlk kez anlarlar: sevdiğin birinin sesini takip etmek güvenli değildir."

    ## 4. Karar ----------------------------------------------------------------
    scene bg town_night with long_fade
    $ amb("town_night")
    narrator "Kasabada arkadaşlar toplanır. Kimse yalnız bekleyemeyecek kadar korkmuş."
    show bora at sil_left2
    show duru at sil_left
    show idil at sil_right
    show kaan at sil_right2
    with dissolve
    bo "Sabaha kadar beklemek zorunda değilsiniz. Biz burada olacağız."
    ka "Arabanın deposu dolu. Telsizleri de buldum."
    du "Aras, babamı bulursan önce bana haber ver."
    narrator "Duru, babalarından uzun süredir haber alamadığını söyler. Telefonu hep kapalı."
    idl "Ben de babamın neden ECHO'dan hiç söz etmediğini öğrenmek istiyorum."
    narrator "İdil Voss. Babası Adrian Voss da ECHO'nun kurucularından. Evde o ismi bir kez bile duymamış."
    hide bora
    hide kaan
    hide duru
    hide idil
    with dissolve

    scene bg mert_room with dissolve
    show mert at sil_center with dissolve
    narrator "Gecenin sonunda Mert mesajı son bir kez dinler."
    $ sfx("phone_beep")
    dz_tel "Abi… eski servis yolundayım."
    $ renpy.music.stop(channel="audio", fadeout=0.5)
    m "Ben gidiyorum."
    show mert at sil_left with move
    show aras at sil_right with dissolve
    a "Bu kez yalnız gitmiyorsun."
    return
