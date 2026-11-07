## BÖLÜM 15 — YENİDEN

label ch15:
    call chapter_intro(15)

    ## 1. Karşılaşma -----------------------------------------------------------
    scene bg transfer_room with long_fade
    $ amb("b3")
    show mert at sil_left with dissolve
    narrator "Transfer Odası 03. Mert kapıya sırtını verip bekler. Her ses, her damla."
    $ sfx("door_open")
    show aras at sil_right with dissolve
    a "Mert?"
    m "Buradayım."
    narrator "İkisi de önce birbirine bakar. Gerçekten bakar. Gecikme var mı, aynı nefes mi."
    narrator "Sonra sessizce sarılırlar. Aras'ın elleri titriyor."
    a "Hakan'ı çıkaramadım."
    m "Biliyorum."
    a "Hayır, görmedin."
    narrator "Mert konuşmayı zorlamaz."

    menu:
        "Su matarasını uzat.":
            narrator "Aras suyu bir dikişte bitirir. Gözlerini kapatır."
        "İlk yardım paketini aç, ellerini sar." if ilkyardim > 0:
            $ ilkyardim -= 1
            narrator "Aras'ın avuçları paramparça; çelik kapıyı zorlarken kesilmiş. Mert sargıyı sararken Aras ilk kez gözlerini ondan kaçırmaz."
            $ aras_sarildi = True
            $ stress(-10)

    a "Beni bırakmadığın için sağ ol."
    m "Bir daha ayrı düşmeyelim."
    a "Yalnızken sürekli Hakan'ın son sözlerini duydum."
    m "Ben de Deniz'in sesini. Ama gerçek ses hangisi, emin olamıyordum."
    a "Burada en azından birbirimizin yüzünü görüyoruz."

    ## 2. Az söz ---------------------------------------------------------------
    narrator "Mert yalnızca gerekli olanı anlatır. Uzun arşiv açıklamaları sonraya kalabilir."
    m "S-17 içeriden açılmış. Deniz'in sesi de gerçek dış mikrofonunda var."
    a "Yani biri onu içeri almış."
    m "Kim olduğunu Z0'da öğreneceğiz."
    if "red_notu" in kanit:
        m "Bir şey daha. Baban deneyi durdurmayı önermiş. Voss reddetmiş."
        a "Önermiş… ama yine de kalmış."
        narrator "Aras, babasının bu olayların içinde olduğunu kabul etmekte zorlanıyor."

    ## 3. İki kişilik geçiş ----------------------------------------------------
    scene bg platform_shaft with dissolve
    show mert at sil_left
    show aras at sil_right
    with dissolve
    narrator "Ağır yük platformu. Derin bir kuyunun ağzında. Güvenlik sensörü iki ayrı noktadan fiziksel doğrulama istiyor."
    a "Bu platform iki kişilik güvenlik algılayıcısı istiyor."
    m "İlk kez burada bir şeyin iki kişi istemesine sevindim."
    narrator "Aras sol algılayıcıya geçer, elini panele koyar. Işık sarıya döner."

label .es:
    menu:
        "Sağ algılayıcıya geç, sen de elini koy.":
            $ sfx("lock_click")
            narrator "İki ışık birlikte yeşile döner. Platform sarsılarak kilidinden kurtulur."
        "Aras'ın yanına git, panele birlikte bak.":
            narrator "Aras'ın paneli kırmızıya döner: ZAMAN AŞIMI."
            a "İki ayrı noktadan, Mert. Biri burada, biri orada."
            jump .es

    $ sfx("platform")
    narrator "Platform inmeye başlar. Sonra bir anda yan yatar."
    $ jolt(True)
    call screen qte("Aras dengesini kaybediyor!", [("Kolunu yakala", "tut"), ("Algılayıcıdan elini çekme", "panel")], 3.0, "gec")
    if _return == "tut":
        narrator "Mert Aras'ın bileğini yakalar. Platform yeniden düzelir."
        a "Birimiz düşerse diğeri tutacak."
    elif _return == "panel":
        $ stress(10)
        narrator "Mert elini panelde tutar. Platform düzelir ama Aras kenara çarpar, yüzü acıyla buruşur."
        a "İyiyim. İyiyim… Bir dahaki sefere beni tut."
    else:
        $ stress(12)
        narrator "Aras korkuluğa son anda tutunur. Mert onu yukarı çeker."
        a "Birimiz düşerse diğeri tutacak. Unutma."
    narrator "Bu bir terminal dizisi değildi. Güvenin yeniden kurulmasıydı."

    ## 4. Beraber korkmak ------------------------------------------------------
    $ amb("z0")
    narrator "Aşağıdaki karanlıktan beş ayrı boru hattının uğultusu geliyor. Beşi birden, beş ayrı tonda."
    a "Orada ne varsa ikimiz de bilmiyoruz."
    m "Korkuyor musun?"
    a "Evet."
    m "Ben de."
    a "O zaman beraber korkarız."
    narrator "Platform Z0'a doğru iner."
    return

default aras_sarildi = False
