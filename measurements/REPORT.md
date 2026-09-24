# arasta · ZSeven ölçüm ve uyumluluk raporu

arasta, ZSeven OpenPencil MCP içinde hazırlanmış bir Türkçe B2B pazar yeri tasarımı ve etkileşimli statik prototiptir. Referans yalnızca karşılaştırma amacıyla incelendi; dosyası, kodu veya görseli alınmadı.

## Ölçülen sonuç

- 484/484 ekran temel tarayıcı denetiminden geçti.
- 17/17 etkileşim testi geçti.
- 50 axe sayfası: 0 ihlal; 5 QR kodu çözüldü.
- 623 native çağrı, %98.23 başarılı (negatif testler dahil).
- 1.680 reusable master; 8.542 ref; 149 değişken.

## Üç tur

1. 320 px önce tasarlandı. Master koordinat mirası ve null patch sorunu bulundu; koordinatsız master + dış kütüphane kapsayıcılarıyla giderildi.
2. 484 native ağaç ve 484 tarayıcı ekranı tarandı. Web alt menüsündeki ikon/metin yönü düzeltildi; forma ait semantik etiket ve flex sarması uygulandı.
3. 155 ProductCard master aralığı 12 → 16 px yapıldı; 976 ref üzerinde yayılım doğrulandı. TV formlarına native vektör QR ve telefon bağlantıları eklendi. Son denetim 484/484 temiz.

## Bulgular

### UYUM · Yerel üretim

22 sayfa × 22 cihaz = 484 frame; 1.680 reusable master, 8.542 ref ve 149 değişken yerel MCP ile yazıldı. Phosphor çizimleri path düğümleri; fotoğraf, SVG/HTML tasarım içe aktarımı yok.

Kanıt: design/arasta.op; generator-state.json

### UYUM · Arka plan çalışması

Üretim ve Chromium testleri Colima factory içindeki Linux konteynerlerinde yapıldı. Masaüstü uygulamasına son iş akışında müdahale edilmedi.

Kanıt: calls.jsonl; browser/results.json

### UYUM · Üçüncü tur yayılımı

155 ProductCard master’ının dikey aralığı 12 → 16 px değiştirildi. 976 doğrudan ref, kendi gap override’ı olmadan yeni değeri kullanıyor.

Kanıt: master-round3.json

### UYUM · Frontend kalite kapısı

484/484 ekran gerçek CSS genişliğinde açıldı: HTTP 200, yatay taşma yok, 16 px altı metin yok, 12 px üstü radius yok, etiketsiz kontrol yok, tek h1. 17 etkileşim testi geçti.

Kanıt: browser/results.json; browser/interactions.json

### UYUM · Erişilebilirlik ek denetimi

320 ve 1440 genişliğindeki 22’şer sayfa ile 6 TV sayfasında axe WCAG A/AA kuralları: 50 sayfada 0 ihlal. 484 yerel ağaçta semantik metin renklerinin en düşük kontrastı 5,056:1.

Kanıt: browser/axe.json; token-contrast.json

### UYUM · TV telefon bağlantısı

Giriş, ödeme, teklif, kayıt ve mesajlar ekranlarındaki 5 QR gerçek hedef URL’ye çözüldü. K74QX bir örnek cihaz kodudur; canlı oturum eşleştirmesi değildir.

Kanıt: browser/axe.json

### KISMİ · Bileşen ve varyant API’si

Reusable master/ref bağlantıları çalışıyor. Durumlar ayrı adlandırılmış master’lardır. list_components bu runtime’da 0 döndürdü; yerel varyant eksenleri/paneli doğrulanmış kabul edilmedi.

Kanıt: capabilities-isolated.json; calls.jsonl

### DİRENÇ · Yerleşim ve null patch

Master’ın kütüphane x/y konumu instance’a miras kaldı. x/y=0 ref’leri üst üste bindirdi; U(x:null) koordinatı kaldırmadı. Master’lar koordinatsız yeniden üretildi, kütüphane konumu dış kapsayıcıya taşındı.

Kanıt: browser-round1-sample.json; calls.jsonl

### DİRENÇ · Agent Teams

Web runtime’ındaki spawn_agents çağrısı 180 saniyede istemci zaman aşımına ulaştı ve servis yoğun kaldı. Kaydedilmiş .op ile ayrı headless süreçte devam edildi; web servisi dosya korunarak geri yüklendi. Headless denemesi yapılandırılmış config argümanını -32602 ile reddetti. Gerçek paralel agent üretimi ve hızlanma ölçülmedi.

Kanıt: calls.jsonl; capabilities-isolated.json

### KISMİ · Kod dışa aktarımı

codegen_plan/submit/assemble hattı, dışarıdan verilen React parçasını doğrulayıp paketledi. Eksik parça doğru hata verdi; başarılı assemble planı tüketti. AI modeli bağlı olmadığı için otonom React/HTML üretimi ve otomatik export görsel sadakati ölçülemedi. Frontend, kaydedilmiş native ağacın deterministik HTML adaptörüdür.

Kanıt: capabilities-isolated.json; web/tools/export_frontend.py

### KISMİ · Görsel sadakat

320 px native render ile frontend incelendi. Native metin ölçümü, hug/fill ve flex davranışında farklar var; HTML adaptörü min-width, sarma, semantik etiketler ve kaydırmayı ayrıca uygular. Piksel düzeyinde 1:1 eşitlik iddia edilmez.

