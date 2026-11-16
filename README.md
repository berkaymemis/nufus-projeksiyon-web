# 🌐 NüfusKaç. — Kentsel Demografi, Mekânsal Analiz ve Nüfus Projeksiyon Platformu

Türkiye'nin **81 İl ve 973 İlçesi** için resmi **TÜİK ADNKS (2015–2025)** veri tabanı, **Prof. Dr. K. Mert Çubukçu** iktisadi taban ve bölgesel pay yöntemleri, **gerçek ilçe ve mahalle idari sınır haritaları**, **Kuşak-Bileşen (Cohort-Component)** yaş piramitleri, **Hansen Mekânsal Çekim Modeli** ve **MPYY (Ek-2) Kentsel Donatı Standartlarını** bir araya getiren web ve PWA uygulamasıdır.

---

## ✨ Temel Özellikler

* **📍 81 İl & 973 İlçe Resmi TÜİK Veri Tabanı**:
  * İl geneli, ilçe veya mahalle/kapsam seçimine göre 2025–2050 hedef yıl projeksiyonları.
  * Nötr başlangıç ekranı, tek tıkla anasayfa sıfırlama (`resetToNeutralHome`) ve paylaşılabilir URL parametreleri (`/?il=...&ilce=...&yil=...`).
* **🗺️ Türkiye Geneli %100 Gerçek İdari Sınır Haritası (`973 / 973` İlçe)**:
  * **81 İl / 973 İlçe Dış Sınırları** ([data/districts/](data/districts/index.json)): Tam çözünürlüklü resmi ilçe poligonları (`MERKEZ`, şapkalı harf ve boşluk varyantları dahil tam eşleşme).
  * **Gerçek Mahalle Sınırları** ([data/mahalleler/](data/mahalleler/README.md)):
    * **695 ilçede** resmi Belediye / MAKS açık veri ve OpenStreetMap (`admin_level=8/9/10`) **gerçek mahalle sınır poligonları**.
    * **278 kırsal ilçede** resmi ilçe sınır poligonu içinde OpenStreetMap'ten doğrulanmış **gerçek yerleşim noktası koordinatları** *(yapay Voronoi / altıgen bölme kullanılmaz)*.
  * Seçili alana göre izole harita görünümü, **Hansen Çekim Gücü ($G_i$)** ve **Kapasite Doygunluğu (%)** choropleth katmanları.
* **📈 6 Matematiksel Eğri Uydurma + 2 Bölgesel Pay Modeli ([core/curve_fitting.py](core/curve_fitting.py))**:
  * *Doğrusal (Linear)*, *2. Derece Polinom*, *3. Derece Polinom*, *Üstel (Exponential)*, *Logaritmik*, *Kuvvet (Power)* regresyonları ile $R^2$, SSE ve negatif çöküş doğrulaması.
  * *Prof. Dr. K. Mert Çubukçu* **Sabit Pay (Formül 4.30)** ve **Değişken Pay / Shift-Share (Formül 4.39)** üst bölge oranlama modelleri.
* **🏭 İktisadi Taban Çarpanı & Demografik Şok Simülatörü ([core/economic_base.py](core/economic_base.py), [core/district_multipliers.py](core/district_multipliers.py), [core/demographic_shocks.py](core/demographic_shocks.py))**:
  * Tüm ilçeler için Konum Katsayısı (**LQ**) ve Minimum Gereksinimler (**MG**) çarpanları ($k$, $b$, $\Delta P = \Delta E_b \cdot k \cdot b$).
  * Yıl bazlı yeni OSB, üniversite kampüsü, hastane veya afet göçü şok simülasyonları.
* **👥 Kuşak-Bileşen (Cohort-Component) & MPYY Ek-2 ([core/cohort_model.py](core/cohort_model.py), [core/hansen_model.py](core/hansen_model.py))**:
  * 17 yaş grubu (`0–4` … `80+`) kadın/erkek yaş piramitleri; *Düşük (%0 Göç)*, *Orta (Trend)*, *Yüksek (Plan Kabulü)* senaryoları.
  * Mekânsal Planlar Yapım Yönetmeliği (Ek-2) kişi başı `19.0 m²` asgari sosyal ve teknik altyapı alanı hesabı.
