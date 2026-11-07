## BÖLÜM 14 — KAYIT DIŞI

label ch14:
    call chapter_intro(14)

    ## 1. D-14'ün gerçeği ------------------------------------------------------
    scene bg control_room with long_fade
    $ amb("b2")
    show mert at sil_left with dissolve
    narrator "Güvenlik yönlendirme odası. Onlarca ekran, çoğu karlı."
    narrator "Mert sistem kayıtlarında 10 Kasım'ı bulur."
    centered "{color=#ff4030}18.03 — BİYOLOJİK TEHDİT ALGILAMASI\nOTOMATİK KARANTİNA: D-14{/color}"
    m "D-14 karantinası otomatik başlamış."
    narrator "Adrian Voss'un kapıyı o anda bizzat kapattığına dair kayıt yok."
    m "Adrian düğmeye basmamış olabilir. Ama bu sistemi o durdurabilirdi."
    $ add_evidence("d14_kayit")
    m "Hakan… seni burada bıraktık."

    ## 2. Canlı görüntü --------------------------------------------------------
    $ sfx("static")
    narrator "Ekranlardan biri titreyerek açılır. D-14, kamera 3."
    narrator "Köşede, bir duvara yaslanmış biri. Yorgun, susuz, sarsılmış."
    m "Aras…"
    m "Yaşıyorsun."
    narrator "Hakan'ın bedeni kadrajın dışında. Mert bakmamaya çalışır."
    narrator "Kontrol panelinde bir interkom düğmesi var."
    $ sfx("radio")
    m "Kamera çalışıyor. Aras, ayağa kalk."
    a_kam "Mert? Bu ses gerçek mi?"
    m "Evet. Sana yol açacağım."
    a_kam "Bir kez daha söyle."
    m "Buradayım."
    narrator "Aras kameraya bakar. O an Mert'in kararı değişir: artık yalnızca araştırmayacak. Arkadaşına yol açacak."
    a_kam "Kamerayı çevirebiliyor musun? Solumda bir geçit var."
    m "Görüyorum. Ama tavanda kırık bir boru sallanıyor."
    a_kam "O zaman diğer yoldan giderim."
    m "Aynen. Bu kez kahramanlık yapma."

    ## 3. Üç güzergâh ----------------------------------------------------------
    narrator "Transfer Odası 03'e uzanan üç güvenlik hattı var. Hasar planı ile canlı kamerayı karşılaştırmak gerek."
    narrator "{b}Hat 1:{/b} Hasar planında yeşil, sorunsuz. Kamera 5: tavan çökmüş, moloz yığını."
    narrator "{b}Hat 2:{/b} Kamera 6: koridor temiz, ışıklar açık. Sistem: {color=#ff4030}BİYOLOJİK KARANTİNA AKTİF{/color}."
    narrator "{b}Hat 3:{/b} Hasar planında sarı, kısmi hasar. Kamera 7: sallanan boru ama geçilebilir. Kapılar uzaktan yönlendirilebilir."

label .rota:
    menu:
        "Aras'ı Hat 1'e yönlendir.":
            $ stress(6)
            $ sfx("radio")
            a_kam "Mert… burada geçit yok. Tavan inmiş."
            narrator "Hasar planı eski. Kamera daha yeni. Aras geri dönmek zorunda."
            m "Haklısın. Plana değil, görüntüye bakmalıydım."
            jump .rota
        "Aras'ı Hat 2'ye yönlendir.":
            $ stress(6)
            $ sfx("alarm")
            narrator "Aras kapıya yaklaşınca kırmızı ışıklar yanar. Kapı kilitli kalır."
            a_kam "Karantina kilidi! Açılmıyor!"
            m "Temiz görünüyor diye güvenli değil. Geri dön."
            jump .rota
        "Aras'ı Hat 3'e yönlendir.":
            m "Birinci koridor çökmüş. İkinci hat karantinada."
            a_kam "Üçüncü?"
            m "Transfer Odası 03'e çıkıyor. Ama güvenlik sürgüsünü açmalıyım."

    ## 4. Kayıt dışı kurtarma --------------------------------------------------
    narrator "Merkezi yönetimden bağımsız bir yerel güvenlik geçidi. Panelde iki seçenek."

label .kapi:
    menu:
        "Yalnızca servis kapısını aç (yerel, kayıt dışı).":
            $ sfx("door_open")
            narrator "Aras'ın önündeki kapı ağır ağır aralanır."
            narrator "Ekrandaki Aras önce tereddüt eder. Sonra kapıya yaklaşır."
            m "Hadi, hadi…"
            a_kam "Kapı hareket etti!"
            m "Yalnızca servis kapısı. Ana geçidi zorlama."
            a_kam "Anlaşıldı. Senden talimat almak tuhaf."
            m "Sonra dalga geçersin."
        "Ana geçidi aç (merkezî sistem).":
            $ stress(12)
            $ sfx("alarm")
            narrator "Ekranda bir uyarı: MERKEZÎ ONAY GEREKİYOR — İSTEK KAYDA ALINDI."
            narrator "Bir yerlerde bir alarm çalar. Uzaktan bir sürüklenme sesi alarma yönelir."
            $ sfx("metal_drag")
            m "Hayır, hayır… iptal."
            narrator "Mert isteği iptal eder. Merkezî sistem onu izliyor olabilir. Yerel yolu kullanmalı."
            jump .kapi

    ## 5. Buluşma noktası ------------------------------------------------------
    narrator "Transfer Odası 03'ün konumu Mert'in haritasında işaretlenir."
    m "Transfer Odası 03. Orada buluşacağız."
    a_kam "Bu kez beni bekle."
    m "Bekleyeceğim."
    narrator "Telsiz bağlantısı hâlâ parçalı. Buluşma ancak fiziksel olarak gerçekleşecek."
    return