Kanıt: native-final-320.png; browser/mobil-dikey-320.png

### KISMİ · Git birleştirme

Yerel ZSeven Git branch/merge arayüzü bu web/headless API’de sunulmuyor. Harici git merge-file testinde ayrı alanlar geçerli JSON olarak birleşti; aynı alan çakışması conflict marker üretti. Bu, yerel Git özelliği testi değildir.

Kanıt: git-merge.json

### KISMİ · Lisans ve kapsam

Güncel paketlerde Roboto ve Roboto Mono lisansı SIL OFL 1.1; briefteki Apache-2.0 ifadesi bu dosyalara uygulanamaz. Gerçek lisanslar aynen saklandı. AI, kimlik doğrulama, mesajlaşma ve ödeme backend’i bağlı değildir; etkileşimler yerel örnek akışlardır.

Kanıt: web/assets/Roboto-LICENSE.txt; web/assets/RobotoMono-LICENSE.txt

### KISMİ · Ölçüm kapsamı

Log, enstrümantasyon başladıktan sonraki native MCP çağrılarını içerir; ilk keşif/önceki GUI denemelerinin eksiksiz kaydı değildir. p50/p95 çağrı bazındadır; batch başına en çok 3 ekran olduğundan tek frame gecikmesi diye sunulmaz. 100 KB sınırı ve 120 saniye iptal davranışı doğrudan eşik testiyle ölçülmedi.

Kanıt: metrics.json; calls.jsonl

## 20 boyutta karşılaştırma

Penpot sütunu kullanıcı briefi ve yayınlanmış referansın gözlemidir; aynı ortamda yeniden benchmark yapılmadı.

| Boyut | Penpot referansı | ZSeven bu çalışma |
|---|---|---|
| Kurulum | Referans yayını mevcut; yeniden kurulmadı. | UYUM · Çalışan v0.8.2 + ayrı Linux worker. |
| Bağlantı | Penpot + MCP; bu turda yeniden ölçülmedi. | UYUM · HTTP MCP ve op CLI. |
| Başsız çalışma | Briefte arka plan heartbeat riski bildirilmiş. | UYUM/KISMİ · GUI olmadan üretim; Teams çağrısı takıldı. |
| Dosya biçimi | Sunucu tabanlı Penpot belgesi. | UYUM · Yaklaşık 20 MB, okunabilir .op JSON. |
| Ölçek | Aynı 484 ekran hedefi; eş zamanlı benchmark yok. | UYUM · 484 frame, 30.141 kayıtlı düğüm. |
| Token API | Kütüphane renkleri ve cihaz temaları. | UYUM · 149 değişken, Light/Dark + 8 Cihaz teması. |
| Master bağlantıları | Referans bileşen yaklaşımı. | UYUM · 976 ref üzerinde master değişikliği doğrulandı. |
| Varyantlar | Briefte grup başına tek varyant listeleme sorunu. | KISMİ · Adlandırılmış durum master’ları; registry 0. |
| Auto layout | Briefte hug/fill ve resize sıfırlama sorunları. | DİRENÇ · x/y mirası ve null patch davranışı. |
| Font çözümü | Briefte fuzzy font lookup riski. | KISMİ · Roboto ismi native; web kendi WOFF2 dosyalarını kullanır. |
| Vektör/ikon | Karşılaştırma için kopyalanmadı. | UYUM · 80 UI ikon × 4 boyut; Phosphor native path. |
| İstek boyutu | Briefte 100 KB sınırı. | KISMİ · En büyük gözlenen istek 61737 bayt; sınır bulunmadı. |
| Timeout/iptal | Briefte 120 saniye ve iptal yokluğu. | DİRENÇ · Teams için 180 saniye istemci timeout; yerel iptal aracı yok. |
| Yazma gecikmesi | Eş donanımda ölçülmedi. | ÖLÇÜM · Çağrı p50 399.27 ms; p95 1623.81 ms. |
| Hata kalitesi | Briefte farklı direnç örnekleri. | KISMİ · Ayrıntılı patch hataları; bazı null işlemler sessizce etkisiz. |
| Kod export | Referans implementasyonu görüntülendi, kodu alınmadı. | KISMİ · Chunk assembler var; otonom AI export doğrulanmadı. |
| Paralel ajan | Bu çalışmada Penpot ajan testi yapılmadı. | DİRENÇ · Native Teams yürütümü ve hızlanma yok. |
| Git/merge | Bu çalışmada Penpot merge testi yapılmadı. | KISMİ · JSON merge dış Git ile test edildi; native UI sunulmadı. |
| Erişilebilirlik | Referans görsel karşılaştırma; yeniden tam denetim yok. | UYUM · 484 geometri/form kontrolü, 50 axe sayfası, 17 etkileşim. |
| Round trip/sadakat | Briefte Figma round trip A aracına özgü. | KISMİ · .op yeniden açıldı ve render edildi; piksel eşitliği yok. |

## Sonuç

Native dosya, tokenlar, reusable ref grafiği ve HTTP MCP ile büyük bir adaptif prototip üretmek mümkün. Buna karşılık native Agent Teams, variant registry, tam otomatik kod export ve yerleşim tutarlılığı bu runtime için enterprise hazır sayılmadı. Üretim ortamına geçişte gerçek kimlik/ödeme servisleri, ürün bazlı detay verileri ve kullanıcı testleri ayrıca gerekir. Otomatik WCAG taraması tam erişilebilirlik sertifikası değildir.
