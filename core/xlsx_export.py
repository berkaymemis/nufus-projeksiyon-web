# -*- coding: utf-8 -*-
"""
Multi-Sheet Excel Export Engine for NüfusKaç (Urban Demographics Pro)
Generates a 5-Sheet Professional Workbook (.xlsx) for the currently selected
Province / District / Mahalle and Target Year:
  1. 01_Secili_Alan_ve_Ozet
  2. 02_Regresyon_ve_Yillik_Seri
  3. 03_Kusak_Bilesen_Piramit
  4. 04_Hansen_Mahalle_Dagilimi
  5. 05_MPYY_Donati_Standartlari

Supports both `openpyxl` (with rich styling) and a zero-dependency standard-library
OpenXML writer fallback so it works in every Python / QGIS runtime.
"""

import os
import re
import zipfile
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Tuple

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False
    openpyxl = None


MODEL_LABELS = {
    "linear": ("Doğrusal (Linear Trend)", "Matematiksel Regresyon"),
    "poly2": ("2. Derece Polinom (Parabolik)", "Matematiksel Regresyon"),
    "poly3": ("3. Derece Polinom", "Matematiksel Regresyon"),
    "exponential": ("Üstel (Exponential)", "Matematiksel Regresyon"),
    "geometric": ("Geometrik (Bileşik Artış)", "Matematiksel Regresyon"),
    "power": ("Kuvvet (Power) Modeli", "Matematiksel Regresyon"),
    "logarithmic": ("Logaritmik (Yavaşlayan)", "Matematiksel Regresyon"),
    "logistic": ("Lojistik (Taşıma Kapasiteli S-Eğrisi)", "Matematiksel Regresyon"),
    "constant_share": ("Sabit Pay (Constant Share — Çubukçu F. 4.30)", "Bölgesel Pay Modeli"),
    "variable_share": ("Değişken Pay (Shift-Share — Çubukçu F. 4.39)", "Bölgesel Pay Modeli"),
}


# ==============================================================================
# ZERO-DEPENDENCY OPENXML FALLBACK WRITER (Used if openpyxl is not installed)
# ==============================================================================
_BAD_SHEET = re.compile(r"[\[\]\:\*\?\/\\]")
_ILLEGAL = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f]")


def _xml_escape(text: Any, extra: dict = None) -> str:
    out = _ILLEGAL.sub("", str(text)).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    for k, v in (extra or {}).items():
        out = out.replace(k, v)
    return out


def _col_letter(n: int) -> str:
    s = ""
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _cell_xml(ref: str, value: Any, style: int = 0) -> str:
    st = f' s="{style}"' if style else ""
    if value is None or value == "":
        return ""
    if isinstance(value, bool):
        value = int(value)
    if isinstance(value, (int, float)):
        if value != value or value in (float("inf"), float("-inf")):
            return ""
        return f'<c r="{ref}"{st}><v>{repr(float(value)) if isinstance(value, float) else value}</v></c>'
    text = _xml_escape(str(value))
    return f'<c r="{ref}" t="inlineStr"{st}><is><t xml:space="preserve">{text}</t></is></c>'


def _sheet_to_xml(rows: List[List[Any]]) -> str:
    out = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
        '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" '
        'activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
    ]
    if rows:
        widths = {}
        for row in rows:
            for c, v in enumerate(row):
                widths[c] = max(widths.get(c, 8), min(55, len(str(v if v is not None else "")) + 3))
        out.append("<cols>")
        for c in sorted(widths):
            out.append(f'<col min="{c + 1}" max="{c + 1}" width="{widths[c]}" customWidth="1"/>')
        out.append("</cols>")
    out.append("<sheetData>")
    for r, row in enumerate(rows):
        cells = "".join(_cell_xml(f"{_col_letter(c)}{r + 1}", v, 1 if r == 0 else 0) for c, v in enumerate(row))
        out.append(f'<row r="{r + 1}">{cells}</row>')
    out.append("</sheetData></worksheet>")
    return "".join(out)


