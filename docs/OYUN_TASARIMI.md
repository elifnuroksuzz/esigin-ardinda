# EŞİĞİN ARDINDA — Oyun Tasarımı Analizi

**Sorun:** v1.0 iyi bir hikâye anlatıyordu ama oyuncu çoğunlukla *okuyordu*. Seçimler vardı,
ancak bir **oyun döngüsü** yoktu: kaynak harcamanın, risk almanın, plan yapmanın anlamı azdı.

**Hedef:** Hikâyeyi koruyup her bölüme *oynanan* bir katman eklemek. Oyuncu okumak yerine
**karar vermeli, harita üzerinde plan yapmalı, kaynak yönetmeli ve hatasının bedelini görmeli.**

---

## 1. Popüler oyunların analizi

| Oyun | Çekirdek döngü | Neden tutuyor | Bizim aldığımız |
|---|---|---|---|
| **Five Nights at Freddy's** | Kameralara bak → tehdidin yerini tahmin et → sınırlı enerjiyle kapı/ışık kullan | Az bilgi + sınırlı kaynak = sürekli gerilim. Ses ipuçları çok güçlü. | **Dinle** eylemi: tehditler görünmez, sesleri duyulur. Fener pili = enerji. |
| **Alien: Isolation** | Hareket algılayıcısıyla tehdidi izle, saklan, gürültü yapma | Yaratık *sesle* avlanır; oyuncunun gürültüsü silahtır da tehlikedir de. | **Gürültü sistemi**: yürümek 1, koşmak 3, ateş 5. Nöbetçi sesi takip eder. |
| **Darkest Dungeon** | Keşfe hazırlan (erzak) → odadan odaya ilerle → stres ve ışık yönet | Hazırlık kararları keşfin kaderini belirler. Stres ikinci bir can barıdır. | **Teçhizat ekranı** (sınırlı çanta). **Nabız** ikinci can barı gibi çalışır. |
| **FTL / Slay the Spire** | Düğüm haritasında rota seç → olay → kaynak kazan/kaybet | Her düğüm bir risk/ödül kararı. Kısa, tekrar oynanabilir oturumlar. | **Düğüm tabanlı tesis haritası**. Kısa yol riskli, uzun yol güvenli ama pahalı. |
| **Duskers** | Karanlık gemide odaları tek tek aç, sensörlerle tehdidi bul | Bilgi bir kaynaktır; *bakmak* tur harcar. | **Ara** eylemi: fener pili harcayarak odadaki malzemeyi/ipucunu bul. |
| **Phasmophobia** | Kanıt topla → varlığın türünü belirle | Gözlem ve çıkarım; oyuncu dedektif olur. | Sahte sesi ayırt etme, **dalga formu analizi**, Taklitçi'nin gecikmesi. |
| **Into the Breach** | Düşmanın *bir sonraki* hamlesini gör, ona göre konumlan | Tam bilgiyle kusursuz plan yapma tatmini. | **Dinle** ile tehdidin hedefini ve yönünü gör; şişe atarak onu yönlendir. |
| **Resident Evil / Signalis** | Kıt mermi, kıt iyileşme, envanter kararları | "Bu mermiyi şimdi mi harcayayım?" sorusu sürekli gerilim yaratır. | Mermi yalnızca Kırpıntı'ya işler; Nöbetçi'ye boşa gider. Rezonans mermisi çok değerli. |
| **Inscryption / Return of the Obra Dinn** | Kuralları kendin keşfet | Oyun oyuncuyu zeki hissettirir. | YANKI kuralları anlatılmaz, **gösterilir**; defter ipucu tutar. |

### Ortak dersler
1. **Bilgi kıt olmalı ve bedeli olmalı.** (FNAF, Duskers) → Dinlemek ve aramak tur/pil harcar.
2. **Oyuncunun gürültüsü hem silah hem tehlike.** (Alien) → Şişe atmak tehdidi uzaklaştırır, ateş etmek her şeyi çağırır.
3. **Hazırlık, keşfin yarısıdır.** (Darkest Dungeon) → Çantaya ne koyduğun sonraki 10 bölümü etkiler.
4. **Hata öğretmeli, cezalandırmamalı.** (Into the Breach) → Yakalanınca keşif baştan başlar, iki başarısızlıktan sonra atlama seçeneği çıkar.
5. **Kısa, puanlanan oturumlar.** (Slay the Spire) → Her keşif 3–8 dakika, sonunda ★ derece.

---

## 2. Yeni oyun döngüsü

```
HİKÂYE SAHNESİ  →  KEŞİF HARİTASI  →  HİKÂYE SAHNESİ  →  BÖLÜM ÖZETİ
  (karar, ipucu)     (strateji, kaynak)    (sonuç)            (★, kanıt, nabız)
```

### Keşif haritası (ana yenilik)
Tur tabanlı, düğüm (oda) haritası. Oyuncu bir tur harcar, sonra tehditler hareket eder.

| Eylem | Tur | Gürültü | Not |
|---|---|---|---|
| **Yürü** | 1 | 1 | Komşu odaya geç |
| **Koş** | 1 | 3 | İki oda ilerle; uzaktan duyulur |
| **Dinle** | 1 | 0 | 2 oda içindeki tehditleri ve hedeflerini gösterir |
| **Ara** | 1 | 0 | Fener pili harcar; malzeme/ipucu bulur |
| **Şişe at** | 1 | 4 (hedefte) | Tehditleri başka odaya çeker |
| **Saklan** | 1 | 0 | Yalnızca saklanma noktalarında |
| **Ateş et** | 1 | 5 | Kırpıntı'yı öldürür; Nöbetçi'ye işlemez |
| **Bekle** | 1 | 0 | Zamanlama için (ör. pres gürültüsü) |

**Tehditler**
- **Nöbetçi:** yavaş (2 turda bir hareket), çok dayanıklı, sesi takip eder, **dar havalandırmalara giremez**.
- **Kırpıntı:** hızlı, kör, sese çok duyarlı, tek mermiyle durur.
- **Sürüngen:** çok hızlı, **ışığa** (Ara eylemine) yönelir.

**Ortam**
- **Pres/makine odaları:** belirli turlarda gürültün örtülür.
- **Havalandırmalar:** Nöbetçi'den güvenli ama dar.
- **Sürgülü kapılar:** bir geçidi birkaç tur kapatır.

**Derece:** Tur sayısı, toplam gürültü ve alınan hasara göre ★–★★★.

### Teçhizat (Bölüm 7)
Çantada 4 yuva. Seçenekler: yedek pil, şişe, ilk yardım, mermi kutusu, ses kaydedici.
Her biri ECHO'daki keşifleri farklı biçimde kolaylaştırır; hepsini alamazsın.

---

## 3. Arayüz yönü

- **Tipografi:** Başlıklar Oswald (sinematik, dar, güçlü), metin DejaVu Sans (okunaklı).
- **Renk dili:** Kat renkleri (B3 sarı, B2 mavi, D kırmızı, Z0 mor) haritada ve arayüzde tutarlı.
- **Harita:** Mavi kopya (blueprint) estetiği: ızgara, ince çizgiler, nabız gibi atan oyuncu işareti,
  tehditler için kırmızı ses halkaları.
- **Diyalog kutusu:** Degrade panel, renkli isim şeridi, numaralı seçimler (1–9 tuşları).
- **HUD:** İkonlu, çubuklu, kompakt panel.
