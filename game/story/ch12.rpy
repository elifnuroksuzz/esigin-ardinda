## BÖLÜM 12 — GÖZLEM

label ch12:
    call chapter_intro(12)

    ## 1. Camın ötesi ----------------------------------------------------------
    scene bg b2_glass with long_fade
    $ amb("b2")
    show mert at sil_left with dissolve
    narrator "B2. Mavi ışık. Araştırma ve gözlem odaları kalın cam duvarlarla ayrılmış."
    narrator "Her şey çok temiz. Fazla temiz."
    m "Camın arkasında biri var."
    show mert as mert_cam at sil_far, delayed_mirror with dissolve
    narrator "Bir odanın içinde, camın arkasında bir insan silueti. Hareketsiz."
    narrator "Kapının yanındaki biyolojik sensör: {color=#6ab0e0}SIFIR HAREKET{/color}."
    m "Biyolojik tarama sıfır gösteriyor."

    menu:
        "Başını yavaşça sağa çevir. Ne yapacağını izle.":
            show mert at sil_left, raise_hand
            show mert as mert_cam at sil_far, delayed_mirror
            narrator "Mert başını çevirir. Siluet de çevirir."
            narrator "Ama bir an sonra. Kalp atışı kadar kısa bir gecikmeyle."
            m "Ben başımı çevirdim… o sonra çevirdi."
            $ taklitci_ipucu = True
            $ add_note("gozlemci")
        "Bakma. Yürümeye devam et.":
            narrator "Mert gözünü cama çevirmeden yürür. Ensesinde bir bakış hisseder."
            $ stress(6)

    $ sfx("door_slam")
    hide mert_cam
    with Dissolve(0.2)
    narrator "Mekanik perde iner. Görüntü kaybolur."
    m "Camın arkasındaki gölge bana bakmıyordu. Ben ona bakınca hareket etti."

    ## 2. 2024 dosyaları -------------------------------------------------------
    scene bg b2_archive with dissolve
    show mert at sil_left with dissolve
    narrator "Arşiv odası. Klasörler, sabit diskler, laboratuvar defterleri."
    narrator "2024 tarihli deney kayıtları: {b}DENEK 14{/b} ve {b}DENEK 16{/b}."
    m "Denek on dört… tarih 2024."
    narrator "Bir an nefesi kesilir. Sonra tarihleri, boy ve yaş bilgisini okur."
    m "Deniz olamaz. O tarihte burada değildi."
    m "Demek bunu yıllardır yapıyorlar."
    $ add_note("denek")
    narrator "Deneylerin amacı YANKI'ları anlamak ve rezonans yoluyla yönlendirmek. Kayıtlarda 'kontrol edildi' yazıyor. Ama hiçbir sonuç bunu desteklemiyor."
    m "Deney kayıtlarında 'gözlemci etkisi' yazıyor. Bu yalnızca bir benzetme mi?"

    ## 3. İtirazın reddi -------------------------------------------------------
    narrator "Bir klasörde iki satır yan yana:"
    centered "{color=#9ec0a0}DR. K. DEMİR — DENEYİN DURDURULMASINI ÖNERİYOR{/color}\n\n{color=#d04a3a}A. VOSS — ÖNERİ REDDEDİLDİ{/color}"
    $ add_evidence("red_notu")
    narrator "Yanında bir ses kaydı. Mert oynatır."
    k_arsiv "Deneyi durdurmalıyız. Tahliye gecikiyor."
    adr_arsiv "Öneriniz reddedildi, Kemal."
    k_arsiv "İçeride insanlar var."
    adr_arsiv "Veri kaybını göze alamam."
    narrator "Arşivin hemen ötesinde kapalı bir tahliye çıkışı. Önünde bırakılmış eşyalar: bir çanta, tek bir ayakkabı, kırık bir kimlik kartı."
    narrator "Zorlanmış bir güvenlik kapısı."
    narrator "Voss'un sorumluluğu yalnızca bir kâğıtta değil. Sonuçlarında da."
    m "Buradan sağ çıkarsam Kemal'e soracağım."

    ## 4. Sahte görüntü --------------------------------------------------------
    scene bg b2_glass with dissolve
    show mert at sil_left with dissolve
    show deniz at sil_far, glitchy with Dissolve(1.0)
    narrator "Bir cam bölmenin ardında bir genç. Kapüşonlu. Omuzları Deniz'inki gibi."
    m "…Deniz?"

    menu:
        "Cama koş, avucunu cama bastır.":
            $ stress(12)
            narrator "Mert cama yapışır. Ama camın öbür tarafında kimse yok."
            narrator "Yalnızca kendi yansıması. Nefesiyle buğulanmış cam."
        "Olduğun yerde kal. Gecikme var mı, izle.":
            narrator "Mert kıpırdamaz. Siluet de kıpırdamaz. Sonra Mert elini kaldırır."
            narrator "Siluet bir an sonra kaldırır. Sonra solup gider."
    hide deniz with dissolve
    m "Bana onu göstererek beni yönetemezsin."
    narrator "Sesinde kuşku kaybolmaz."
    m "Perde kapanınca siluet kayboldu."
    m "Gördüğüme güvenemem. Ama camdaki gecikmeyi unutmayacağım."
    narrator "Oyun bu sahneyi Deniz'in hayatta olduğuna kanıt olarak kullanmaz. Mert de kullanmamaya çalışır."
    $ drain_pil(5)
    call pil_check
    return
