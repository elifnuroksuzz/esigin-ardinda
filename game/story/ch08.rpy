## BÖLÜM 08 — ECHO

label ch08:
    call chapter_intro(8)
    $ show_hud = True

    ## 1. Yeraltına iniş -------------------------------------------------------
    scene bg b3_corridor with long_fade
    $ amb("b3")
    centered "{size=+6}10 Kasım — 12.07{/size}\n\n{size=-2}ECHO · B3 bakım katı{/size}"
    show mert at sil_left
    show aras at sil_right
    with dissolve
    narrator "Sarı ışıklı mekanik koridorlar. Zemin yağlı. Duvarlar kalın servis borularıyla dolu."
    narrator "Her şey çalışıyor. Ama kimse yok."
    a "B3 bakım katı. Zemindeki sarı çizgi servis hattına gidiyor."
    m "Burada kimse yok gibi."
    a "Bu, güvenli olduğu anlamına gelmiyor."
    narrator "Duvardaki yönlendirme tabelası okunaklı. Her katın bir rengi var:"
    narrator "{color=#e8eef8}B1 — YÖNETİM{/color}   ·   {color=#6ab0e0}B2 — ARAŞTIRMA{/color}   ·   {color=#c8a24a}B3 — BAKIM{/color}   ·   {color=#d04030}ARA KAT D — KARANTİNA{/color}   ·   {color=#8070c0}Z0 — MERKEZ{/color}"
    $ add_note("katlar")
    call tip("hud", "Hayatta kalma göstergesi", "Sağ üstte {b}fener pili{/b}, {b}mermi{/b}, {b}ilk yardım{/b} ve {b}nabız{/b} var. Karanlık bölümler pili tüketir. Nabız yükseldikçe algın bozulur; 70'in üstünde kalbini duyarsın.")
    $ drain_pil(5)

    ## 2. Eski güvenlik --------------------------------------------------------
    scene bg security_hall with dissolve
    show mert at sil_left
    show aras at sil_right
    with dissolve
    narrator "Güvenlik holü. Soğuk beyaz ışık, sıra sıra dolaplar."
    m "Şu dolapta tüfek var."
    narrator "Kalın camın arkasında sıradan bir güvenlik tüfeği. Kilit paneli kırmızı: MERKEZÎ KİLİT."
    a "Merkezi kilitli. Zorlayamayız."
    $ add_note("tufek_dolabi")
    narrator "Hemen yanında, duvara gömülü eski bir panel. Toz tutmuş bir etiket:"
    centered "{color=#c8a24a}ACİL REZONANS BASTIRMA\nMANUEL TEST HATTI{/color}"
    m "Ya şu eski düzenek?"
    a "'Acil rezonans bastırma.' Besleme kapalı."
    narrator "Göstergeler sönük. Kolu çekmek hiçbir şey yapmaz. Arızalı, devre dışı."
    $ add_note("bastirma_hatti")
    narrator "İki nesne de Mert'in aklında bir yere yerleşir."

    ## 3. Nöbetçi'nin sesi -----------------------------------------------------
    scene bg b3_dark with long_fade
    $ amb("b3")
    show mert at sil_left
    show aras at sil_right
    with dissolve
    $ sfx("metal_drag")
    narrator "Uzakta ağır bir sürtünme. Sonra metal üzerinde ölçülü darbeler."
    $ sfx("metal_knock")
    m "Yine o sürüklenme sesi."
    a "Ağır bir şey metalin üzerinde hareket ediyor."
    m "Görüyor mu bizi?"
    a "Bilmiyorum. Ama sesimizi duymasın."
    $ drain_pil(8)
    narrator "Koridorun ortasında dev bir hidrolik pres. Birkaç saniyede bir gürleyerek iniyor, sonra sessizce kalkıyor."
    narrator "Ötede, koridorun sonunda karanlık bir gövde dönüyor. Yavaş. Çok yavaş."
    show nobetci at creature_far
    $ sfx("growl")

label .gecis:
    $ sfx("fan")
    call screen qte("Pres iniyor — GÜRÜLTÜ!", [("Şimdi geç", "gec"), ("Bekle", "bekle")], 3.0, "bekle")
    if _return == "gec":
        $ sfx("footsteps")
        narrator "Presin gürültüsü adımlarını yutar. Koridoru geçip bir boru yığınının arkasına çökerler."
        narrator "Gövde döner, ama onlara değil. Presin olduğu yere."
    else:
        $ stress(10)
        narrator "Pres yeniden kalkar. Koridorda derin bir sessizlik."
        $ sfx("metal_drag")
        narrator "Karanlıktaki gövde sana doğru bir adım atar. Durur. Dinler."
        a "{size=-4}Bir sonrakinde. Gürültüyü bekle.{/size}"
        jump .gecis

    hide nobetci with dissolve
    narrator "Yaratığın ağır bedeni dar alanda yavaş dönüyor. Bu fiziksel bir sınır."
    $ add_note("nobetci")
    call pil_check

    ## 4. Hakan ----------------------------------------------------------------
    scene bg security_hall with dissolve
    $ sfx("lock_click")
    show hakan at sil_center with dissolve
    narrator "Bir köşeyi döndüklerinde bir fener yüzlerine doğrultulur. Arkasında bir tabanca."
    h "Silahları indirin! Siz kimsiniz?"
    show hakan at sil_right with move
    show aras at sil_left with dissolve
    a "Deniz Aydın'ı arıyoruz."
    h "Burada olmamanız gerekiyor."
    show mert at sil_left2 with dissolve
    m "Kardeşim burada olabilir. Çıkmam."
    narrator "Adam bir an tereddüt eder. Üniformasında isim: HAKAN ERSOY — GÜVENLİK."
    narrator "Silahı indirir. Uzaktan yeniden o sürüklenme sesi geliyor."
    h "Buraya nasıl girdiğinizi sonra konuşuruz. Şimdi ses çıkarmayın."
    h "Burada ışıklar söndüğünde işaret çizgilerini izleyin. Beyaz koridor sizi yanıltır."
    $ add_note("beyaz_koridor")
    m "Siz kaç yıldır buradasınız?"
    h "Yeterince uzun. Keşke daha önce soru sorsaydım."
    return
