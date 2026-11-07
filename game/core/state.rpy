## Oyun durumu: kaynaklar, gerginlik, defter ve kanıtlar ######################

## Kaynaklar
default pil = 100            # fener pili (%)
default mermi = 0            # normal tabanca mermisi
default rezonans = 0         # Rezonans Kesici mermi (Bölüm 17'de 3 adet)
default rezonans_alindi = False
default ilkyardim = 0        # ilk yardım paketi
default gerginlik = 0        # 0–100; sahte seslere kanmak, panik kararlar
default show_hud = False

## Hikâye bayrakları
default current_chapter = 1
default chapter_cursor = 1
default rota5 = None              # "kisa" / "uzun"
default sahte_kanma = 0           # YANKI taklidine kaç kez kanıldı
default hakan_resmi = False       # Hakan'ın kızının resmini konuştu mu
default taklitci_ipucu = False    # Bölüm 12'de gecikmeyi fark etti mi
default kirpinti_atlatma = 0      # Kırpıntı'yı sessizce atlatma sayısı
default final_yontem = None       # "rezonans" / "bastirma"

## Defter
default notes = []
default kanit = []

## Kalıcı (tüm oyunlar boyunca)
default persistent.max_chapter = 1
default persistent.completed = False
default persistent.allow_shake = True
default persistent.allow_flash = True
default persistent.qte_relaxed = False

