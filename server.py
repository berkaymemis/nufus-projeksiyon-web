#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Urban Demographics Pro - Standalone Web & Mobile HTTP Server
Zero-Dependency REST API & Responsive Web Application Server
Supports Desktop Browsers and Mobile Smartphones (iOS / Android PWA)
"""

import os
import sys
import json
import socket
import base64
import tempfile
import mimetypes
import webbrowser
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Ensure core plugin modules are in path
CURRENT_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = CURRENT_DIR.parent
WORKSPACE_ROOT = PLUGIN_ROOT.parent.parent

# Local imports
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from core.curve_fitting import CurveFittingEngine
from core.cohort_model import CohortComponentEngine, AGE_GROUPS
from core.economic_base import EconomicBaseEngine
from core.demographic_shocks import ShockEngine, DemographicShock
from core.hansen_model import HansenAllocationEngine
from core.city_templates import CITY_TEMPLATES
from core.data_import import DataImportEngine
from core.xlsx_export import ExcelReportEngine
from core.researchgate_citations import CUBUKCU_CITATIONS, EXPLANATION_TEXTS
from core.district_multipliers import (
    DISTRICT_BASE_MULTIPLIERS, get_all_provinces, get_districts_by_province,
    get_district_info, parse_custom_multiplier_file, CITATION_CUBUKCU_2011, CITATION_KUZIP_2026
)
from core.tuik_adnks import (
    TUIK_ADNKS_DATA, get_adnks_provinces, get_adnks_districts,
    get_adnks_district_data, search_adnks_districts, parse_tuik_adnks_file,
    _normalize_str
)


def get_local_ip() -> str:
    """Finds machine's local Wi-Fi / LAN IP address for phone connection."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'


