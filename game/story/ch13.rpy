## BÖLÜM 13 — DERİNLİK

label ch13:
    call chapter_intro(13)

    ## 1. Dar hat --------------------------------------------------------------
    scene bg drain with long_fade
    $ amb("b3")
    show mert at sil_left with dissolve
    narrator "B2'nin drenaj ve bakım geçitleri. Su dizlere kadar. Tavan baş hizasında."
    m "Bu hat insan için yapılmamış."
    $ drain_pil(8)
    $ sfx("kirpinti")
    narrator "Aşağıda, bir ızgaranın altında tıkırtılar. Üç, belki dört Kırpıntı."
    m "Kırpıntı aşağıda. Kabloyu sarsarsam duyacak."
    narrator "Haritada bir bakım pervanesi işaretli. Çalıştırılırsa gürültüsü her şeyi kendine çeker."
    m "Yem. Pervane bir yem olabilir."
    call explore("drenaj")
    $ add_note("pervane")

    ## 2. S-17'nin iki tarafı --------------------------------------------------
    scene bg b2_archive with dissolve
    show mert at sil_left with dissolve
    narrator "Servis arşivi. Duvarda S-17 servis kapısının mekanik bir maketi."
    m "S-17'nin dış çağrı düğmesi var. İç açma kolu da."
    narrator "Yedek olay kaydı. 6 Kasım, 22.44:"
    centered "{color=#c8a24a}S-17 — YEREL KİLİT ÇÖZÜLDÜ (İÇ TARAF){/color}"
    m "Altı Kasım'da kapı içeriden açılmış."
    m "Deniz tek başına girmemiş olabilir."
    $ add_evidence("s17")
    m "Kapının dışından çağrı yapılmış, içeriden sürgü kaldırılmış."
    m "Birisi Deniz'in geldiğini biliyordu."
    m "Ama kapıyı açan kişi onu kurtarmaya mı çalıştı, teslim mi etti?"

    ## 3. K-2 izi --------------------------------------------------------------
    narrator "Güvenlik birimlerinin görev kayıtları dağınık. Üç satır, sırası karışık:"
    narrator "• K-2 bağlantısı sustu.\n• S-17 içeriden açıldı.\n• K-2 eski servis yoluna yönlendirildi."
    $ sira = []
label .zaman:
    menu:
        "İlk olay hangisi? — K-2 eski servis yoluna yönlendirildi (22.42)." if not sira:
            $ sira.append("yon")
            jump .zaman2
        "İlk olay hangisi? — S-17 içeriden açıldı (22.44)." if not sira:
            $ stress(3)
            narrator "Hayır. Kapı açılmadan önce biri dışarı gitmiş olmalı."
            jump .zaman
        "İlk olay hangisi? — K-2 bağlantısı sustu (22.46)." if not sira:
            $ stress(3)
            narrator "Hayır. Sustuysa önce bir yere gönderilmiş olmalı."
            jump .zaman
label .zaman2:
    menu:
        "Sonra? — S-17 içeriden açıldı (22.44).":
            pass
        "Sonra? — K-2 bağlantısı sustu (22.46).":
            $ stress(3)
            narrator "Saatlere tekrar bak. 22.44, 22.46'dan önce gelir."
            jump .zaman2

    narrator "22.42: K-2 yola çıkar. 22.44: S-17 içeriden açılır. 22.46: K-2 susar."
    m "K-2 görevlendirilmiş… sonra iletişim kesilmiş."
    m "Kimdi K-2? Deniz'i neden aldı?"
    narrator "K-2'nin Deniz'i yakaladığı ya da kurtardığı henüz kanıtlanmıyor."
    $ add_evidence("k2")
    m "Bunu Kemal'e soracağım."

    ## 4. Başarısız mühimmat ---------------------------------------------------
    narrator "Arşivin dibinde mühürlü bir kasa. İçinde boş mermi yatakları ve bir rapor."
    centered "{color=#9080ff}REZONANS KESİCİ — PROTOTİP (2024){/color}"
    m "Rezonans Kesici… prototip."
    m "İki test başarılı, üçüncünün sonucu yok."
    narrator "Rapor, büyük YANKI'lara normal kurşunun neden işlemediğini kısmen açıklıyor. Gövdelerini bir arada tutan şey bir rezonans. Onu bozmadan mermi geçmiyor."
    narrator "Kasa boş. Çalışan mermiler başka bir yerde."
    m "Bir çözüm değil. Belki bir şans."
    $ add_note("rezonans_proto")

    ## 5. Merkez yetkisi -------------------------------------------------------
    narrator "Erişim kayıtlarında Z0 adı geçiyor. Bütün kulelerden veri alan, ama kendisi bir kule olmayan merkez."
    m "Z0 erişimi yalnızca yönetimde."
    m "Demek cevaplar en aşağıda."
    $ add_note("z0_yetki")
    m "Aras'ı almadan inmiyorum."
    call pil_check
    return

default sira = []
