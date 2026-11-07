## BÖLÜM 17 — EŞİK

label ch17:
    call chapter_intro(17)

    ## 1. Gerçek ve taklit -----------------------------------------------------
    scene bg core_room with long_fade
    $ amb("z0")
    $ bgm("dread")
    narrator "Çekirdeğin kapısı açılır. İçeride iki adam var."
    narrator "İkisi de yaralı görünüyor. İkisi de Dr. Kemal Demir'e benziyor."
    $ gercek = renpy.random.choice(["sol", "sag"])
    show kemal as kemal_sol at sil_left
    show kemal as kemal_sag at sil_right
    with dissolve
    show mert at sil_center with dissolve
    narrator "Bir tanesi YANKI. TAKLİTÇİ. Ses ve görünüş taklit ediyor."
    narrator "Kapı eşiğinden bir anda geçemiyor; görüşü ve hareket alanı sınırlı. Ama ikisi de sana bakıyor."

label .kim:
    k "Aras, gerçek olan benim. Elimi kaldırıyorum."
    if gercek == "sol":
        show kemal as kemal_sol at sil_left, raise_hand
        show kemal as kemal_sag at sil_right, delayed_mirror
        narrator "Soldaki elini kaldırır. Sağdaki de kaldırır. Bir an sonra."
    else:
        show kemal as kemal_sag at sil_right, raise_hand
        show kemal as kemal_sol at sil_left, delayed_mirror
        narrator "Sağdaki elini kaldırır. Soldaki de kaldırır. Bir an sonra."
    takl "Elimi kaldırıyorum."
    if taklitci_ipucu:
        thought "B2'deki cam. Siluet her hareketi bir an geç yapıyordu. Gecikmeli olan taklit."
    a "Hangisi, Mert?"
    menu:
        "Soldaki gerçek.":
            $ secim = "sol"
        "Sağdaki gerçek.":
            $ secim = "sag"

    if secim != gercek:
        $ stress(15)
        $ sfx("growl")
        $ flash("#300000")
        narrator "Mert'in gösterdiği adam başını çevirir. Bir an sonra. Ağzı fazla açılır."
        narrator "Kapı eşiğine atılır, ama mekanik çerçeveye takılır. Metal inler."
        a "O değil! Gecikmeli olan o!"
        m "İkincisi bir an geç kaldı."
        narrator "Taklitçi geri çekilir. Yeniden Kemal'in yüzünü takınır. Yeniden bekler."
        jump .kim

    m "İkincisi bir an geç kaldı."
    a "O gecikmeyi kullanacağız."

    ## 2. Çıkarma --------------------------------------------------------------
    narrator "Mekanik bir perde, odayı ikiye bölebilir. Gerçek Kemal'in arkasında tek kişilik bir acil tahliye kapağı var."
    k "Acil tahliye kapağı bir kişi alır. Çabuk olun."
    m "Test sesini veriyorum. Hazır mısın?"
    a "Perdeyi kapatacağım."
    $ sfx("whisper")
    call screen qte("Taklitçi sesin geldiği yöne döndü — ŞİMDİ!", [("Perdeyi indir", "perde"), ("Bekle", "bekle")], 3.0, "bekle")
    if _return != "perde":
        $ stress(10)
        narrator "Bir saniye fazla beklerler. Taklitçi başını onlara geri çevirir."
        narrator "Mert test sesini yeniden verir. Bu kez Aras beklemez."
    $ sfx("door_slam")
    narrator "Perde iner. Görüş kesilir."
    a "Baba, sürün. Şimdi!"
    narrator "Kemal acil tahliye geçidinden sürünerek çıkar. Taklitçi çekirdekte kalır. Öldürülmüş sayılmaz."
    hide kemal_sol
    hide kemal_sag
    with dissolve
    scene bg z0_core with dissolve
    show kemal at sil_right
    show aras at sil_left
    with dissolve
    narrator "Aras babasına bakar. Üç yıl. Üç yıldır neredeyse hiç konuşmamışlar."
    a "Üç yıldır bunu söylemek için mi bekliyordun?"
    k "Büyümüşsün."

    ## 3. Hesaplaşma -----------------------------------------------------------
    a "Hakan öldü. D-14'te. Senin kurduğun yerde."
    narrator "Kemal gözlerini kapatır."
    k "Biliyorum. Durdurmalıydım."
    a "İnsanlar ölürken mi fark ettin?"
    k "Hayır. Daha önce fark ettim. Ve yine de kaldım."
    a "Senden af dilemeyi bırakmanı istiyorum. Gerçeği söyle."
    k "Sizi korumaya çalıştığımı söylemek kolay olurdu."
    a "Ama doğru olmazdı."
    k "Hayır. Korktum. İşimi, itibarımı, sonra da hayatımı kaybetmekten korktum."
    a "Hakan bunların hiçbirini seçemedi."
    narrator "Kemal kendini kahraman ilan etmez. Bağışlanmayı istemez."
    narrator "Aras'ın onu kurtarması, affettiği anlamına gelmez."

    ## 4. 6 Kasım gerçeği ------------------------------------------------------
    show mert at sil_center with dissolve
    m "Deniz. 6 Kasım gecesi ne oldu?"
    k "Deniz eski servis yolunda bir YANKI'dan kaçıyordu. K-2, güvenlik birimimiz, onu yaratığın önünden çekip aldı."
    k "S-17'yi içerideki görevli açtı. Deniz yardım için içeri alındı."
    m "Sonra onu neden bırakmadınız?"
    k "Voss veriyi istedi. Ben karşı çıkmakta geç kaldım."
    narrator "Deniz bırakılmadı. Gözlem altında tutuldu. Ölçüldü. Korkutuldu."
    m "Kurtardınız… sonra hapsettiniz."
    narrator "Kemal başını eğer."
    m "Deniz bir deney değil."
    k "Haklısın. Deniz rezonansın kaynağı değil. Hiçbir zaman olmadı. Sadece… ölçtükleri bir insan."

    ## 5. Üç atış --------------------------------------------------------------
    narrator "Kemal ceketinin iç cebinden küçük, metal bir kutu çıkarır."
    k "Üç Rezonans Kesici var. İkisi denendi; üçüncüsü denenmedi."
    narrator "Mermiler tüfeğe değil, yalnızca Mert'in tabancasına uygun."
    $ rezonans = 3
    $ rezonans_alindi = True
    $ add_note("uc_atis")
    a "Büyük olanı öldürür mü?"
    k "Rezonansı saniyelerce bozuyor. O sırada normal mermi işler mi, bilmiyoruz."
    a "O sırada vurulsalar?"
    k "Bilmiyoruz. Fiziksel dayanıklılıklarını test edemedik."
    m "Yani işe yarayabilir."
    k "Evet. Ama güvenmeyin."
    m "O zaman yalnızca son çare."

    ## 6. Camın ardında --------------------------------------------------------
    scene bg isolation with long_fade
    $ bgm(None)
    $ amb("tension")
    narrator "Alt izolasyon odası. Kalın bir camın arkası."
    show deniz at sil_far with Dissolve(2.0)
    narrator "Camın arkasında biri var."
    narrator "Gerçek. Yorgun. Korkmuş. Hiçbir özel gücü olmayan, on altı yaşında bir çocuk."
    show mert at sil_left with dissolve
    narrator "Mert cama yaklaşır. Bu kez gecikme yok. Deniz onu görünce irkilir, sonra öne atılır."
    dz "Abi?"
    m "Deniz…"
    dz "Geleceğini biliyordum."
    m "Biraz geç kaldım."
    dz "Geldin ya."
    m "Beni duyuyor musun?"
    narrator "Deniz avucunu cama koyar."
    dz "Beni bırakma."
    m "Bırakmayacağım."
    narrator "Fiziksel kurtarma henüz gerçekleşmedi. Arada bir cam, bir kilit ve bir yönetim yetkisi var."
    return

default gercek = "sol"
default secim = None
