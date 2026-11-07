# EŞİĞİN ARDINDA

**Çamlık Kasabası • ECHO • YANKI**

Tek gecelik bir korku/gizem görsel romanı. 18 bölüm, Türkçe, Ren'Py ile yapıldı.

> Deniz Aydın 6 Kasım gecesi eski servis yolunda kayboldu. Telefonunda son bir sesli
> mesaj kaldı. Ve o mesajın arkasında, ona benzeyen ama ona ait olmayan bir ses.

---

## Hemen oyna

### Seçenek A: Hazır paket (önerilen)
1. Repo'da **Actions** sekmesine git → son başarılı **Build** çalışmasını aç.
2. **Artifacts** bölümünden işletim sistemine uygun paketi indir:
   - `EsiginArdinda-pc` → Windows + Linux
   - `EsiginArdinda-mac` → macOS
   - `EsiginArdinda-web` → tarayıcı sürümü (itch.io'ya direkt yüklenebilir)
3. Zip'i aç, `EsiginArdinda.exe` (Windows), `EsiginArdinda.sh` (Linux) veya `.app` (Mac) ile başlat.

### Seçenek B: Ren'Py SDK ile (geliştirme için)
1. [Ren'Py SDK](https://www.renpy.org/latest.html) indir ve aç (Python ayrıca gerekmez).
2. Bu repoyu klonla:
   ```bash
   git clone https://github.com/elifnuroksuzz/esigin-ardinda.git
   ```
3. Ren'Py Launcher → **Preferences → Projects Directory** olarak repo'nun bulunduğu klasörü seç.
4. Listede **esigin-ardinda** görünür → **Launch Project**.

Komut satırından:
```bash
/yol/renpy-sdk/renpy.sh /yol/esigin-ardinda
```

---

## Oyun ne tür?

Hikâye odaklı bir korku oyunu, ama yalnızca okumuyorsun. Her bölümde hikâye sahneleri ile
**tur tabanlı keşif haritaları** dönüşümlü gelir (Alien: Isolation, FNAF, Darkest Dungeon ve
Into the Breach'ten esinlenildi; analiz: [docs/OYUN_TASARIMI.md](docs/OYUN_TASARIMI.md)).

- **7 keşif haritası:** kule çevresi, orman, servis yolu, B3 bakım katı, B3/B2 geçişi, drenaj, son tahliye.
- **Gürültü sistemi:** yaratıklar sesle avlanır. Yürümek sessiz, koşmak ve ateş etmek uzaktan duyulur.
- **Kıt bilgi:** yaratıkları görmezsin, duyarsın. *Dinle* turu harcar ama nereye gittiklerini gösterir.
- **Kaynaklar:** fener pili (aramak için), mermi, şişe, ses kaydedici, ilk yardım, Rezonans Kesici.
- **Teçhizat:** ECHO'ya inmeden önce 4 yuvalık çantanı sen hazırlarsın.
- **Derece:** her keşif tur, gürültü ve hasara göre ★–★★★ ile puanlanır.

## Nasıl oynanır

| Tuş | İşlev |
|---|---|
| Tık / Boşluk / Enter | İlerle |
| Fare tekerleği yukarı | Geri sar |
| **J** | **Defter** (ipuçları ve kanıtlar) |
| **1–9** | Numaralı seçimi seç |
| Esc / sağ tık | Menü |
| Ctrl | Atla |

- **Kırmızı çubuklu seçimler zamanlıdır.** Süre biterse karar senin yerine verilir.
  (Ayarlar → *Zamanlı seçimde 2× süre*.)
- **Sağ üstte HUD** (ECHO içinde): fener pili, mermi, Rezonans Kesici, ilk yardım, nabız.
- **Duyduğun her sese güvenme.** Tekrar eden nefes, gecikme ve yön değişimi YANKI'nın işaretidir.
- Hata yapmak oyunu bitirmez; bir bedeli olur ya da yeniden denersin.
- Bir bölüme ulaştıktan sonra ana menüde **Bölüm Seç** açılır.
- Yeni oyunda **Gerilim** (önerilen) veya **Hikâye** (2× süre, yavaş gerginlik) modu seçilir.
- Her bölüm sonunda özet kartı ve otomatik kayıt; ana menüde **Devam Et**.
- **13 başarım** (ana menü → Başarımlar). Bazıları gizli yetenek ister: hiç YANKI'ya kanmamak,
  hiçbir zamanlı seçimi kaçırmamak, Kırpıntı'ları mermi harcamadan atlatmak…

### Sunum
- Konuşan karakter aydınlanır, diğerleri gölgede kalır.
- Film greni, vinyet ve hafifçe "nefes alan" kamera (Ayarlar → Görüntü'den kapatılabilir).
- Nabız 70'i geçince kalp atışı duyulur, 75'te ekran kenarları kızarır.

---

## Proje yapısı

```
game/
  options.rpy, gui.rpy, screens.rpy   Ren'Py ayarları ve arayüz
  core/                               karakterler, durum, efektler, sistemler (HUD, QTE, defter)
  story/ch01.rpy … ch18.rpy           18 bölüm
  images/bg, images/char              arka planlar ve silüetler
  audio/amb, audio/sfx, audio/music   ambiyans, efektler, müzik
tools/
  gen_assets.py                       tüm görsel ve sesleri üretir
  check_story.py                      Ren'Py'sız statik kontrol
docs/
  PLAN.md                             geniş geliştirme planı ve yol haritası
  hikaye_kaynak.md                    kanon hikâye dosyası
```

Ayrıntılı plan ve yol haritası: **[docs/PLAN.md](docs/PLAN.md)**

---

## Görselleri ve sesleri değiştirmek

Tüm görsel ve sesler `tools/gen_assets.py` ile prosedürel üretildi (lisans derdi yok).
Daha iyisini bulduğunda **aynı dosya adıyla** üzerine yaz; kod değişmez.

| Tür | Klasör | Biçim |
|---|---|---|
| Arka plan | `game/images/bg/` | 1280×720 `.jpg` |
| Karakter silüeti | `game/images/char/` | 520×720 şeffaf `.png` |
| Ambiyans (döngü) | `game/audio/amb/` | `.ogg` |
| Efekt | `game/audio/sfx/` | `.ogg` |
| Müzik | `game/audio/music/` | `.ogg` |

Yeniden üretmek için (Python 3.9+, numpy, Pillow, ffmpeg):
```bash
pip install numpy pillow
python tools/gen_assets.py
```

---

## Geliştirici notları

- **Statik kontrol:** `python tools/check_story.py` (label, görsel, ses, karakter referansları)
- **Ren'Py lint:** `renpy.sh . lint`
- **Otomatik oynanış testi:** `ESIK_AUTOTEST=1 ESIK_FAST=1 renpy.sh .` — oyunu rastgele
  seçimlerle baştan sona oynar, sonunda istatistik basar ve kapanır (`game/dev_autotest.rpy`).
- **CI:** her push'ta lint + statik kontrol + PC/Mac/Web paketleri (`.github/workflows/build.yml`).
