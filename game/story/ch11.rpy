## BÖLÜM 11 — YALNIZLIK

label ch11:
    call chapter_intro(11)

    ## 1. Kendi sesi -----------------------------------------------------------
    scene bg b3_dark with long_fade
    $ amb("b3")
    show mert at sil_center with dissolve
    narrator "B3'ün arka koridorları. Işıkların yarısı sönük. Fener ışığı duvarlarda titriyor."
    $ drain_pil(6)
    $ sfx("kirpinti")
    narrator "Metal zeminde tıkırtılar. Küçük, soluk, gözsüz bir şey bir boru yığınının altından çıkıp karanlığa karışıyor."
    show kirpinti at creature_floor
    kirp "(Metal üzerinde tıkırtı.)"
    m "{size=-4}Kör. Sese geliyor. Bir tane daha var… belki daha fazla.{/size}"
    hide kirpinti with dissolve
    $ add_note("kirpinti")
    narrator "Tabancada [mermi] mermi var. Her atış koridorlarda yankılanır. Bir şişe çok daha sessiz bir silahtır."
    call explore("gecis")
    scene bg b3_corridor with dissolve
    show mert at sil_center with dissolve
    narrator "Silah sınırsız üstünlük sağlamıyor. Büyük YANKI'lara karşı ise hiç güvenilir değil."

    ## 4. Aras'a söz -----------------------------------------------------------
    $ sfx("radio")
    narrator "Mert bozuk telsizi açar."
    m_tel "Aras, beni duyuyorsan… vazgeçmedim."
    $ sfx("static")
    a_tel "{size=-6}…buradayım…{/size}"
    m_tel "Dayan. Geliyorum."
    narrator "Aras'ın öldüğüne dair bir kanıt yok. Bu yeter."
    narrator "Bir sonraki kapının ardında soğuk, mavi ışıklı araştırma katı uzanıyor."
    call pil_check
    return


## Haritadaki "Hoparlör koridoru" odasına ilk girişte
label ev_hoparlor:
    scene bg b3_dark with dissolve
    show mert at sil_center with dissolve
    $ sfx("echo_voice")
    m_fake "Buraya gel."
    m "Bu benim sesim."
    $ sfx("echo_voice")
    m_fake "Buraya gel."
    narrator "Ses iki ayrı yönden geliyor. Sol koridorda tavana asılı bir ECHO hoparlörü var. Sağ koridor karanlık."
    m "Kendi sesim bana bir kapının ardından cevap veriyor."

    menu:
        "Sol koridordaki hoparlörün kablosunu çek.":
            $ sfx("static")
            narrator "Kablo çıkınca sol taraftaki ses kesilir."
        "Bekle ve iki sesi karşılaştır.":
            $ stress(5)
            narrator "İkisi de aynı cümleyi söylüyor. Ama sol taraftakinde hafif bir elektronik cızırtı var."
            narrator "Mert sonunda hoparlörün kablosunu çeker. Sol taraf susar."

    $ sfx("echo_voice")
    m_fake "Buraya gel."
    m "Hoparlörü kapattım. İkincisi hâlâ konuşuyor."
    m "Hoparlör sustu ama o susmadı. Demek burada iki ayrı şey var."
    $ add_note("hoparlor_yanki")

    menu:
        "Sağ taraftaki karanlığa, sesin geldiği yere bak.":
            $ stress(15)
            $ sahte_kanma += 1
            narrator "Mert sağa birkaç adım atar. Karanlıkta bir şey kıpırdar. Ses birden kesilir."
            $ sfx("growl")
            narrator "Geri çekilir. Kalbi kulaklarında atıyor."
            m "Aptal. Sesi duyunca gidilmez."
        "Sesi duymazdan gel ve uzaklaş.":
            narrator "Mert arkasını döner. Karanlık bir süre daha 'Buraya gel' der. Sonra susar."
    return


## Haritadaki "Kontrol odası" odasına ilk girişte
label ev_ses_izi:
    scene bg control_room with dissolve
    show mert at sil_left with dissolve
    narrator "Küçük bir kontrol odası. Ekranlardan biri hâlâ açık: DIŞ MİKROFON ARŞİVİ."
    narrator "Mert 6 Kasım gecesini bulur. 22.41."
    $ sfx("phone_beep")
    dz_kayit "Abi… eski servis yolundayım."
    m "Rüzgâr aynı. Bu, oradaki gerçek kayıt."
    narrator "Hemen ardından aynı tonla ikinci bir çağrı. Ama arkasında rüzgâr yok."
    m "Deniz gerçekten oradaydı. Ama ardından duyulan her ses ona ait değildi."
    m "Birileri seni dinlemiş, Deniz."
    $ add_evidence("deniz_ses")
    m "Deniz'in sesini duyarsam önce nereden geldiğini anlayacağım."
    return