class DemographicsWebHandler(BaseHTTPRequestHandler):
    server_version = "UrbanDemographicsPro/1.0"

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html"):
            self.serve_file(CURRENT_DIR / "index.html", "text/html; charset=utf-8")
        elif path in ("/classic", "/index_classic.html"):
            self.serve_file(CURRENT_DIR / "index_classic.html", "text/html; charset=utf-8")
        elif path == "/manifest.json":
            self.serve_file(CURRENT_DIR / "manifest.json", "application/manifest+json")
        elif path == "/sw.js":
            self.serve_file(CURRENT_DIR / "sw.js", "application/javascript")
        elif path == "/icon.svg":
            self.serve_file(CURRENT_DIR / "icon.svg", "image/svg+xml")
        elif path == "/api/status":
            local_ip = get_local_ip()
            port = self.server.server_port
            self.send_json({
                "status": "ok",
                "version": "1.0.0",
                "local_ip": local_ip,
                "port": port,
                "lan_url": f"http://{local_ip}:{port}",
                "local_url": f"http://localhost:{port}"
            })
        elif path == "/api/templates":
            self.send_json({"templates": CITY_TEMPLATES})
        elif path == "/api/citations":
            self.send_json({
                "citations": CUBUKCU_CITATIONS,
                "explanations": EXPLANATION_TEXTS
            })
        elif path == "/api/district-multipliers":
            self.send_json({
                "provinces": get_all_provinces(),
                "districts": DISTRICT_BASE_MULTIPLIERS,
                "citation": CITATION_CUBUKCU_2011,
                "citation_kuzip": CITATION_KUZIP_2026
            })
        elif path == "/api/tuik-adnks":
            params = parse_qs(parsed.query)
            prov = params.get("province", [""])[0]
            dist = params.get("district", [""])[0]
            q = params.get("q", [""])[0]
            if q:
                self.send_json({"results": search_adnks_districts(q)})
            elif prov and dist:
                d = get_adnks_district_data(prov, dist)
                if d:
                    self.send_json({"success": True, "data": d})
                else:
                    self.send_json({"success": False, "error": "İlçe bulunamadı"})
            else:
                self.send_json({
                    "provinces": get_adnks_provinces(),
                    "districts": TUIK_ADNKS_DATA,
                    "total_districts": sum(len(d) for d in TUIK_ADNKS_DATA.values())
                })
        elif path == "/api/download-template":
            self.handle_download_template()
        elif path == "/api/download-cohort-template":
            self.handle_download_cohort_template()
        else:
            # Check if static file in web directory
            potential_file = CURRENT_DIR / path.lstrip("/")
            if potential_file.is_file() and not potential_file.name.endswith(".py"):
                mime_type, _ = mimetypes.guess_type(str(potential_file))
                self.serve_file(potential_file, mime_type or "application/octet-stream")
            else:
                self.send_error(404, "Not Found")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/calculate":
            self.handle_calculate()
        elif path == "/api/upload":
            self.handle_upload()
        elif path == "/api/upload-multipliers":
            self.handle_upload_multipliers()
        elif path == "/api/upload-tuik-adnks":
            self.handle_upload_tuik_adnks()
        elif path == "/api/export-report":
            self.handle_export_report()
        else:
            self.send_error(404, "Endpoint Not Found")

    def serve_file(self, file_path: Path, content_type: str):
        if not file_path.is_file():
            self.send_error(404, "Not Found")
            return
        try:
            data = file_path.read_bytes()
            self.send_response(200)
            self.send_cors_headers()
            self.send_header("Content-Type", content_type)
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except Exception as exc:
            self.send_error(500, "Internal Server Error")

    def send_json(self, data: dict, status: int = 200):
        try:
            payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            accept_enc = self.headers.get("Accept-Encoding", "") if hasattr(self, "headers") and self.headers else ""
            use_gzip = "gzip" in accept_enc and len(payload) > 4096
            if use_gzip:
                import gzip
                payload = gzip.compress(payload, compresslevel=6)
            self.send_response(status)
            self.send_cors_headers()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            if use_gzip:
                self.send_header("Content-Encoding", "gzip")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        except Exception as exc:
            self.send_error(500, "Internal Server Error")

    def read_json_body(self) -> dict:
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length <= 0:
            return {}
        body = self.rfile.read(content_length)
        return json.loads(body.decode("utf-8", errors="replace"))

    def handle_download_template(self):
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            DataImportEngine.generate_blank_template(tmp_path)
            data = Path(tmp_path).read_bytes()
            self.send_response(200)
            self.send_cors_headers()
            self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            self.send_header("Content-Disposition", 'attachment; filename="Ornek_Kentsel_Veri_Sablonu.xlsx"')
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def handle_download_cohort_template(self):
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            DataImportEngine.generate_blank_cohort_template(tmp_path)
            data = Path(tmp_path).read_bytes()
            self.send_response(200)
            self.send_cors_headers()
            self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            self.send_header("Content-Disposition", 'attachment; filename="Ornek_Yas_Kohort_Sablonu.xlsx"')
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def handle_upload(self):
        try:
            req = self.read_json_body()
            filename = req.get("filename", "upload.xlsx")
            file_base64 = req.get("file_base64", "")

            if not file_base64:
                self.send_json({"error": "Dosya içeriği boş"}, 400)
                return

            # Clean potential data URI header (e.g. data:application/vnd...;base64,)
            if "," in file_base64:
                file_base64 = file_base64.split(",", 1)[1]

            file_bytes = base64.b64decode(file_base64)
            suffix = ".csv" if filename.lower().endswith(".csv") else ".xlsx"

            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name

            try:
                # Check whether cohort file or settlements file
                is_cohort = req.get("is_cohort", False)
                if is_cohort:
                    parsed = DataImportEngine.load_cohort_distribution(tmp_path)
                    self.send_json({"success": True, "type": "cohort", "data": parsed})
                else:
                    if suffix == ".csv":
                        parsed = DataImportEngine.load_from_csv(tmp_path)
                    else:
                        parsed = DataImportEngine.load_from_excel(tmp_path)

                    raw_subzones = parsed.get("subzones", [])
                    norm_subzones = []
                    for idx, sz in enumerate(raw_subzones):
                        p = sz.get("base_pop", sz.get("current_pop", 0))
                        j = sz.get("jobs", sz.get("employment", int(p * 0.4)))
                        a = sz.get("capacity_ha", sz.get("vacant_area_ha", 5.0))
                        d = sz.get("distance_to_center_min", sz.get("dist_to_center_min", 5.0))
                        c = sz.get("plan_pop_capacity", sz.get("plan_capacity_pop", int(p * 1.3)))
                        norm_subzones.append({
                            "id": sz.get("id", idx + 1),
                            "name": sz.get("name", f"Mahalle {idx + 1}"),
                            "current_pop": p,
                            "base_pop": p,
                            "employment": j,
                            "jobs": j,
                            "vacant_area_ha": a,
                            "capacity_ha": a,
                            "dist_to_center_min": d,
                            "distance_to_center_min": d,
                            "plan_capacity_pop": c,
                            "plan_pop_capacity": c
                        })

                    tot_p = sum(s["current_pop"] for s in norm_subzones)
                    if tot_p == 0 and parsed.get("base_pop", 0) > 0:
                        tot_p = parsed["base_pop"]

                    years_h = parsed.get("years_hist", [])
                    pop_h = parsed.get("pop_hist", [])
                    macro_h = [{"year": y, "pop": p} for y, p in zip(years_h, pop_h)]

                    res_data = {
                        "settlements": norm_subzones,
                        "subzones": norm_subzones,
                        "total_population": tot_p,
                        "base_pop": tot_p,
                        "area_name": parsed.get("name", "İçe Aktarılan Alan"),
                        "base_year": parsed.get("base_year", 2025),
                        "macro_history": macro_h
                    }
                    self.send_json({"success": True, "type": "settlements", "data": res_data})
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

        except Exception as exc:
            self.send_json({"error": f"Yükleme ve ayrıştırma hatası: {str(exc)}"}, 500)

    def handle_upload_multipliers(self):
        try:
            req = self.read_json_body()
            filename = req.get("filename", "multipliers.csv")
            file_base64 = req.get("file_base64", "")
            if not file_base64:
                self.send_json({"error": "Dosya boş"}, 400)
                return
            if "," in file_base64:
                file_base64 = file_base64.split(",", 1)[1]
            file_bytes = base64.b64decode(file_base64)
            suffix = ".csv" if filename.lower().endswith(".csv") else ".xls"
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name
            try:
                parsed = parse_custom_multiplier_file(tmp_path)
                for prov, d_dict in parsed.items():
                    if prov not in DISTRICT_BASE_MULTIPLIERS:
                        DISTRICT_BASE_MULTIPLIERS[prov] = {}
                    DISTRICT_BASE_MULTIPLIERS[prov].update(d_dict)
                self.send_json({
                    "success": True,
                    "updated_provinces": len(parsed),
                    "total_districts": sum(len(v) for v in parsed.values()),
                    "message": f"'{filename}' başarıyla yüklendi! Çarpan veri tabanı güncellendi."
                })
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        except Exception as exc:
            self.send_json({"error": f"Çarpan dosyası yüklenemedi: {exc}"}, 500)

    def handle_upload_tuik_adnks(self):
        try:
            req = self.read_json_body()
            filename = req.get("filename", "tuik_adnks.csv")
            file_base64 = req.get("file_base64", "")
            if not file_base64:
                self.send_json({"error": "Dosya boş"}, 400)
                return
            if "," in file_base64:
                file_base64 = file_base64.split(",", 1)[1]
            file_bytes = base64.b64decode(file_base64)
            result = parse_tuik_adnks_file(file_bytes, filename)
            self.send_json(result)
        except Exception as exc:
            self.send_json({"error": f"TÜİK tablosu okunamadı: {exc}"}, 500)

    def handle_calculate(self):
        try:
            req = self.read_json_body()
            template_key = req.get("template_key", "standart_kentsel_plan")
            tmpl = CITY_TEMPLATES.get(template_key, CITY_TEMPLATES["standart_kentsel_plan"])

            base_pop = int(req.get("base_pop", tmpl.get("base_pop", 65395)))
            base_year = int(req.get("base_year", tmpl.get("base_year", 2025)))
            target_1 = int(req.get("target_year_1", 2045))
            target_2 = int(req.get("target_year_2", 2050))
            # Yıl tutarlılığı: hedef yıllar başlangıç yılından sonra olmalı ve Hedef 2 >= Hedef 1
            if target_1 <= base_year:
                target_1 = base_year + 1
            if target_2 < target_1:
                target_2 = target_1
            end_year = max(target_1, target_2)
            tfr = float(req.get("tfr", tmpl.get("tfr", 1.545)))
            alpha = float(req.get("alpha", 2.0))
            hh_size = float(req.get("household_size", 2.85))

            # Macro / Historical data
            macro_hist = req.get("macro_history", tmpl.get("macro_history", []))
            if not macro_hist:
                macro_hist = [
                    {"year": 2010, "pop": int(base_pop * 0.85)},
                    {"year": 2015, "pop": int(base_pop * 0.90)},
                    {"year": 2020, "pop": int(base_pop * 0.95)},
                    {"year": base_year, "pop": base_pop}
                ]
            macro_hist = sorted(macro_hist, key=lambda item: int(item["year"]))

            t_hist = [int(item["year"]) for item in macro_hist]
            p_hist = [float(item["pop"]) for item in macro_hist]

            # Üst Bölge (İl veya Türkiye Geneli) Popülasyon Serisi (Prof. Dr. K. Mert Çubukçu Pay Modelleri)
            prov_input = str(req.get("province", "")).strip()
            dist_input = str(req.get("district", "")).strip()
            upper_pop_hist = None
            upper_name = "Türkiye Geneli"

            if dist_input == "IL_GENELI" or dist_input == "TÜM İLÇELER" or (not dist_input and prov_input):
                # İl Geneli modellendiğinde üst bölge Türkiye Geneli'dir (85 Milyon)
                upper_name = "Türkiye Geneli"
                hist_len = len(t_hist)
                turkey_hist_sum = [0.0] * hist_len
                for pk, prov_dict in TUIK_ADNKS_DATA.items():
                    for dk, d_info in prov_dict.items():
                        dh = d_info.get("pop_history", [])
                        for i in range(min(len(dh), hist_len)):
                            turkey_hist_sum[i] += float(dh[i])
                if any(v > 0 for v in turkey_hist_sum):
                    upper_pop_hist = turkey_hist_sum
            elif prov_input:
                prov_norm = _normalize_str(prov_input)
                matched_prov = None
                for pk in TUIK_ADNKS_DATA.keys():
                    if _normalize_str(pk) == prov_norm:
                        matched_prov = pk
                        break
                if matched_prov:
                    districts_dict = TUIK_ADNKS_DATA[matched_prov]
                    hist_len = len(t_hist)
                    prov_hist_sum = [0.0] * hist_len
                    valid_dist_count = 0
                    for d_key, d_info in districts_dict.items():
                        dh = d_info.get("pop_history", [])
                        if len(dh) >= hist_len:
                            valid_dist_count += 1
                            for i in range(hist_len):
                                prov_hist_sum[i] += float(dh[i])
                    if valid_dist_count > 0:
                        upper_pop_hist = prov_hist_sum
                        upper_name = f"{matched_prov} Geneli"

            # 1. Curve Fitting Engine (8 Models: 6 Matematiksel Regresyon + 2 Çubukçu Pay Modeli)
            curve_years = sorted(set(t_hist) | set(range(min(t_hist), end_year + 1)) | {target_1, target_2})
            curve_results = CurveFittingEngine.evaluate_all_models(
                t_hist, p_hist, curve_years,
                upper_pop_hist=upper_pop_hist,
                upper_name=upper_name
            )
            curve_results["years"] = curve_years
            curve_results["target_years"] = [target_1, target_2]
            curve_results["history"] = {"years": t_hist, "pop": p_hist}
            best_model_key = "linear"
            best_r2 = -1.0
            best_sse = float("inf")
            # Kentsel Planlama ve En Küçük Kareler Regresyon Standardı (Prof. Dr. K. Mert Çubukçu):
            # En yüksek R² ve en düşük SSE (hata kareleri toplamı) veren, ileriye dönük negatif çöküş
            # üretmeyen bilimsel olarak en uyumlu analitik model seçilir.
            for m_key, m_val in curve_results["models"].items():
                if not m_val.get("is_valid", True):
                    continue
                preds = list(m_val.get("predictions", {}).values())
                if any(p <= 0 for p in preds):
                    continue
                r2 = m_val["metrics"].get("r2", 0.0)
                sse = m_val["metrics"].get("sse", float("inf"))
                if r2 > best_r2 + 1e-5:
                    best_r2 = r2
                    best_sse = sse
                    best_model_key = m_key
                elif abs(r2 - best_r2) <= 1e-5 and sse < best_sse:
                    best_sse = sse
                    best_model_key = m_key

            if best_r2 < 0.0 and "linear" in curve_results["models"]:
                best_model_key = "linear"

            curve_results["best_model"] = best_model_key

            # 2. Economic Base Engine
            tot_jobs = int(req.get("total_jobs", tmpl.get("total_employment", int(base_pop * 0.51))))
            target_jobs = int(req.get("target_jobs", 0))
            basic_jobs = int(req.get("basic_jobs", tmpl.get("basic_employment", int(tot_jobs * 0.20))))
            new_basic = int(req.get("new_basic_jobs", 2650))
            raw_enable_mig = req.get("enable_econ_migration")
            enable_econ_mig = True if raw_enable_mig is None else bool(raw_enable_mig)

            # Granular param toggles from individual card checkboxes
            use_k = bool(req.get("use_k", True))
            use_b = bool(req.get("use_b", True))
            use_cur_emp = bool(req.get("use_cur_emp", True))
            use_target_emp = bool(req.get("use_target_emp", True))
            use_mig_rate = bool(req.get("use_mig_rate", True))

            econ_ratios = EconomicBaseEngine.calculate_ratios(base_pop, tot_jobs, basic_jobs)
            k_mult = float(req.get("base_multiplier_k", econ_ratios["base_multiplier_k"])) if use_k else 1.0
            b_ratio = float(req.get("dependency_ratio_b", econ_ratios["dependency_ratio_b"])) if use_b else 1.0

            if not use_cur_emp:
                tot_jobs = 0

            years_diff = max(1, target_1 - base_year)
            direct_mig_pop = req.get("direct_migrant_pop")
            mig_rate_pct = req.get("migration_rate_pct")
            mig_mode = req.get("migration_mode", "employment")
            net_new_emp = 0
            migrant_pop = 0
            calc_rate = 0.0

            if not enable_econ_mig or (not use_target_emp and not use_mig_rate):
                econ_mig = {
                    "new_basic_jobs": 0,
                    "base_multiplier_k": round(k_mult, 3),
                    "dependency_ratio_b": round(b_ratio, 3),
                    "total_new_jobs": 0,
                    "non_basic_new_jobs": 0,
                    "total_migrant_pop": 0,
                    "plan_share_pct": 100.0,
                    "plan_migrant_pop": 0,
                    "annual_migration_rate": 0.0,
                    "formula_summary": "Doğal Projeksiyon (Seçili Göç/İstihdam Müdahalesi Yok)"
                }
            elif use_mig_rate and not use_target_emp:
                rate_val = float(mig_rate_pct if mig_rate_pct is not None else 1.82)
                migrant_pop = round(base_pop * (rate_val / 100.0) * years_diff)
                calc_rate = rate_val
                net_new_emp = round(migrant_pop / max(0.5, b_ratio)) if use_b else migrant_pop
                new_basic = max(1, int(net_new_emp / max(1.0, k_mult))) if use_k else net_new_emp
                econ_mig = {
                    "new_basic_jobs": new_basic,
                    "base_multiplier_k": round(k_mult, 3),
                    "dependency_ratio_b": round(b_ratio, 3),
                    "total_new_jobs": net_new_emp,
                    "non_basic_new_jobs": max(0, net_new_emp - new_basic),
                    "total_migrant_pop": migrant_pop,
                    "plan_share_pct": 100.0,
                    "plan_migrant_pop": migrant_pop,
                    "annual_migration_rate": calc_rate,
                    "formula_summary": f"Yıllık Net Göç Hızı: %{calc_rate:.2f} (Yılda {round(migrant_pop / years_diff):,} Kişi) --> Toplam Göç: {migrant_pop:,} Kişi"
                }
            elif use_target_emp and not use_mig_rate:
                net_new_emp = max(0, target_jobs - tot_jobs)
                new_basic = max(1, int(net_new_emp / max(1.0, k_mult))) if use_k else net_new_emp
                migrant_pop = round(net_new_emp * b_ratio) if use_b else net_new_emp
                calc_rate = round((migrant_pop / years_diff) / base_pop * 100.0, 2)
                econ_mig = {
                    "new_basic_jobs": new_basic,
                    "base_multiplier_k": round(k_mult, 3),
                    "dependency_ratio_b": round(b_ratio, 3),
                    "total_new_jobs": net_new_emp,
                    "non_basic_new_jobs": max(0, net_new_emp - new_basic),
                    "total_migrant_pop": migrant_pop,
                    "plan_share_pct": 100.0,
                    "plan_migrant_pop": migrant_pop,
                    "annual_migration_rate": calc_rate,
                    "formula_summary": f"Hedef İstihdam Artışı: +{net_new_emp:,} İş --> Toplam Göç: {migrant_pop:,} Kişi (Yıllık %{calc_rate:.2f})"
                }
            else:
                mig_mode = req.get("migration_mode", "employment")
                if mig_mode == "rate" and mig_rate_pct is not None:
                    rate_val = float(mig_rate_pct)
                    migrant_pop = round(base_pop * (rate_val / 100.0) * years_diff)
                    calc_rate = rate_val
                    net_new_emp = round(migrant_pop / max(0.5, b_ratio)) if use_b else migrant_pop
                    new_basic = max(1, int(net_new_emp / max(1.0, k_mult))) if use_k else net_new_emp
                else:
                    if target_jobs > tot_jobs:
                        net_new_emp = target_jobs - tot_jobs
                        new_basic = max(1, int(net_new_emp / max(1.0, k_mult))) if use_k else net_new_emp
                    else:
                        net_new_emp = int(new_basic * k_mult)
                    migrant_pop = round(net_new_emp * b_ratio) if use_b else net_new_emp
                    calc_rate = round((migrant_pop / years_diff) / base_pop * 100.0, 2)

                econ_mig = {
                    "new_basic_jobs": new_basic,
                    "base_multiplier_k": round(k_mult, 3),
                    "dependency_ratio_b": round(b_ratio, 3),
                    "total_new_jobs": net_new_emp,
                    "non_basic_new_jobs": max(0, net_new_emp - new_basic),
                    "total_migrant_pop": migrant_pop,
                    "plan_share_pct": 100.0,
                    "plan_migrant_pop": migrant_pop,
                    "annual_migration_rate": calc_rate,
                    "formula_summary": f"Net Yeni İstihdam: +{net_new_emp:,} | Yıllık Göç Hızı: %{calc_rate:.2f} --> Toplam Göç: {migrant_pop:,} Kişi"
                }

            # High scenario targets
            plan_high_2045 = base_pop + econ_mig["plan_migrant_pop"]
            plan_high_2050 = int(plan_high_2045 * 1.055)

            # 3. Demographic Shocks Engine
            shock_engine = ShockEngine()
            raw_shocks = req.get("shocks")
            if raw_shocks is not None:
                for s in raw_shocks:
                    shock_engine.add_shock(DemographicShock.from_dict(s))
            elif "preset_shocks" in req:
                for s in ShockEngine.PRESET_SHOCKS[:2]:
                    shock_engine.add_shock(DemographicShock.from_dict(s))

            shock_dict_list = [s.to_dict() for s in shock_engine.shocks]

            # 4. Cohort Component Engine
            cohort_engine = CohortComponentEngine(base_year=base_year, base_population=base_pop, tfr=tfr)

            custom_m = req.get("cohort_male", [])
            custom_f = req.get("cohort_female", [])
            if custom_m and custom_f and len(custom_m) == 17 and len(custom_f) == 17:
                m_init = [int(v) for v in custom_m]
                f_init = [int(v) for v in custom_f]
            else:
                male_ratio = float(req.get("male_ratio") or 0.505)
                male_ratio = min(0.70, max(0.30, male_ratio))
                m_init, f_init = CohortComponentEngine.synthesize_standard_age_sex_distribution(
                    base_pop, male_ratio=male_ratio, tfr=tfr
                )

            indicators = CohortComponentEngine.calculate_indicators(m_init, f_init)

            # Simulate scenarios
            step_set = set()
            yy = base_year + 5
            while yy < end_year:
                step_set.add(yy)
                yy += 5
            step_set.update({target_1, target_2})
            steps = sorted(y for y in step_set if y > base_year)

            def run_scenario(annual_mig, apply_shocks=False):
                cur_m, cur_f = list(m_init), list(f_init)
                prev_year = base_year
                out = {}
                for yr in steps:
                    cur_m, cur_f = cohort_engine.project_period(
                        cur_m, cur_f, years=yr - prev_year,
                        annual_migration=annual_mig,
                        shock_engine=shock_engine if apply_shocks else None,
                        start_year=prev_year
                    )
                    prev_year = yr
                    ind_yr = CohortComponentEngine.calculate_indicators(cur_m, cur_f)
                    out[yr] = {
                        "total": sum(cur_m) + sum(cur_f),
                        "male": list(cur_m),
                        "female": list(cur_f),
                        "indicators": ind_yr
                    }
                return out

            # Low scenario (0 net migration)
            low_steps = run_scenario(0.0, apply_shocks=False)

            # High scenario (distributing migration + plan shocks)
            annual_mig_high = econ_mig["plan_migrant_pop"] / max(1, (target_1 - base_year))
            high_steps = run_scenario(annual_mig_high, apply_shocks=True)

            # Mid scenario (trend: average of linear model & natural growth)
            lin_pred_t1 = curve_results["models"]["linear"]["predictions"].get(target_1, base_pop * 1.1)
            annual_mig_mid = max(0, (lin_pred_t1 - low_steps[target_1]["total"]) / max(1, (target_1 - base_year)))
            mid_steps = run_scenario(annual_mig_mid)

            # Summary Table and Alternative Scenarios for Planning Studio
            natural_t1 = low_steps[target_1]["total"]
            migrant_t1 = round(econ_mig["plan_migrant_pop"])
            total_plan_t1 = natural_t1 + migrant_t1

            summary_table = {
                "base_year": base_year,
                "base_pop": base_pop,
                "target_year": target_1,
                "natural_pop": natural_t1,
                "current_jobs": tot_jobs,
                "target_jobs": target_jobs if target_jobs > 0 else tot_jobs + round(econ_mig["total_new_jobs"]),
                "net_jobs": net_new_emp if enable_econ_mig else 0,
                "multiplier_k": round(k_mult, 2),
                "dependency_b": round(b_ratio, 2),
                "migrant_pop": migrant_t1,
                "annual_migration_rate": econ_mig.get("annual_migration_rate", 0.0),
                "total_plan_pop": total_plan_t1
            }

            best_model_name = curve_results.get("best_model", "linear")
            mid_curve_pop = curve_results["models"].get(best_model_name, {}).get("predictions", {}).get(target_1, mid_steps[target_1]["total"])

            if mig_mode == "rate" and enable_econ_mig:
                high_assumption = f"Yıllık Net Göç Hızı (%{econ_mig.get('annual_migration_rate', 0.0):.2f}) ile Toplam +{migrant_t1:,} Göçmen Nüfus"
            elif enable_econ_mig:
                high_assumption = f"İktisadi Taban Sanayi Genişlemesi + Baz Çarpanı ({k_mult:.2f}) + Bağımlılık ({b_ratio:.2f}) Göçü"
            else:
                high_assumption = "Plan kabulü / Dinamik Şoklar"

            alternative_scenarios = {
                "low": {
                    "title": "DÜŞÜK (DURGUNLUK)",
                    "population": natural_t1,
                    "diff_pct": round(((natural_t1 - base_pop) / base_pop) * 100.0, 2),
                    "assumption": "Sıfır göç, sadece demografik doğal yaşlanma (Kuşak-Bileşen kapalı model)",
                    "role": "En Düşük Altyapı Risk Eşiği"
                },
                "mid": {
                    "title": "ORTA (TREND / REGRESYON)",
                    "population": mid_curve_pop,
                    "diff_pct": round(((mid_curve_pop - base_pop) / base_pop) * 100.0, 2),
                    "assumption": f"Geçmiş eğilimin analitik devamı ({best_model_name})",
                    "role": "Mevcut Eğilim Devamı (Trend)"
                },
                "high": {
                    "title": "YÜKSEK (SANAYİ / VİZYON)",
                    "population": total_plan_t1,
                    "diff_pct": round(((total_plan_t1 - base_pop) / base_pop) * 100.0, 2),
                    "assumption": high_assumption,
                    "role": "Nazım İmar Planı Kabulü & Donatı Eşiği (Önerilen)"
                }
            }

            # Shock integrated timeline
            base_timeline = {base_year: base_pop}
            for yr in steps:
                base_timeline[yr] = mid_steps[yr]["total"]
            shock_timeline_res = shock_engine.apply_to_timeline(base_timeline)

            cohort_results = {
                "base_year": base_year,
                "base_pop": base_pop,
                "years": {"base": base_year, "t1": target_1, "t2": target_2},
                "step_years": steps,
                "age_groups": AGE_GROUPS,
                "initial_pyramid": {"male": m_init, "female": f_init},
                "sx_male": cohort_engine.sx_m,
                "sx_female": cohort_engine.sx_f,
                "tfr": tfr,
                "indicators": indicators,
                "scenarios": {
                    "low": {"title": "Düşük Senaryo (%0 Göç)", "steps": low_steps},
                    "mid": {"title": "Orta Senaryo (Geçmiş Trend)", "steps": mid_steps},
                    "high": {"title": "Yüksek Senaryo (Plan Kabulü)", "steps": high_steps},
                    "shock": {"title": "Şoklu Dinamik Senaryo", "timeline": shock_timeline_res}
                }
            }

            # 5. Hansen Spatial Allocation Engine
            subzones = req.get("subzones", tmpl.get("subzones", []))
            if not subzones:
                # Synthesize 5 representative subzones scaled to base_pop (Prof. Dr. K. Mert Çubukçu / KUZİP Standartları)
                p_merkez = int(base_pop * 0.35)
                p_gelisme = int(base_pop * 0.25)
                p_sanayi = int(base_pop * 0.15)
                p_cumhuriyet = int(base_pop * 0.15)
                p_kirsal = max(1, base_pop - (p_merkez + p_gelisme + p_sanayi + p_cumhuriyet))
                subzones = [
                    {"id": 1, "name": "Merkez Mahalle", "current_pop": p_merkez, "base_pop": p_merkez, "employment": int(p_merkez * 0.45), "jobs": int(p_merkez * 0.45), "vacant_area_ha": 8.0, "capacity_ha": 8.0, "dist_to_center_min": 1.5, "distance_to_center_min": 1.5, "plan_capacity_pop": int(p_merkez * 1.65), "plan_pop_capacity": int(p_merkez * 1.65)},
                    {"id": 2, "name": "Yeni Gelişme Bölgesi", "current_pop": p_gelisme, "base_pop": p_gelisme, "employment": int(p_gelisme * 0.35), "jobs": int(p_gelisme * 0.35), "vacant_area_ha": 55.0, "capacity_ha": 55.0, "dist_to_center_min": 3.0, "distance_to_center_min": 3.0, "plan_capacity_pop": int(p_gelisme * 2.80), "plan_pop_capacity": int(p_gelisme * 2.80)},
                    {"id": 3, "name": "Sanayi ve İş Çevresi", "current_pop": p_sanayi, "base_pop": p_sanayi, "employment": int(p_sanayi * 0.70), "jobs": int(p_sanayi * 0.70), "vacant_area_ha": 30.0, "capacity_ha": 30.0, "dist_to_center_min": 4.5, "distance_to_center_min": 4.5, "plan_capacity_pop": int(p_sanayi * 2.20), "plan_pop_capacity": int(p_sanayi * 2.20)},
                    {"id": 4, "name": "Cumhuriyet Konut Alanı", "current_pop": p_cumhuriyet, "base_pop": p_cumhuriyet, "employment": int(p_cumhuriyet * 0.30), "jobs": int(p_cumhuriyet * 0.30), "vacant_area_ha": 35.0, "capacity_ha": 35.0, "dist_to_center_min": 3.5, "distance_to_center_min": 3.5, "plan_capacity_pop": int(p_cumhuriyet * 2.50), "plan_pop_capacity": int(p_cumhuriyet * 2.50)},
                    {"id": 5, "name": "Kırsal / Çevre Mahalle", "current_pop": p_kirsal, "base_pop": p_kirsal, "employment": int(p_kirsal * 0.25), "jobs": int(p_kirsal * 0.25), "vacant_area_ha": 45.0, "capacity_ha": 45.0, "dist_to_center_min": 7.5, "distance_to_center_min": 7.5, "plan_capacity_pop": int(p_kirsal * 1.80), "plan_pop_capacity": int(p_kirsal * 1.80)},
                ]

            additional_pop = high_steps[target_1]["total"] - base_pop
            if additional_pop <= 0:
                additional_pop = max(100, int(base_pop * 0.15))

            hansen_res = HansenAllocationEngine.allocate_population(
                subzones=subzones,
                total_additional_pop=additional_pop,
                alpha=alpha,
                household_size=hh_size
            )

            # 6. MPYY Urban Standards (Mekânsal Planlar Yapım Yönetmeliği Ek-2)
            # Standards per capita: Eğitim: 4 m², Sağlık: 1.5 m², Yeşil Alan: 10 m², Sosyal/Kültür: 1.5 m², İbadet: 0.5 m², Teknik: 1.5 m² = Toplam 19 m² ilave alan
            add_pop_val = max(100, high_steps[target_1]["total"] - base_pop)
            mpyy_standards = {
                "egitim": {"name": "Eğitim Tesisleri (Anaokulu, İlkokul, Orta, Lise)", "per_capita": 4.0, "total_sqm": add_pop_val * 4.0, "ha": (add_pop_val * 4.0) / 10000.0},
                "saglik": {"name": "Sağlık Tesisleri (ASM, Semt Polikliniği, Hastane)", "per_capita": 1.5, "total_sqm": add_pop_val * 1.5, "ha": (add_pop_val * 1.5) / 10000.0},
                "yesil": {"name": "Açık ve Yeşil Alanlar (Park, Çocuk Bahçesi, Rekreasyon)", "per_capita": 10.0, "total_sqm": add_pop_val * 10.0, "ha": (add_pop_val * 10.0) / 10000.0},
                "sosyal_kultur": {"name": "Sosyal ve Kültürel Tesisler", "per_capita": 1.5, "total_sqm": add_pop_val * 1.5, "ha": (add_pop_val * 1.5) / 10000.0},
                "ibadet": {"name": "İbadet Alanları (Cami, Mescit)", "per_capita": 0.5, "total_sqm": add_pop_val * 0.5, "ha": (add_pop_val * 0.5) / 10000.0},
                "teknik_altyapi": {"name": "Teknik Altyapı ve Ulaşım Tesisleri", "per_capita": 1.5, "total_sqm": add_pop_val * 1.5, "ha": (add_pop_val * 1.5) / 10000.0},
                "total": {
                    "per_capita": 19.0,
                    "total_sqm": add_pop_val * 19.0,
                    "ha": (add_pop_val * 19.0) / 10000.0
                }
            }

            # Top KPI Summary
            kpis = {
                "base_pop": base_pop,
                "base_year": base_year,
                "target_year_1": target_1,
                "target_year_2": target_2,
                "low_t1": low_steps[target_1]["total"],
                "mid_t1": mid_steps[target_1]["total"],
                "high_t1": high_steps[target_1]["total"],
                "low_t2": low_steps[target_2]["total"],
                "mid_t2": mid_steps[target_2]["total"],
                "high_t2": high_steps[target_2]["total"],
                "low_2045": low_steps[target_1]["total"],
                "mid_2045": mid_steps[target_1]["total"],
                "high_2045": high_steps[target_1]["total"],
                "best_curve_model": curve_results["best_model"],
                "best_curve_r2": curve_results["models"][curve_results["best_model"]]["metrics"]["r2"],
                "best_curve_t1": curve_results["models"][curve_results["best_model"]]["predictions"].get(target_1, 0),
                "best_curve_2045": curve_results["models"][curve_results["best_model"]]["predictions"].get(target_1, 0),
                "mpyy_additional_ha": round(mpyy_standards["total"]["ha"], 2),
                "total_settlements": len(subzones),
                "total_jobs": tot_jobs,
                "basic_multiplier_k": round(k_mult, 3),
                "dependency_ratio_b": round(b_ratio, 3)
            }

            response_data = {
                "success": True,
                "years": {"base": base_year, "t1": target_1, "t2": target_2},
                "kpis": kpis,
                "curve_results": curve_results,
                "economic_base": {
                    "ratios": econ_ratios,
                    "migration": econ_mig,
                    "new_basic_jobs": new_basic,
                    "summary_table": summary_table,
                    "alternative_scenarios": alternative_scenarios
                },
                "demographic_shocks": {
                    "shocks": shock_dict_list,
                    "timeline": shock_timeline_res
                },
                "cohort_results": cohort_results,
                "hansen_results": hansen_res,
                "mpyy_standards": mpyy_standards
            }

            self.send_json(response_data)

        except Exception as exc:
            import traceback
            traceback.print_exc()
            self.send_json({"error": f"Hesaplama hatası: {str(exc)}"}, 500)

    def handle_export_report(self):
        try:
            req = self.read_json_body()
            template_data = req.get("template_data", {})
            curve_results = req.get("curve_results", {})
            cohort_results = req.get("cohort_results", {})
            econ_results = req.get("economic_base", {})
            shock_results = req.get("demographic_shocks", {})

            with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
                tmp_path = tmp.name

            try:
                ExcelReportEngine.generate_full_workbook(
                    filepath=tmp_path,
                    template_data=template_data,
                    curve_results=curve_results,
                    cohort_results=cohort_results,
                    econ_results=econ_results,
                    shock_results=shock_results
                )
                data = Path(tmp_path).read_bytes()
                self.send_response(200)
                self.send_cors_headers()
                self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                self.send_header("Content-Disposition", 'attachment; filename="Kentsel_Projeksiyon_Raporu.xlsx"')
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

        except Exception as exc:
            self.send_json({"error": f"Excel raporu üretilemedi: {str(exc)}"}, 500)


