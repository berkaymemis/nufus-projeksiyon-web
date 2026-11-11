# -*- coding: utf-8 -*-
"""
Hansen Accessibility & Spatial Population Allocation Engine
Prof. Dr. K. Mert Çubukçu — "Kuzey İzmir Mekânsal Gelişme Perspektifi (KUZİP) 2026" (Ek-1) &
"Planlamada Klasik Sayısal Yöntemler" (Bölüm: Hansen Erişilebilirlik Modeli)

Formülasyon:
1. Ulaşılabilirlik Endeksi: Ai = Σ (Ej / dij^α)
2. Çekim / Dağıtım Oranı: Ri = (Ai × Hi) / Σ (Ak × Hk)
3. Mahalleye / Bölgeciğe Yerleşecek Ek Nüfus: Gi = GT × Ri
4. Gelecek Hedef Nüfus: Pi(t+1) = Pi(t0) + Gi
5. İmar Planı Doluluk Oranı (%): (Pi(t+1) / Plan Kapasitesi) × 100
6. Yeni Konut İhtiyacı: Gi / Ortalama Hanehalkı Büyüklüğü
"""

import math
from typing import List, Dict, Any, Optional


class HansenAllocationEngine:
    """
    Yer çekimi (gravity) temelli erişilebilirlik ve ek nüfus mekânsal dağıtım modeli.
    """

    @staticmethod
    def calculate_accessibility(
        employment_nodes: List[Dict[str, Any]],
        distance_matrix: List[List[float]],
        alpha: float = 2.0
    ) -> List[float]:
        """
        Ai = Σ (Ej / dij^α)
        employment_nodes: [{'name': '...', 'jobs': 12000}, ...]
        distance_matrix: N x N mesafe (dakika veya km) matrisi
        alpha: mesafe sürtünme katsayısı (KUZİP standart değeri: 2.00)
        """
        n = len(employment_nodes)
        accessibility_scores = []

        for i in range(n):
            a_i = 0.0
            for j in range(n):
                d_ij = max(1.0, distance_matrix[i][j])  # 0 mesafede sıfıra bölme engeli
                e_j = employment_nodes[j].get("jobs", 1000)
                a_i += e_j / (d_ij ** alpha)
            accessibility_scores.append(round(a_i, 4))

        return accessibility_scores

    @staticmethod
    def allocate_population(
        subzones: List[Dict[str, Any]],
        total_additional_pop: float,
        alpha: float = 2.0,
        household_size: float = 2.85
    ) -> Dict[str, Any]:
        """
        subzones: [
            {
                'id': 1, 'name': 'Fatih',
                'base_pop': 11988,
                'jobs': 6500,
                'capacity_ha': 45.0,        # Yerleşime uygun boş konut/gelişme alanı (Hi)
                'plan_pop_capacity': 18000, # İmar planı nüfus taşıma kapasitesi
                'distance_to_center_min': 5.0
            }, ...
        ]
        """
        n = len(subzones)
        if n == 0 or total_additional_pop <= 0:
            return {"subzones": [], "total_allocated": 0}

        # 1. Sentetik / Gerçek Mesafe ve Erişilebilirlik
        # Eğer tam NxN matris yoksa, merkeze ve istihdam akslarına göre mesafe hesaplanır
        accessibility_list = []
        for i, sz in enumerate(subzones):
            d_center = max(1.0, float(sz.get("distance_to_center_min") or sz.get("dist_to_center_min") or 5.0))
            jobs = float(sz.get("jobs") if sz.get("jobs") is not None else (sz.get("employment") or 1000))
            # Yerel cazibe + merkeze erişilebilirlik
            a_i = (jobs / (d_center ** alpha)) + 10.0
            accessibility_list.append(a_i)

        # 2. Ri = (Ai × Hi) / Σ (Ak × Hk)
        weighted_scores = []
        for i, sz in enumerate(subzones):
            h_i = max(1.0, float(sz.get("capacity_ha") if sz.get("capacity_ha") is not None else (sz.get("vacant_area_ha") or 10.0)))
            score = accessibility_list[i] * h_i
            weighted_scores.append(score)

        tot_score = sum(weighted_scores) if sum(weighted_scores) > 0 else 1.0
        allocation_ratios = [w / tot_score for w in weighted_scores]

        # 3. Gi = GT × Ri ve Plan Doluluk Oranı
        results = []
        tot_allocated = 0
        for i, sz in enumerate(subzones):
            r_i = allocation_ratios[i]
            g_i = int(round(total_additional_pop * r_i))
            tot_allocated += g_i

            p_base = int(sz.get("base_pop") if sz.get("base_pop") is not None else (sz.get("current_pop") or 0))
            p_target = p_base + g_i
            p_cap = int(sz.get("plan_pop_capacity") or sz.get("plan_capacity_pop") or max(1, round(p_target * 1.25)))

            saturation_pct = round((p_target / p_cap) * 100.0, 1) if p_cap > 0 else 100.0
            housing_need = int(round(g_i / household_size)) if g_i > 0 else 0

            # KUZİP Değerlendirmesi
            if saturation_pct > 100.0:
                review = "⚠️ PLAN KAPASİTESİ YETERSİZ: İlave imar planı ve konut alanı açılmalı"
                status = "deficit"
            elif saturation_pct >= 85.0:
                review = "🟠 KRİTİK EŞİKTE: Plan kapasitesi doygunluğa yaklaşıyor"
                status = "critical"
            else:
                review = "✅ PLAN KAPASİTESİ YETERLİ: Rezerv konut alanı mevcut"
                status = "sufficient"

            results.append({
                "id": sz.get("id", i + 1),
                "name": sz.get("name", f"Bölgecik {i+1}"),
                "base_pop": p_base,
                "jobs": sz.get("jobs", 0),
                "capacity_ha": sz.get("capacity_ha", 0.0),
                "plan_capacity": p_cap,
                "accessibility_score": round(accessibility_list[i], 2),
                "distribution_ratio_pct": round(r_i * 100.0, 2),
                "additional_pop_Gi": g_i,
                "target_pop_Pi": p_target,
                "saturation_pct": saturation_pct,
                "housing_need": housing_need,
                "review": review,
                "status": status
            })

        # Yuvarlama farkı düzeltmesi
        diff = int(round(total_additional_pop)) - tot_allocated
        if diff != 0 and results:
            results[0]["additional_pop_Gi"] += diff
            results[0]["target_pop_Pi"] += diff

        return {
            "total_additional_pop": total_additional_pop,
            "household_size": household_size,
            "subzones": results
        }
