# arasta · ZSeven OpenPencil

Türkçe bir B2B pazar yeri için **22 sayfa × 22 ekran = 484 canlı prototip**. Tasarım, ZSeven’in native MCP araçlarıyla `.op` içinde oluşturuldu; HTML, kayıtlı native ağaçtan üretildi.

[Canlı izleyici](https://karacaismail.github.io/arasta-openpencil-zseven/) · [Ölçüm raporu](https://karacaismail.github.io/arasta-openpencil-zseven/rapor/) · [Native dosya](design/arasta.op)

## Doğrulama

- 484/484 gerçek genişlikte ekran: taşma, min. 16 px, maks. 12 px radius, etiketler, tek h1 ve HTTP 200.
- 17/17 etkileşim testi; 50 axe sayfasında 0 ihlal; 5 QR bağlantısı çözüldü.
- 1.680 reusable master, 8.542 ref, 149 değişken. 155 master değişikliği 976 ref üzerinde doğrulandı.
- 320 px önce; 8 farklı cihaz ailesi; TV koyu tema ve yön tuşları.

Bunlar bir prototipin otomatik test sonuçlarıdır; tam WCAG sertifikası veya canlı ticaret backend’i değildir. AI, giriş, ödeme, şirket sorgusu ve mesaj gönderimi örnek etkileşimlerdir. Ürün detay ekranı organik penye örneğidir.

## Yapı

- `design/`: native `.op` tasarım.
- `web/`: bağımlılıksız HTML/CSS/JS; kendi fontları ve Phosphor SVG sprite.
- `web/tools/`: native üretim ve HTML adaptörü; geliştirme/denetim araçları.
- `docs/`: GitHub Pages çıktısı, kökte cihaz izleyicisi.
- `measurements/`: ham native çağrılar, QA, üç tur, bulgular ve 20 boyutta karşılaştırma.

## Yerel görüntüleme ve yeniden üretim

`python3 -m http.server 8000 --directory docs` ile statik yayını açabilirsiniz. Kaydedilmiş native dosyadan HTML’yi yeniden üretmek için `python3 web/tools/export_frontend.py` kullanılır. QA araçları geliştirme aşamasında Playwright, axe-core, jsQR ve pngjs kullanır; yayınlanan uygulamada paket veya CDN bağımlılığı yoktur.

## Araç sınırları

Native Teams denemesi zaman aşımı/yapılandırılmış argüman hatası verdi; gerçek native paralellik ve hızlanma ölçülmedi. `list_components` 0 döndürdü; durum master’ları yerel variant registry olarak sunulmaz. Kod export hattı dışarıdan verilen chunk’ları paketledi; otonom React/HTML export doğrulanmadı. Harici Git üç yönlü merge test edildi; native Git UI bu runtime’da erişilebilir değildi. Native ve HTML metin/flex davranışları farklı olduğundan piksel düzeyinde 1:1 iddiası yoktur. Ayrıntılar [raporda](measurements/REPORT.md).

Referans yalnızca karşılaştırma amacıyla incelendi; dosya, kod veya görseli kopyalanmadı. İlk keşif çağrıları kayıt başlamadan önceydi; `calls.jsonl` o aşamanın eksiksiz geçmişi değildir.

## Lisanslar

Proje: [MIT](LICENSE). Phosphor Icons: [MIT](web/assets/Phosphor-LICENSE.txt). Dahil edilen güncel [Roboto](web/assets/Roboto-LICENSE.txt) ve [Roboto Mono](web/assets/RobotoMono-LICENSE.txt): SIL OFL 1.1. Briefteki Apache-2.0 ifadesi bu güncel font paketlerinin lisansı değildir. Lisans dosyaları değiştirilmeden korunmuştur.

Git author/committer politikası yerel koruma kancalarıyla uygulandı. AI/bot ortak yazar veya generated-with imzası eklenmedi.