def print_banner(local_ip: str, port: int):
    print("=" * 70)
    print("  🌐 KENTSEL VE BÖLGESEL DEMOGRAFİK PROJEKSİYON MODELİ PRO")
    print("  📱 Bağımsız Web & Mobil Uygulama Sunucusu (Zero-Dependency)")
    print("=" * 70)
    print(f"  💻 Bilgisayarınızdan Erişim:  http://localhost:{port}")
    print(f"  📱 Telefonunuzdan Erişim:     http://{local_ip}:{port}")
    print("=" * 70)
    print("  İpucu: Cep telefonunuz bilgisayarınızla aynı Wi-Fi ağına bağlıyken,")
    print(f"  telefon tarayıcınıza (Safari/Chrome) http://{local_ip}:{port} yazın veya")
    print("  ekrandaki QR kodu okutarak 'Ana Ekrana Ekle' (PWA) yapın!")
    print("=" * 70)


def run_server(port: int = 8080, open_browser: bool = True):
    local_ip = get_local_ip()

    # Find open port if 8080 occupied
    server = None
    for trial_port in range(port, port + 20):
        try:
            server = ThreadingHTTPServer(("0.0.0.0", trial_port), DemographicsWebHandler)
            port = trial_port
            break
        except OSError:
            continue

    if not server:
        print(f"HATA: {port} ile {port + 20} arasındaki portlar meşgul!")
        sys.exit(1)

    print_banner(local_ip, port)

    if open_browser:
        try:
            webbrowser.open(f"http://localhost:{port}")
        except Exception:
            pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu kapatıldı.")
        server.server_close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Urban Demographics Pro Web/Mobile Server")
    env_port = int(os.environ.get("PORT", 8080))
    is_cloud = bool(os.environ.get("PORT") or os.environ.get("RENDER") or os.environ.get("RAILWAY_ENVIRONMENT"))
    parser.add_argument("--port", type=int, default=env_port, help="Port to listen on (default 8080)")
    parser.add_argument("--no-browser", action="store_true", default=is_cloud, help="Do not open browser automatically")
    args = parser.parse_args()

    run_server(port=args.port, open_browser=not args.no_browser)