def _write_fallback_xlsx(filepath: str, sheets: List[Tuple[str, List[List[Any]]]]) -> str:
    names = []
    for name, _ in sheets:
        clean = _BAD_SHEET.sub("_", str(name))[:31] or "Sayfa"
        base, k = clean, 2
        while clean in names:
            suffix = f"_{k}"
            clean = base[:31 - len(suffix)] + suffix
            k += 1
        names.append(clean)

    pkg = "application/vnd.openxmlformats-package."
    sml = "application/vnd.openxmlformats-officedocument.spreadsheetml."
    rel = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"

    ct = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
        f'<Default Extension="rels" ContentType="{pkg}relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        f'<Override PartName="/xl/workbook.xml" ContentType="{sml}sheet.main+xml"/>',
        f'<Override PartName="/xl/styles.xml" ContentType="{sml}styles+xml"/>'
    ]
    for i in range(len(sheets)):
        ct.append(f'<Override PartName="/xl/worksheets/sheet{i + 1}.xml" ContentType="{sml}worksheet+xml"/>')
    ct.append("</Types>")

    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f'<Relationship Id="rId1" Type="{rel}officeDocument" Target="xl/workbook.xml"/>'
        '</Relationships>'
    )
    wb = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'
    ]
    wbr = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    ]
    for i, name in enumerate(names):
        esc_name = _xml_escape(name, {'"': "&quot;"})
        wb.append(f'<sheet name="{esc_name}" sheetId="{i + 1}" r:id="rId{i + 1}"/>')
        wbr.append(f'<Relationship Id="rId{i + 1}" Type="{rel}worksheet" Target="worksheets/sheet{i + 1}.xml"/>')
    wb.append("</sheets></workbook>")
    wbr.append(f'<Relationship Id="rId{len(names) + 1}" Type="{rel}styles" Target="styles.xml"/>')
    wbr.append("</Relationships>")

    styles = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="2"><font><sz val="10"/><name val="Segoe UI"/></font>'
        '<font><b/><sz val="10"/><color rgb="FFFFFFFF"/><name val="Segoe UI"/></font></fonts>'
        '<fills count="3"><fill><patternFill patternType="none"/></fill>'
        '<fill><patternFill patternType="gray125"/></fill>'
        '<fill><patternFill patternType="solid"><fgColor rgb="FF1E3A8A"/>'
        '<bgColor indexed="64"/></patternFill></fill></fills>'
        '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
        '<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/></cellXfs>'
        '</styleSheet>'
    )
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    with zipfile.ZipFile(filepath, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "".join(ct))
        z.writestr("_rels/.rels", rels)
        z.writestr("xl/workbook.xml", "".join(wb))
        z.writestr("xl/_rels/workbook.xml.rels", "".join(wbr))
        z.writestr("xl/styles.xml", styles)
        for i, (_, rows) in enumerate(sheets):
            z.writestr(f"xl/worksheets/sheet{i + 1}.xml", _sheet_to_xml(rows))
    return filepath


