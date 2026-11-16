# Mahalle İdari Sınır ve Yerleşim Verileri (`data/mahalleler/`)

Türkiye genelindeki tüm **973 / 973 ilçe** için gerçek coğrafi mahalle/yerleşim katmanlarını (`<il_slug>_<ilce_slug>.json`) içerir:

* **695 ilçe**: Resmi Belediye / MAKS açık veri portalları (`ttezer/turkiye-harita-verisi`), yerel resmi GIS (`izmir_tire.json`) ve OpenStreetMap (`Geofabrik turkey-latest.osm.pbf`, `admin_level=8/9/10` + `place`) gerçek mahalle sınır poligonları.
* **278 kırsal ilçe**: Yapay Voronoi kullanılmaksızın, resmi `admin_level=6` ilçe sınır poligonu içinde OpenStreetMap'ten doğrulanmış gerçek yerleşim merkezi koordinatları (`geometry_mode: "points"`).
* Ek olarak `/api/mahalle-boundaries` uç noktası canlı Overpass API yedeği sağlar.
