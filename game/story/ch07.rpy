## BÖLÜM 07 — GİZLİ GİRİŞ

label ch07:
    call chapter_intro(7)

    ## 1. Hazırlık -------------------------------------------------------------
    scene bg town_morning with long_fade
    $ amb("wind")
    narrator "Sabah. Gri, kararsız bir ışık. Kimse uyumamış."
    show bora at sil_left2
    show kaan at sil_left
    show elif at sil_right
    show emir at sil_right2
    with dissolve
    narrator "Bora ve Kaan araç, yakıt ve iletişim planını düzenliyor. Elif ve Emir sağlık malzemesi topluyor."
    ka "Yedek bataryaları koydum. İki fener de çalışıyor."
    el "İlk yardım çantasını al. Geri getireceksin."
    em "Telsizleri iki kanala ayarladım. Biri kesilirse diğerine geçin."
    narrator "Bora, eski bir tabancayı ve altı mermiyi masaya bırakır."
    bo "Babamın ruhsatlı tabancası. Kullanmak zorunda kalmayın. Ama yanınızda olsun."
    m "Geri gelmeye çalışacağız."
    bo "Hayır. Geri geleceksiniz."

    $ mermi = 6
    $ ilkyardim = 1
    $ pil = 100

    narrator "Masada daha fazlası var. Ama çantada yer az. Teçhizatı hafif tutmaları gerek."
    $ quick_menu = False
    window hide
    call screen loadout
    $ loadout_apply(_return)
    $ quick_menu = True
    if "pil" in _return:
        ka "İyi seçim. Karanlık, aşağıda en büyük düşmanınız olacak."
    if "kaydedici" in _return:
        em "Kaydediciye senin sesini koydum. Kendi sesin onları kandırsın, onlar seni değil."
    if "ilkyardim" in _return:
        el "Umarım hepsini geri getirirsin. Kapağı açılmamış hâlde."

    hide bora
    hide kaan
    hide elif
    hide emir
    with dissolve
    show duru at sil_left
    show idil at sil_right
    with dissolve
    narrator "Duru, Aras'ın babasıyla ilgili sorularını saklamaz. İdil ise hatırladığı küçük bir şeyi anlatır."
    idl "Babam Çamlık'ta görünmeyen bir güvenlik koridoru kullanırdı. Arabası kasabaya girer, sonra hiçbir kamerada görünmezdi."
    idl "Yerini bilmiyorum. Bilseydim söylerdim."
    narrator "Kimse ECHO'ya kahramanca dalmaya zorlanmıyor. Yüzey ekibi arama ve yardım zincirini sürdürecek."
    du "Telsizden sesiniz gelmezse ne kadar bekleyelim?"
    show aras at sil_center with dissolve
    a "Önce yedek kanalı dene. Sonra Bora'yla güvenli bölgeye dön."
    du "Bana emir verme. Sadece geri dön."

    ## 2. B3 servis çizimi ------------------------------------------------------
    scene bg map_table with long_fade
    show aras at sil_right
    show mert at sil_left
    with dissolve
    narrator "Aras, babasının eski evrakları arasında bir teknik plan bulur. Tarih: 9 Kasım. Başlık: B3 BAKIM GİRİŞİ."
    a "B3 hattı ana girişten ayrı. Bakım çalışanları burayı kullanmış."
    m "İçerideki kapı nereden açılıyor?"
    a "Eski mekanik mandal var. Enerji kesilse bile çalışmalı."
    $ add_note("b3_plan")
    narrator "Plan eski. Bütün kapıların çalışacağı garanti değil."
    narrator "Teçhizat: telsiz, el feneri, sınırlı ilk yardım, temel aletler. Ve Bora'nın tabancası."

    ## 3. Vedalaşma ------------------------------------------------------------
    scene bg town_morning with dissolve
    show duru at sil_left
    show aras at sil_right
    with dissolve
    du "Aras, babama kızgın olabilirsin. Ama önce onu sağ bul."
    a "Bunun için elimden geleni yapacağım."
    du "Babamı bulursan bana gerçeği söyle."
    hide duru with dissolve
    show idil at sil_left with dissolve
    idl "Babamı görürsen… bana yalan söyleme."
    show mert at sil_center with dissolve
    m "Söylemeyiz."
    hide idil with dissolve
    narrator "Mert, Deniz'in fotoğrafını telefonunun kilit ekranında bırakır."
    show bora at sil_left with dissolve
    bo "Sinyaliniz kesilirse beklemeyeceğiz. Yardım çağıracağız."

    ## 4. Eşik -----------------------------------------------------------------
    scene bg echo_gate with long_fade
    $ amb("wind")
    centered "{size=+6}10 Kasım — 11.58{/size}"
    show mert at sil_left
    show aras at sil_right
    with dissolve
    narrator "Çamlık'ın altındaki tesise giden bakım geçidi. Planda gösterilen yer, ormanın içinde, yosun tutmuş bir kapak."
    $ sfx("lever")
    narrator "Mekanik mandal gıcırdar. Sonra yerinden oynar."
    $ sfx("door_open")
    narrator "Demir kapının ardında soğuk hava ve uzak metal vuruntuları."
    m "Saat on ikiye geliyor."
    a "İçeri girince telsiz zayıflayacak."
    a "İçeri girdikten sonra geri dönüş aynı yol olmayabilir."
    m "Deniz'in de olmadı."
    m "Deniz, geliyorum."
    a "Beraber."
    return

default yedek_pil = 0
