## KEŞİF HARİTALARI ###########################################################
##
## Her harita farklı bir strateji sorusu sorar:
##   kule     (Bölüm 3)  — öğretici: ara, iz topla. Tehdit yok.
##   orman    (Bölüm 5)  — kısa ve riskli mi, uzun ve güvenli mi?
##   servis   (Bölüm 6)  — ışığa yönelen hızlı avcıdan dar geçitle kaç.
##   b3       (Bölüm 8)  — pres gürültüsünü zamanla, Nöbetçi'yi havalandırmayla atlat.
##   gecis    (Bölüm 11) — iki Kırpıntı, şişe mi mermi mi?
##   drenaj   (Bölüm 13) — pervaneyle yem kur, üç Kırpıntı'nın arasından süzül.
##   tahliye  (Bölüm 18) — sedyeyle koşamazsın; sürgüleri kapatarak kaç.
##
## Oda alanları:
##   name, pos (ekran koordinatı), desc
##   hide=True            saklanma noktası
##   mask="machine"       çift turlarda gürültüyü örter; "always" her zaman
##   loot="pil|sise|ilkyardim|mermi|kaydedici"   Ara ile bulunur
##   clue=(bayrak, metin)  Ara ile bulunur, gereksinim olabilir
##   event="label"        ilk girişte hikâye sahnesi; sets="bayrak"
##   use=dict(type="lure"|"block", label=..., ...)
## Bağlantı: (a, b) ya da (a, b, "vent") — havalandırma, Nöbetçi/Sürüngen giremez.

