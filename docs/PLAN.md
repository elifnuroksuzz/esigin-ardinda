# EŞİĞİN ARDINDA — Geliştirme Planı

Bu doküman, `docs/hikaye_kaynak.md` dosyasındaki 18 bölümlük hikâyenin
oynanabilir bir Ren'Py görsel romanına dönüştürülme planıdır. Plan dört katmanlıdır:
**ürün kararı → mimari → içerik/oynanış → yol haritası.**

---

## 1. Ürün kararı

| Soru | Karar | Gerekçe |
|---|---|---|
| Tür | Korku/gizem görsel roman (VN) + hafif bulmaca ve kaynak yönetimi | Hikâye diyalog ağırlıklı, tek gece, sahne akışlı. |
| Motor | **Ren'Py 8.5** | Ücretsiz, Python tabanlı, VN için birebir. PC/Mac/Linux/Web/Android çıktısı tek komut. |
| Dil | Türkçe (tüm arayüz ve metin) | Kaynak metin Türkçe. DejaVu Sans font Türkçe karakterleri destekler. |
| Görsel yaklaşım | Prosedürel atmosferik arka planlar + **silüet** karakterler | "Yüz göstermeyen" korku: bilinmezlik korkuyu büyütür, AI yüz tutarsızlığı riski yok. |
| Ses yaklaşımı | Prosedürel üretilmiş ambiyans ve efektler (rüzgâr, uğultu, parazit, metal sürtünmesi, kalp atışı) | Korkuda sesin payı %50. Lisans riski sıfır. Sonradan freesound.org ile değiştirilebilir. |
| Kapsam (v1.0) | 18 bölümün tamamı, baştan sona oynanır, tek kanonik son + değişken epilog satırları | Hikâye dosyası tek kanonik son belirliyor; seçimler yolu ve bedeli değiştirir, sonucu değil. |
| Dağıtım | GitHub Actions: lint + PC/Linux/Mac zip + Web build (GitHub Pages'e hazır) | Her push'ta oynanabilir paket üretilir. |

**Yanlış yön (bilerek yapılmayanlar):** Tam animasyonlu sprite, 3D, açık dünya, Unity/Godot.
Bunlar oyunu çıkarmadan aylar yer.

---

## 2. Mimari

```
esigin-ardinda/
├── game/
│   ├── options.rpy          # oyun adı, sürüm, build ayarları
│   ├── gui.rpy              # renk/yazı tipi/ölçü değişkenleri
│   ├── screens.rpy          # tüm arayüz: diyalog, seçim, menüler, kayıt, ayarlar
│   ├── core/
│   │   ├── characters.rpy   # karakter tanımları (renk + ses tonu)
│   │   ├── state.rpy        # oyun değişkenleri, envanter, kanıtlar
│   │   ├── effects.rpy      # geçişler, sarsıntı, glitch, ses kanalları
│   │   ├── systems.rpy      # zamanlı seçim (QTE), HUD, defter, bölüm kartı
│   │   └── chapters.rpy     # bölüm listesi + bölüm seçme ekranı
│   ├── story/
│   │   ├── script.rpy       # label start → 18 bölümü sırayla çağırır
│   │   └── ch01.rpy … ch18.rpy
│   ├── images/bg/*.jpg      # tools/gen_assets.py üretir
│   ├── images/char/*.png    # silüetler
│   └── audio/{amb,sfx,music}/*.ogg
├── tools/
│   ├── gen_assets.py        # arka plan, silüet ve sesleri üretir (PIL + numpy + ffmpeg)
│   └── check_story.py       # Ren'Py'sız statik kontrol: label/jump, görsel/ses dosyası, karakter
├── docs/
│   ├── PLAN.md              # bu dosya
│   └── hikaye_kaynak.md     # orijinal hikâye dosyası (kanon)
└── .github/workflows/build.yml
```

**Akış:** `start` → `ch01` … `ch18` her biri `call` ile çağrılır, bölüm sonunda `return`.
Böylece **Bölüm Seç** ekranı herhangi bir bölümü tek başına başlatabilir (oyunu test etmek
ve tekrar oynamak için). Bölüm seçimi, o bölüme gelmiş oyuncular için açılır (`persistent`).

**Renk kodlu mekânlar (kanondan):** B1 beyaz/soğuk, B2 mavi/cam, B3 sarı bakım,
Ara Kat D kırmızı karantina, Z0 karanlık merkez. Arka planlar, HUD ve ambiyans bu kodu izler.

---

## 3. Oynanış sistemleri

Kanondaki ilke: *"Her 2–3 dakikada aynı görev türünü tekrar etme. Hata kalıcı çıkmaz
değil, okunabilir bir bedel veya yeniden deneme olsun."*

| Sistem | Ne yapar | Nerede |
|---|---|---|
| **Kaynaklar (HUD)** | Fener pili %, normal mermi, Rezonans Kesici, ilk yardım | ECHO içinde sol üstte |
| **Gerginlik** | Sahte sesi takip etmek, panik kararlar gerginliği artırır; yüksek gerginlik ekranı ve metni etkiler | Tüm oyun |
| **Defter (D tuşu)** | Bulunan ipuçları ve kanıtlar; bulmacalarda ipucu | Tüm oyun |
| **Zamanlı seçim** | Geri sayım çubuklu karar; süre biterse varsayılan (genelde kötü) sonuç | Kovalamacalar, Kırpıntı, Nöbetçi |
| **Ses ayırt etme** | Gerçek sesle YANKI taklidini ayırma (tekrar eden nefes, gecikme, yön) | Bölüm 2, 3, 11, 16, 17 |
| **Mekân okuma** | Kablo izi, ayak izi, çizik, korkuluk, boru etiketi ile yön bulma | Bölüm 3, 4, 5, 16 |
| **Zaman çizelgesi** | Kayıtları doğru sıraya koyma (22.42 → 22.44 → 22.46) | Bölüm 13 |
| **Kamera yönlendirme** | 3 güzergâhtan doğrusunu seçip Aras'a yol açma; yanlışsa geri dön | Bölüm 14 |
| **İki kişilik eşzaman** | Mert ve Aras'ın hareketlerini eşlemek | Bölüm 15 |
| **Gerçek/Taklitçi** | Gecikmeyle hareket edeni bulmak | Bölüm 17 |
| **Final savunması** | Rezonans mermisi kaldıysa onu, yoksa acil bastırma hattını kullan | Bölüm 18 |
| **Kanıt teslimi** | Toplanan kanıt sayısı epilog metnini değiştirir | Bölüm 18 |

**Kanon korunur:** Deniz'in gücü yok, Hakan ölür (kurtarılamaz), Kemal yaşar ve ifade verir,
Voss kaçar, Nöbetçi finalde ölür, kredi sonrası "İkinci tesis aktif".

**Metin düzenlemesi:** Kaynak dosyada her sahnenin sonuna aynı 3 satırlık blok kopyalanmış
(ör. "Son mesajını defalarca dinledim…"). Bunlar oyunda **bölüm başına bir kez**, en doğal
yere yerleştirildi; tekrar eden metin oyuncuyu yorar.

---

## 4. Yol haritası (adım adım)

### Faz 0 — Altyapı ✅
- [x] Repo yapısı, Ren'Py proje dosyaları (options/gui/screens)
- [x] Karakterler, durum değişkenleri, efektler, sistem ekranları
- [x] Asset üretici ve statik kontrol aracı
- [x] CI: Ren'Py lint + PC/Linux/Mac/Web derlemesi

### Faz 1 — Dikey dilim ✅
- [x] Bölüm 01 baştan sona: sesli mesaj, Aras, ilk iz, karar
- [x] Ana menü, kayıt/yükle, ayarlar, defter çalışıyor

### Faz 2 — Tüm hikâye ✅
- [x] Bölüm 02–07 (yüzey: defter, kuleler, röle, orman, Sürüngen, hazırlık)
- [x] Bölüm 08–15 (ECHO: Hakan, D-14, yalnızlık, B2, arşiv, kurtarma, buluşma)
- [x] Bölüm 16–18 (Z0, Eşik, Son Geçit, epilog, kredi sonrası)

### Doğrulama ✅
- [x] Ren'Py lint: 0 hata (991 diyalog bloğu, 30 seçim)
- [x] Otomatik oynanış: rastgele seçimlerle 18 bölüm baştan sona, birden çok tur, çalışma zamanı hatası yok

### Faz 3 — Cila (senin sıradaki adımların)
- [ ] Arka planları AI/foto ile değiştir (aynı dosya adlarıyla `game/images/bg/` içine koy — kod değişmez)
- [ ] freesound.org'dan gerçek kayıtlarla sesleri güçlendir (aynı dosya adları)
- [ ] Silüetleri kendi çizimlerinle değiştir (`game/images/char/`)
- [ ] Müzik (ana tema + epilog)
- [ ] Oyun testi: her bölüm 5–10 dk mı? Tempo notları
- [ ] Android build (Ren'Py launcher → Android)
- [ ] itch.io yayını (Web build zip'i direkt yüklenebilir)

### Faz 4 — İsteğe bağlı
- [ ] İngilizce çeviri (`game/tl/english/` — Ren'Py "Generate Translations")
- [ ] Başarımlar (Hakan'ın resmini incele, hiç sahte sese kanma, tüm kanıtlar)
- [ ] "Proje Beş" devam oyunu için kanca

---

## 5. Varlık (asset) değiştirme rehberi

Kod yalnızca **dosya adına** bakar. Daha iyi bir görsel bulduğunda:

1. 1280×720 boyutuna getir (Krita/Photopea).
2. Aynı adla kaydet: ör. `game/images/bg/forest_night.jpg`.
3. Oyunu yeniden başlat (Shift+R oyun içinde yeniden yükler).

Silüetler 500×700 şeffaf PNG; sesler `.ogg`. Tam liste: `python tools/gen_assets.py --list`.

---

## 6. Riskler

| Risk | Önlem |
|---|---|
| Uzun metin → tempo düşer | Diyalog dışı anlatım kısa tutuldu; her bölümde en az bir etkileşim. |
| Prosedürel görsel "ucuz" görünebilir | Hepsi değiştirilebilir; karanlık palet + vinyet + sis tutarlılık sağlar. |
| Kanon tutarsızlığı | `docs/hikaye_kaynak.md` "Kesin süreklilik" bölümü referans; isimler sabit. |
| Kayıt uyumluluğu | Değişkenler `default` ile tanımlı; yeni sürümler eski kayıtları bozmaz. |
