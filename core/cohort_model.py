# -*- coding: utf-8 -*-
"""
Generalized Cohort-Component Population Projection Engine
Prof. Dr. K. Mert Çubukçu — "Planlamada Klasik Sayısal Yöntemler" (Bölüm: Kuşak-Bileşenleri Yöntemi)
Yaşam Tabloları (Sx), Yaşa Özel Doğurganlık Hızları (ASFR), Göç Senaryoları ve Şok Entegrasyonu
"""

import math
from typing import List, Dict, Any, Tuple, Optional
from .demographic_shocks import ShockEngine, DemographicShock


AGE_GROUPS = [
    "0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39",
    "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+"
]

# Standart TÜİK / WHO Yaşam Tablosu 5 Yıllık Hayatta Kalma Oranları (Sx)
DEFAULT_SX_MALE = [
    0.9935, 0.9982, 0.9978, 0.9965, 0.9950, 0.9940, 0.9925, 0.9895,
    0.9840, 0.9750, 0.9610, 0.9380, 0.9010, 0.8420, 0.7550, 0.6250, 0.4400
]
DEFAULT_SX_FEMALE = [
    0.9948, 0.9988, 0.9985, 0.9978, 0.9970, 0.9962, 0.9950, 0.9930,
    0.9895, 0.9835, 0.9730, 0.9560, 0.9280, 0.8850, 0.8150, 0.7100, 0.5200
]

# Doğurgan Çağdaki Kadınlar (15-49 yaş, 7 kohort: 15-19, 20-24, ... 45-49) için Standart ASFR Dağılım Ağırlıkları
ASFR_WEIGHTS_7 = [0.035, 0.220, 0.325, 0.260, 0.125, 0.030, 0.005]