init -3 python:

    ## Defter girdileri: id -> (başlık, metin)
    JOURNAL = {
        "sesli_mesaj": ("Son sesli mesaj", "Deniz 6 Kasım gecesi eski servis yolundaydı. 'O insan değil' dedi. Arkada ona benzeyen ama ona ait olmayan bir ses adını söyledi."),
        "ikinci_ses": ("İkinci ses", "Mesajdaki ikinci 'Deniz…' çağrısında rüzgâr yok. Sanki başka bir yerden kopyalanıp eklenmiş."),
        "kus_sesi": ("Kuşlar susuyor", "Ormanda belli aralıklarla bütün kuş sesleri aynı anda kesiliyor."),
        "echo_isareti": ("ECHO işareti", "Çit direğinde eskimiş bir ECHO işareti. Aras'ın babası Kemal yıllardır yakındaki bir tesiste çalışıyor."),
        "kara_dosya": ("KARA DOSYA — 001", "'İşitmek, anlamak değildir.' 'Ses, sahibini gerektirmez.' 'Beş nokta. Tek merkez.' Yazarı belli değil."),
        "tekrar_nefes": ("Tekrar eden nefes", "Sahte ses aynı cümleyi aynı nefesle, birebir tekrar ediyor. Gerçek bir insan her seferinde biraz farklı konuşur."),
        "bes_tepe": ("Beş tepe", "Defterdeki topoğrafya çizimi Çamlık çevresinde beş tepeyi gösteriyor. Deniz'in son sinyali tam ortalarında."),
        "bes_kule": ("Beş kule, tek merkez", "Beş tepedeki bakım yapıları ECHO'nun yüzey kuleleri. Laboratuvar değil; yer altındaki tek bir merkeze veri ve enerji taşıyorlar."),
        "kule_izleri": ("Kuledeki izler", "Kesilmiş tel örgü, yakın zamanda bırakılmış ayak izleri, toprağın altına inen kullanılmış kablo hattı. Biri hâlâ çalıştırıyor."),
        "kemal_uyari": ("Kemal'in kesilen uyarısı", "Kemal, Voss'a: deneyi durdurun, kuleleri aynı anda susturmayın, personeli tahliye edin. Yanıt yok."),
        "ruza_sessizlik": ("Rıza'nın gecesi", "6 Kasım gecesi köpekler sabaha kadar havladı, sonra elektrik kesintisiyle aynı dakika sustular."),
        "isitmek": ("İşitmek, anlamak değildir", "Ormanda yollar döngüye girdi. Ses değil, iz takip edilmeli: çamur, eğim, taştaki çizik, kablo."),
        "lastik_izi": ("Yeni lastik izleri", "Deniz kaybolduktan sonra da birileri eski servis yoluna araçla gelmiş."),
        "surungen": ("SÜRÜNGEN", "Duvar ve dik yüzeylerde ilerleyen YANKI. Sese ve ışığa yöneliyor. Normal mermi onu güvenilir biçimde durdurmuyor."),
        "kapi_izleri": ("Dış kapıdaki çizikler", "ECHO dış güvenlik kapısında çizikler içeriden dışarı doğru. Deniz'in ayakkabısına benzeyen bir taban izi."),
        "b3_plan": ("B3 bakım girişi", "9 Kasım tarihli gizli B3 bakım girişi. Eski mekanik mandal enerji kesilse de çalışmalı."),
        "katlar": ("ECHO katları", "B1 yönetim (beyaz), B2 araştırma (mavi, cam), B3 bakım (sarı), Ara Kat D karantina (kırmızı), Z0 merkez (karanlık)."),
        "tufek_dolabi": ("Güvenlik dolabı", "Güvenlik holünde merkezî kilitli bir dolapta sıradan bir tüfek var. Merkez kilitleri açılmadan alınamaz."),
        "bastirma_hatti": ("Acil rezonans bastırma hattı", "'ACİL REZONANS BASTIRMA — MANUEL TEST HATTI.' Devre dışı, ama acil beslemesi ayrı. Hakan: 'Güvenilir değil diye çıkardılar.'"),
        "nobetci": ("NÖBETÇİ", "Sesle avlanan büyük YANKI. Ağır; dar alanda yavaş dönüyor. Mekanik gürültü onun kulağını örtüyor."),
        "beyaz_koridor": ("Hakan'ın uyarısı", "'Işıklar söndüğünde işaret çizgilerini izleyin. Beyaz koridor sizi yanıltır.'"),
        "hakan_ailesi": ("BABAM, ANNEM VE BEN", "Hakan'ın on iki yaşındaki kızının çizimi. 'Boyumu biraz abartmış. Sabah götürecektim.'"),
        "d14_otomatik": ("D-14 karantinası", "Biyolojik tehdit algılandığında kapılar insan onayı beklemeden kapanıyor."),
        "hoparlor_yanki": ("Hoparlör ve YANKI", "Hoparlör kapatılınca elektronik ses susar. Susmayan ses YANKI'dır."),
        "kirpinti": ("KIRPINTI", "Küçük, kör, sese duyarlı. Normal mermiyle durdurulabilir ama mermi az. Fırlatılan bir nesne dikkatini dağıtır."),
        "gozlemci": ("Gözlemci etkisi", "Camın ardındaki siluet, ben başımı çevirdikten bir an sonra çevirdi. Taklit gecikmeli hareket ediyor."),
        "denek": ("Denek 14 ve Denek 16", "2024 tarihli deneyler. Deniz değil; ama bunu yıllardır yapıyorlar."),
        "pervane": ("Bakım pervanesi", "Pervanenin gürültüsü Kırpıntı'ların dikkatini çekiyor."),
        "rezonans_proto": ("Rezonans Kesici prototipleri", "2024 prototipleri. İki test başarılı, üçüncünün sonucu yok."),
        "z0_yetki": ("Z0 yetkisi", "Z0 tüm kulelerden veri alıyor ama ayrı bir kule değil. Erişim yalnızca yönetimde."),
        "kademeli": ("Kademeli ayırma", "'Beş nokta aynı anda sustuğunda, kapı açık kalır.' Kuleler tek tek ayrılmalı."),
        "iki_kemal": ("İki Kemal", "Kapının ardından iki Kemal sesi. Biri hafif gecikmeyle tekrar ediyor. Sese değil harekete bak."),
        "uc_atis": ("Üç atış", "Üç Rezonans Kesici mermi; yalnızca Mert'in tabancasına uygun. Büyük YANKI'da rezonansı saniyelerce bozar. Son çare."),
    }

    ## Kanıtlar: id -> (başlık, metin) — finalde yetkililere teslim edilir
    EVIDENCE = {
        "deniz_ses": ("Dış mikrofon kaydı", "6 Kasım: Deniz'in gerçek sesi ve hemen ardından aynı tonla yapılmış ikinci çağrı."),
        "red_notu": ("A. VOSS — ÖNERİ REDDEDİLDİ", "Kemal'in deneyi durdurma önerisine Voss'un ret kaydı."),
        "s17": ("S-17 olay izi", "6 Kasım 22.44: S-17 servis kapısı içeriden açıldı."),
        "k2": ("K-2 görev kaydı", "22.42 K-2 eski servis yoluna yönlendirildi; 22.46 bağlantı sustu."),
        "d14_kayit": ("D-14 karantina kaydı", "10 Kasım 18.03: otomatik biyolojik tehdit algılaması ve karantina."),
        "voss_komut": ("Yönetim komutu 04.17", "A. VOSS — YÖNETİM OTURUMU / KOMUT 04.17 / ERİŞİM: B1. ECHO-3 aşırı yüklendi."),
    }

    def add_note(nid):
        if nid not in notes:
            notes.append(nid)
            renpy.notify("Deftere eklendi: " + JOURNAL[nid][0] + "   ·   J")
            renpy.sound.play("audio/sfx/notify.ogg", channel="audio")

    def add_evidence(eid):
        if eid not in kanit:
            kanit.append(eid)
            renpy.notify("Kanıt: " + EVIDENCE[eid][0])
            renpy.sound.play("audio/sfx/notify.ogg", channel="audio")

    def stress(n):
        global gerginlik
        if n > 0 and store.zorluk == "hikaye":
            n = max(1, n // 2)
        elif n > 0 and store.zorluk == "kabus":
            n = int(n * 1.5)
        gerginlik = max(0, min(100, gerginlik + n))
        update_pulse()

    def drain_pil(n):
        global pil
        pil = max(0, pil - n)

    def use_bullet():
        """Bir normal mermi harcar. Mermi yoksa False döner."""
        global mermi
        if mermi <= 0:
            return False
        mermi -= 1
        return True

    def setup_for(n):
        """Bölüm Seç ile ortadan başlarken o bölüme uygun kaynakları kurar."""
        global pil, mermi, rezonans, rezonans_alindi, ilkyardim, show_hud, chapter_cursor, notes, kanit
        chapter_cursor = n
        if n >= 7:
            mermi = 6
            ilkyardim = 1
        if n >= 8:
            store.sise = 2
            store.yedek_pil = 1
            store.kaydedici = 1
        if n >= 8:
            show_hud = True
        if n >= 11:
            mermi = 5
            pil = 80
        if n >= 15:
            pil = 60
        if n >= 18:
            rezonans = 3
            rezonans_alindi = True
        # Önceki bölümlerin temel ipuçlarını deftere ekle (bildirim göstermeden)
        order = list(JOURNAL.keys())
        cut = {1: 0, 2: 4, 3: 6, 4: 9, 5: 11, 6: 13, 7: 15, 8: 16, 9: 20, 10: 22, 11: 23, 12: 25, 13: 27, 14: 30, 15: 30, 16: 30, 17: 32, 18: 33}
        notes = order[:cut.get(n, 0)]
        ev = list(EVIDENCE.keys())
        ecut = {11: 0, 12: 1, 13: 2, 14: 4, 15: 5, 16: 5, 17: 6, 18: 6}
        kanit = ev[:ecut.get(n, 0)] if n >= 11 else []
