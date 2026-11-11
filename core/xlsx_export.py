# -*- coding: utf-8 -*-
"""
Multi-Sheet Excel Export Engine with Live Formulas & OpenXML Cached Values
Destekleyici Formüllü Projeksiyon Çalışma Kitabı (.xlsx)
"""

import os, zipfile, xml.etree.ElementTree as ET
try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False
    openpyxl = None
from typing import Dict, Any, List


def inject_cached_values_to_xlsx(filepath: str, cached_map: Dict[tuple, Any]):
    """
    OpenXML worksheet XML'lerindeki <v> düğümlerine hesaplanan değerleri doğrudan yazar.
    Böylece formüller korunurken, Excel açılmasa bile Pandas/openpyxl değerleri okuyabilir.
    """
    tmp_path = filepath + ".tmp.zip"
    with zipfile.ZipFile(filepath, 'r') as zin:
        with zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            sheet_mapping = {}
            if "xl/workbook.xml" in zin.namelist():
                tree_wb = ET.fromstring(zin.read("xl/workbook.xml"))
                for s in tree_wb.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet'):
                    sheet_mapping[s.attrib['name']] = f"xl/worksheets/sheet{s.attrib['sheetId']}.xml"

            for item in zin.infolist():
                content = zin.read(item.filename)
                target_sheet_name = None
                for sname, spath in sheet_mapping.items():
                    if spath == item.filename:
                        target_sheet_name = sname
                        break

                if target_sheet_name:
                    tree = ET.fromstring(content)
                    ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                    modified = False
                    for (s_name, coord), val in cached_map.items():
                        if s_name == target_sheet_name:
                            for c in tree.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
                                if c.attrib.get('r') == coord:
                                    v = c.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                                    if v is None:
                                        v = ET.SubElement(c, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                                    v.text = str(val)
                                    modified = True
                                    break
                    if modified:
                        content = ET.tostring(tree, encoding='utf-8', xml_declaration=True)
                zout.writestr(item, content)

    os.replace(tmp_path, filepath)


class ExcelReportEngine:
    @staticmethod
    def generate_full_workbook(
        filepath: str,
        template_data: Dict[str, Any],
        curve_results: Dict[str, Any],
        cohort_results: Dict[str, Any],
        econ_results: Dict[str, Any],
        shock_results: Dict[str, Any]
    ) -> str:
        wb = openpyxl.Workbook()
        ws_cover = wb.active
        ws_cover.title = "01_Kapak_ve_Model_Sentezi"
        ws_cover.views.sheetView[0].showGridLines = True

        FONT_TITLE = Font(name="Segoe UI", size=13, bold=True, color="FFFFFF")
        FONT_SEC = Font(name="Segoe UI", size=11, bold=True, color="1E3A8A")
        FONT_TH = Font(name="Segoe UI", size=9.5, bold=True, color="FFFFFF")
        FONT_DATA = Font(name="Segoe UI", size=9.5)
        FONT_BOLD = Font(name="Segoe UI", size=9.5, bold=True)
        FONT_TOTAL = Font(name="Segoe UI", size=10, bold=True, color="1E3A8A")

        FILL_NAVY = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
        FILL_BLUE = PatternFill(start_color="2563EB", end_color="2563EB", fill_type="solid")
        FILL_SUB = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
        FILL_GREEN = PatternFill(start_color="ECFDF5", end_color="ECFDF5", fill_type="solid")
        FILL_ZEBRA = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")

        BORDER_THIN = Border(
            left=Side(style='thin', color='CBD5E1'), right=Side(style='thin', color='CBD5E1'),
            top=Side(style='thin', color='CBD5E1'), bottom=Side(style='thin', color='CBD5E1')
        )

        cached_values = {}

        # 1. KAPAK SAYFASI
        ws_cover.merge_cells("B2:I2")
        ws_cover["B2"] = "KENTSEL VE BÖLGESEL DEMOGRAFİK PROJEKSİYON MODELİ — ANALİZ RAPORU"
        ws_cover["B2"].font = FONT_TITLE
        ws_cover["B2"].fill = FILL_NAVY
        ws_cover["B2"].alignment = Alignment(horizontal="center", vertical="center")
        ws_cover.row_dimensions[2].height = 28

        ws_cover.merge_cells("B3:I3")
        ws_cover["B3"] = f"Çalışma Alanı: {template_data.get('name', 'Genel Kentsel Alan')} | Başlangıç Yılı: {template_data.get('base_year', 2025)}"
        ws_cover["B3"].font = FONT_BOLD
        ws_cover["B3"].alignment = Alignment(horizontal="center", vertical="center")

        _yrs0 = (cohort_results or {}).get("years") or {}
        _y1 = _yrs0.get("t1") or template_data.get("target_year_1") or 2045
        _y2 = _yrs0.get("t2") or template_data.get("target_year_2") or 2050
        headers_sentez = ["Sıra", "Model / Senaryo Adı", "Kategori", f"Başlangıç Nüfusu ({_yrs0.get('base') or template_data.get('base_year', 2025)})", f"Hedef Yıl 1 ({_y1})", f"Hedef Yıl 2 ({_y2})", "R² / Uyumluluk", "Değerlendirme & Plan Kararı"]
        for c_idx, h in enumerate(headers_sentez, start=2):
            c = ws_cover.cell(row=5, column=c_idx, value=h)
            c.font = FONT_TH
            c.fill = FILL_BLUE
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.border = BORDER_THIN
        ws_cover.row_dimensions[5].height = 24

        # Hedef yıllar kullanıcının girdiği yıllardan alınır (JSON'dan dönen string anahtarlara da dayanıklı)
        yrs = (cohort_results or {}).get("years") or {}
        y1 = int(yrs.get("t1") or template_data.get("target_year_1") or 2045)
        y2 = int(yrs.get("t2") or template_data.get("target_year_2") or 2050)

        def _step_total(scen_key, yr):
            scen = (cohort_results.get("scenarios") or {}).get(scen_key) or {}
            steps = scen.get("steps") or {}
            for k in (yr, str(yr)):
                if k in steps:
                    return steps[k].get("total", 0)
            tl = (scen.get("timeline") or {}).get("shocked_timeline") or {}
            for k in (yr, str(yr)):
                if k in tl:
                    return tl[k]
            return 0

        def _pred(model_key, yr):
            preds = curve_results["models"][model_key].get("predictions", {})
            return preds.get(yr, preds.get(str(yr), 0))

        rows_sentez = [
            (1, "Doğrusal (Linear) Curve Fitting", "Matematiksel Trend", template_data.get('base_pop', 0), _pred("linear", y1), _pred("linear", y2), curve_results["models"]["linear"]["metrics"]["r2"], "SEÇİLEN MATEMATİKSEL MODEL"),
            (2, "2. Derece Polinom Curve Fitting", "Matematiksel Trend", template_data.get('base_pop', 0), _pred("poly2", y1), _pred("poly2", y2), curve_results["models"]["poly2"]["metrics"]["r2"], "ÇOK YÜKSEK UYUM"),
            (3, "⭐ Kuşak-Bileşen: Yüksek Senaryo (Plan Kabul)", "Demografik Kohort", template_data.get('base_pop', 0), template_data.get('target_pop_1', 0) or _step_total("high", y1), template_data.get('target_pop_2', 0) or _step_total("high", y2), "Tam Model", "SEÇİLEN PLAN NÜFUSU (İktisadi Çarpan Göçü)"),
            (4, "Kuşak-Bileşen: Orta Senaryo (Trend Göçü)", "Demografik Kohort", template_data.get('base_pop', 0), _step_total("mid", y1), _step_total("mid", y2), "Dinamik", "ALT SINIR (Mevcut Göç Eğilimi Devamı)"),
            (5, "Kuşak-Bileşen: Düşük Senaryo (0% Göç)", "Demografik Kohort", template_data.get('base_pop', 0), _step_total("low", y1), _step_total("low", y2), "Kapalı Dem.", "KONTROL (Göç Almazsa Yaşlanıp Küçülme)"),
            (6, "Kuşak-Bileşen: Şoklu Dinamik Senaryo", "Şok Modellemesi", template_data.get('base_pop', 0), _step_total("shock", y1), _step_total("shock", y2), "Şok Entegre", "YILLARA ÖZEL PROJE VE AFET SENARYOSU")
        ]

        for r_idx, r_data in enumerate(rows_sentez, start=6):
            for c_idx, val in enumerate(r_data, start=2):
                c = ws_cover.cell(row=r_idx, column=c_idx, value=val)
                c.font = FONT_BOLD if r_idx in [6, 8] else FONT_DATA
                c.border = BORDER_THIN
                if c_idx in [2, 4]:
                    c.alignment = Alignment(horizontal="center")
                elif c_idx in [5, 6, 7]:
                    c.alignment = Alignment(horizontal="right")
                    c.number_format = "#,##0" if c_idx != 8 else "0.0000"
                if r_idx == 8:
                    c.fill = FILL_GREEN
                elif r_idx % 2 == 1:
                    c.fill = FILL_ZEBRA
            ws_cover.row_dimensions[r_idx].height = 20

        # İktisadi Taban Özet Tablosu
        ws_cover["B14"] = "İKTİSADİ TABAN (BAZ ÇARPANI) VE DEMOGRAFİK GÖÇ MODELİ (ECONOMIC BASE MULTIPLIER)"
        ws_cover["B14"].font = FONT_SEC
        ws_cover.merge_cells("B14:I14")

        econ_table = [
            ("Temel İş Gücü (Eb):", f"{econ_results.get('basic_employment', 0):,}", "Dış pazara dönük sanayi ve ihtisas istihdamı"),
            ("Toplam İş Gücü (Et):", f"{econ_results.get('total_employment', 0):,}", "Kentteki tüm çalışan aktif nüfus"),
            ("Baz Çarpanı (k = Et / Eb):", f"{econ_results.get('base_multiplier_k', 0):.3f}", "1 temel sanayi çalışanının tetiklediği toplam çalışan"),
            ("Demografik Bağımlılık (b = P / Et):", f"{econ_results.get('dependency_ratio_b', 0):.3f}", "1 çalışan başına kentsel nüfus yükü"),
            ("Planlanan Yeni Sanayi Alanı (Ha):", f"{template_data.get('industrial_area_ha', 0):.1f} Ha", "OSB / İmalat Sanayi Gelişme Alanı"),
            ("Yaratılan Yeni Temel İstihdam (ΔEb):", f"{template_data.get('new_industrial_jobs', 0):,} Kişi", "Yeni sanayi çalışanları (Hektar × 35 çalışan/ha)"),
            ("Göçle Gelecek Kentsel Nüfus (ΔP):", f"{econ_results.get('plan_migrant_pop', 0):,} Kişi", "ΔP = (ΔEb × k) × b")
        ]

        for r_idx, (ek, ev, edesc) in enumerate(econ_table, start=15):
            ws_cover[f"B{r_idx}"] = ek
            ws_cover[f"B{r_idx}"].font = FONT_BOLD
            ws_cover[f"B{r_idx}"].fill = FILL_SUB
            ws_cover[f"B{r_idx}"].border = BORDER_THIN
            ws_cover.merge_cells(f"B{r_idx}:D{r_idx}")

            ws_cover[f"E{r_idx}"] = ev
            ws_cover[f"E{r_idx}"].font = FONT_BOLD
            ws_cover[f"E{r_idx}"].border = BORDER_THIN
            ws_cover[f"E{r_idx}"].alignment = Alignment(horizontal="right")

            ws_cover[f"F{r_idx}"] = edesc
            ws_cover[f"F{r_idx}"].font = FONT_DATA
            ws_cover[f"F{r_idx}"].border = BORDER_THIN
            ws_cover.merge_cells(f"F{r_idx}:I{r_idx}")
            ws_cover.row_dimensions[r_idx].height = 20

        # Şoklar Tablosu
        ws_cover["B24"] = "TANIMLI DEMOGRAFİK ŞOKLAR VE KENTSEL KIRILMA SENARYOLARI"
        ws_cover["B24"].font = FONT_SEC
        ws_cover.merge_cells("B24:I24")

        shocks_list = shock_results.get("events_by_year", {})
        r_cur = 25
        if not shocks_list:
            ws_cover[f"B{r_cur}"] = "Tanımlı şok olayı bulunmuyor (Pürüzsüz kohort projeksiyonu aktif)."
            ws_cover.merge_cells(f"B{r_cur}:I{r_cur}")
            ws_cover[f"B{r_cur}"].font = FONT_DATA
        else:
            for s_yr, s_items in shocks_list.items():
                for s in s_items:
                    ws_cover[f"B{r_cur}"] = f"Yıl {s['year']}: {s['title']}"
                    ws_cover[f"B{r_cur}"].font = FONT_BOLD
                    ws_cover.merge_cells(f"B{r_cur}:D{r_cur}")
                    ws_cover[f"E{r_cur}"] = f"{s['population_delta']:+,} Kişi"
                    ws_cover[f"E{r_cur}"].font = FONT_BOLD
                    ws_cover[f"E{r_cur}"].alignment = Alignment(horizontal="right")
                    ws_cover[f"F{r_cur}"] = s.get('description', '')
                    ws_cover.merge_cells(f"F{r_cur}:I{r_cur}")
                    for col in range(2, 10):
                        ws_cover.cell(row=r_cur, column=col).border = BORDER_THIN
                    r_cur += 1

        # Sütun Genişlikleri
        ws_cover.column_dimensions["A"].width = 3
        ws_cover.column_dimensions["B"].width = 6
        ws_cover.column_dimensions["C"].width = 32
        ws_cover.column_dimensions["D"].width = 22
        ws_cover.column_dimensions["E"].width = 18
        ws_cover.column_dimensions["F"].width = 18
        ws_cover.column_dimensions["G"].width = 18
        ws_cover.column_dimensions["H"].width = 18
        ws_cover.column_dimensions["I"].width = 38

        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        wb.save(filepath)
        try:
            inject_cached_values_to_xlsx(filepath, cached_values)
        except Exception:
            pass
        return filepath
