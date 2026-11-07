## BÖLÜM 16 — MERKEZ

label ch16:
    call chapter_intro(16)

    ## 1. Beş hat, tek merkez --------------------------------------------------
    scene bg z0_core with long_fade
    $ amb("z0")
    show mert at sil_left
    show aras at sil_right
    with dissolve
    narrator "Z0. Beş yüzey kulesinden gelen dev iletim kanalları karanlığın ortasında birleşiyor."
    narrator "Defterdeki cümle burada bir benzetme değil. Bir mimari."
    a "Beş ayrı kule. Hepsi Z0'a iniyor."
    m "Z0 beşinci kule değil."
    a "Hayır. Hepsinin toplandığı merkez."
    narrator "Aras defteri açar. Son sayfadaki, ilk okuduklarında anlamadıkları satır:"
    narrator "{i}Beş nokta aynı anda sustuğunda, kapı açık kalır.{/i}"
    m "Bütün kuleler aynı anda susarsa ne olacak?"
    a "Defter bunun tehlikeli olduğunu söylüyor. Merkezi kademeli ayırmamız gerek."
    m "Demek mesele kapatmak değil, nasıl kapattığımız."
    $ add_note("kademeli")

    ## 2. Boşluk ---------------------------------------------------------------
    scene bg z0_bridge with dissolve
    show mert at sil_left
    show aras at sil_right
    with dissolve
    narrator "Servis köprüleri. Aynı kapıya yaklaştıklarını sanıyorlar. Ama kapı yaklaşmıyor."
    m "Koridor uzuyor gibi."
    $ drain_pil(8)

label .bosluk:
    a "Neye tutunacağız?"
    menu:
        "Gözlerine: kapıya bakarak düz yürü.":
            $ stress(8)
            narrator "Kapıya bakarak yürürler. Beş dakika. On dakika. Kapı hep aynı uzaklıkta."
            narrator "Sonra bir an başlarını çevirdiklerinde, bambaşka bir yükseklikteki köprüde olduklarını fark ederler."
            jump .bosluk
        "Boru hatlarının uğultusuna: sese doğru yürü.":
            $ stress(10)
            $ sfx("echo_voice")
            narrator "Uğultu her adımda yer değiştiriyor. Bir ses, aralarında, adlarını söylüyor."
            a "Hayır. Sesi değil. Asla sesi değil."
            jump .bosluk
        "Ellerine: korkuluğu ve boru etiketlerini.":
            narrator "Aras bir elini korkuluktan hiç ayırmaz. Her boru etiketinde durup numarayı okur: Z0-3-114, Z0-3-115, Z0-3-116…"
            a "Duvara bak. Çatlak aynı yerde."
            m "Demek mesafe değil, algımız değişiyor."
            narrator "Mekânın kendisi gerçek. Algı güvenilmez. Etiketler sırayla artarken kapı sonunda yaklaşır."

    call pil_check

    ## 3. Yönetim komutu -------------------------------------------------------
    $ sfx("alarm")
    narrator "Bir anda bütün kanallarda bir uğultu yükselir. ECHO-3 hattında uzaktan yük bindirme başlıyor."
    centered "{color=#d04a3a}A. VOSS — YÖNETİM OTURUMU\nKOMUT 04.17\nERİŞİM: B1 YÖNETİM HATTI{/color}"
    a "A. Voss yönetim oturumu. B1 hattından."
    m "ECHO-3'ü aşırı yükledi."
    $ add_evidence("voss_komut")
    $ sfx("thud")
    $ jolt(True)
    call screen qte("Köprü bağlantısı kopuyor!", [("Korkuluğa sarıl", "tut"), ("Karşı tarafa koş", "kos")], 3.0, "dus")
    if _return == "tut":
        narrator "Köprü bir metre aşağı çöker, sonra takılır. Korkuluğa sarılan ikili sallanarak durur."
    elif _return == "kos":
        $ stress(10)
        narrator "Koşarlar. Arkalarında köprünün bir parçası karanlığa düşer. Son adımı Aras Mert'i sürükleyerek atar."
    else:
        $ stress(15)
        narrator "Mert'in ayağı boşluğa kayar. Aras onu kemerinden yakalar."
        if ilkyardim > 0:
            $ ilkyardim -= 1
            narrator "Dizinde derin bir sıyrık. Son sargılardan birini harcarlar."
    a "Bizi gördüğü için mi yaptı?"
    m "Görmese bile içeride biri olabileceğini biliyordu."
    narrator "Bunun doğrudan bir suikast olduğu kanıtlanamaz. Ama pervasızlığı açık."

    ## 4. Kemal'in izi ---------------------------------------------------------
    scene bg core_room with dissolve
    show mert at sil_left
    show aras at sil_right
    with dissolve
    narrator "Kontrol terminalinde 8 Kasım'dan kalma kısa bir mesaj. Gönderen: K. Demir. Alıcı: yok."
    k_kayit "Bunu durdurabileceğimi sandım."
    k_kayit "Sistem eşzamanlı kapanmamalı. İzolasyon halkası kullanılabilir. Tek tek… tek tek ayrılmalı."
    narrator "Sesinde pişmanlık var. Ama hiçbir cümle işlediği hataları silmiyor."
    a "Baba… neden eve dönmedin?"
    m "Cevabı kendisinden alacağız."

    ## 5. İki Kemal ------------------------------------------------------------
    $ sfx("metal_knock")
    narrator "Yönetim çekirdeğinin kapalı kapısının ardından sesler gelir."
    k_fake1 "Aras, kapıyı aç."
    k_fake2 "Aras, ona güvenme."
    narrator "Biri yardım istiyor. Diğeri aynı kelimeleri hafif gecikmeyle tekrarlıyor. İçeride iki hareket var."
    a "İkisi de babam gibi."
    m "O zaman seslerini değil, hareketlerini izleyeceğiz."
    $ add_note("iki_kemal")
    return
