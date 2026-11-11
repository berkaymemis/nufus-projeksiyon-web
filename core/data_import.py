# -*- coding: utf-8 -*-
"""
Data Import & Excel/CSV Reader Engine
Kentsel Mahalle, İlçe ve Geçmiş Nüfus Verilerini İçe Aktarma Motoru
Herhangi bir şehir, ilçe veya çalışma alanı için Excel (.xlsx) ve CSV entegrasyonu
"""

import os, re, csv
from typing import Dict, Any, List, Optional
try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False
    openpyxl = None


def normalize_col_name(name: str) -> str:
    """Türkçe karakterleri ve boşlukları temizleyerek karşılaştırma için normalize eder."""
    if not name:
        return ""
    text = str(name).strip().lower()
    rep = {
        'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
        'İ': 'i', 'Ğ': 'g', 'Ü': 'u', 'Ş': 's', 'Ö': 'o', 'Ç': 'c'
    }
    for tr, en in rep.items():
        text = text.replace(tr, en)
    text = re.sub(r'[^a-z0-9]', '', text)
    return text


class DataImportEngine:
    """
    Excel ve CSV formatındaki mahalle/ilçe nüfus ve imar verilerini okuyup
    demografik modeller için standart veri yapısına dönüştüren motor.
    """

    @staticmethod
    def generate_blank_template(filepath: str) -> str:
        """
        Kullanıcıların kendi şehir/mahalle verilerini doldurabilmesi için
        hazır, formatlı ve açıklamalı örnek Excel şablonu üretir.
        """
        wb = openpyxl.Workbook()

        # Stiller
        FONT_TITLE = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
        FONT_TH = Font(name="Segoe UI", size=9.5, bold=True, color="FFFFFF")
        FONT_DATA = Font(name="Segoe UI", size=9.5)
        FONT_BOLD = Font(name="Segoe UI", size=9.5, bold=True)
        FILL_NAVY = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
        FILL_BLUE = PatternFill(start_color="2563EB", end_color="2563EB", fill_type="solid")
        FILL_GREEN = PatternFill(start_color="059669", end_color="059669", fill_type="solid")
        FILL_ZEBRA = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
        BORDER_THIN = Border(
            left=Side(style='thin', color='CBD5E1'), right=Side(style='thin', color='CBD5E1'),
            top=Side(style='thin', color='CBD5E1'), bottom=Side(style='thin', color='CBD5E1')
        )

        # SAYFA 1: Mahalle ve Alt Bölge Verileri
        ws1 = wb.active
        ws1.title = "1_Mahalle_Verileri"
        ws1.views.sheetView[0].showGridLines = True

        ws1.merge_cells("A1:F1")
        ws1["A1"] = "KENTSEL ÇALIŞMA ALANI MAHALLE / ALT BÖLGE VERİ GİRİŞ TABLOSU"
        ws1["A1"].font = FONT_TITLE
        ws1["A1"].fill = FILL_NAVY
        ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
        ws1.row_dimensions[1].height = 26

        headers1 = [
            ("A3", "Mahalle / Bölge Adı", 28),
            ("B3", "Mevcut Nüfus (Kişi)", 20),
            ("C3", "İstihdam / Çalışan (İşgücü)", 24),
            ("D3", "Boş Gelişme Alanı (Ha)", 22),
            ("E3", "Merkeze Mesafe (Dakika)", 24),
            ("F3", "Plan Nüfus Kapasitesi (Kişi)", 26),
        ]

        for cell_ref, text, width in headers1:
            cell = ws1[cell_ref]
            cell.value = text
            cell.font = FONT_TH
            cell.fill = FILL_BLUE
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = BORDER_THIN
            col_letter = cell_ref[0]
            ws1.column_dimensions[col_letter].width = width
        ws1.row_dimensions[3].height = 24

        sample_subzones = [
            ("Fatih Mahallesi", 11988, 4200, 45.0, 4.5, 18000),
            ("Hürriyet Mahallesi", 8683, 3100, 25.0, 3.0, 12000),
            ("Atatürk Mahallesi", 6153, 2800, 35.0, 5.0, 10500),
            ("Yeni Gelişme Aksı", 2719, 800, 60.0, 8.0, 9000),
            ("Tarihi Merkez / Çekirdek Mahalleler", 35852, 22465, 15.0, 1.5, 38000),
        ]

        for r_idx, row in enumerate(sample_subzones, start=4):
            for c_idx, val in enumerate(row, start=1):
                c = ws1.cell(row=r_idx, column=c_idx, value=val)
                c.font = FONT_DATA
                c.border = BORDER_THIN
                if c_idx == 1:
                    c.alignment = Alignment(horizontal="left", vertical="center")
                elif c_idx in [2, 3, 6]:
                    c.alignment = Alignment(horizontal="right", vertical="center")
                    c.number_format = "#,##0"
                else:
                    c.alignment = Alignment(horizontal="right", vertical="center")
                    c.number_format = "#,##0.0"
                if r_idx % 2 == 1:
                    c.fill = FILL_ZEBRA
            ws1.row_dimensions[r_idx].height = 20

        # SAYFA 2: Geçmiş Yıllar Nüfus Serisi (Curve Fitting İçin)
        ws2 = wb.create_sheet(title="2_Gecmis_Nufus_Serisi")
        ws2.views.sheetView[0].showGridLines = True

        ws2.merge_cells("A1:B1")
        ws2["A1"] = "GEÇMİŞ YILLIK NÜFUS SERİSİ (TÜİK ADNKS)"
        ws2["A1"].font = FONT_TITLE
        ws2["A1"].fill = FILL_NAVY
        ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")
        ws2.row_dimensions[1].height = 26

        ws2["A3"] = "Yıl (Takvim Yılı)"
        ws2["A3"].font = FONT_TH
        ws2["A3"].fill = FILL_GREEN
        ws2["A3"].alignment = Alignment(horizontal="center", vertical="center")
        ws2["A3"].border = BORDER_THIN
        ws2.column_dimensions["A"].width = 18

        ws2["B3"] = "Toplam Kentsel Nüfus (Kişi)"
        ws2["B3"].font = FONT_TH
        ws2["B3"].fill = FILL_GREEN
        ws2["B3"].alignment = Alignment(horizontal="center", vertical="center")
        ws2["B3"].border = BORDER_THIN
        ws2.column_dimensions["B"].width = 28
        ws2.row_dimensions[3].height = 22

        hist_sample = [
            (2015, 57421), (2016, 58342), (2017, 59281), (2018, 60195),
            (2019, 61084), (2020, 61922), (2021, 62788), (2022, 63654),
            (2023, 64521), (2024, 65395)
        ]

        for r_idx, (y, p) in enumerate(hist_sample, start=4):
            cy = ws2.cell(row=r_idx, column=1, value=y)
            cy.font = FONT_DATA
            cy.alignment = Alignment(horizontal="center", vertical="center")
            cy.border = BORDER_THIN

            cp = ws2.cell(row=r_idx, column=2, value=p)
            cp.font = FONT_DATA
            cp.alignment = Alignment(horizontal="right", vertical="center")
            cp.number_format = "#,##0"
            cp.border = BORDER_THIN
            if r_idx % 2 == 1:
                cy.fill = FILL_ZEBRA
                cp.fill = FILL_ZEBRA
            ws2.row_dimensions[r_idx].height = 19

        # SAYFA 3: Kullanım Rehberi
        ws3 = wb.create_sheet(title="3_Kullanim_Rehberi")
        ws3.views.sheetView[0].showGridLines = True
        ws3.column_dimensions["A"].width = 4
        ws3.column_dimensions["B"].width = 85

        ws3["B2"] = "📖 URBAN DEMOGRAPHICS PRO — EXCEL VERİ GİRİŞİ REHBERİ"
        ws3["B2"].font = FONT_TITLE
        ws3["B2"].fill = FILL_NAVY
        ws3.row_dimensions[2].height = 26

        guides = [
            "1. İstediğiniz herhangi bir ilçe veya kentsel plan sınırına ait mahalleleri '1_Mahalle_Verileri' sayfasına yapıştırabilirsiniz.",
            "2. 'Mahalle / Bölge Adı' ve 'Mevcut Nüfus' sütunları zorunludur.",
            "3. İstihdam, Boş Gelişme Alanı ve Mesafe sütunlarını boş bırakırsanız eklenti standart kentsel ortalamaları otomatik hesaplar.",
            "4. Eğer '2_Gecmis_Nufus_Serisi' sayfasına geçmiş yıllara ait toplam nüfusları girerseniz, Curve Fitting eğrileri otomatik hesaplanır.",
            "5. Dosyayı kaydedip eklentideki 'Excel Dosyası Yükle' butonu ile seçtiğinizde tüm projeksiyon anında güncellenir!"
        ]
        for idx, g in enumerate(guides, start=4):
            c = ws3.cell(row=idx, column=2, value=g)
            c.font = FONT_DATA
            ws3.row_dimensions[idx].height = 20

        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        wb.save(filepath)
        return filepath

    @staticmethod
    def load_from_excel(filepath: str) -> Dict[str, Any]:
        """
        Kullanıcının yüklediği herhangi bir Excel dosyasını akıllıca okur.
        TÜİK ADNKS mahalle tablolarını veya şablon dosyalarını ayrıştırır.
        """
        wb = openpyxl.load_workbook(filepath, data_only=True)
        subzones = []
        years_hist = []
        pop_hist = []
        area_name = os.path.splitext(os.path.basename(filepath))[0]

        # 1. Mahalle Verilerini Arama
        sheet_subzones = None
        for sname in wb.sheetnames:
            norm_s = normalize_col_name(sname)
            if any(k in norm_s for k in ["mahalle", "bolge", "subzone", "yerlesim", "veri"]):
                sheet_subzones = wb[sname]
                break
        if sheet_subzones is None:
            sheet_subzones = wb.active

        # Başlık satırını bul (En az 2 dolu hücreye sahip ve isim+metrik içeren satır)
        header_row_idx = None
        headers = []
        for r_idx in range(1, min(35, sheet_subzones.max_row + 1)):
            row_vals = [sheet_subzones.cell(row=r_idx, column=c).value for c in range(1, sheet_subzones.max_column + 1)]
            non_empty = [v for v in row_vals if v is not None and str(v).strip()]
            if len(non_empty) < 2:
                continue
            row_norm = [normalize_col_name(v) for v in non_empty]
            has_name = any(any(k in v for k in ["mahalle", "bolge", "yerlesim", "koy"]) for v in row_norm)
            has_metric = any(any(k in v for k in ["geneltoplam", "toplam", "nufus", "pop", "kayitno", "ilceadi", "mevcut", "istihdam", "202", "201", "200"]) for v in row_norm)
            if has_name and has_metric:
                header_row_idx = r_idx
                headers = row_vals
                break
            if any("mahalle" in v for v in row_norm) and any(any(k in v for k in ["nufus", "pop", "mevcut"]) for v in row_norm):
                header_row_idx = r_idx
                headers = row_vals
                break

        if header_row_idx is not None:
            col_map = {}
            year_cols = []  # Eğer sütunlar yıl ise: (col_idx, year_int)

            # Mahalle Adı Sütunu (Öncelik: mahalle+adı > mahalle (kod/nitelik hariç) > yerleşim+adı)
            for c_idx, h in enumerate(headers, start=1):
                if not h: continue
                nh = normalize_col_name(h)
                if "mahalle" in nh and any(k in nh for k in ["adi", "ad", "name"]):
                    col_map["name"] = c_idx
                    break
            if "name" not in col_map:
                for c_idx, h in enumerate(headers, start=1):
                    if not h: continue
                    nh = normalize_col_name(h)
                    if "mahalle" in nh and not any(k in nh for k in ["kayit", "kod", "id", "no", "nitelik"]):
                        col_map["name"] = c_idx
                        break
            if "name" not in col_map:
                for c_idx, h in enumerate(headers, start=1):
                    if not h: continue
                    nh = normalize_col_name(h)
                    if any(k in nh for k in ["yerlesim", "koy", "bolge"]) and any(k in nh for k in ["adi", "ad", "name"]):
                        col_map["name"] = c_idx
                        break
            if "name" not in col_map:
                col_map["name"] = 1

            # Nüfus Sütunu (Öncelik: geneltoplam > toplamnufus / mevcutnufus > nufus / pop / toplam)
            for c_idx, h in enumerate(headers, start=1):
                if not h: continue
                nh = normalize_col_name(h)
                if "geneltoplam" in nh:
                    col_map["pop"] = c_idx
                    break
                elif "toplamnufus" in nh or "mevcutnufus" in nh:
                    col_map["pop"] = c_idx
                    break
            if "pop" not in col_map:
                for c_idx, h in enumerate(headers, start=1):
                    if not h: continue
                    nh = normalize_col_name(h)
                    if nh in ["toplam", "nufus", "pop", "population"] and not any(k in nh for k in ["kayit", "kod", "no", "kapasite"]):
                        col_map["pop"] = c_idx
                        break

            # Diğer öznitelikler
            for c_idx, h in enumerate(headers, start=1):
                if not h:
                    continue
                norm_h = normalize_col_name(h)
                m_year = re.search(r'\b(20[0-3][0-9])\b', str(h))
                if m_year:
                    year_cols.append((c_idx, int(m_year.group(1))))

                if any(k in norm_h for k in ["istihdam", "isgucu", "calisan", "job", "employment"]):
                    col_map["jobs"] = c_idx
                elif any(k in norm_h for k in ["alan", "bosalan", "kapasiteha", "ha", "hektar"]):
                    col_map["area"] = c_idx
                elif any(k in norm_h for k in ["mesafe", "dakika", "dk", "uzaklik", "distance"]):
                    col_map["distance"] = c_idx
                elif any(k in norm_h for k in ["plankapasite", "plannufus", "kapasitesi"]):
                    col_map["plan_cap"] = c_idx
                elif "ilceadi" in norm_h or norm_h == "ilce":
                    col_map["ilce"] = c_idx
                elif "iladi" in norm_h or norm_h == "il":
                    col_map["il"] = c_idx

            # Alt başlık kontrolü (Örn: TOPLAM, ERKEK, KADIN)
            start_row = header_row_idx + 1
            if header_row_idx + 1 <= sheet_subzones.max_row:
                sub_vals = [normalize_col_name(sheet_subzones.cell(row=header_row_idx + 1, column=c).value) for c in range(1, sheet_subzones.max_column + 1)]
                if any(x in ["toplam", "erkek", "kadin"] for x in sub_vals):
                    start_row = header_row_idx + 2

            # Yıl sütunları sıralaması
            year_cols.sort(key=lambda x: x[1])
            year_totals = {y: 0 for _, y in year_cols}
            blacklist = ["aciklama", "kayitno", "toplam", "geneltoplam", "organize", "31aralik", "genisyas", "mevzuat"]

            # Veri Satırlarını Oku
            for r in range(start_row, sheet_subzones.max_row + 1):
                c_name_idx = col_map.get("name", 1)
                name_val = sheet_subzones.cell(row=r, column=c_name_idx).value
                if not name_val:
                    continue
                s_name = str(name_val).strip()
                norm_name = normalize_col_name(s_name)
                if any(b in norm_name for b in blacklist):
                    continue
                if re.match(r'^\d+$', s_name):
                    continue
                if len(re.findall(r'[a-zA-ZğüşıöçĞÜŞİÖÇ]', s_name)) < 2:
                    continue

                # İlçe Adı tespit edilirse çalışma alanı adını güncelle
                if "ilce" in col_map:
                    v_ilce = sheet_subzones.cell(row=r, column=col_map["ilce"]).value
                    if v_ilce and str(v_ilce).strip():
                        area_name = str(v_ilce).strip()
                        if "il" in col_map:
                            v_il = sheet_subzones.cell(row=r, column=col_map["il"]).value
                            if v_il and str(v_il).strip():
                                area_name += f" ({str(v_il).strip()})"

                # Nüfus değeri: Belirlenen pop sütunu veya en son yıl sütunu
                p_val = 0
                if "pop" in col_map:
                    raw_p = sheet_subzones.cell(row=r, column=col_map["pop"]).value
                    try:
                        p_val = int(float(str(raw_p).replace('.', '').replace(',', '.')))
                    except Exception:
                        p_val = 0
                elif year_cols:
                    latest_col, _ = year_cols[-1]
                    raw_p = sheet_subzones.cell(row=r, column=latest_col).value
                    try:
                        p_val = int(float(str(raw_p).replace('.', '').replace(',', '.')))
                    except Exception:
                        p_val = 0

                # Yıl toplamlarını biriktir
                for c_idx, y in year_cols:
                    val_y = sheet_subzones.cell(row=r, column=c_idx).value
                    try:
                        year_totals[y] += int(float(str(val_y).replace('.', '').replace(',', '.')))
                    except Exception:
                        pass

                # İstihdam
                jobs_val = int(round(p_val * 0.40))
                if "jobs" in col_map:
                    raw_j = sheet_subzones.cell(row=r, column=col_map["jobs"]).value
                    try:
                        jobs_val = int(float(str(raw_j).replace('.', '').replace(',', '.')))
                    except Exception:
                        pass

                # Alan (Ha)
                area_val = round(max(5.0, p_val * 0.003), 1)
                if "area" in col_map:
                    raw_a = sheet_subzones.cell(row=r, column=col_map["area"]).value
                    try:
                        area_val = float(str(raw_a).replace(',', '.'))
                    except Exception:
                        pass

                # Mesafe
                dist_val = 5.0
                if "distance" in col_map:
                    raw_d = sheet_subzones.cell(row=r, column=col_map["distance"]).value
                    try:
                        dist_val = float(str(raw_d).replace(',', '.'))
                    except Exception:
                        pass

                # Plan Kapasitesi
                plan_cap_val = int(round(p_val * 1.30))
                if "plan_cap" in col_map:
                    raw_pc = sheet_subzones.cell(row=r, column=col_map["plan_cap"]).value
                    try:
                        plan_cap_val = int(float(str(raw_pc).replace('.', '').replace(',', '.')))
                    except Exception:
                        pass

                subzones.append({
                    "id": len(subzones) + 1,
                    "name": str(name_val).strip(),
                    "base_pop": p_val,
                    "jobs": jobs_val,
                    "capacity_ha": area_val,
                    "distance_to_center_min": dist_val,
                    "plan_pop_capacity": plan_cap_val
                })

            if year_cols:
                years_hist = [y for _, y in year_cols]
                pop_hist = [year_totals[y] for y in years_hist]

        # 2. Eğer ayrı bir Geçmiş Nüfus Sayfası varsa oku
        for sname in wb.sheetnames:
            norm_s = normalize_col_name(sname)
            if any(k in norm_s for k in ["gecmis", "tarih", "adnks", "seri", "trend"]):
                ws_h = wb[sname]
                y_list, p_list = [], []
                for r in range(2, ws_h.max_row + 1):
                    v_y = ws_h.cell(row=r, column=1).value
                    v_p = ws_h.cell(row=r, column=2).value
                    try:
                        y_int = int(float(str(v_y).strip()))
                        p_int = int(float(str(v_p).replace('.', '').replace(',', '.')))
                        if 1950 <= y_int <= 2035 and p_int > 0:
                            y_list.append(y_int)
                            p_list.append(p_int)
                    except Exception:
                        continue
                if len(y_list) >= 3:
                    years_hist = y_list
                    pop_hist = p_list
                break

        # Toplam Nüfus ve İstihdam Hesabı
        tot_pop = sum(sz["base_pop"] for sz in subzones)
        tot_jobs = sum(sz["jobs"] for sz in subzones)

        # Eğer geçmiş nüfus bulunamadıysa sentetik geçmiş oluştur
        if len(years_hist) < 3 and tot_pop > 0:
            years_hist = [2015, 2017, 2019, 2021, 2023, 2024]
            pop_hist = [
                int(round(tot_pop * 0.88)),
                int(round(tot_pop * 0.91)),
                int(round(tot_pop * 0.94)),
                int(round(tot_pop * 0.96)),
                int(round(tot_pop * 0.985)),
                tot_pop
            ]

        latest_year = years_hist[-1] if years_hist else 2025
        t1_year = latest_year + 20
        t2_year = latest_year + 25

        return {
            "id": "imported_area",
            "name": f"{area_name} (İçe Aktarılan Alan)",
            "category": f"Kullanıcı Verisi ({len(subzones)} Mahalle / Bölge)",
            "base_year": latest_year,
            "base_pop": tot_pop if tot_pop > 0 else (pop_hist[-1] if pop_hist else 50000),
            "target_year_1": t1_year,
            "target_pop_1": int(round((tot_pop if tot_pop > 0 else 50000) * 1.30)),
            "target_year_2": t2_year,
            "target_pop_2": int(round((tot_pop if tot_pop > 0 else 50000) * 1.38)),
            "years_hist": years_hist,
            "pop_hist": pop_hist,
            "total_labour": tot_jobs if tot_jobs > 0 else int(round(tot_pop * 0.45)),
            "basic_labour": int(round((tot_jobs if tot_jobs > 0 else int(round(tot_pop * 0.45))) * 0.22)),
            "new_industrial_jobs": int(round(tot_pop * 0.15)),
            "industrial_area_ha": round(max(30.0, tot_pop * 0.004), 1),
            "workers_per_ha": 35.0,
            "tfr": 1.52,
            "annual_trend_mig": int(round(tot_pop * 0.005)),
            "description": f"Excel dosyasından içe aktarılan {len(subzones)} mahalle/bölge verisi.",
            "subzones": subzones
        }

    @staticmethod
    def load_from_csv(filepath: str) -> Dict[str, Any]:
        """
        CSV formatındaki mahalle listesini okur.
        Ayraç (virgül, noktalı virgül, tab) otomatik tespit edilir.
        """
        # İlk satırdan ayracı tahmin et
        delimiter = ','
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            first_line = f.readline()
            if ';' in first_line:
                delimiter = ';'
            elif '\t' in first_line:
                delimiter = '\t'

        subzones = []
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.reader(f, delimiter=delimiter)
            rows = list(reader)

        if not rows:
            return {"subzones": [], "base_pop": 0}

        # 1. Başlık satırını bul (Açıklama veya tek hücreli banner satırlarını atla, en az 2 dolu hücre)
        header_idx = -1
        for r_i, r in enumerate(rows[:35]):
            non_empty = [c for c in r if c.strip()]
            if len(non_empty) < 2:
                continue
            norm_r = [normalize_col_name(c) for c in r]
            has_m = any(any(k in c for k in ["mahalle", "bolge", "yerlesim", "koy"]) for c in norm_r)
            has_p = any(any(k in c for k in ["geneltoplam", "toplam", "nufus", "pop", "kayitno", "ilceadi", "mevcut", "istihdam", "202", "201", "200"]) for c in norm_r)
            if has_m and has_p:
                header_idx = r_i
                break
            if any("mahalle" in c for c in norm_r) and any(any(k in c for k in ["nufus", "pop", "mevcut"]) for c in norm_r):
                header_idx = r_i
                break

        if header_idx == -1:
            header_idx = 0

        header_row = rows[header_idx]
        sub_row = rows[header_idx + 1] if header_idx + 1 < len(rows) else []

        col_name = -1
        # Mahalle Adı Sütunu (Öncelik: mahalle+adı > mahalle (kod/nitelik hariç) > yerleşim+adı)
        for c_i, c in enumerate(header_row):
            nc = normalize_col_name(c)
            if "mahalle" in nc and any(k in nc for k in ["adi", "ad", "name"]):
                col_name = c_i
                break
        if col_name == -1:
            for c_i, c in enumerate(header_row):
                nc = normalize_col_name(c)
                if "mahalle" in nc and not any(k in nc for k in ["kayit", "kod", "id", "no", "nitelik"]):
                    col_name = c_i
                    break
        if col_name == -1:
            for c_i, c in enumerate(header_row):
                nc = normalize_col_name(c)
                if any(k in nc for k in ["yerlesim", "koy", "bolge"]) and any(k in nc for k in ["adi", "ad", "name"]):
                    col_name = c_i
                    break
        if col_name == -1:
            col_name = 0

        # Nüfus Sütunu
        col_pop = -1
        for c_i, c in enumerate(header_row):
            nc = normalize_col_name(c)
            if "geneltoplam" in nc or "toplamnufus" in nc or "mevcutnufus" in nc:
                col_pop = c_i
                break
        if col_pop == -1:
            for c_i, c in enumerate(header_row):
                nc = normalize_col_name(c)
                if nc in ["toplam", "nufus", "pop", "population"] and not any(k in nc for k in ["kayit", "kod", "no", "kapasite"]):
                    col_pop = c_i
                    break

        col_jobs, col_area, col_dist, col_plan_cap, col_ilce, col_il = -1, -1, -1, -1, -1, -1
        for c_i, c in enumerate(header_row):
            nc = normalize_col_name(c)
            if any(k in nc for k in ["istihdam", "isgucu", "calisan", "job"]):
                col_jobs = c_i
            elif any(k in nc for k in ["alan", "bosalan", "ha", "hektar"]):
                col_area = c_i
            elif any(k in nc for k in ["mesafe", "dakika", "dk", "uzaklik"]):
                col_dist = c_i
            elif any(k in nc for k in ["plankapasite", "kapasitesi"]):
                col_plan_cap = c_i
            elif "ilceadi" in nc or nc == "ilce":
                col_ilce = c_i
            elif "iladi" in nc or nc == "il":
                col_il = c_i

        start_row = header_idx + 1
        if sub_row and any(normalize_col_name(x) in ["toplam", "erkek", "kadin"] for x in sub_row):
            start_row = header_idx + 2

        blacklist = ["aciklama", "kayitno", "toplam", "geneltoplam", "organize", "31aralik", "genisyas", "mevzuat"]
        area_name = os.path.splitext(os.path.basename(filepath))[0]

        for r in rows[start_row:]:
            if not r or len(r) == 0:
                continue
            if col_name >= len(r) or not r[col_name].strip():
                continue
            s_name = r[col_name].strip()
            norm_name = normalize_col_name(s_name)
            if any(b in norm_name for b in blacklist):
                continue
            if re.match(r'^\d+$', s_name):
                continue
            if len(re.findall(r'[a-zA-ZğüşıöçĞÜŞİÖÇ]', s_name)) < 2:
                continue

            # Nüfus
            p_val = 0
            if col_pop != -1 and col_pop < len(r):
                try:
                    p_val = int(float(r[col_pop].replace('.', '').replace(',', '.').strip()))
                except Exception:
                    p_val = 0

            # İlçe ve İl Tespiti
            if col_ilce != -1 and col_ilce < len(r) and r[col_ilce].strip():
                v_ilce = r[col_ilce].strip()
                area_name = v_ilce
                if col_il != -1 and col_il < len(r) and r[col_il].strip():
                    area_name += f" ({r[col_il].strip()})"

            jobs_val = int(round(p_val * 0.40))
            if col_jobs != -1 and col_jobs < len(r):
                try:
                    jobs_val = int(float(r[col_jobs].replace('.', '').replace(',', '.').strip()))
                except Exception:
                    pass

            area_val = round(max(5.0, p_val * 0.003), 1)
            if col_area != -1 and col_area < len(r):
                try:
                    area_val = float(r[col_area].replace(',', '.').strip())
                except Exception:
                    pass

            dist_val = 5.0
            if col_dist != -1 and col_dist < len(r):
                try:
                    dist_val = float(r[col_dist].replace(',', '.').strip())
                except Exception:
                    pass

            plan_cap_val = int(round(p_val * 1.30))
            if col_plan_cap != -1 and col_plan_cap < len(r):
                try:
                    plan_cap_val = int(float(r[col_plan_cap].replace('.', '').replace(',', '.').strip()))
                except Exception:
                    pass

            subzones.append({
                "id": len(subzones) + 1,
                "name": s_name,
                "base_pop": p_val,
                "jobs": jobs_val,
                "capacity_ha": area_val,
                "distance_to_center_min": dist_val,
                "plan_pop_capacity": plan_cap_val
            })
        tot_pop = sum(sz["base_pop"] for sz in subzones)

        return {
            "id": "imported_csv_area",
            "name": f"{area_name} (CSV)",
            "category": f"Kullanıcı CSV Verisi ({len(subzones)} Mahalle)",
            "base_year": 2025,
            "base_pop": tot_pop if tot_pop > 0 else 50000,
            "target_year_1": 2045,
            "target_pop_1": int(round((tot_pop if tot_pop > 0 else 50000) * 1.30)),
            "target_year_2": 2050,
            "target_pop_2": int(round((tot_pop if tot_pop > 0 else 50000) * 1.38)),
            "years_hist": [2015, 2018, 2021, 2024],
            "pop_hist": [
                int(round(tot_pop * 0.88)), int(round(tot_pop * 0.92)),
                int(round(tot_pop * 0.96)), tot_pop
            ],
            "total_labour": sum(sz["jobs"] for sz in subzones),
            "basic_labour": int(round(sum(sz["jobs"] for sz in subzones) * 0.22)),
            "new_industrial_jobs": int(round(tot_pop * 0.15)),
            "industrial_area_ha": round(max(30.0, tot_pop * 0.004), 1),
            "workers_per_ha": 35.0,
            "tfr": 1.52,
            "annual_trend_mig": int(round(tot_pop * 0.005)),
            "description": f"CSV dosyasından içe aktarılan {len(subzones)} mahalle.",
            "subzones": subzones
        }

    @staticmethod
    def generate_blank_cohort_template(filepath: str) -> str:
        """Kullanıcının kentine ait yaş-cinsiyet kohort dağılımını girmesi için Excel şablonu üretir."""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Yas_Cinsiyet_Dagilimi"
        ws.views.sheetView[0].showGridLines = True

        FONT_TITLE = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
        FONT_TH = Font(name="Segoe UI", size=9.5, bold=True, color="FFFFFF")
        FONT_DATA = Font(name="Segoe UI", size=9.5)
        FILL_NAVY = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
        FILL_BLUE = PatternFill(start_color="2563EB", end_color="2563EB", fill_type="solid")
        BORDER_THIN = Border(
            left=Side(style='thin', color='CBD5E1'), right=Side(style='thin', color='CBD5E1'),
            top=Side(style='thin', color='CBD5E1'), bottom=Side(style='thin', color='CBD5E1')
        )

        ws.merge_cells("A1:D1")
        ws["A1"] = "TÜİK ADNKS YAŞ VE CİNSİYET KOHORTLARI VERİ GİRİŞİ (17 YAŞ GRUBU)"
        ws["A1"].font = FONT_TITLE
        ws["A1"].fill = FILL_NAVY
        ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[1].height = 25

        headers = ["Yaş Grubu", "Erkek Nüfus", "Kadın Nüfus", "Toplam (Formül)"]
        for col_idx, h in enumerate(headers, 1):
            cell = ws.cell(row=3, column=col_idx, value=h)
            cell.font = FONT_TH
            cell.fill = FILL_BLUE
            cell.alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[3].height = 22

        age_groups = [
            "0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39",
            "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+"
        ]
        sample_m = [1800, 1950, 2100, 2200, 2350, 2500, 2600, 2500, 2350, 2250, 2150, 2000, 1750, 1500, 1250, 900, 750]
        sample_f = [1700, 1850, 2050, 2150, 2300, 2450, 2550, 2400, 2300, 2200, 2100, 1950, 1700, 1450, 1200, 880, 720]

        for idx, ag in enumerate(age_groups, 4):
            c_ag = ws.cell(row=idx, column=1, value=ag)
            c_m = ws.cell(row=idx, column=2, value=sample_m[idx - 4])
            c_f = ws.cell(row=idx, column=3, value=sample_f[idx - 4])
            c_tot = ws.cell(row=idx, column=4, value=f"=B{idx}+C{idx}")

            for c in [c_ag, c_m, c_f, c_tot]:
                c.font = FONT_DATA
                c.border = BORDER_THIN
            c_ag.alignment = Alignment(horizontal="center")
            c_m.alignment = Alignment(horizontal="right")
            c_f.alignment = Alignment(horizontal="right")
            c_tot.alignment = Alignment(horizontal="right")

        ws.column_dimensions["A"].width = 16
        ws.column_dimensions["B"].width = 18
        ws.column_dimensions["C"].width = 18
        ws.column_dimensions["D"].width = 18

        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        wb.save(filepath)
        return filepath

    @staticmethod
    def load_cohort_distribution(filepath: str) -> Dict[str, Any]:
        """Excel veya CSV dosyasından yaş-cinsiyet kohort verilerini okur."""
        age_labels = [
            "0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39",
            "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+"
        ]
        m_arr = [0] * 17
        f_arr = [0] * 17
        matched_count = 0

        if filepath.lower().endswith(".csv"):
            rows = []
            for enc in ["utf-8-sig", "utf-8", "cp1254", "latin1"]:
                try:
                    with open(filepath, "r", encoding=enc) as f:
                        first_line = f.readline()
                        sep = ";" if ";" in first_line else ","
                        f.seek(0)
                        reader = csv.reader(f, delimiter=sep)
                        rows = list(reader)
                        if rows:
                            break
                except Exception:
                    continue

            c_age, c_male, c_female = -1, -1, -1
            header_idx = -1
            for r_i, row in enumerate(rows[:15]):
                for c_i, cell in enumerate(row):
                    norm = normalize_col_name(str(cell or "").strip())
                    if any(x in norm for x in ["yas", "cohort", "age"]):
                        c_age = c_i
                    elif any(x in norm for x in ["erkek", "male", "bay"]):
                        c_male = c_i
                    elif any(x in norm for x in ["kadin", "female", "bayan"]):
                        c_female = c_i
                if c_age != -1 and (c_male != -1 or c_female != -1):
                    header_idx = r_i
                    break

            if header_idx != -1:
                for row in rows[header_idx + 1:]:
                    if len(row) <= c_age:
                        continue
                    ag_val = str(row[c_age] or "").strip()
                    clean_ag = ag_val.replace(" ", "").replace("_", "-")
                    target_idx = -1
                    for idx, standard_ag in enumerate(age_labels):
                        if standard_ag in clean_ag or clean_ag in standard_ag:
                            target_idx = idx
                            break
                        nums = re.findall(r'\d+', clean_ag)
                        if nums:
                            s_nums = re.findall(r'\d+', standard_ag)
                            if s_nums and nums[0] == s_nums[0]:
                                target_idx = idx
                                break
                    if target_idx != -1:
                        try:
                            m_str = str(row[c_male]).replace(".", "").replace(",", ".").replace(" ", "") if c_male < len(row) else "0"
                            m_val = float(m_str or 0)
                        except Exception:
                            m_val = 0.0
                        try:
                            f_str = str(row[c_female]).replace(".", "").replace(",", ".").replace(" ", "") if c_female < len(row) else "0"
                            f_val = float(f_str or 0)
                        except Exception:
                            f_val = 0.0
                        m_arr[target_idx] = int(round(m_val))
                        f_arr[target_idx] = int(round(f_val))
                        matched_count += 1

            tot_m = sum(m_arr)
            tot_f = sum(f_arr)
            return {
                "matched_cohorts": matched_count,
                "male": m_arr,
                "female": f_arr,
                "total_male": tot_m,
                "total_female": tot_f,
                "total_pop": tot_m + tot_f
            }

        # Excel Okuma
        wb = openpyxl.load_workbook(filepath, data_only=True)
        # sheet ara
        ws = None
        for name in wb.sheetnames:
            norm = normalize_col_name(name)
            if "yas" in norm or "cohort" in norm or "cinsiyet" in norm:
                ws = wb[name]
                break
        if ws is None:
            ws = wb.active

        # Başlık satırını bul
        header_row = -1
        c_age, c_male, c_female = -1, -1, -1

        for r in range(1, 15):
            for c in range(1, 15):
                val = str(ws.cell(row=r, column=c).value or "").strip().lower()
                norm = normalize_col_name(val)
                if any(x in norm for x in ["yas", "cohort", "age"]):
                    c_age = c
                elif any(x in norm for x in ["erkek", "male", "bay"]):
                    c_male = c
                elif any(x in norm for x in ["kadin", "female", "bayan"]):
                    c_female = c
            if c_age != -1 and (c_male != -1 or c_female != -1):
                header_row = r
                break

        if header_row == -1:
            # Sütunları 1, 2, 3 varsay
            c_age, c_male, c_female = 1, 2, 3
            header_row = 1

        row_idx = header_row + 1
        matched_count = 0
        while row_idx <= ws.max_row:
            ag_val = str(ws.cell(row=row_idx, column=c_age).value or "").strip()
            if not ag_val:
                row_idx += 1
                continue

            # Eşleştirme yap
            target_idx = -1
            clean_ag = ag_val.replace(" ", "").replace("_", "-")
            for idx, standard_ag in enumerate(age_labels):
                if standard_ag in clean_ag or clean_ag in standard_ag:
                    target_idx = idx
                    break
                # Sayısal aralık kontrolü (örn 0 - 4)
                nums = re.findall(r'\d+', clean_ag)
                if nums:
                    s_nums = re.findall(r'\d+', standard_ag)
                    if s_nums and nums[0] == s_nums[0]:
                        target_idx = idx
                        break

            if target_idx != -1:
                try:
                    m_val = float(ws.cell(row=row_idx, column=c_male).value or 0)
                except Exception:
                    m_val = 0.0
                try:
                    f_val = float(ws.cell(row=row_idx, column=c_female).value or 0)
                except Exception:
                    f_val = 0.0
                m_arr[target_idx] = int(round(m_val))
                f_arr[target_idx] = int(round(f_val))
                matched_count += 1

            row_idx += 1

        tot_m = sum(m_arr)
        tot_f = sum(f_arr)
        return {
            "matched_cohorts": matched_count,
            "male": m_arr,
            "female": f_arr,
            "total_male": tot_m,
            "total_female": tot_f,
            "total_pop": tot_m + tot_f
        }
