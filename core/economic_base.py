# -*- coding: utf-8 -*-
"""
Economic Base Multiplier & Labour-to-Migration Engine
Prof. Dr. K. Mert Çubukçu — "Planlamada Klasik Sayısal Yöntemler"
İktisadi Taban Analizi ve İş Gücüne Bağlı Nüfus Göçü Modeli
"""

import math
from typing import Dict, Any, Tuple, Optional, List
from .district_multipliers import (
    DISTRICT_BASE_MULTIPLIERS,
    get_all_provinces,
    get_districts_by_province,
    get_district_info,
    CITATION_CUBUKCU_2011,
    CITATION_KUZIP_2026
)


class EconomicBaseEngine:
    """
    İktisadi Taban (Economic Base Multiplier) ve Nüfus-İş Gücü İlişkisi Modeli (Çubukçu, 2014):
    
    1. Temel İş Gücü (Eb): Dış pazara dönük, bölge dışına mal/hizmet ihraç eden istihdam (Sanayi, Lojistik, İhracat Tarımı vb.)
    2. Temel Olmayan İş Gücü (Enb): Yerel iç tüketime dönük hizmet ve ticaret (Bakkal, fırın, berber, yerel hizmetler vb.)
    3. Toplam İş Gücü (Et): Et = Eb + Enb
    4. Baz Çarpanı (k): k = Et / Eb (Her 1 birim temel sanayi çalışanı kaç toplam çalışan tetikler?)
    5. Demografik Bağımlılık Oranı (b): b = Nüfus (P) / Toplam İş Gücü (Et) (1 çalışan başına kentsel nüfus yükü)
    6. Göç Potansiyeli (ΔP): ΔP = ΔEt × b = (ΔEb × k) × b
    """

    BENCHMARK_PROFILES = {
        "sanayi_kenti": {
            "name": "Sanayi Odaklı Gelişen Kent / Ağır Sanayi Havzası",
            "k_default": 4.80,
            "b_default": 2.05,
            "workers_per_ha": 35.0,
            "desc": "Ağır sanayi, OSB ve lojistik odaklı yüksek çarpan etkisi (k=4.5-5.5, b=1.9-2.2)"
        },
        "metropol_hizmet": {
            "name": "Metropoliten Merkez / Üçüncül Hizmet Kenti",
            "k_default": 3.60,
            "b_default": 2.20,
            "workers_per_ha": 45.0,
            "desc": "Finans, yönetim, bilişim ve üçüncül sektör ağırlıklı (k=3.2-4.0, b=2.1-2.4)"
        },
        "tarim_kirsal": {
            "name": "Tarım ve Kırsal Sanayi / Gıda İhtisas Havzası",
            "k_default": 4.90,
            "b_default": 1.96,
            "workers_per_ha": 30.0,
            "desc": "Tarıma dayalı ihtisas sanayi, gıda ve yerel iş gücü (k=4.5-5.2, b=1.8-2.1)"
        },
        "turizm_kentsel": {
            "name": "Turizm, Kıyı ve Rekreasyon Yerleşimi",
            "k_default": 3.80,
            "b_default": 1.85,
            "workers_per_ha": 25.0,
            "desc": "Mevsimsel turizm, otelcilik ve rekreasyon istihdamı (k=3.5-4.2, b=1.7-2.0)"
        }
    }

    @staticmethod
    def calculate_ratios(
        population: float,
        total_employment: float,
        basic_employment: float
    ) -> Dict[str, Any]:
        """
        Nüfus, toplam iş gücü ve temel iş gücünden k ve b oranlarını otomatik çıkarır.
        """
        if basic_employment <= 0:
            basic_employment = 1.0
        if total_employment <= 0:
            total_employment = basic_employment

        k = total_employment / basic_employment
        b = population / total_employment if total_employment > 0 else 2.0
        non_basic = max(0.0, total_employment - basic_employment)
        activity_rate = (total_employment / population * 100.0) if population > 0 else 0.0

        return {
            "population": population,
            "total_employment": total_employment,
            "basic_employment": basic_employment,
            "non_basic_employment": non_basic,
            "base_multiplier_k": round(k, 3),
            "dependency_ratio_b": round(b, 3),
            "activity_rate_pct": round(activity_rate, 2),
            "formula_k": f"k = Et / Eb = {total_employment:,.0f} / {basic_employment:,.0f} = {k:.3f}",
            "formula_b": f"b = P / Et = {population:,.0f} / {total_employment:,.0f} = {b:.3f}"
        }

    @staticmethod
    def project_employment_migration(
        new_basic_jobs: float,
        base_multiplier_k: float,
        dependency_ratio_b: float,
        share_to_plan_pct: float = 100.0
    ) -> Dict[str, Any]:
        """
        İktisadi Taban Modeli (Economic Base Multiplier Formülü):
        ΔEt = ΔEb × k
        ΔP_toplam = ΔEt × b
        ΔP_plan = ΔP_toplam × (share_to_plan_pct / 100)
        """
        total_new_jobs = new_basic_jobs * base_multiplier_k
        non_basic_new_jobs = total_new_jobs - new_basic_jobs
        total_migrant_pop = total_new_jobs * dependency_ratio_b
        plan_migrant_pop = total_migrant_pop * (share_to_plan_pct / 100.0)

        return {
            "new_basic_jobs": round(new_basic_jobs),
            "base_multiplier_k": round(base_multiplier_k, 3),
            "dependency_ratio_b": round(dependency_ratio_b, 3),
            "total_new_jobs": round(total_new_jobs),
            "non_basic_new_jobs": round(non_basic_new_jobs),
            "total_migrant_pop": round(total_migrant_pop),
            "plan_share_pct": share_to_plan_pct,
            "plan_migrant_pop": round(plan_migrant_pop),
            "formula_summary": (
                f"ΔEb ({new_basic_jobs:,.0f}) × k ({base_multiplier_k:.2f}) = ΔEt ({total_new_jobs:,.0f} Toplam İş Gücü) "
                f"--> ΔEt ({total_new_jobs:,.0f}) × b ({dependency_ratio_b:.2f}) = {total_migrant_pop:,.0f} Kişi Göç "
                f"(Plan Sınırına Gelen: {plan_migrant_pop:,.0f} Kişi)"
            )
        }

    @staticmethod
    def calculate_from_industrial_area(
        area_hectares: float,
        workers_per_ha: float,
        base_multiplier_k: float,
        dependency_ratio_b: float,
        share_to_plan_pct: float = 100.0
    ) -> Dict[str, Any]:
        """
        Sanayi / OSB alan büyüklüğünden (Hektar) göç eden nüfusu adım adım türetir.
        """
        new_basic_jobs = area_hectares * workers_per_ha
        res = EconomicBaseEngine.project_employment_migration(
            new_basic_jobs, base_multiplier_k, dependency_ratio_b, share_to_plan_pct
        )
        res["area_hectares"] = area_hectares
        res["workers_per_ha"] = workers_per_ha
        return res

    @staticmethod
    def get_district_multiplier(
        province: str,
        district: str,
        method: str = "LQ"
    ) -> float:
        """
        Prof. Dr. K. Mert Çubukçu (2011) veri tabanından seçilen il ve ilçenin
        resmi Base Multiplier (k) değerini döner.
        method: 'LQ' (Konum Katsayısı) veya 'MG' (Minimum Gereksinimler)
        """
        info = get_district_info(province, district)
        if not info:
            return 3.0  # Standart kentsel ortalama fallback
        if str(method).strip().upper() == "MG":
            return info.get("bm_mg", 2.0)
        return info.get("bm_lq", 2.5)

    @staticmethod
    def compare_district_methods(
        new_basic_jobs: float,
        province: str,
        district: str,
        dependency_ratio_b: float,
        share_to_plan_pct: float = 100.0
    ) -> Dict[str, Any]:
        """
        Aynı ilçe için LQ ve Minimum Gereksinimler (MG) yöntemlerinin sonuçlarını
        karşılaştırmalı olarak döner.
        """
        info = get_district_info(province, district) or {"bm_lq": 3.271, "bm_mg": 2.295, "pop_2000": 42988}
        k_lq = info.get("bm_lq", 3.271)
        k_mg = info.get("bm_mg", 2.295)

        res_lq = EconomicBaseEngine.project_employment_migration(
            new_basic_jobs, k_lq, dependency_ratio_b, share_to_plan_pct
        )
        res_mg = EconomicBaseEngine.project_employment_migration(
            new_basic_jobs, k_mg, dependency_ratio_b, share_to_plan_pct
        )

        return {
            "province": province,
            "district": district,
            "pop_2000": info.get("pop_2000", 0),
            "lq_method": {
                "name": "Konum Katsayısı (Location Quotient - LQ)",
                "k": k_lq,
                "result": res_lq
            },
            "mg_method": {
                "name": "Minimum Gereksinimler (Minimum Requirements - MG)",
                "k": k_mg,
                "result": res_mg
            },
            "pop_diff": res_lq["plan_migrant_pop"] - res_mg["plan_migrant_pop"],
            "citation": CITATION_CUBUKCU_2011
        }
