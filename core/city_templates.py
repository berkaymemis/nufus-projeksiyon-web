# -*- coding: utf-8 -*-
"""
Preset Study Area Templates (Hazır Kent ve Plan Tipolojisi Şablonları)
Tüm kentsel ve bölgesel çalışma alanları için hazır başlangıç profilleri ve geçmiş nüfus serileri
Metodoloji: Prof. Dr. K. Mert Çubukçu — "Planlamada Klasik Sayısal Yöntemler" ve Kentsel Modelleme Pratikleri
"""

from typing import Dict, Any, List


CITY_TEMPLATES = {
    "tire_88_adnks": {'id': 'tire_88_adnks', 'name': 'Standart İlçe Mahalle Dağılım Şablonu (88 Mahalle - 87.528 Nüfus)', 'category': 'Resmi TÜİK Veri Tabanı (88 Kentsel & Kırsal Mahalle)', 'base_year': 2025, 'base_pop': 87528, 'target_year_1': 2045, 'target_pop_1': 113786, 'target_year_2': 2050, 'target_pop_2': 120788, 'years_hist': [2015, 2017, 2019, 2021, 2023, 2024, 2025], 'pop_hist': [77025, 79650, 82276, 84027, 86215, 87000, 87528], 'total_labour': 39388, 'basic_labour': 8753, 'new_industrial_jobs': 3500, 'industrial_area_ha': 120.0, 'workers_per_ha': 35.0, 'tfr': 1.545, 'annual_trend_mig': 400, 'description': 'Standart bir ilçe genelinin (88 mahalle) örnek nüfus veri tabanı. Tarımsal havza, merkez mahalleler ve sanayi aksı.', 'subzones': [{'id': 1, 'name': 'BAHARİYE', 'base_pop': 1068, 'jobs': 427, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 1388}, {'id': 2, 'name': 'CUMHURİYET', 'base_pop': 3545, 'jobs': 1418, 'capacity_ha': 10.6, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 4608}, {'id': 3, 'name': 'DERE', 'base_pop': 1358, 'jobs': 543, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 1765}, {'id': 4, 'name': 'DUATEPE', 'base_pop': 374, 'jobs': 150, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 486}, {'id': 5, 'name': 'DUMLUPINAR', 'base_pop': 557, 'jobs': 223, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 724}, {'id': 6, 'name': 'ERTUĞRUL', 'base_pop': 650, 'jobs': 260, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 845}, {'id': 7, 'name': 'İHSANİYE', 'base_pop': 1856, 'jobs': 742, 'capacity_ha': 5.6, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 2413}, {'id': 8, 'name': 'İPEKÇİLER', 'base_pop': 1629, 'jobs': 652, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 2118}, {'id': 9, 'name': 'İSTİKLAL', 'base_pop': 1249, 'jobs': 500, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 1624}, {'id': 10, 'name': 'KARACA ALİ', 'base_pop': 233, 'jobs': 93, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 303}, {'id': 11, 'name': 'KETENCİ', 'base_pop': 1322, 'jobs': 529, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 1719}, {'id': 12, 'name': 'KURTULUŞ', 'base_pop': 4891, 'jobs': 1956, 'capacity_ha': 14.7, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 6358}, {'id': 13, 'name': 'PAŞA', 'base_pop': 875, 'jobs': 350, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 1138}, {'id': 14, 'name': 'TURAN', 'base_pop': 1578, 'jobs': 631, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 2051}, {'id': 15, 'name': 'YENİ', 'base_pop': 1299, 'jobs': 520, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 1689}, {'id': 16, 'name': '4 EYLÜL', 'base_pop': 4062, 'jobs': 1625, 'capacity_ha': 12.2, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 5281}, {'id': 17, 'name': 'ADNAN MENDERES', 'base_pop': 5014, 'jobs': 2006, 'capacity_ha': 15.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 6518}, {'id': 18, 'name': 'ATATÜRK', 'base_pop': 6153, 'jobs': 2461, 'capacity_ha': 18.5, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 7999}, {'id': 19, 'name': 'HÜRRİYET', 'base_pop': 8683, 'jobs': 3473, 'capacity_ha': 26.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 11288}, {'id': 20, 'name': 'TOKİ', 'base_pop': 2719, 'jobs': 1088, 'capacity_ha': 8.2, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 3535}, {'id': 21, 'name': 'İBNİ MELEK', 'base_pop': 4525, 'jobs': 1810, 'capacity_ha': 13.6, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 5882}, {'id': 22, 'name': 'FATİH', 'base_pop': 11988, 'jobs': 4795, 'capacity_ha': 36.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 15584}, {'id': 23, 'name': 'GÖKÇEN', 'base_pop': 926, 'jobs': 370, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 1204}, {'id': 24, 'name': 'AKKOYUNLU', 'base_pop': 456, 'jobs': 182, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 593}, {'id': 25, 'name': 'AKMESCİT', 'base_pop': 457, 'jobs': 183, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 594}, {'id': 26, 'name': 'ALACALI', 'base_pop': 228, 'jobs': 91, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 296}, {'id': 27, 'name': 'ARMUTLU', 'base_pop': 46, 'jobs': 18, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 60}, {'id': 28, 'name': 'AYAKLIKIRI', 'base_pop': 302, 'jobs': 121, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 393}, {'id': 29, 'name': 'BAŞKÖY', 'base_pop': 454, 'jobs': 182, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 590}, {'id': 30, 'name': 'BOYNUYOĞUN', 'base_pop': 326, 'jobs': 130, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 424}, {'id': 31, 'name': 'BÜYÜKKEMERDERE', 'base_pop': 359, 'jobs': 144, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 467}, {'id': 32, 'name': 'BÜYÜKKÖMÜRCÜ', 'base_pop': 318, 'jobs': 127, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 413}, {'id': 33, 'name': 'CAMBAZLI', 'base_pop': 252, 'jobs': 101, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 328}, {'id': 34, 'name': 'ÇAYIRLI', 'base_pop': 264, 'jobs': 106, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 343}, {'id': 35, 'name': 'ÇERİKÖZÜ', 'base_pop': 342, 'jobs': 137, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 445}, {'id': 36, 'name': 'ÇİNİYERİ', 'base_pop': 557, 'jobs': 223, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 724}, {'id': 37, 'name': 'ÇUKURKÖY', 'base_pop': 129, 'jobs': 52, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 168}, {'id': 38, 'name': 'DAĞDERE', 'base_pop': 325, 'jobs': 130, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 422}, {'id': 39, 'name': 'DALLIK', 'base_pop': 316, 'jobs': 126, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 411}, {'id': 40, 'name': 'DEREBAŞI', 'base_pop': 840, 'jobs': 336, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 1092}, {'id': 41, 'name': 'DİBEKÇİ', 'base_pop': 76, 'jobs': 30, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 99}, {'id': 42, 'name': 'DOYRANLI', 'base_pop': 286, 'jobs': 114, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 372}, {'id': 43, 'name': 'DÜNDARLI', 'base_pop': 307, 'jobs': 123, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 399}, {'id': 44, 'name': 'ESKİOBA', 'base_pop': 481, 'jobs': 192, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 625}, {'id': 45, 'name': 'HİSARLIK', 'base_pop': 188, 'jobs': 75, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 244}, {'id': 46, 'name': 'IŞIKLAR', 'base_pop': 460, 'jobs': 184, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 598}, {'id': 47, 'name': 'IŞIKLI', 'base_pop': 742, 'jobs': 297, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 965}, {'id': 48, 'name': 'KAPLAN', 'base_pop': 108, 'jobs': 43, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 140}, {'id': 49, 'name': 'KARATEKE', 'base_pop': 558, 'jobs': 223, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 725}, {'id': 50, 'name': 'KİRELİ', 'base_pop': 669, 'jobs': 268, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 870}, {'id': 51, 'name': 'KÜÇÜKBURUN', 'base_pop': 143, 'jobs': 57, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 186}, {'id': 52, 'name': 'KÜÇÜKKEMERDERE', 'base_pop': 593, 'jobs': 237, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 771}, {'id': 53, 'name': 'KÜÇÜKKÖMÜRCÜ', 'base_pop': 120, 'jobs': 48, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 156}, {'id': 54, 'name': 'KÜRDÜLLÜ', 'base_pop': 282, 'jobs': 113, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 367}, {'id': 55, 'name': 'MAHMUTLAR', 'base_pop': 324, 'jobs': 130, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 421}, {'id': 56, 'name': 'MUSALAR', 'base_pop': 215, 'jobs': 86, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 280}, {'id': 57, 'name': 'ORTAKÖY', 'base_pop': 129, 'jobs': 52, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 168}, {'id': 58, 'name': 'SOMAK', 'base_pop': 187, 'jobs': 75, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 243}, {'id': 59, 'name': 'TOPALAK', 'base_pop': 161, 'jobs': 64, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 209}, {'id': 60, 'name': 'TOPARLAR', 'base_pop': 105, 'jobs': 42, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 136}, {'id': 61, 'name': 'TURGUTLU', 'base_pop': 141, 'jobs': 56, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 183}, {'id': 62, 'name': 'YAMANDERE', 'base_pop': 225, 'jobs': 90, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 292}, {'id': 63, 'name': 'YEMİŞLER', 'base_pop': 92, 'jobs': 37, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 120}, {'id': 64, 'name': 'YENİÇİFTLİK', 'base_pop': 523, 'jobs': 209, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 680}, {'id': 65, 'name': 'YENİOBA', 'base_pop': 233, 'jobs': 93, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 303}, {'id': 66, 'name': 'BÜYÜKKALE', 'base_pop': 463, 'jobs': 185, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 602}, {'id': 67, 'name': 'AKÇAŞEHİR', 'base_pop': 213, 'jobs': 85, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 277}, {'id': 68, 'name': 'AKYURT', 'base_pop': 366, 'jobs': 146, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 476}, {'id': 69, 'name': 'ALAYLI', 'base_pop': 224, 'jobs': 90, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 291}, {'id': 70, 'name': 'HALKAPINAR', 'base_pop': 159, 'jobs': 64, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 207}, {'id': 71, 'name': 'HASANÇAVUŞLAR', 'base_pop': 150, 'jobs': 60, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 195}, {'id': 72, 'name': 'KURŞAK', 'base_pop': 154, 'jobs': 62, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 200}, {'id': 73, 'name': 'KÜÇÜKKALE', 'base_pop': 212, 'jobs': 85, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 276}, {'id': 74, 'name': 'MEHMETLER', 'base_pop': 188, 'jobs': 75, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 244}, {'id': 75, 'name': 'ÜZÜMLER', 'base_pop': 169, 'jobs': 68, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 220}, {'id': 76, 'name': 'ÇOBANKÖY', 'base_pop': 260, 'jobs': 104, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 338}, {'id': 77, 'name': 'DERELİ', 'base_pop': 260, 'jobs': 104, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 338}, {'id': 78, 'name': 'EĞRİDERE', 'base_pop': 612, 'jobs': 245, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 796}, {'id': 79, 'name': 'KIRTEPE', 'base_pop': 439, 'jobs': 176, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 571}, {'id': 80, 'name': 'KIZILCAHAVLU', 'base_pop': 473, 'jobs': 189, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 615}, {'id': 81, 'name': 'KOCAALİLER', 'base_pop': 81, 'jobs': 32, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 105}, {'id': 82, 'name': 'OSMANCIK', 'base_pop': 257, 'jobs': 103, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 334}, {'id': 83, 'name': 'PEŞREFLİ', 'base_pop': 562, 'jobs': 225, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 731}, {'id': 84, 'name': 'SARILAR', 'base_pop': 506, 'jobs': 202, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 658}, {'id': 85, 'name': 'SARUHANLI', 'base_pop': 208, 'jobs': 83, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 270}, {'id': 86, 'name': 'YEĞENLİ', 'base_pop': 441, 'jobs': 176, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 573}, {'id': 87, 'name': 'YENİŞEHİR', 'base_pop': 106, 'jobs': 42, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 138}, {'id': 88, 'name': 'KAHRAT', 'base_pop': 1152, 'jobs': 461, 'capacity_ha': 5.0, 'distance_to_center_min': 5.0, 'plan_pop_capacity': 1498}]},

    "standart_kentsel_plan": {
        "id": "standart_kentsel_plan",
        "name": "Orta Ölçekli Kentsel Planlama Şablonu (65.000 Nüfus)",
        "category": "Sanayi & Tarım Odaklı Kentsel Plan",
        "base_year": 2025,
        "base_pop": 65395,
        "target_year_1": 2045,
        "target_pop_1": 85000,
        "target_year_2": 2050,
        "target_pop_2": 89500,
        "years_hist": [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        "pop_hist": [50757, 51433, 52187, 52899, 53823, 54746, 55653, 56586, 57421, 58342, 59281, 60195, 61084, 61922, 62788, 63654, 64521, 65395],
        "total_labour": 33365,
        "basic_labour": 6800,
        "new_industrial_jobs": 13000,
        "industrial_area_ha": 370.0,
        "workers_per_ha": 35.0,
        "tfr": 1.545,
        "annual_trend_mig": 300,
        "description": "Orta büyüklükte bir kent merkezi için 1/5000 Nazım İmar Planı projeksiyon şablonu. Sanayi gelişme alanı, iktisadi taban çarpanı ve hedef plan eşiği.",
        "subzones": [
            {"id": 1, "name": "Kuzey Gelişme Mahallesi", "base_pop": 11988, "jobs": 4200, "capacity_ha": 45.0, "plan_pop_capacity": 18000, "distance_to_center_min": 4.5},
            {"id": 2, "name": "Doğu Konut Mahallesi", "base_pop": 8683, "jobs": 3100, "capacity_ha": 25.0, "plan_pop_capacity": 12000, "distance_to_center_min": 3.0},
            {"id": 3, "name": "Batı Konut ve Donatı Mahallesi", "base_pop": 6153, "jobs": 2800, "capacity_ha": 35.0, "plan_pop_capacity": 10500, "distance_to_center_min": 5.0},
            {"id": 4, "name": "Yeni Gelişme Aksı (Toplu Konut)", "base_pop": 2719, "jobs": 800, "capacity_ha": 60.0, "plan_pop_capacity": 9000, "distance_to_center_min": 8.0},
            {"id": 5, "name": "Tarihi Merkez / Çekirdek Mahalleler", "base_pop": 35852, "jobs": 22465, "capacity_ha": 15.0, "plan_pop_capacity": 38000, "distance_to_center_min": 1.5}
        ]
    },
    "metropoliten_alt_bolge": {
        "id": "metropoliten_alt_bolge",
        "name": "Çok Merkezli Kentsel Havza Şablonu (290.000 Nüfus)",
        "category": "Bölgesel Gelişme ve Ulaşılabilirlik Sentezi",
        "base_year": 2023,
        "base_pop": 290882,
        "target_year_1": 2040,
        "target_pop_1": 530419,  # A0 Senaryosu
        "target_year_2": 2040,
        "target_pop_2": 601612,  # Amaks Senaryosu
        "years_hist": [2007, 2010, 2013, 2016, 2019, 2023],
        "pop_hist": [230500, 243100, 256800, 270900, 282400, 290882],
        "total_labour": 128000,
        "basic_labour": 38000,
        "new_industrial_jobs": 44000,
        "industrial_area_ha": 1250.0,
        "workers_per_ha": 35.0,
        "tfr": 1.52,
        "annual_trend_mig": 3500,
        "description": "Liman, ağır sanayi, tarım ve turizm odaklı alt merkezlerden oluşan çok merkezli kentsel bölge şablonu (Hansen mekânsal dağıtım modeli).",
        "subzones": [
            {"id": 1, "name": "Liman & Ağır Sanayi Alt Merkezi", "base_pop": 106167, "jobs": 52000, "capacity_ha": 180.0, "plan_pop_capacity": 175000, "distance_to_center_min": 10.0},
            {"id": 2, "name": "Hizmet, Kültür & OSB Alt Merkezi", "base_pop": 107132, "jobs": 48000, "capacity_ha": 260.0, "plan_pop_capacity": 280000, "distance_to_center_min": 25.0},
            {"id": 3, "name": "Kıyı & Turizm Alt Merkezi", "base_pop": 48379, "jobs": 17000, "capacity_ha": 120.0, "plan_pop_capacity": 95000, "distance_to_center_min": 35.0},
            {"id": 4, "name": "Kırsal & Tarımsal İhtisas Alt Merkezi", "base_pop": 29204, "jobs": 11000, "capacity_ha": 90.0, "plan_pop_capacity": 55000, "distance_to_center_min": 40.0}
        ]
    },
    "hizli_buyuyen_sanayi": {
        "id": "hizli_buyuyen_sanayi",
        "name": "Hızlı Büyüyen Ağır Sanayi ve Lojistik Kenti (200.000 Nüfus)",
        "category": "Yüksek Göç ve Sanayi Odaklı Gelişme",
        "base_year": 2025,
        "base_pop": 207500,
        "target_year_1": 2045,
        "target_pop_1": 315000,
        "target_year_2": 2050,
        "target_pop_2": 340000,
        "years_hist": [2007, 2010, 2013, 2016, 2019, 2022, 2024],
        "pop_hist": [121990, 133037, 144293, 164981, 185908, 201476, 207500],
        "total_labour": 98000,
        "basic_labour": 21000,
        "new_industrial_jobs": 25000,
        "industrial_area_ha": 650.0,
        "workers_per_ha": 38.0,
        "tfr": 1.62,
        "annual_trend_mig": 2200,
        "description": "Organize sanayi bölgeleri, lojistik üsler ve banliyö/raylı sistem entegrasyonuyla hızla büyüyen kentsel merkez şablonu.",
        "subzones": [
            {"id": 1, "name": "Merkez Kentsel Bölge", "base_pop": 85000, "jobs": 42000, "capacity_ha": 120.0, "plan_pop_capacity": 140000, "distance_to_center_min": 5.0},
            {"id": 2, "name": "Metropol Eşiği Gelişme Aksı", "base_pop": 65000, "jobs": 28000, "capacity_ha": 150.0, "plan_pop_capacity": 110000, "distance_to_center_min": 12.0},
            {"id": 3, "name": "OSB & Sanayi Yerleşimi", "base_pop": 18000, "jobs": 19000, "capacity_ha": 80.0, "plan_pop_capacity": 35000, "distance_to_center_min": 15.0},
            {"id": 4, "name": "Kırsal Yerleşim Kuşağı", "base_pop": 39500, "jobs": 9000, "capacity_ha": 40.0, "plan_pop_capacity": 55000, "distance_to_center_min": 25.0}
        ]
    },
    "tarimsal_havza": {
        "id": "tarimsal_havza",
        "name": "Tarımsal Havza ve Kırsal Merkez Şablonu (130.000 Nüfus)",
        "category": "Tarımsal Havza / Durgun Demografi",
        "base_year": 2025,
        "base_pop": 132700,
        "target_year_1": 2045,
        "target_pop_1": 142000,
        "target_year_2": 2050,
        "target_pop_2": 144500,
        "years_hist": [2007, 2010, 2013, 2016, 2019, 2022, 2024],
        "pop_hist": [128259, 129210, 129295, 131342, 132876, 132740, 132700],
        "total_labour": 58000,
        "basic_labour": 11500,
        "new_industrial_jobs": 2500,
        "industrial_area_ha": 80.0,
        "workers_per_ha": 30.0,
        "tfr": 1.48,
        "annual_trend_mig": 80,
        "description": "Verimli tarım havzası. Düşük göç, yaşlanan nüfus yapısı ve kentsel doygunluk özellikleri içeren şablon.",
        "subzones": [
            {"id": 1, "name": "Kent Merkezi", "base_pop": 82000, "jobs": 38000, "capacity_ha": 70.0, "plan_pop_capacity": 95000, "distance_to_center_min": 4.0},
            {"id": 2, "name": "Tarihi & Kırsal Kuşak", "base_pop": 18000, "jobs": 6000, "capacity_ha": 20.0, "plan_pop_capacity": 22000, "distance_to_center_min": 15.0},
            {"id": 3, "name": "Ova Köyleri & Tarımsal Odaklar", "base_pop": 32700, "jobs": 14000, "capacity_ha": 30.0, "plan_pop_capacity": 38000, "distance_to_center_min": 22.0}
        ]
    },
    "ozel_alan": {
        "id": "ozel_alan",
        "name": "⚙️ Özel Kullanıcı Tanımlı Çalışma Alanı (Serbest Giriş)",
        "category": "Kullanıcı Tanımlı",
        "base_year": 2025,
        "base_pop": 50000,
        "target_year_1": 2045,
        "target_pop_1": 70000,
        "target_year_2": 2050,
        "target_pop_2": 75000,
        "years_hist": [2010, 2015, 2020, 2024],
        "pop_hist": [40000, 44000, 47500, 50000],
        "total_labour": 24000,
        "basic_labour": 5500,
        "new_industrial_jobs": 5000,
        "industrial_area_ha": 150.0,
        "workers_per_ha": 33.0,
        "tfr": 1.55,
        "annual_trend_mig": 400,
        "description": "Herhangi bir şehir, ilçe, imar planlama sınırı veya bölgesel araştırma alanı için serbestçe özelleştirilebilir şablon.",
        "subzones": [
            {"id": 1, "name": "Kentsel Merkez", "base_pop": 32000, "jobs": 17000, "capacity_ha": 40.0, "plan_pop_capacity": 42000, "distance_to_center_min": 3.0},
            {"id": 2, "name": "Gelişme Alanı 1", "base_pop": 11000, "jobs": 4500, "capacity_ha": 65.0, "plan_pop_capacity": 25000, "distance_to_center_min": 8.0},
            {"id": 3, "name": "Gelişme Alanı 2", "base_pop": 7000, "jobs": 2500, "capacity_ha": 50.0, "plan_pop_capacity": 18000, "distance_to_center_min": 12.0}
        ]
    }
}
