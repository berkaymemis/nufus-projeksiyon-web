# -*- coding: utf-8 -*-
"""
Academic Citations & ResearchGate References
Prof. Dr. K. Mert Çubukçu — Dokuz Eylül Üniversitesi Mimarlık Fakültesi Şehir ve Bölge Planlama Bölümü
Başvuru Eserleri, Ders Notları ve Metodolojik Referanslar
"""

from typing import Dict, Any, List


CUBUKCU_CITATIONS = {
    "author": "Prof. Dr. K. Mert Çubukçu",
    "affiliation": "Dokuz Eylül Üniversitesi, Mimarlık Fakültesi, Şehir ve Bölge Planlama Bölümü",
    "researchgate_url": "https://www.researchgate.net/profile/K-Mert-Cubukcu",
    "books": [
        {
            "title": "Planlamada Klasik Sayısal Yöntemler",
            "publisher": "Nobel Akademik Yayıncılık / ODTÜ Geliştirme Vakfı Yayıncılık",
            "year": "2018 / 2022",
            "isbn": "978-605-247-000-0",
            "chapters": [
                "Bölüm 1: Ekstrapolasyon Nüfus Projeksiyon Yöntemleri (Matematiksel Modeller)",
                "Bölüm 2: Kuşak-Bileşenleri (Cohort-Component) Nüfus Projeksiyon Tekniği",
                "Bölüm 3: İşgücü ve Ekonomik Aktivite Analiz Teknikleri (İktisadi Taban / Baz Çarpanı)",
                "Bölüm 4: Hansen Erişilebilirlik ve Yer Seçimi Modelleri",
                "Bölüm 5: Karar Ağacı, Doğrusal Programlama ve Oyun Teorisi"
            ],
            "description": "Şehir ve bölge planlama pratiğinde 1960'lardan bugüne kullanılan temel analitik yöntemleri basamak atlamadan, çözümlü kentsel örneklerle aktaran başvuru kitabı."
        }
    ],
    "selected_papers": [
        {
            "title": "The spatial distribution of economic base multipliers: A GIS and spatial statistics-based cluster analysis",
            "venue": "ITU Journal, 8(2), 49-62",
            "year": "2011",
            "topic": "Türkiye genelindeki tüm ilçelerin Konum Katsayısı (LQ) ve Minimum Gereksinimler (MG) yöntemleriyle hesaplanmış iktisadi taban çarpanları (Base Multipliers) ve mekânsal kümelenme analizi."
        },
        {
            "title": "Kuzey İzmir Mekânsal Gelişme Perspektifi (KUZİP) Sentez Raporu",
            "venue": "Dokuz Eylül Üniversitesi & İzmir Kalkınma Ajansı (İZKA)",
            "year": "2026",
            "topic": "Sıfır göç (kapalı demografi), trend göç, A0 (Muhtemel Gelişim) ve Amaks (Azami Gelişim) senaryoları; Hansen çekim modeliyle 45 bölgeciğe nüfus dağıtımı ve plan doluluk oranları."
        },
        {
            "title": "Türkiye Yerleşimler Sistemini Anlama, Kavrama ve Çözümleme Projesi (YER-SİS)",
            "venue": "Sanayi ve Teknoloji Bakanlığı / Kalkınma Ajansları Genel Müdürlüğü Araştırma Raporu",
            "year": "2021",
            "topic": "Türkiye genelindeki tüm kentsel ve kırsal yerleşimlerin iş gücü, göç ve sosyoekonomik kademelenmesi."
        }
    ]
}


EXPLANATION_TEXTS = {
    "economic_base_box": (
        "<b>İktisadi Taban (Economic Base Multiplier) ve İş Gücüne Bağlı Göç Metodolojisi:</b><br/>"
        "• <i>Temel İstihdam (Eb):</i> Kent dışına ihracat yapan sanayi, lojistik ve ihtisas hizmetleridir.<br/>"
        "• <i>Baz Çarpanı (k = Et / Eb):</i> Her 1 temel sanayi çalışanının kentte tetiklediği toplam istihdam katsayısıdır.<br/>"
        "• <i>Demografik Bağımlılık (b = P / Et):</i> 1 çalışan başına düşen kentsel nüfus yükünü ifade eder.<br/>"
        "• <i>Sanayi Yatırımı Kaynaklı Göç:</i> <code>ΔP = (ΔEb × k) × b</code> formülüyle hesaplanır. Yeni sanayi alanı "
        "büyüklüğü (Ha) × çalışan yoğunluğu ile yeni temel istihdam bulunur ve doğrudan nüfus projeksiyonuna entegre edilir."
    ),
    "cohort_component_box": (
        "<b>Kuşak Bileşenleri (Cohort-Component) Modeli:</b><br/>"
        "• Demografik planlamanın altın standardıdır. Kentin nüfusunu 5'er yıllık yaş ve cinsiyet kohortlarına (0-4, 5-9 ... 80+) ayırır.<br/>"
        "• <i>Ölümlülük (Sx):</i> TÜİK/WHO Yaşam Tabloları ile her kohortun bir sonraki yaş basamağına geçişi hesaplanır.<br/>"
        "• <i>Doğurganlık (ASFR):</i> 15-49 yaş arasındaki kadınların yaşa özel doğurganlık hızları ile yeni doğan 0-4 yaş grubu üretilir.<br/>"
        "• <i>Göç:</i> Yaş profilli olarak doğrudan çalışma çağındaki genç nüfus basamaklarına eklenir."
    ),
    "demographic_shocks_box": (
        "<b>Yıllara Özel Demografik Şoklar (Shock Events):</b><br/>"
        "• Planlama sürecinde nüfusun yalnızca pürüzsüz matematiksel eğrilerle değil, kentsel kırılmalarla değiştiği gerçeğini modeller.<br/>"
        "• <i>Pozitif Şoklar:</i> Yeni OSB etabı, demiryolu/otoyol bağlantısı, üniversite kampüsü veya afet sonrası güvenli kente sığınma.<br/>"
        "• <i>Negatif Şoklar:</i> Sanayi tesisi kapanışı, ekonomik kriz, tarımsal kuraklık veya afet göçü.<br/>"
        "• Şoklar belirli bir yıldan itibaren kümülatif olarak devreye girer ve yaş kohortlarına ağırlıklı olarak dağıtılır."
    ),
    "curve_fitting_box": (
        "<b>Matematiksel Ekstrapolasyon (Eğri Uydurma) Yöntemleri:</b><br/>"
        "• Geçmiş ADNKS nüfus serilerine Doğrusal, 2. ve 3. Derece Polinom, Üstel, Logaritmik ve Kuvvet eğrileri uydurulur.<br/>"
        "• Modeller Hata Kareleri Toplamı (SSE), RMSE ve Belirlilik Katsayısı (R²) metrikleriyle denetlenir.<br/>"
        "• <i>Uyarı:</i> 3. Derece Polinom geçmişe çok yüksek uyum gösterse bile ileriye dönük parabolik çöküş veya patlama üretebilir; "
        "plan kararlarında Doğrusal veya 2. Derece Polinom gibi istikrarlı eğriler Kuşak-Bileşen modeliyle mutabakat halinde seçilmelidir."
    )
}
