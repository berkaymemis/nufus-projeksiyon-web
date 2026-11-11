# -*- coding: utf-8 -*-
"""
Demographic Shock Events Engine
Prof. Dr. K. Mert Çubukçu — Şehir ve Bölge Planlamada Dinamik Senaryo ve Şok Modellemesi
Kentsel Projeksiyonlarda Yıllara Özel Pozitif / Negatif Şok Etkileri
"""

from typing import List, Dict, Any, Optional
import copy


class DemographicShock:
    """
    Belirli bir yıla ait demografik kırılma veya şok olayı (Shock Event).
    """
    def __init__(
        self,
        year: int,
        title: str,
        impact_type: str = "positive_mig",
        population_delta: int = 10000,
        age_bias: str = "working_age",
        description: str = ""
    ):
        self.year = int(year)
        self.title = str(title)
        self.impact_type = str(impact_type)  # positive_mig, negative_mig, disaster, industrial, campus
        self.population_delta = int(population_delta)
        self.age_bias = str(age_bias)  # working_age, family, student, general, elderly
        self.description = str(description)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "year": self.year,
            "title": self.title,
            "impact_type": self.impact_type,
            "population_delta": self.population_delta,
            "age_bias": self.age_bias,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'DemographicShock':
        return cls(
            year=d.get("year", 2030),
            title=d.get("title", "Şok Olayı"),
            impact_type=d.get("impact_type", "positive_mig"),
            population_delta=d.get("population_delta", 5000),
            age_bias=d.get("age_bias", "working_age"),
            description=d.get("description", "")
        )


class ShockEngine:
    """
    Demografik şokların zaman serisi ve kohort matrisleri üzerindeki kümülatif etkisini yönetir.
    """
    PRESET_SHOCKS = [
        {
            "year": 2030,
            "title": "Bölgesel Organize Sanayi 2. Etabı & Lojistik Üs Açılışı",
            "impact_type": "industrial",
            "population_delta": 12500,
            "age_bias": "working_age",
            "description": "350 Ha sanayi genişlemesi ve planlanan temel istihdam artışının 1. dalgası (+12.500 göç)."
        },
        {
            "year": 2033,
            "title": "Hızlı Demiryolu / Banliyö ve Toplu Taşıma Entegrasyonu",
            "impact_type": "positive_mig",
            "population_delta": 6500,
            "age_bias": "family",
            "description": "Merkez kente erişilebilirlik sıçraması ve konut desantralizasyon göçü."
        },
        {
            "year": 2035,
            "title": "Sanayi Kümelenmesi Tam Kapasite & Tamamlayıcı Hizmet Sıçraması",
            "impact_type": "positive_mig",
            "population_delta": 6000,
            "age_bias": "working_age",
            "description": "İmalat sanayi kümelenmesinin tetiklediği 2. dalga hizmet çarpanı istihdamı ve göç."
        },
        {
            "year": 2028,
            "title": "Afet / Deprem Sonrası Güvenli Kente Ters Göç Dalgası",
            "impact_type": "disaster",
            "population_delta": 8000,
            "age_bias": "family",
            "description": "Büyük metropol merkezlerinden zemin açısından sağlam ikincil ilçelere ani yerleşim göçü."
        },
        {
            "year": 2032,
            "title": "Sanayi Tesisi Dönüşümü / Kriz Kaynaklı İstihdam Düşüşü",
            "impact_type": "negative_mig",
            "population_delta": -4500,
            "age_bias": "working_age",
            "description": "Sektörel durgunluk veya tesis relokasyonu nedeniyle net dış göç."
        }
    ]

    # Yaş kohortlarına (0-4, 5-9 ... 80+) dağıtım profilleri (17 kohort)
    AGE_COHORT_WEIGHTS = {
        # Genç çalışan ağırlıklı göç (20-39 yaş yoğun, yanlarında 0-9 yaş çocuklar)
        "working_age": [
            0.08, 0.07, 0.04, 0.06, 0.18, 0.22, 0.16, 0.09, 0.05, 0.03, 0.01, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0
        ],
        # Aile göçü (Dengeli çocuk ve orta yaş)
        "family": [
            0.10, 0.10, 0.08, 0.06, 0.12, 0.14, 0.13, 0.11, 0.08, 0.04, 0.02, 0.01, 0.01, 0.0, 0.0, 0.0, 0.0
        ],
        # Öğrenci / Genç nüfus göçü (15-24 yaş yoğun)
        "student": [
            0.01, 0.01, 0.03, 0.35, 0.45, 0.10, 0.02, 0.01, 0.01, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        ],
        # Genel oransal dağılım
        "general": [
            0.05, 0.06, 0.06, 0.06, 0.07, 0.08, 0.08, 0.08, 0.08, 0.08, 0.07, 0.06, 0.05, 0.04, 0.04, 0.02, 0.02
        ]
    }

    def __init__(self, initial_shocks: Optional[List[DemographicShock]] = None):
        self.shocks: List[DemographicShock] = initial_shocks or []

    def add_shock(self, shock: DemographicShock):
        self.shocks.append(shock)
        self.shocks.sort(key=lambda s: s.year)

    def remove_shock(self, index: int):
        if 0 <= index < len(self.shocks):
            self.shocks.pop(index)

    def clear(self):
        self.shocks.clear()

    def get_shocks(self) -> List[DemographicShock]:
        return copy.deepcopy(self.shocks)

    def apply_to_timeline(
        self,
        base_timeline: Dict[int, float]
    ) -> Dict[str, Any]:
        """
        Temel projeksiyon zaman serisine şokları kümülatif olarak uygular.
        Her şok yılından itibaren sonraki tüm yıllara o şokun etkisi yansır.
        """
        sorted_years = sorted(base_timeline.keys())
        shocked_timeline = {}
        shock_details_by_year = {}

        cumulative_shock = 0.0
        prev_yr = None
        for yr in sorted_years:
            if prev_yr is None:
                yr_shocks = [s for s in self.shocks if s.year <= yr]
            else:
                yr_shocks = [s for s in self.shocks if prev_yr < s.year <= yr]
            prev_yr = yr

            for s in yr_shocks:
                cumulative_shock += s.population_delta
                shock_details_by_year[yr] = shock_details_by_year.get(yr, []) + [s.to_dict()]
            
            shocked_timeline[yr] = round(base_timeline[yr] + cumulative_shock)

        return {
            "original_timeline": base_timeline,
            "shocked_timeline": shocked_timeline,
            "total_net_shock": cumulative_shock,
            "shock_count": len(self.shocks),
            "events_by_year": shock_details_by_year
        }

    def distribute_to_cohorts(
        self,
        population_delta: int,
        age_bias: str = "working_age",
        male_ratio: float = 0.512
    ) -> Dict[str, List[int]]:
        """
        Şok nüfusunu yaş gruplarına (0-4 ... 80+) ve kadın-erkek ayrımına dağıtır.
        """
        weights = self.AGE_COHORT_WEIGHTS.get(age_bias, self.AGE_COHORT_WEIGHTS["general"])
        # Normalize weights
        tot_w = sum(weights)
        weights = [w / tot_w for w in weights]

        male_cohorts = []
        female_cohorts = []
        for w in weights:
            group_total = population_delta * w
            m_count = int(round(group_total * male_ratio))
            f_count = int(round(group_total * (1.0 - male_ratio)))
            male_cohorts.append(m_count)
            female_cohorts.append(f_count)

        return {
            "male": male_cohorts,
            "female": female_cohorts,
            "total_male": sum(male_cohorts),
            "total_female": sum(female_cohorts),
            "total": sum(male_cohorts) + sum(female_cohorts)
        }
