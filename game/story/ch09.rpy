## BÖLÜM 09 — BİR RESİM

label ch09:
    call chapter_intro(9)

    ## 1. Kısa sığınak ---------------------------------------------------------
    scene bg safe_room with long_fade
    $ amb("b3")
    show hakan at sil_right
    show mert at sil_left
    with dissolve
    narrator "Hakan onları güvenlik bölümünün arkasındaki küçük bir odaya alır. Kapıyı kilitler. İlk kez rahat nefes alıyorlar."
    h "Burada biraz soluklanın. Sonra D-14'e geçeceğiz."
    narrator "Hakan tesisin her bölümünün aynı tehlikede olmadığını anlatır."
    h "B1 temiz. Yönetim ofisleri. B2 cam bölmeli araştırma odaları. B3 bakım, burası. D katı karantina."
    h "Eski protokoller hâlâ çalışıyor. Ve artık insanlardan hızlı karar veriyorlar."
    m "Bize neden yardım ediyorsun?"
    h "Çünkü artık burada olup bitene göz yumamıyorum."

    ## 2. Kızının çizimi -------------------------------------------------------
    narrator "Masanın üzerinde, kahve lekeli bir kâğıt. Pastel boyalarla çizilmiş üç figür:"
    centered "{color=#e0c890}BABAM, ANNEM VE BEN{/color}"

    menu:
        "Çizimi sor.":
            $ hakan_resmi = True
            show aras at sil_left2 with dissolve
            a "Çizimi kızınız mı yaptı?"
            h "On iki yaşında. Boyumu biraz abartmış."
            narrator "Hakan gülümser. Bu odada ilk kez biri gülümsüyor."
            m "Güzel çizmiş."
            h "Sabah götürecektim. Hâlâ götüreceğim."
            $ add_note("hakan_ailesi")
            $ unlock("bir_resim")
            narrator "Çizimin arkasında, aynı pastel boyayla yazılmış birkaç satır var. Hakan kâğıdı Mert'e uzatır."
            h "Oku istersen. Ben ezbere biliyorum."
            call read_doc("hakan_kizi")
        "Sessiz kal, çizime bakmaya devam et.":
            narrator "Mert bir şey sormaz. Ama gözleri bir süre o üç figürde kalır."
            narrator "Hakan bunu fark eder. Kâğıdı dikkatlice katlar ve göğüs cebine koyar."
            h "Eve götürecektim. Hâlâ götüreceğim."

    h "Kızım bana 'Gece neden çalışıyorsun?' diye soruyor."
    show aras at sil_left2 with dissolve
    a "Ne cevap veriyorsunuz?"
    h "İnsanların güvende olması için diyorum. Son zamanlarda buna kendim de inanmıyorum."

    ## 3. Test hattı -----------------------------------------------------------
    m "Girişte gördüğümüz rezonans test hattı çalışıyor mu?"
    h "Eski test sistemi. Güvenlik için kurdular ama güvenilir bulmadıkları için devreden çıkardılar. Acil beslemesi ayrı."
    a "Merkez kilitleri açılırsa erişebiliriz."
    h "Tüfek dolabı da öyle. Merkez kilidi açılmadan kimse alamaz. Ben bile."
    h "Umarım gerek kalmaz."

    ## 4. D-14'e gidiş ---------------------------------------------------------
    narrator "Hakan'ın ekranında bir hareket kaydı belirir. D-14 yakınındaki aktarım sistemi. Tarih: 6 Kasım gecesi."
    m "Bu Deniz olabilir."
    h "Olabilir. Ama sizi oraya yalnız göndermem."
    h "D-14 kapıları biyolojik tehlikede kendiliğinden kapanır."
    m "İçeride biri kalırsa?"
    h "İşte en çok korktuğum soru bu."

    scene bg b3_dark with dissolve
    show hakan at sil_center
    show mert at sil_left
    show aras at sil_right
    with dissolve
    narrator "Üçlü kısa ve dikkatli bir geçişe çıkar."
    $ sfx("metal_drag")
    narrator "Duvarın ötesinde Nöbetçi'nin sesi. Her seferinde biraz daha yakın."
    $ drain_pil(6)
    call pil_check
    return