class CohortComponentEngine:
    """
    Herhangi bir başlangıç yılı, nüfus ve hedef yıllar için çok periyotlu Kuşak-Bileşen modeli kurar.
    """

    def __init__(
        self,
        base_year: int = 2025,
        base_population: float = 65395,
        tfr: float = 1.52,
        sx_male: Optional[List[float]] = None,
        sx_female: Optional[List[float]] = None,
        sex_ratio_at_birth: float = 1.05  # %51.2 Erkek / %48.8 Kadın
    ):
        self.base_year = base_year
        self.base_population = base_population
        self.tfr = tfr
        self.sx_m = sx_male or list(DEFAULT_SX_MALE)
        self.sx_f = sx_female or list(DEFAULT_SX_FEMALE)
        self.sex_ratio = sex_ratio_at_birth

    @staticmethod
    def synthesize_standard_age_sex_distribution(
        total_pop: float,
        male_ratio: float = 0.505,
        tfr: float = 1.51
    ) -> Tuple[List[int], List[int]]:
        """
        Kullanıcı hazır yaş-cinsiyet matrisi girmediğinde, ilin TFR doğurganlık katsayısına ve
        TÜİK demografik piramit ağırlıklarına göre dengeli bir başlangıç matrisi üretir.
        """
        # Üç referans piramit: yaşlanan (TFR≈1.15), Türkiye ortalaması (TFR≈1.51), genç (TFR≈2.6+).
        # Arada kalan TFR değerleri doğrusal enterpolasyonla karıştırılır; böylece her il/ilçe farklı bir yapı alır.
        w_aging = [
            0.045, 0.048, 0.052, 0.058, 0.064, 0.070, 0.074, 0.076,
            0.075, 0.074, 0.072, 0.068, 0.062, 0.054, 0.044, 0.034, 0.030
        ]
        w_mid = [
            0.054, 0.058, 0.062, 0.065, 0.068, 0.072, 0.075, 0.073,
            0.069, 0.066, 0.062, 0.058, 0.051, 0.043, 0.036, 0.026, 0.022
        ]
        w_young = [
            0.092, 0.090, 0.086, 0.081, 0.076, 0.072, 0.067, 0.062,
            0.057, 0.051, 0.045, 0.038, 0.031, 0.024, 0.015, 0.008, 0.005
        ]
        t = float(tfr)
        if t <= 1.15:
            weights = list(w_aging)
        elif t <= 1.51:
            a = (t - 1.15) / (1.51 - 1.15)
            weights = [x * (1 - a) + y * a for x, y in zip(w_aging, w_mid)]
        elif t <= 2.6:
            a = (t - 1.51) / (2.6 - 1.51)
            weights = [x * (1 - a) + y * a for x, y in zip(w_mid, w_young)]
        else:
            weights = list(w_young)
        tot_w = sum(weights)
        weights = [w / tot_w for w in weights]

        # Yaşa göre erkek payı: doğumda ~%51.2, ileri yaşlarda kadın fazlası. Genel erkek oranı male_ratio'ya ölçeklenir.
        base_share = [
            0.512, 0.512, 0.511, 0.510, 0.508, 0.506, 0.504, 0.503,
            0.502, 0.500, 0.495, 0.485, 0.475, 0.460, 0.445, 0.425, 0.385
        ]
        overall = sum(w * s for w, s in zip(weights, base_share))
        shift = male_ratio - overall
        shares = [min(0.62, max(0.30, s + shift)) for s in base_share]

        m_arr = [int(round(total_pop * w * s)) for w, s in zip(weights, shares)]
        f_arr = [int(round(total_pop * w * (1.0 - s))) for w, s in zip(weights, shares)]

        diff = int(round(total_pop)) - (sum(m_arr) + sum(f_arr))
        m_arr[5] += diff  # 25-29 yaş grubuna yuvarlama farkı
        return m_arr, f_arr

    @staticmethod
    def calculate_indicators(m_cohorts: List[int], f_cohorts: List[int]) -> Dict[str, float]:
        """
        Demografik bağımlılık ve yaşlanma göstergelerini hesaplar.
        """
        totals = [m + f for m, f in zip(m_cohorts, f_cohorts)]
        child = sum(totals[0:3])       # 0-14 yaş
        working = sum(totals[3:13])    # 15-64 yaş
        elderly = sum(totals[13:17])   # 65+ yaş
        total = child + working + elderly

        tot_dep = ((child + elderly) / working * 100.0) if working > 0 else 0.0
        child_dep = (child / working * 100.0) if working > 0 else 0.0
        old_dep = (elderly / working * 100.0) if working > 0 else 0.0
        aging_idx = (elderly / child * 100.0) if child > 0 else 0.0

        return {
            "total_population": total,
            "child_0_14": child,
            "working_15_64": working,
            "elderly_65_plus": elderly,
            "total_dependency_ratio": round(tot_dep, 2),
            "child_dependency_ratio": round(child_dep, 2),
            "elderly_dependency_ratio": round(old_dep, 2),
            "old_age_dependency_ratio": round(old_dep, 2),
            "aging_index": round(aging_idx, 2)
        }

    def project_step_5yr(
        self,
        m_curr: List[int],
        f_curr: List[int],
        net_migration_5yr: int = 0,
        age_bias: str = "working_age",
        shock_engine: Optional[ShockEngine] = None,
        period_start_year: int = 2025,
        years: float = 5.0
    ) -> Tuple[List[int], List[int]]:
        """
        5 yıllık kohort geçişi:
        1. Hayatta Kalma (Sx ile çapraz yaş basamağına aktarma)
        2. Doğumlar (15-49 yaş kadınların ASFR'si ile 0-4 yaş grubunu üretme)
        3. Net Göç ve Şokların Yaş Kohortlarına Enjeksiyonu

        `years` < 5 verilirse (ör. hedef yıl 5'in katı değilse) kısmi adım uygulanır:
        her kohortun years/5 kadarı bir sonraki yaş grubuna geçer, Sx üssü years/5 alınır,
        doğumlar years ile orantılanır. `net_migration_5yr` bu durumda ilgili dönemin toplam göçüdür.
        """
        if years < 5.0 - 1e-9:
            return self._project_partial_step(
                m_curr, f_curr, net_migration_5yr, age_bias, shock_engine, period_start_year, years
            )

        m_next = [0] * 17
        f_next = [0] * 17

        # 1. Yaşlanma ve Hayatta Kalma
        for i in range(16):
            m_next[i + 1] = int(round(m_curr[i] * self.sx_m[i]))
            f_next[i + 1] = int(round(f_curr[i] * self.sx_f[i]))
        # 80+ açık uçlu kohort birikimi
        m_next[16] += int(round(m_curr[16] * self.sx_m[16]))
        f_next[16] += int(round(f_curr[16] * self.sx_f[16]))

        # 2. Doğumlar (ASFR & TFR)
        # 5 yıllık dönemde doğurgan kadınların ortalama nüfusu
        total_births_5yr = 0
        asfr_per_cohort = [(w * self.tfr / 5.0) for w in ASFR_WEIGHTS_7]
        for idx, c_idx in enumerate(range(3, 10)):  # 15-19'dan 45-49'a
            f_avg = (f_curr[c_idx] + f_next[c_idx]) / 2.0
            births_per_year = f_avg * asfr_per_cohort[idx]
            total_births_5yr += births_per_year * 5.0

        male_births = int(round(total_births_5yr * (self.sex_ratio / (1.0 + self.sex_ratio))))
        female_births = int(round(total_births_5yr - male_births))

        # Yeni doğanların 0-4 yaşta hayatta kalması
        m_next[0] = int(round(male_births * self.sx_m[0]))
        f_next[0] = int(round(female_births * self.sx_f[0]))

        # 3. Göç Dağıtımı
        if net_migration_5yr != 0:
            weights = ShockEngine.AGE_COHORT_WEIGHTS.get(age_bias, ShockEngine.AGE_COHORT_WEIGHTS["working_age"])
            tot_w = sum(weights)
            norm_w = [w / tot_w for w in weights]
            for i in range(17):
                g_mig = net_migration_5yr * norm_w[i]
                m_next[i] = max(0, m_next[i] + int(round(g_mig * 0.512)))
                f_next[i] = max(0, f_next[i] + int(round(g_mig * 0.488)))

        # 4. Bu 5 yıllık periyoda denk gelen Şoklar
        if shock_engine:
            for s in shock_engine.get_shocks():
                if period_start_year < s.year <= period_start_year + 5:
                    s_dist = shock_engine.distribute_to_cohorts(s.population_delta, s.age_bias)
                    for i in range(17):
                        m_next[i] = max(0, m_next[i] + s_dist["male"][i])
                        f_next[i] = max(0, f_next[i] + s_dist["female"][i])

        return m_next, f_next

    def _project_partial_step(
        self,
        m_curr: List[int],
        f_curr: List[int],
        net_migration: float,
        age_bias: str,
        shock_engine: Optional[ShockEngine],
        period_start_year: int,
        years: float
    ) -> Tuple[List[int], List[int]]:
        """5 yıldan kısa (kesirli) bir dönem için kohort ilerletme."""
        years = max(0.0, float(years))
        frac = years / 5.0
        m_next = [0.0] * 17
        f_next = [0.0] * 17

        # 1. Kısmi yaşlanma + hayatta kalma (Sx^frac)
        for i in range(17):
            sm = self.sx_m[i] ** frac
            sf = self.sx_f[i] ** frac
            j = min(i + 1, 16)
            m_next[i] += m_curr[i] * (1.0 - frac) * sm
            m_next[j] += m_curr[i] * frac * sm
            f_next[i] += f_curr[i] * (1.0 - frac) * sf
            f_next[j] += f_curr[i] * frac * sf

        # 2. Doğumlar (dönem süresiyle orantılı)
        total_births = 0.0
        asfr_per_cohort = [(w * self.tfr / 5.0) for w in ASFR_WEIGHTS_7]
        for idx, c_idx in enumerate(range(3, 10)):
            f_avg = (f_curr[c_idx] + f_next[c_idx]) / 2.0
            total_births += f_avg * asfr_per_cohort[idx] * years
        male_births = total_births * (self.sex_ratio / (1.0 + self.sex_ratio))
        female_births = total_births - male_births
        m_next[0] += male_births * (self.sx_m[0] ** frac)
        f_next[0] += female_births * (self.sx_f[0] ** frac)

        # 3. Göç
        if net_migration:
            weights = ShockEngine.AGE_COHORT_WEIGHTS.get(age_bias, ShockEngine.AGE_COHORT_WEIGHTS["working_age"])
            tot_w = sum(weights)
            for i in range(17):
                g_mig = net_migration * (weights[i] / tot_w)
                m_next[i] = max(0.0, m_next[i] + g_mig * 0.512)
                f_next[i] = max(0.0, f_next[i] + g_mig * 0.488)

        m_out = [int(round(v)) for v in m_next]
        f_out = [int(round(v)) for v in f_next]

        # 4. Dönem içindeki şoklar
        if shock_engine:
            for s in shock_engine.get_shocks():
                if period_start_year < s.year <= period_start_year + years:
                    s_dist = shock_engine.distribute_to_cohorts(s.population_delta, s.age_bias)
                    for i in range(17):
                        m_out[i] = max(0, m_out[i] + s_dist["male"][i])
                        f_out[i] = max(0, f_out[i] + s_dist["female"][i])

        return m_out, f_out

    def project_period(
        self,
        m_curr: List[int],
        f_curr: List[int],
        years: float,
        annual_migration: float = 0.0,
        age_bias: str = "working_age",
        shock_engine: Optional[ShockEngine] = None,
        start_year: int = 2025
    ) -> Tuple[List[int], List[int]]:
        """Herhangi bir süreyi (ör. 6 veya 21 yıl) 5 yıllık + kalan kısmi adımlarla ilerletir."""
        remaining = float(years)
        cur_year = start_year
        m, f = list(m_curr), list(f_curr)
        while remaining > 1e-9:
            dt = min(5.0, remaining)
            m, f = self.project_step_5yr(
                m, f,
                net_migration_5yr=int(round(annual_migration * dt)),
                age_bias=age_bias,
                shock_engine=shock_engine,
                period_start_year=int(cur_year),
                years=dt
            )
            remaining -= dt
            cur_year += dt
        return m, f

    def run_multi_scenario_projection(
        self,
        target_years: List[int],
        m_init: List[int],
        f_init: List[int],
        trend_annual_mig: float = 300.0,
        vision_annual_mig: float = 980.0,
        shock_engine: Optional[ShockEngine] = None
    ) -> Dict[str, Any]:
        """
        Tüm senaryoları (Düşük, Orta, Yüksek ve Şoklu) aynı anda modeller.
        """
        step_years = [self.base_year] + [yr for yr in target_years if (yr - self.base_year) % 5 == 0]
        step_years = sorted(list(set(step_years)))

        scenarios = {
            "low": {"name": "Düşük Senaryo (%0 Göç / Doğal Artış)", "steps": {}, "indicators": {}},
            "mid": {"name": "Orta Senaryo (Trend Göçü)", "steps": {}, "indicators": {}},
            "high": {"name": "Yüksek Senaryo (Plan Kabulü / Vizyon)", "steps": {}, "indicators": {}},
            "shock": {"name": "Şoklu Dinamik Senaryo (Yıllara Özel Olaylar)", "steps": {}, "indicators": {}}
        }

        # Başlangıç
        for s_key in scenarios:
            scenarios[s_key]["steps"][self.base_year] = {
                "male": list(m_init),
                "female": list(f_init),
                "total": sum(m_init) + sum(f_init)
            }
            scenarios[s_key]["indicators"][self.base_year] = self.calculate_indicators(m_init, f_init)

        for i in range(len(step_years) - 1):
            y_start = step_years[i]
            y_end = step_years[i + 1]
            dur = y_end - y_start

            # 1. Düşük (0% Göç)
            m_l, f_l = scenarios["low"]["steps"][y_start]["male"], scenarios["low"]["steps"][y_start]["female"]
            m_l_next, f_l_next = self.project_step_5yr(m_l, f_l, net_migration_5yr=0, period_start_year=y_start)
            scenarios["low"]["steps"][y_end] = {"male": m_l_next, "female": f_l_next, "total": sum(m_l_next)+sum(f_l_next)}
            scenarios["low"]["indicators"][y_end] = self.calculate_indicators(m_l_next, f_l_next)

            # 2. Orta (Trend Göç)
            m_m, f_m = scenarios["mid"]["steps"][y_start]["male"], scenarios["mid"]["steps"][y_start]["female"]
            mig_m = int(round(trend_annual_mig * dur))
            m_m_next, f_m_next = self.project_step_5yr(m_m, f_m, net_migration_5yr=mig_m, age_bias="family", period_start_year=y_start)
            scenarios["mid"]["steps"][y_end] = {"male": m_m_next, "female": f_m_next, "total": sum(m_m_next)+sum(f_m_next)}
            scenarios["mid"]["indicators"][y_end] = self.calculate_indicators(m_m_next, f_m_next)

            # 3. Yüksek (Vizyon / Sanayi Çarpanı)
            m_h, f_h = scenarios["high"]["steps"][y_start]["male"], scenarios["high"]["steps"][y_start]["female"]
            mig_h = int(round(vision_annual_mig * dur))
            m_h_next, f_h_next = self.project_step_5yr(m_h, f_h, net_migration_5yr=mig_h, age_bias="working_age", period_start_year=y_start)
            scenarios["high"]["steps"][y_end] = {"male": m_h_next, "female": f_h_next, "total": sum(m_h_next)+sum(f_h_next)}
            scenarios["high"]["indicators"][y_end] = self.calculate_indicators(m_h_next, f_h_next)

            # 4. Şoklu Senaryo (High tabanına + Şok motoru)
            m_s, f_s = scenarios["shock"]["steps"][y_start]["male"], scenarios["shock"]["steps"][y_start]["female"]
            m_s_next, f_s_next = self.project_step_5yr(
                m_s, f_s, net_migration_5yr=mig_h, age_bias="working_age",
                shock_engine=shock_engine, period_start_year=y_start
            )
            scenarios["shock"]["steps"][y_end] = {"male": m_s_next, "female": f_s_next, "total": sum(m_s_next)+sum(f_s_next)}
            scenarios["shock"]["indicators"][y_end] = self.calculate_indicators(m_s_next, f_s_next)

        return {
            "base_year": self.base_year,
            "step_years": step_years,
            "scenarios": scenarios
        }