* **📊 5 Sayfalı Otomatik Excel (`.xlsx`) Raporu ([core/xlsx_export.py](core/xlsx_export.py))**:
  * Seçili İl / İlçe / Mahalle ve Hedef Yıl adına göre 5 sekmeli çalışma kitabı indirir: `01_Secili_Alan_ve_Ozet`, `02_Regresyon_ve_Yillik_Seri`, `03_Kusak_Bilesen_Piramit`, `04_Hansen_Mahalle_Dagilimi`, `05_MPYY_Donati_Standartlari`.
* **🏛️ Çift Arayüz, Çift Dil & PWA**:
  * Modern görünüm (`/`), Klasik Plancı Modu (`/classic`), Türkçe / İngilizce (`TR / EN`) arayüz ve Service Worker ([sw.js](sw.js)) desteği.

---

## 📁 Dizin ve Mimari Yapısı

| Dosya / Klasör | Açıklama |
| :--- | :--- |
| [server.py](server.py) | Çok iş parçacıklı Python HTTP/REST sunucusu (gzip + `/api/*` uç noktaları) |
| [index.html](index.html) | Ana web uygulaması arayüzü (Chart.js, Leaflet.js, Tailwind CSS) |
| [index_classic.html](index_classic.html) | Eski / klasik planlama laboratuvarı görünümü (`/classic`) |
| [core/](core/README.md) | Saf Python hesaplama motorları (`curve_fitting.py`, `cohort_model.py`, `economic_base.py`, `hansen_model.py`, `xlsx_export.py` vb.) |
| [data/districts/](data/districts/README.md) | 81 il / 973 ilçeye ait tam çözünürlüklü GeoJSON ilçe sınırları |
| [data/mahalleler/](data/mahalleler/README.md) | 973 / 973 ilçe için önbelleğe alınmış gerçek mahalle poligonları ve yerleşim koordinatları |
| [render.yaml](render.yaml), [Dockerfile](Dockerfile), [Procfile](Procfile) | Bulut ve konteyner dağıtım yapılandırmaları |
| [manifest.json](manifest.json), [sw.js](sw.js) | PWA manifesti ve Service Worker |

### Temel API Uç Noktaları

* `GET /api/tuik-adnks` — 81 il / 973 ilçe resmi TÜİK nüfus ve demografi verileri
* `GET /api/mahalle-boundaries?province=...&district=...` — Seçili ilçe için gerçek mahalle GeoJSON sınırları (önbellek + Overpass yedeği)
* `POST /api/calculate` — Tüm eğri uydurma, kuşak-bileşen, iktisadi taban, Hansen ve MPYY hesaplamaları
* `POST /api/export-report` — Seçili çalışma alanı için 5 sayfalı `.xlsx` raporu üretimi
* `GET /api/district-multipliers`, `/api/templates`, `/api/citations`, `/api/status` — Çarpanlar, şablonlar, akademik kaynaklar ve sunucu durumu

---

## 🚀 Çalıştırma ve Canlı Dağıtım

### Yerel Çalıştırma
Zorunlu harici bağımlılık gerekmez (isteğe bağlı zengin biçimli `.xlsx` çıktısı için `openpyxl>=3.1.2` kurulabilir; kurulu değilse yerleşik sıfır-bağımlılıklı OpenXML yazıcısı otomatik çalışır):

```bash
pip install -r requirements.txt
python server.py
```

Tarayıcınızda açın: `http://localhost:8080` *(Ekran görüntüsü / tarayıcı açmadan çalıştırmak için `--no-browser` parametresini kullanabilirsiniz).*

### Render.com / Railway / Docker Üzerinde Dağıtım
Depo kökünde hazır [render.yaml](render.yaml), [Procfile](Procfile) ve [Dockerfile](Dockerfile) bulunur:

1. GitHub deposunu Render.com (`New Web Service`) veya Railway hesabınıza bağlayın.
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `python server.py --port $PORT --no-browser`
4. **Health Check**: `/api/status`

---

## 📚 Metodoloji ve Veri Kaynakları

* **Demografik Veriler**: TÜİK Adrese Dayalı Nüfus Kayıt Sistemi (ADNKS 2015–2025)
* **Analitik Modeller**: Prof. Dr. K. Mert Çubukçu (Dokuz Eylül Üniversitesi) — *Planlamada Klasik Sayısal Yöntemler*, İTÜ Dergisi LQ/MG İktisadi Taban Çarpanları (2011) & KUZİP Sentez Raporu (2026)
* **Mekânsal Sınırlar**: Büyükşehir Belediyeleri & MAKS Açık Veri Portalları (`ttezer/turkiye-harita-verisi`) ve © OpenStreetMap contributors / Geofabrik (ODbL)