init -1 python:

    MAPS = {}

    ## ------------------------------------------------------------------ KULE
    MAPS["kule"] = dict(
        title="BİRİNCİ KULE",
        goal_text="Kulenin çevresini incele. En az iki iz bul, sonra kule tabanına git.",
        theme="#8fb0c8", bg="tower", amb="tower_hum", par=9,
        start="yol", goal="kule",
        require=["tel", "iz", "kablo"], require_count=2,
        require_log="Önce çevreyi incelemelisin. ARA ile iz bul.",
        win_note="kule_izleri",
        intro_log="Kule tepede, uğulduyor. Önce çevresine bak.",
        rooms={
            "yol": dict(name="Servis yolu", pos=(170, 520), desc="Çamurlu toprak yol. Geldiğiniz araç burada."),
            "cit": dict(name="Tel örgü", pos=(360, 400), desc="Paslı bir çit kuleyi çevreliyor.",
                        clue=("tel", "Tel örgü kesilmiş, sonra özensizce geri bükülmüş. Kesik uçlar paslanmamış.")),
            "camur": dict(name="Çamurlu patika", pos=(360, 600), desc="Yağmur sonrası çamur her izi tutuyor.",
                          clue=("iz", "İş botu izleri. İki kişi. En fazla birkaç günlük.")),
            "sirt": dict(name="Sırt", pos=(570, 500), desc="Kasabanın ışıkları aşağıda. Rüzgâr sert."),
            "kapak": dict(name="Bakım kapağı", pos=(570, 300), desc="Kulenin dibinde ağır bir metal kapak.",
                          clue=("kablo", "Kapağın ardındaki zırhlı kablo toprağa iniyor. Tozu yeni silinmiş.")),
            "kulube": dict(name="Eski kulübe", pos=(790, 560), desc="Çatısı çökmüş bir bekçi kulübesi.", loot="sise"),
            "kule": dict(name="Kule tabanı", pos=(790, 260), desc="Metal gövdeden düşük bir uğultu geliyor."),
        },
        links=[("yol", "cit"), ("yol", "camur"), ("cit", "kapak"), ("cit", "sirt"), ("camur", "sirt"),
               ("sirt", "kapak"), ("kapak", "kule"), ("sirt", "kulube"), ("kulube", "kule")],
        threats=[],
    )

    ## ----------------------------------------------------------------- ORMAN
    MAPS["orman"] = dict(
        title="YANLIŞ SES",
        goal_text="Servis yoluna ulaş. Kısa yol açık ama bir şey orada dolaşıyor.",
        theme="#8fae8a", bg="forest_fog", amb="forest_night", par=7,
        start="ayrim", goal="servis",
        intro_log="Deniz'in sesi açıklık tarafından geliyor. Ona güvenme.",
        rooms={
            "ayrim": dict(name="Yol ayrımı", pos=(160, 380), desc="Taşa attığınız üç çizik burada."),
            "aciklik": dict(name="Açıklık", pos=(380, 240), desc="Ağaçlar seyrek. Saklanacak yer yok."),
            "sis": dict(name="Sisli patika", pos=(610, 220), desc="Sis diz boyu. Tıkırtılar buradan geliyordu."),
            "agac": dict(name="Devrik ağaç", pos=(500, 400), desc="Yıldırım çarpmış gövdenin altı oyuk.", hide=True),
            "kayalik": dict(name="Taşlık", pos=(330, 540), desc="Kayalar ayağının altında kayıyor.", loot="sise"),
            "yamac": dict(name="Yamaç", pos=(560, 600), desc="Dik ve yorucu, ama kimse yok."),
            "dere": dict(name="Dere yatağı", pos=(760, 560), desc="Suyun sesi adımlarını örtüyor.", mask="always"),
            "servis": dict(name="Servis yolu", pos=(820, 360), desc="Çamurda yeni lastik izleri."),
        },
        links=[("ayrim", "aciklik"), ("aciklik", "sis"), ("sis", "servis"), ("ayrim", "kayalik"),
               ("kayalik", "yamac"), ("yamac", "dere"), ("dere", "servis"), ("aciklik", "agac"),
               ("agac", "yamac"), ("agac", "sis")],
        threats=[dict(type="kirpinti", start="sis", patrol=["sis", "agac", "aciklik", "agac"])],
    )

    ## ---------------------------------------------------------------- SERVİS
    MAPS["servis"] = dict(
        title="SÜRÜNGEN",
        goal_text="ECHO'nun dış kapısına ulaş. Sürüngen çok hızlı ve ışığa yönelir.",
        theme="#a8b4c0", bg="road_car", amb="wind", par=6,
        start="araba", goal="kapi",
        intro_log="Araçtan sürünerek çıktın. Yaratık ağaçlıkta.",
        rooms={
            "araba": dict(name="Araba", pos=(160, 300), desc="Tavanı göçmüş. Burada kalamazsın."),
            "hendek": dict(name="Hendek", pos=(360, 180), desc="Yol kenarı, dizlere kadar su."),
            "duvar": dict(name="Taş duvar", pos=(360, 440), desc="Duvarın gölgesi geniş.", hide=True),
            "orman": dict(name="Ağaçlık", pos=(580, 300), desc="Dallar arasında bir şey tırmanıyor olabilir.", loot="sise"),
            "kaya": dict(name="Kaya yarığı", pos=(580, 560), desc="İki kaya arası dar boşluk. Büyük bir gövde giremez."),
            "viraj": dict(name="Yol virajı", pos=(780, 180), desc="Açık alan. Farların ışığı burada bitiyor."),
            "kapi": dict(name="ECHO dış kapısı", pos=(800, 440), desc="Beton duvara gömülü ağır kapı."),
        },
        links=[("araba", "hendek"), ("araba", "duvar"), ("hendek", "orman"), ("duvar", "orman"),
               ("duvar", "kaya", "vent"), ("kaya", "kapi", "vent"), ("orman", "viraj"), ("viraj", "kapi")],
        threats=[dict(type="surungen", start="orman", patrol=["orman", "duvar", "hendek", "orman", "viraj"])],
    )

    ## -------------------------------------------------------------------- B3
    MAPS["b3"] = dict(
        title="B3 BAKIM KATI",
        goal_text="Güvenlik ofisine ulaş. Nöbetçi sesle avlanır; pres hattı gürültünü örter.",
        theme="#d4ae55", bg="b3_dark", amb="b3", par=9,
        start="giris", goal="ofis",
        require=["guvenlik"], require_log="Ofise gitmeden önce güvenlik holüne bakmalısın.",
        intro_log="Uzakta ağır bir sürtünme. Bir şey metal zeminde yürüyor.",
        rooms={
            "giris": dict(name="B3 girişi", pos=(150, 360), desc="Arkanızda kapanan bakım kapısı."),
            "koridor": dict(name="Sarı koridor", pos=(340, 360), desc="Zeminde sarı servis çizgisi."),
            "pres": dict(name="Pres hattı", pos=(520, 220), desc="Hidrolik pres çift turlarda gürler; o anlarda sesin duyulmaz.", mask="machine"),
            "guvenlik": dict(name="Güvenlik holü", pos=(720, 200), desc="Dolaplar, kilitli bir tüfek, eski bir panel.",
                             event="ev_b3_guvenlik", sets="guvenlik"),
            "kazan": dict(name="Kazan dairesi", pos=(520, 500), desc="Sıcak, karanlık, buharlı.", loot="pil"),
            "havalandirma": dict(name="Havalandırma", pos=(330, 580), desc="Dar bir boru. Büyük bir gövde buraya giremez."),
            "depo": dict(name="Malzeme deposu", pos=(720, 560), desc="Rafların arkasında boşluk var.", hide=True, loot="sise"),
            "ofis": dict(name="Güvenlik ofisi", pos=(860, 380), desc="Işık yanıyor. Biri burada."),
        },
        links=[("giris", "koridor"), ("koridor", "pres"), ("koridor", "kazan"), ("pres", "guvenlik"),
               ("kazan", "depo"), ("depo", "ofis"), ("guvenlik", "ofis"),
               ("giris", "havalandirma", "vent"), ("havalandirma", "kazan", "vent"), ("havalandirma", "depo", "vent")],
        threats=[dict(type="nobetci", start="pres", patrol=["pres", "guvenlik", "pres", "koridor", "kazan", "koridor"])],
    )

    ## ----------------------------------------------------------------- GEÇİŞ
    MAPS["gecis"] = dict(
        title="YALNIZLIK",
        goal_text="Kontrol odasındaki ses arşivine ulaş, sonra B2 kapısına geç. İki Kırpıntı dolaşıyor.",
        theme="#d4ae55", bg="b3_dark", amb="b3", par=12,
        start="baslangic", goal="b2kapi",
        require=["ses_izi"], require_log="Önce kontrol odasındaki dış mikrofon arşivine bakmalısın.",
        intro_log="Aras'ın sesi kesildi. Yalnızsın.",
        rooms={
            "baslangic": dict(name="Arka koridor", pos=(150, 330), desc="Işıkların yarısı sönük."),
            "hoparlor": dict(name="Hoparlör koridoru", pos=(330, 190), desc="Tavanda bir ECHO hoparlörü.", event="ev_hoparlor"),
            "karanlik": dict(name="Karanlık koridor", pos=(330, 480), desc="Fenerin ışığı burada kısa kalıyor."),
            "borular": dict(name="Boru yığını", pos=(530, 330), desc="Boruların arasında bir insan sığacak boşluk.", hide=True),
            "atolye": dict(name="Atölye", pos=(520, 610), desc="Alet tezgâhları, devrik sandalyeler.", loot="sise"),
            "kontrol": dict(name="Kontrol odası", pos=(720, 190), desc="Bir ekran hâlâ açık: DIŞ MİKROFON ARŞİVİ.",
                            event="ev_ses_izi", sets="ses_izi"),
            "depo2": dict(name="Soğuk depo", pos=(720, 520), desc="Raflarda tıbbi malzeme.", loot="ilkyardim"),
            "b2kapi": dict(name="B2 kapısı", pos=(860, 360), desc="Ardında mavi, soğuk bir ışık."),
        },
        links=[("baslangic", "hoparlor"), ("baslangic", "karanlik"), ("hoparlor", "borular"),
               ("karanlik", "borular"), ("karanlik", "atolye"), ("atolye", "depo2"), ("borular", "kontrol"),
               ("borular", "depo2"), ("kontrol", "b2kapi"), ("depo2", "b2kapi")],
        threats=[dict(type="kirpinti", start="atolye", patrol=["atolye", "karanlik", "atolye", "depo2"]),
                 dict(type="kirpinti", start="kontrol", patrol=["kontrol", "borular", "kontrol", "b2kapi"])],
    )

    ## ---------------------------------------------------------------- DRENAJ
    MAPS["drenaj"] = dict(
        title="DERİNLİK",
        goal_text="B2 servis arşivine ulaş. Pervane, Kırpıntı'ları kendine çeken bir yem olabilir.",
        theme="#6ab4b0", bg="drain", amb="b3", par=10,
        start="kapak", goal="arsiv",
        intro_log="Su dizlerine kadar. Izgaranın altında tıkırtılar.",
        rooms={
            "kapak": dict(name="Drenaj kapağı", pos=(150, 260), desc="Yukarısı B2. Aşağısı karanlık."),
            "kanal1": dict(name="Ana kanal", pos=(340, 260), desc="Su akıntısı bacaklarını itiyor.", loot="sise"),
            "pervane": dict(name="Pervane odası", pos=(540, 140), desc="Paslı bir bakım pervanesi ve şalteri.",
                            use=dict(type="lure", label="Pervane", turns=4, log="Pervane homurdanarak döndü. Tıkırtılar sese yöneliyor.")),
            "izgara": dict(name="Izgara", pos=(340, 520), desc="Altında bir şeyler kıpırdıyor.", loot="mermi"),
            "toplama": dict(name="Su toplama", pos=(540, 380), desc="Geniş havuz. Sesler yankılanıyor."),
            "sifon": dict(name="Sifon", pos=(540, 610), desc="Bir borunun içine sığabilirsin.", hide=True),
            "boru": dict(name="Dar boru", pos=(740, 240), desc="Emeklemek zorundasın."),
            "arsiv": dict(name="Servis arşivi", pos=(820, 480), desc="Kuru zemin. Raflar. S-17'nin maketi."),
        },
        links=[("kapak", "kanal1"), ("kapak", "izgara"), ("kanal1", "pervane"), ("kanal1", "toplama"),
               ("izgara", "toplama"), ("izgara", "sifon"), ("toplama", "boru"), ("pervane", "boru"),
               ("sifon", "arsiv"), ("toplama", "arsiv"), ("boru", "arsiv")],
        threats=[dict(type="kirpinti", start="toplama", patrol=["toplama", "izgara", "toplama", "kanal1"]),
                 dict(type="kirpinti", start="boru", patrol=["boru", "toplama", "boru", "pervane"]),
                 dict(type="kirpinti", start="sifon", patrol=["sifon", "arsiv", "sifon", "izgara"])],
    )

    ## --------------------------------------------------------------- TAHLİYE
    MAPS["tahliye"] = dict(
        title="SON GEÇİT",
        goal_text="Kemal sedyede: koşamazsın. Nöbetçi peşinde. Sürgüleri kapatarak B3 rampasına ulaş.",
        theme="#d4ae55", bg="b3_dark", amb="b3", par=8, no_run=True,
        start="platform", goal="rampa",
        intro_log="Deniz: 'Metal üzerinde bir şey sürükleniyor.'",
        rooms={
            "kuyu": dict(name="Z0 kuyusu", pos=(160, 160), desc="Aşağıdan sürtünme sesi yükseliyor."),
            "platform": dict(name="Yük platformu", pos=(160, 420), desc="Kemal'in sedyesi burada."),
            "panelA": dict(name="Sürgü paneli A", pos=(350, 580), desc="Kuyuya açılan geçitleri kapatabilir.",
                           use=dict(type="block", label="Sürgü A", turns=5, links=[("kuyu", "platform"), ("kuyu", "koridor")],
                                    log="Ağır sürgüler kuyunun önüne indi.")),
            "koridor": dict(name="Servis koridoru", pos=(380, 290), desc="Sedye tekerlekleri burada gıcırdıyor."),
            "pres2": dict(name="Pres hattı", pos=(590, 230), desc="Pres çift turlarda gürler.", mask="machine"),
            "atolye2": dict(name="Atölye", pos=(590, 520), desc="Devrilmiş tezgâhlar.", loot="ilkyardim"),
            "panelB": dict(name="Sürgü paneli B", pos=(760, 380), desc="Rampaya giden son kapı.",
                           use=dict(type="block", label="Sürgü B", turns=5, links=[("pres2", "panelB"), ("atolye2", "panelB")],
                                    log="Arkanızdaki iki geçit de kapandı.")),
            "rampa": dict(name="B3 servis rampası", pos=(880, 560), desc="Yukarıda gün ışığı."),
        },
        links=[("kuyu", "platform"), ("kuyu", "koridor"), ("platform", "koridor"), ("platform", "panelA"),
               ("panelA", "atolye2"), ("koridor", "pres2"), ("pres2", "panelB"), ("atolye2", "panelB"),
               ("panelB", "rampa")],
        threats=[dict(type="nobetci", start="kuyu", hunt="platform", chase=True)],
    )
