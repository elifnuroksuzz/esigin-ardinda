## BÖLÜM 06 — SÜRÜNGEN

label ch06:
    call chapter_intro(6)

    ## 1. Yol kesiliyor --------------------------------------------------------
    scene bg road_car with long_fade
    $ amb("wind")
    narrator "Kaan'ın arabası, servis yolunun kenarında. Farlar sisi deliyor."
    narrator "Mert ve Aras araca döner. Kapılar kapanır. Bir an, sadece motorun soğuyan metalinin tıkırtısı."
    show mert at sil_left
    show aras at sil_right
    with dissolve
    $ sfx("crawl")
    narrator "Far ışığının kenarından bir şey geçer. Uzun. Eklemleri yanlış yerlerde."
    show surungen at creature_wall
    $ sfx("sting")
    m "Arabanın üstünde bir şey var."
    a "Kapıları kilitle. Camdan uzaklaş."
    $ sfx("thud")
    $ jolt(True)
    m "Tavan çöküyor!"

    call screen qte("Tavan içeri göçüyor!", [("Motoru çalıştır, kaç", "motor"), ("Kıpırdama, sessiz kal", "sessiz"), ("Kapıyı aç, dışarı fırla", "kapi")], 4.0, "panik")
    if _return == "sessiz":
        a "Motoru çalıştırma. Sese geliyor!"
        narrator "İkisi de nefesini tutar. Tavandaki ağırlık bir yandan öbür yana kayar."
        narrator "Yaratık kaputun üzerinden yola iner. Durur. Başını, ya da baş olan şeyi, sağa sola çevirir."
    elif _return == "motor":
        $ stress(12)
        $ sfx("door_slam")
        narrator "Motor homurdanır. Tavandaki ağırlık bir anda sese doğru, ön cama atılır."
        a "Motoru çalıştırma! Sese geliyor!"
        narrator "Aras kontağı kapatır. Cam çatlar ama dayanır."
    elif _return == "kapi":
        $ stress(15)
        narrator "Mert kapı koluna uzanır. Aras onu geri çeker."
        a "Dışarıda ne olduğunu bilmiyoruz!"
    else:
        $ stress(10)
        narrator "Mert donakalır. Belki de bu, yapılacak en doğru şeydi."
        a "Motoru çalıştırma. Sese geliyor."
    hide surungen with dissolve

    narrator "Araçtan ayrılmak zorundalar. Burada kalırlarsa o şey geri gelecek."

    ## 2. Gürültü ve gölge -----------------------------------------------------
    scene bg forest_fog with dissolve
    $ amb("forest_night")
    $ bgm("chase", 0.5)
    show mert at sil_left
    show aras at sil_right
    with dissolve
    narrator "Sürünerek araçtan çıkarlar. Ağaçların arasında, bir taş duvarın gölgesine doğru."
    $ sfx("crawl")
    show surungen at creature_floor
    narrator "Arkalarında tıkırtı başlar."

    call screen qte("Peşinizde!", [("Feneri yere at, ışığı takip etsin", "fener"), ("Koş!", "kos"), ("Dar geçide gir, görüşünü kes", "gecit")], 4.0, "yakalandi")
    if _return == "fener":
        a "Feneri yere tut. Bizi değil, ışığı takip etsin."
        $ sfx("flashlight")
        narrator "Fener çalılara yuvarlanır. Yaratık ışığa atılır. İkili ters yöne süzülür."
    elif _return == "gecit":
        narrator "İki kaya arasındaki dar boşluğa sıkışırlar. Yaratığın gövdesi bu boşluğa girmez."
        narrator "Kayaları tırmalar, sonra ilgisini kaybeder."
    elif _return == "kos":
        $ stress(12)
        $ sfx("footsteps")
        a "Bilmiyorum. Koş!"
        narrator "Koşarlar. Dallar yüzlerini keser. Yaratık bir an yanlarında, bir an arkalarında."
    else:
        $ stress(18)
        $ sfx("growl")
        $ jolt(True)
        narrator "Bir şey Mert'in sırtına çarpar. Yere düşer. Aras onu kolundan tutup çeker."
        narrator "Kaya duvarının ardına yuvarlanırlar. Ceketinde üç uzun yırtık."

    hide surungen with dissolve
    m "Duvara tırmandı… nasıl tırmandı o?"
    narrator "Servis duvarının üzerinde, tesis yönüne doğru tırmanıp kaybolur. Yok olmaz. Sadece gider."
    $ add_note("surungen")
    $ bgm(None)

    ## 3. Kapıdaki iz ----------------------------------------------------------
    scene bg echo_gate with long_fade
    $ amb("wind")
    show mert at sil_left
    show aras at sil_right
    with dissolve
    narrator "Servis yolunun sonunda beton bir duvar ve gömülü, ağır bir kapı."
    m "Şu metal kapıda ECHO işareti var."
    a "Çizikler içeriden dışarı doğru."
    m "Bir şey çıkmış buradan."
    a "Ya da birileri çıkmasını engelleyememiş."
    narrator "Kapının dibinde eski kan izleri. Kırılmış bir telsiz. Çamura gömülmüş boş kovanlar ve kapıda ezik mermi izleri."
    a "Biri buna ateş etmiş. Defalarca. İşe yaramamış."
    narrator "Çamurda bir taban izi. Mert'in kalbi durur: Deniz'in spor ayakkabısına benziyor."
    m "Bu… Deniz'in olabilir."
    a "Olabilir. Ama emin olamayız."
    $ add_note("kapi_izleri")
    narrator "Kapı aktif erişim olmadan açılmıyor. Ne kol var ne kart okuyucunun ışığı."
    m "O şey bizi takip etmeyi neden bıraktı?"
    a "Metal kapının yanındaki titreşim değişti. Belki ondan kaçındı."
    m "İlk kez bir kapının arkasında ne olduğunu merak etmek istemiyorum."

    ## 4. Yeni plan ------------------------------------------------------------
    $ sfx("radio")
    bo_tel "Sesiniz kesildi! İyi misiniz?"
    m_tel "Yaşıyoruz. Eski servis kapısını bulduk."
    du_tel "Lütfen acele etmeyin."
    a "Acele etmeyeceğiz. Ama durmayacağız."
    narrator "Aras tesisin B3 bakım hattına ait eski bir giriş olabileceğini düşünür."
    narrator "İkili geri çekilir. Bu bir yenilgi değil. Bilinçli bir içeri giriş hazırlığı."
    return
