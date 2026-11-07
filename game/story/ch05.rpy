## BÖLÜM 05 — YANLIŞ SES

label ch05:
    call chapter_intro(5)

    ## 1. Döngü ----------------------------------------------------------------
    scene bg forest_loop with long_fade
    $ amb("forest_night")
    show mert at sil_left
    show aras at sil_right
    with dissolve
    narrator "Ormanda yollar birbirine benziyor. Ama bu farklı."
    narrator "Yıldırım çarpmış, yere devrilmiş bir ağaç. İkinci kez önlerine çıkıyor."
    m "Bu ağacı az önce geçtik."
    a "Çizik aynı. Ama pusula başka yön gösteriyor."
    m "Yol mu değişti?"
    a "Belki algımız. İzi takip et."
    a "Taşa üç çizik attım. Yine buraya gelirsek döndüğümüzü anlayacağız."
    m "Ya çizikler de değişirse?"
    a "O zaman kendi hafızamıza değil, birlikte gördüğümüz şeye tutunacağız."

    $ dongu = 0
label .dongu:
    narrator "Önlerinde üç yol ayrımı var. Neyi izleyeceksin?"
    menu:
        "Ağaçların arasından gelen fısıltıyı.":
            $ dongu += 1
            $ stress(8)
            $ sfx("whisper")
            narrator "Fısıltı yaklaştıkça geri çekiliyor. On dakika yürürler."
            scene bg forest_loop with dissolve
            show mert at sil_left
            show aras at sil_right
            narrator "Devrik ağaç yine önlerinde. Taşta üç çizik."
            jump .dongu
        "Pusulanın gösterdiği kuzeyi.":
            $ dongu += 1
            $ stress(5)
            narrator "İbre bir an kuzeyi gösterir, sonra yavaşça döner. Yine de yürürler."
            scene bg forest_loop with dissolve
            show mert at sil_left
            show aras at sil_right
            narrator "Devrik ağaç. Üç çizik. Aras dişlerini sıkar."
            jump .dongu
        "Çamurdaki izleri ve zeminin eğimini.":
            narrator "Mert yere eğilir. Su hep aşağı akar. Yağmur sonrası çamur, servis araçlarının lastik izlerini tutmuş."
            narrator "Eğimi takip ederler. Bu kez ağaç arkalarında kalır. Ve geri gelmez."
            if dongu == 0:
                a "İlk denemede. Duyduğuna değil, gördüğüne güvendin."

    $ add_note("isitmek")
    narrator "Bu bir ışınlanma değil. Yanlış algılanan yol ayrımları, kısa döngüler. BOŞLUK denen şeyin etkisi."

    ## 2. İki rota -------------------------------------------------------------
    scene bg forest_fog with long_fade
    show mert at sil_left
    show aras at sil_right
    with dissolve
    $ sfx("echo_voice")
    dz_fake "Abi, acele et!"
    m "Kısa yol sesin geldiği tarafta."
    a "Uzun yolun taş işaretleri sağlam. Seçim senin."
    m "Sesi duyuyorum diye doğru olduğuna inanmam gerekmiyor."

    menu:
        "Kısa yol: açık ama sesin geldiği taraf. Gizlenerek ilerle.":
            $ rota5 = "kisa"
            jump .kisa
        "Uzun yol: taşlık ve sessiz. Daha güvenli ama yorucu.":
            $ rota5 = "uzun"
            jump .uzun

label .kisa:
    call tip("qte", "Zamanlı seçim", "Kırmızı çubuklu seçimlerde süre sınırlıdır. Süre biterse karar senin yerine verilir; çoğu zaman iyi bir karar olmaz.")
    narrator "Patika açık. Ağaçlar seyrek. Sis yerden diz boyu yükseliyor."
    $ sfx("crawl")
    narrator "Sağdan, çalıların arasından bir şey yaklaşıyor. Hızlı. Çok ayaklı bir şeyin tıkırtısı."
    call screen qte("Bir şey yaklaşıyor!", [("Yere çök ve kıpırdama", "cok"), ("Feneri yak, ne olduğunu gör", "fener"), ("Koş", "kos")], 4.0, "donakal")
    if _return == "cok":
        narrator "Mert Aras'ı da kolundan çekip yere çöker. Nefeslerini tutarlar."
        narrator "Tıkırtı bir metre ötelerinden geçer. Durur. Sonra uzaklaşır."
    elif _return == "fener":
        $ stress(12)
        $ flash("#ffffff")
        narrator "Işık sisin içinde bir duvar gibi yanar. Hiçbir şey göremezler; ama bir şey onları görür."
        $ sfx("growl")
        a "Söndür! Söndür onu!"
        narrator "Karanlıkta, kıpırdamadan beklerler. Uzun bir süre sonra tıkırtı uzaklaşır."
    elif _return == "kos":
        $ stress(15)
        $ sfx("footsteps")
        narrator "Koşarlar. Arkalarındaki tıkırtı da hızlanır. Bir dere yatağına atlayıp suyun sesine saklanırlar."
        $ jolt()
    else:
        $ stress(10)
        narrator "Mert donakalır. Neyse ki Aras onu yere çeker."
        narrator "Tıkırtı yanlarından geçer, uzaklaşır."
    jump .rota_sonu

label .uzun:
    narrator "Taşlık yol kalçaları yakan bir yokuşla başlıyor. Her adımda kayalar ayaklarının altında kayıyor."
    narrator "Yavaş ilerliyorlar. Ama kimse onları duymuyor."
    $ stress(-5)
    a "Yarım saat kaybettik."
    m "Yarım saat. Deniz için ne demek bilmiyorum."
    jump .rota_sonu

label .rota_sonu:
    ## 3. Kişisel sınav --------------------------------------------------------
    scene bg forest_night with dissolve
    show mert at sil_left
    show aras at sil_right
    m "Deniz beni beklerken ben burada hesap yapıyorum."
    a "Onu bulmak için hayatta kalmaya çalışıyorsun."
    m "Ya geç kaldıysam?"
    a "Bunu henüz bilmiyoruz."

    $ sfx("echo_voice")
    k_baba_fake "Aras. Buraya gelme."
    show aras at sil_right, shake_loop
    narrator "Aras donar. Bu ses, telefonda yıllardır duyduğu ses."
    a "Baba?"
    narrator "Aras bir adım atar. Sesin geldiği karanlığa doğru."

    menu:
        "Aras'ı kolundan tut.":
            m "Aras. Bana bak."
            show aras at sil_right
            a "…"
            a "Gerçekten oysa bile beni burada beklemezdi."
            m "Hadi. Kabloyu takip edelim."
        "Bir şey deme. Kendi kararını versin.":
            narrator "Mert konuşmaz. Yalnızca bekler. Aras'ın omuzları yavaşça iner."
            show aras at sil_right
            a "Gerçekten oysa bile beni burada beklemezdi."
            a "Teşekkürler. Durdurmadığın için."

    narrator "İkili sesin yönünü değil, bakım kablosunu takip eder."

    ## 4. Çıkış ----------------------------------------------------------------
    scene bg service_road with long_fade
    show mert at sil_left
    show aras at sil_right
    with dissolve
    a "Bak, yol tekrar açıldı."
    m "Az önce ne yaşadık?"
    a "Defterdeki cümleyi: İşitmek, anlamak değildir."
    narrator "Ormanın sonunda eski servis yolu. Çamurda yeni lastik izleri."
    $ add_note("lastik_izi")
    m "Deniz kaybolduktan sonra da birileri buraya gelmiş."
    narrator "Uzakta bir aracın farları söner. Sonra yeniden yanar."
    return