class ExcelReportEngine:
    @staticmethod
    def generate_full_workbook(
        filepath: str,
        template_data: Dict[str, Any],
        curve_results: Dict[str, Any],
        cohort_results: Dict[str, Any],
        econ_results: Dict[str, Any],
        shock_results: Dict[str, Any],
        hansen_results: Dict[str, Any] = None,
        mpyy_standards: Dict[str, Any] = None
    ) -> str:
        template_data = template_data or {}
        curve_results = curve_results or {}
        cohort_results = cohort_results or {}
        econ_results = econ_results or {}
        shock_results = shock_results or {}
        hansen_results = hansen_results or {}
        mpyy_standards = mpyy_standards or {}

        yrs = cohort_results.get("years") or {}
        base_year = int(yrs.get("base") or template_data.get("base_year") or 2025)
        y1 = int(yrs.get("t1") or template_data.get("target_year_1") or 2030)
        y2 = int(yrs.get("t2") or template_data.get("target_year_2") or 2050)
        base_pop = int(template_data.get("base_pop") or cohort_results.get("base_pop") or 0)
        area_name = str(template_data.get("name") or "Seçili Kentsel Çalışma Alanı")
        prov_name = str(template_data.get("province") or "-")
        dist_name = str(template_data.get("district") or "-")
        zone_name = str(template_data.get("zone_name") or "Tüm Alt Bölgeler / Mahalleler")
        upper_name = str(template_data.get("upper_region_name") or "Türkiye Geneli")
        tfr_val = float(cohort_results.get("tfr") or template_data.get("tfr") or 1.51)

        models = curve_results.get("models") or {}
        best_model_key = curve_results.get("best_model") or "linear"

        def _pred(m_key: str, yr: int) -> int:
            m_obj = models.get(m_key) or {}
            preds = m_obj.get("predictions") or {}
            val = preds.get(yr, preds.get(str(yr), 0))
            try:
                return max(0, int(round(float(val))))
            except Exception:
                return 0

        def _r2(m_key: str) -> float:
            m_obj = models.get(m_key) or {}
            metrics = m_obj.get("metrics") or {}
            try:
                return float(metrics.get("r2", 0.0))
            except Exception:
                return 0.0

        def _sse(m_key: str) -> float:
            m_obj = models.get(m_key) or {}
            metrics = m_obj.get("metrics") or {}
            try:
                return float(metrics.get("sse", 0.0))
            except Exception:
                return 0.0

        def _step_obj(scen_key: str, yr: int) -> Dict[str, Any]:
            scen = (cohort_results.get("scenarios") or {}).get(scen_key) or {}
            steps = scen.get("steps") or {}
            for k in (yr, str(yr)):
                if k in steps and isinstance(steps[k], dict):
                    return steps[k]
            return {}

        def _step_total(scen_key: str, yr: int) -> int:
            st = _step_obj(scen_key, yr)
            if "total" in st:
                return int(st["total"])
            scen = (cohort_results.get("scenarios") or {}).get(scen_key) or {}
            tl = (scen.get("timeline") or {}).get("shocked_timeline") or {}
            for k in (yr, str(yr)):
                if k in tl:
                    return int(tl[k])
            return 0

        # Extract Economic Base fields accurately from nested structure
        ratios = econ_results.get("ratios") or {}
        mig = econ_results.get("migration") or {}
        sum_tab = econ_results.get("summary_table") or {}

        tot_jobs = int(sum_tab.get("current_jobs") or ratios.get("total_employment") or econ_results.get("total_employment") or round(base_pop * 0.45))
        k_mult = float(mig.get("base_multiplier_k") or ratios.get("base_multiplier_k") or sum_tab.get("multiplier_k") or 2.85)
        b_ratio = float(mig.get("dependency_ratio_b") or ratios.get("dependency_ratio_b") or sum_tab.get("dependency_b") or 2.22)
        act_rate = float(ratios.get("activity_rate_pct") or (tot_jobs / max(1, base_pop) * 100.0))
        basic_jobs = int(ratios.get("basic_employment") or econ_results.get("basic_employment") or round(tot_jobs / max(1.0, k_mult)))
        new_basic_jobs = int(mig.get("new_basic_jobs") or econ_results.get("new_basic_jobs") or 0)
        total_new_jobs = int(mig.get("total_new_jobs") or sum_tab.get("net_jobs") or 0)
        plan_mig_pop = int(mig.get("plan_migrant_pop") or sum_tab.get("migrant_pop") or 0)

        high_y1 = int(template_data.get("target_pop_1") or _step_total("high", y1) or (base_pop + plan_mig_pop))
        high_y2 = int(template_data.get("target_pop_2") or _step_total("high", y2) or round(high_y1 * 1.055))
        mid_y1 = int(_step_total("mid", y1) or _pred(best_model_key, y1))
        mid_y2 = int(_step_total("mid", y2) or _pred(best_model_key, y2))
        low_y1 = int(_step_total("low", y1) or base_pop)
        low_y2 = int(_step_total("low", y2) or base_pop)
        shock_y1 = int(_step_total("shock", y1) or mid_y1)
        shock_y2 = int(_step_total("shock", y2) or mid_y2)

        # Build Sheet 1 Rows (Summary & Synthesis)
        s1_rows = [
            ["NÜFUSKAÇ — SEÇİLİ ALAN DEMOGRAFİK PROJEKSİYON VE MEKÂNSAL ANALİZ RAPORU", "", "", "", "", "", "", ""],
            ["Seçili Çalışma Alanı:", area_name, "İl:", prov_name, "İlçe:", dist_name, "Mahalle / Kapsam:", zone_name],
            ["Başlangıç Yılı:", base_year, "2025 TÜİK Nüfusu:", base_pop, "Seçili Hedef Yıl:", y1, "Uzun Vade Yılı:", y2],
            ["Üst Bölge (Pay Modeli):", upper_name, "Doğurganlık Hızı (TFR):", round(tfr_val, 2), "En Uyumlu Model:", MODEL_LABELS.get(best_model_key, (best_model_key, ""))[0], "Model R²:", round(_r2(best_model_key), 4)],
            [],
            ["Sıra", "Model / Senaryo Adı", "Kategori", f"Başlangıç ({base_year})", f"Hedef Yıl ({y1})", f"Uzun Vade ({y2})", "R² / Uyum", "Planlama Değerlendirmesi"]
        ]

        idx_counter = 1
        for m_key in ["linear", "poly2", "poly3", "exponential", "geometric", "power", "logarithmic", "logistic", "constant_share", "variable_share"]:
            if m_key not in models:
                continue
            m_label, m_cat = MODEL_LABELS.get(m_key, (m_key, "Regresyon"))
            is_best = (m_key == best_model_key)
            is_val = models[m_key].get("is_valid", True) and (_pred(m_key, y2) > 0)
            note = "⭐ EN YÜKSEK UYUMLU MODEL" if is_best else ("Alternatif Trend Modeli" if is_val else "⚠️ Geçersiz (Negatif Çöküş)")
            s1_rows.append([
                idx_counter, m_label, m_cat, base_pop, _pred(m_key, y1), _pred(m_key, y2), round(_r2(m_key), 4), note
            ])
            idx_counter += 1

        s1_rows.extend([
            [idx_counter, "⭐ Kuşak-Bileşen: Yüksek Senaryo (Plan Kabulü)", "Demografik Kohort", base_pop, high_y1, high_y2, "Tam Model", "SEÇİLEN PLAN NÜFUSU (Doğal + İktisadi Göç)"],
            [idx_counter + 1, "Kuşak-Bileşen: Orta Senaryo (Trend Göçü)", "Demografik Kohort", base_pop, mid_y1, mid_y2, "Dinamik", "ORTA SENARYO (Geçmiş Eğilim Devamı)"],
            [idx_counter + 2, "Kuşak-Bileşen: Düşük Senaryo (%0 Net Göç)", "Demografik Kohort", base_pop, low_y1, low_y2, "Kapalı Dem.", "ALT SINIR (Doğal Yaşlanma Eşiği)"],
            [idx_counter + 3, "Kuşak-Bileşen: Şoklu Dinamik Senaryo", "Şok Simülasyonu", base_pop, shock_y1, shock_y2, "Şok Entegre", "Yatırım / Afet Müdahaleli Senaryo"],
            [],
            ["İKTİSADİ TABAN (ECONOMIC BASE MULTIPLIER) VE GÖÇ SENTEZİ (Prof. Dr. K. Mert Çubukçu)", "", "", "", "", "", "", ""],
            ["Parametre Adı", "Değer", "Birim / Açıklama", "", "", "", "", ""],
            ["Mevcut Toplam İstihdam (Et)", tot_jobs, "Çalışan Kişi", "", "", "", "", ""],
            ["Mevcut Temel / Baz İstihdam (Eb)", basic_jobs, "İhracata / Dış Pazara Yönelik İstihdam", "", "", "", "", ""],
            ["İktisadi Taban Çarpanı (k = Et / Eb)", round(k_mult, 3), f"Seçili Yöntem: {template_data.get('multiplier_method', 'LQ')}", "", "", "", "", ""],
            ["Demografik Bağımlılık Oranı (b = P / Et)", round(b_ratio, 3), "1 Çalışan Başına Toplam Nüfus", "", "", "", "", ""],
            ["İşgücü Aktivite Oranı (%)", round(act_rate, 2), "Toplam İstihdam / Toplam Nüfus (%)", "", "", "", "", ""],
            ["Planlanan Yeni Temel İstihdam (ΔEb)", new_basic_jobs, "Yeni OSB / Sanayi / Yatırım İstihdamı", "", "", "", "", ""],
            ["Toplam Yeni İstihdam Artışı (ΔEt = ΔEb × k)", total_new_jobs, "Temel + Hizmet İstihdamı Artışı", "", "", "", "", ""],
            ["Göç İle Gelecek Nüfus (ΔP = ΔEt × b)", plan_mig_pop, f"{y1} Hedef Yılına Kadar Beklenen Net Göç", "", "", "", "", ""],
            ["Toplam Plan Kabul Nüfusu", high_y1, f"{y1} Yılı Doğal Nüfus + Göç Nüfusu", "", "", "", "", ""],
        ])

        shocks_arr = shock_results.get("shocks") or []
        s1_rows.append([])
        s1_rows.append(["TANIMLI DEMOGRAFİK ŞOKLAR VE YATIRIM MÜDAHALELERİ", "", "", "", "", "", "", ""])
        if not shocks_arr:
            s1_rows.append(["Tanımlı dışsal şok bulunmuyor (Şoksuz doğal/trend projeksiyon aktif).", "", "", "", "", "", "", ""])
        else:
            s1_rows.append(["Yıl", "Şok / Proje Adı", "Nüfus Etkisi (+/-)", "Hedef Yaş Grubu", "Müdahale Türü", "", "", ""])
            for s in shocks_arr:
                s1_rows.append([
                    s.get("year", ""), s.get("title", ""), s.get("population_delta", 0),
                    s.get("age_bias", ""), s.get("impact_type", ""), "", "", ""
                ])

        # Build Sheet 2 Rows (Regression Models & Year-by-Year Historical + Projected Series)
        s2_rows = [
            [f"MATEMATİKSEL EĞRİ UYDURMA VE BÖLGESEL PAY MODELLERİ ({area_name})", "", "", "", "", "", ""],
            ["Model Adı", "Matematiksel Formül", "Belirlilik Katsayısı (R²)", "Hata Kareleri Toplamı (SSE)", f"{y1} Projeksiyonu", f"{y2} Projeksiyonu", "Durum"]
        ]
        active_m_keys = [k for k in ["linear", "poly2", "poly3", "exponential", "geometric", "power", "logarithmic", "logistic", "constant_share", "variable_share"] if k in models]
        for mk in active_m_keys:
            m_obj = models[mk]
            m_label, _ = MODEL_LABELS.get(mk, (mk, ""))
            is_best = (mk == best_model_key)
            is_val = m_obj.get("is_valid", True) and (_pred(mk, y2) > 0)
            s2_rows.append([
                f"{'⭐ ' if is_best else ''}{m_label}",
                m_obj.get("formula_str") or m_obj.get("formula") or "-",
                round(_r2(mk), 4),
                round(_sse(mk), 2),
                _pred(mk, y1),
                _pred(mk, y2),
                "En Yüksek Uyum" if is_best else ("Geçerli" if is_val else "Geçersiz (Çöküş)")
            ])

        s2_rows.append([])
        hist_obj = curve_results.get("history") or {}
        hist_map = {}
        for hy, hp in zip(hist_obj.get("years") or [], hist_obj.get("pop") or []):
            hist_map[int(hy)] = int(round(float(hp)))

        all_years = sorted(set(curve_results.get("years") or list(range(2015, y2 + 1))))
        year_header = ["Yıl", "TÜİK Gözlenen Nüfus"] + [MODEL_LABELS.get(mk, (mk, ""))[0] for mk in active_m_keys]
        s2_rows.append(year_header)
        for yr in all_years:
            row_yr = [yr, hist_map.get(yr, "")]
            for mk in active_m_keys:
                row_yr.append(_pred(mk, yr))
            s2_rows.append(row_yr)

        # Build Sheet 3 Rows (Cohort-Component 17 Age Groups Pyramid)
        age_groups = cohort_results.get("age_groups") or [
            "0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39",
            "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+"
        ]
        init_pyr = cohort_results.get("initial_pyramid") or {}
        m_base = init_pyr.get("male") or [0] * len(age_groups)
        f_base = init_pyr.get("female") or [0] * len(age_groups)
        sx_m = cohort_results.get("sx_male") or [0.99] * len(age_groups)
        sx_f = cohort_results.get("sx_female") or [0.99] * len(age_groups)

        st_low = _step_obj("low", y1)
        st_mid = _step_obj("mid", y1)
        st_high = _step_obj("high", y1)
        m_high = st_high.get("male") or [0] * len(age_groups)
        f_high = st_high.get("female") or [0] * len(age_groups)
        m_mid = st_mid.get("male") or [0] * len(age_groups)
        f_mid = st_mid.get("female") or [0] * len(age_groups)
        m_low = st_low.get("male") or [0] * len(age_groups)
        f_low = st_low.get("female") or [0] * len(age_groups)

        s3_rows = [
            [f"KUŞAK-BİLEŞEN (COHORT-COMPONENT) YAŞ VE CİNSİYET PROJEKSİYONU ({area_name})", "", "", "", "", "", "", "", "", "", ""],
            [
                "Yaş Grubu",
                f"{base_year} Erkek", f"{base_year} Kadın", f"{base_year} Toplam",
                "Hayatta Kalma (Sx Erkek)", "Hayatta Kalma (Sx Kadın)",
                f"{y1} Plan (Yüksek) Erkek", f"{y1} Plan (Yüksek) Kadın", f"{y1} Plan (Yüksek) Toplam",
                f"{y1} Trend (Orta) Toplam", f"{y1} Doğal (Düşük) Toplam"
            ]
        ]
        for i, ag in enumerate(age_groups):
            mb = int(m_base[i]) if i < len(m_base) else 0
            fb = int(f_base[i]) if i < len(f_base) else 0
            mh = int(m_high[i]) if i < len(m_high) else 0
            fh = int(f_high[i]) if i < len(f_high) else 0
            mm = (int(m_mid[i]) if i < len(m_mid) else 0) + (int(f_mid[i]) if i < len(f_mid) else 0)
            ml = (int(m_low[i]) if i < len(m_low) else 0) + (int(f_low[i]) if i < len(f_low) else 0)
            sxm = round(float(sx_m[i]), 4) if i < len(sx_m) else 0.99
            sxf = round(float(sx_f[i]), 4) if i < len(sx_f) else 0.99
            s3_rows.append([ag, mb, fb, mb + fb, sxm, sxf, mh, fh, mh + fh, mm, ml])

        s3_rows.append([
            "TOPLAM",
            sum(int(x) for x in m_base), sum(int(x) for x in f_base), sum(int(x) for x in m_base) + sum(int(x) for x in f_base),
            "-", "-",
            sum(int(x) for x in m_high), sum(int(x) for x in f_high), sum(int(x) for x in m_high) + sum(int(x) for x in f_high),
            sum(int(x) for x in m_mid) + sum(int(x) for x in f_mid),
            sum(int(x) for x in m_low) + sum(int(x) for x in f_low),
        ])

        # Build Sheet 4 Rows (Hansen Spatial Allocation for Selected District/Province Mahalles)
        subzones = hansen_results.get("subzones") or []
        s4_rows = [
            [f"HANSEN MEKÂNSAL ÇEKİM VE MAHALLE / ALT BÖLGE NÜFUS DAĞITIMI ({area_name} — Hedef {y1})", "", "", "", "", "", "", "", "", "", "", ""],
            [
                "Sıra", "Mahalle / Alt Bölge Adı", f"{base_year} Mevcut Nüfus", "Mevcut İstihdam",
                "Boş Gelişme Alanı (Ha)", "Merkeze Mesafe (dk)", "Erişilebilirlik Skoru (Ai)",
                "Rekabetçi Pay (%)", f"Dağıtılan İlave Nüfus (Gi)", f"{y1} Hedef Nüfus (Pi)",
                "Yeni Konut İhtiyacı", "Plan Doygunluk (%)"
            ]
        ]
        tot_cur_sz = 0
        tot_add_sz = 0
        tot_tgt_sz = 0
        tot_house_sz = 0
        for idx, sz in enumerate(subzones, start=1):
            cur_p = int(sz.get("current_pop") or sz.get("base_pop") or 0)
            emp_p = int(sz.get("employment") or sz.get("jobs") or round(cur_p * 0.4))
            vac_ha = float(sz.get("vacant_area_ha") or sz.get("capacity_ha") or 0.0)
            dist_m = float(sz.get("dist_to_center_min") or sz.get("distance_to_center_min") or 0.0)
            ai_sc = round(float(sz.get("accessibility_Ai") or 0.0), 2)
            sh_pct = round(float(sz.get("relative_share_pct") or 0.0), 2)
            add_p = int(sz.get("additional_pop_Gi") or 0)
            tgt_p = int(sz.get("target_pop_Pi") or sz.get("target_pop_2045") or (cur_p + add_p))
            h_need = int(sz.get("housing_need") or round(add_p / 2.85))
            sat_pct = round(float(sz.get("saturation_pct") or 0.0), 1)
            tot_cur_sz += cur_p
            tot_add_sz += add_p
            tot_tgt_sz += tgt_p
            tot_house_sz += h_need
            s4_rows.append([
                idx, sz.get("name", f"Bölge {idx}"), cur_p, emp_p,
                round(vac_ha, 1), round(dist_m, 1), ai_sc, sh_pct,
                add_p, tgt_p, h_need, sat_pct
            ])
        if subzones:
            s4_rows.append([
                "", "TOPLAM", tot_cur_sz, "", "", "", "", 100.0,
                tot_add_sz, tot_tgt_sz, tot_house_sz, ""
            ])

        # Build Sheet 5 Rows (MPYY Ek-2 Social & Technical Infrastructure Standards)
        s5_rows = [
            [f"MEKÂNSAL PLANLAR YAPIM YÖNETMELİĞİ (EK-2) DONATI STANDARTLARI ({area_name} — Hedef {y1})", "", "", ""],
            ["Kentsel Donatı Kategorisi", "Yasal Kişi Başı Standart (m²/kişi)", "Gereken İlave Alan (m²)", "Gereken İlave Alan (Hektar - Ha)"]
        ]
        mpyy_keys = ["egitim", "saglik", "yesil", "sosyal_kultur", "ibadet", "teknik_altyapi"]
        for mk in mpyy_keys:
            item = mpyy_standards.get(mk)
            if isinstance(item, dict):
                s5_rows.append([
                    item.get("name", mk),
                    float(item.get("per_capita", 0.0)),
                    round(float(item.get("total_sqm", 0.0)), 1),
                    round(float(item.get("ha", 0.0)), 3)
                ])
        tot_mpyy = mpyy_standards.get("total") or {}
        if tot_mpyy:
            s5_rows.append([
                "TOPLAM ASGARİ SOSYAL VE TEKNİK ALTYAPI ALANI",
                float(tot_mpyy.get("per_capita", 19.0)),
                round(float(tot_mpyy.get("total_sqm", 0.0)), 1),
                round(float(tot_mpyy.get("ha", 0.0)), 3)
            ])

        sheets_data = [
            ("01_Secili_Alan_ve_Ozet", s1_rows),
            ("02_Regresyon_ve_Yillik_Seri", s2_rows),
            ("03_Kusak_Bilesen_Piramit", s3_rows),
            ("04_Hansen_Mahalle_Dagilimi", s4_rows),
            ("05_MPYY_Donati_Standartlari", s5_rows),
        ]

        if not HAS_OPENPYXL:
            return _write_fallback_xlsx(filepath, sheets_data)

        # Rich openpyxl formatting when openpyxl is available
        wb = openpyxl.Workbook()
        # Remove default sheet after creating ours
        default_ws = wb.active

        FONT_TITLE = Font(name="Segoe UI", size=12, bold=True, color="FFFFFF")
        FONT_TH = Font(name="Segoe UI", size=9.5, bold=True, color="FFFFFF")
        FONT_SEC = Font(name="Segoe UI", size=10, bold=True, color="1E3A8A")
        FONT_BOLD = Font(name="Segoe UI", size=9.5, bold=True, color="0F172A")
        FONT_DATA = Font(name="Segoe UI", size=9.5, color="1E293B")

        FILL_NAVY = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
        FILL_BLUE = PatternFill(start_color="2563EB", end_color="2563EB", fill_type="solid")
        FILL_SUB = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")
        FILL_ZEBRA = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
        FILL_GREEN = PatternFill(start_color="ECFDF5", end_color="ECFDF5", fill_type="solid")

        BORDER_THIN = Border(
            left=Side(style="thin", color="CBD5E1"),
            right=Side(style="thin", color="CBD5E1"),
            top=Side(style="thin", color="CBD5E1"),
            bottom=Side(style="thin", color="CBD5E1"),
        )

        for s_title, rows in sheets_data:
            ws = wb.create_sheet(title=s_title[:31])
            ws.views.sheetView[0].showGridLines = True
            col_widths = {}

            for r_idx, row in enumerate(rows, start=1):
                if not row:
                    continue
                is_banner = (r_idx == 1)
                is_header = (
                    (s_title.startswith("01") and r_idx in (6, 20))
                    or (s_title.startswith("02") and (r_idx == 2 or (len(row) > 1 and row[0] == "Yıl")))
                    or (s_title.startswith("03") and r_idx == 2)
                    or (s_title.startswith("04") and r_idx == 2)
                    or (s_title.startswith("05") and r_idx == 2)
                )
                is_total = (len(row) > 1 and (str(row[0]).startswith("TOPLAM") or str(row[1]).startswith("TOPLAM") or "⭐" in str(row[0]) or "⭐" in str(row[1])))

                for c_idx, val in enumerate(row, start=1):
                    cell = ws.cell(row=r_idx, column=c_idx, value=val)
                    cell.border = BORDER_THIN
                    val_str = str(val if val is not None else "")
                    if not is_banner:
                        col_widths[c_idx] = max(col_widths.get(c_idx, 10), min(46, len(val_str) + 4))

                    if is_banner:
                        cell.font = FONT_TITLE
                        cell.fill = FILL_NAVY
                        cell.alignment = Alignment(horizontal="left", vertical="center")
                    elif is_header:
                        cell.font = FONT_TH
                        cell.fill = FILL_BLUE
                        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                    elif is_total:
                        cell.font = FONT_BOLD
                        cell.fill = FILL_GREEN
                    elif s_title.startswith("01") and r_idx in (2, 3, 4):
                        cell.font = FONT_BOLD if (c_idx % 2 == 1) else FONT_DATA
                        cell.fill = FILL_SUB if (c_idx % 2 == 1) else FILL_ZEBRA
                    else:
                        cell.font = FONT_DATA
                        if r_idx % 2 == 1:
                            cell.fill = FILL_ZEBRA

                    if isinstance(val, int) and not isinstance(val, bool):
                        if c_idx > 1 and val > 2100:
                            cell.number_format = "#,##0"
                    elif isinstance(val, float):
                        cell.number_format = "0.0000" if abs(val) < 2.0 else "#,##0.00"

                ws.row_dimensions[r_idx].height = 25 if is_banner else (22 if is_header else 19)

            for c_idx, w in col_widths.items():
                ws.column_dimensions[get_column_letter(c_idx)].width = w

        if default_ws in wb.worksheets and len(wb.worksheets) > 1:
            wb.remove(default_ws)

        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        wb.save(filepath)
        return filepath
