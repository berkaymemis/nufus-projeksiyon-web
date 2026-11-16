# `core/` — Saf Python Demografi ve Mekânsal Hesaplama Motorları

`qgis` veya `PyQt` bağımlılığı taşımayan saf Python analiz modülleridir:

* `tuik_adnks.py` — 81 il / 973 ilçe resmi TÜİK ADNKS nüfus serileri ve mahalle alt bölge verileri
* `curve_fitting.py` — 6 matematiksel regresyon modeli ve Prof. Dr. K. Mert Çubukçu Sabit/Değişken Pay (4.30 / 4.39) modelleri
* `cohort_model.py` — 17 yaş grubu Kuşak-Bileşen (Cohort-Component) yaş piramidi projeksiyonu
* `economic_base.py` & `district_multipliers.py` — İktisadi Taban (LQ / MG) baz çarpanları ve göç hesaplayıcısı
* `demographic_shocks.py` — Yıl bazlı OSB, üniversite, afet vb. demografik şok motoru
* `hansen_model.py` — Hansen mekânsal çekim, konut ihtiyacı ve plan doygunluk dağıtım modeli
* `xlsx_export.py` — 5 sayfalı `.xlsx` rapor üreticisi (`openpyxl` + sıfır-bağımlılıklı OpenXML yedeği)
* `data_import.py`, `city_templates.py`, `researchgate_citations.py` — Veri içe aktarma, plan şablonları ve akademik referanslar
