## BÖLÜM 02 — KARA DOSYA

label ch02:
    call chapter_intro(2)

    ## 1. Eski defter ----------------------------------------------------------
    scene bg depot with long_fade
    $ amb("wind")
    narrator "Kemal'in yıllar önce kullandığı depo. Toz, paslı raflar, kapağı ezilmiş bir metal kutu."
    show aras at sil_right
    show mert at sil_left
    with dissolve
    narrator "Elektrik yok. Telefonlarının ışığıyla rafları tararlar."
    window hide
    $ quick_menu = False
    call screen flashlight_search("depot", [("kutu", "Ezik metal kutu", "▣", 1000, 560), ("foto", "Solmuş fotoğraf", "▭", 240, 300), ("plan", "Bakım planı", "▤", 610, 470)], "KEMAL'İN DEPOSU")
    $ quick_menu = True
    narrator "Solmuş bir fotoğraf: iki adam, yeni açılmış bir tesisin önünde. Arkasında: {i}K. Demir · A. Voss · Açılış{/i}."
    narrator "Duvardan sökülmüş eski bir bakım planı. Köşesinde beş noktalı, ortası boş bir sembol."
    $ sfx("lock_click")
    narrator "Ve ezik metal kutu. Aras kutuyu açar. İçinden siyah kapaklı bir defter çıkar. Kapağında elle yazılmış:"
    centered "{size=+8}KARA DOSYA — 001{/size}"
    m "Bu defteri kim yazmış?"
    a "Bilmiyorum. Babamın el yazısına da benzemiyor."
    narrator "Sayfalarda düzenli bir anlatım yok. Yalnızca parçalı uyarılar, bazıları üstü çizilip yeniden yazılmış:"
    narrator "{i}İşitmek, anlamak değildir.{/i}"
    narrator "{i}Ses, sahibini gerektirmez.{/i}"
    narrator "{i}Beş nokta. Tek merkez.{/i}"
    $ add_note("kara_dosya")
    m "'Ses, sahibini gerektirmez.' Ne demek bu?"
    a "Ormanda duyduğumuz şeyi düşününce… anlamak istemiyorum."
    a "Bu defterdeki işaretler süs değil. Aynı sembolü eski bakım planında gördüm."
    m "O zaman bunu yazan kişi tesisi biliyordu."
    a "Ya da tesiste olan bir şeyi dışarıya anlatmaya çalışıyordu."

    ## 2. İki olasılık ---------------------------------------------------------
    narrator "Mert'in aklında daha basit bir açıklama var."
    m "Hoparlör olabilir. Birileri Deniz'in kaydını oynatıyor olabilir."
    a "O zaman sesin geldiği yön değiştiğinde gecikme ölçmeliyiz."
    m "Sen ölç. Ben onu bulacağım."
    a "İkisini aynı anda yapacağız."
    narrator "Aras, ormanda telefonla kaydettikleri sesleri dizüstüne aktarır. Deniz'in sesli mesajını da yanına koyar."
    narrator "Ekranda üç ses parçası var."

label .bulmaca:
    a "Dinle. Ve bak. Hangisi gerçek Deniz?"
    window hide
    $ quick_menu = False
    call screen waveform_puzzle
    $ quick_menu = True
    $ dalga = _return
    if dalga == "A":
            $ sfx("phone_beep")
            a "Rüzgâr sesi mikrofona çarpıyor, nefesi korkudan bölünüyor. Ağaçlardan gelen dalga boyları da çevreyle uyumlu."
            a "Bu gerçek. Bu, Deniz'in kendisi."
            m "…Biliyordum. Ama bunu duymak başka."
    elif dalga == "B":
            $ stress(5)
            $ sfx("echo_voice")
            a "Üst üste koyuyorum, bak. Tek bir milisaniye bile kaymıyor."
            a "İnsan aynı kelimeyi iki kez aynı şekilde söyleyemez. Bu bir kopya."
            m "Peki gerçek olan hangisi?"
            jump .bulmaca
    else:
            $ stress(5)
            a "Rüzgârın aniden kesildiğini duyuyor musun? Ses başka bir ortamdan alınıp yapıştırılmış gibi."
            a "Bu Deniz'in sesi bile değil. Onun adını söyleyen şey."
            jump .bulmaca

    $ add_note("tekrar_nefes")
    a "Kopyalar aynı cümleyi aynı nefesle tekrar ediyor. Bunu unutma."
    narrator "Aras'ın teknik bilgisi kesin bir cevap vermez. Yalnızca neyin ölçülebileceğini gösterir."

    ## 3. Duru'nun uyarısı -----------------------------------------------------
    scene bg town_night with long_fade
    $ amb("town_night")
    show duru at sil_center with dissolve
    narrator "Demirlerin evi. Duru mutfak masasında, babasının eski telefonuna bakıyor."
    du "Babam son konuşmasında 'Voss sistemi durdurmayacak' dedi."
    show duru at sil_left with move
    show aras at sil_right with dissolve
    a "Peki babam neden çıkıp gelmedi?"
    du "Bilmiyorum. Ama onu bulacaksan kendini de kaybetme."
    hide duru with dissolve
    show mert at sil_left with dissolve
    narrator "Duru odadan çıktığında ikili ilk kez açıkça konuşur."
    a "Babam kurban mı, suç ortağı mı? Bunu sormaktan korkuyorum."

    menu:
        "'Belki de kurtulmaya çalışıyordur.'":
            m "Belki de içeride sıkıştı. Belki kurtulmaya çalışıyordur."
            a "Buna inanmak istiyorum. Ama Duru'ya yalan söylemek istemiyorum."
        "'Bildiklerini sakladı. Bunu ikimiz de biliyoruz.'":
            m "Bildiklerini sakladı, Aras. Bunu ikimiz de biliyoruz."
            a "…Evet. Ve bu, hiçbir şeyi hafifletmiyor."
        "'Önce gerçeği bulalım. Sonra karar veririz.'":
            m "Önce gerçeği bulalım. Hüküm vermek için acele etmeyelim."
            a "Haklısın. Yanlış kesinlik daha tehlikeli."

    ## 4. Beş işaret -----------------------------------------------------------
    scene bg map_table with long_fade
    show aras at sil_right
    show mert at sil_left
    with dissolve
    narrator "Defterin son sayfalarında eski bir topoğrafya çizimi var. Çamlık'ın çevresinde beş tepe, beşi de kırmızı mürekkeple işaretlenmiş."
    a "Beş işaret var. Hepsi aynı merkeze bakıyor."
    m "Deniz'in son sinyali de tam aralarında."
    $ add_note("bes_tepe")
    a "Tesadüf olabilir."
    m "Olabilir. Ama bakmadan bilemeyiz."
    return

default dalga = None
