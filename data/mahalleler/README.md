# Mahalle İdari Sınır Verileri (`data/mahalleler`)

Bu klasör, seçilen ilçelerin gerçek `admin_level=8` idari mahalle sınır poligonlarını (GeoJSON) barındırır.
- Yerel önbellekte bulunan ilçeler (`izmir_tire.json` vb.) doğrudan buradan yüklenir.
- Türkiye'deki diğer tüm ilçeler için tarayıcı ve sunucu, OpenStreetMap Overpass API (`boundary=administrative`, `admin_level=8`) üzerinden gerçek mahalle sınırlarını canlı çekip bu klasöre / önbelleğe kaydeder.
