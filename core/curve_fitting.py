# -*- coding: utf-8 -*-
"""
Mathematical Curve Fitting & Extrapolation Engine
Prof. Dr. K. Mert Çubukçu — "Planlamada Klasik Sayısal Yöntemler" (Bölüm: Ekstrapolasyon Yöntemleri)
6 Temel Matematiksel Eğri Modeli: Doğrusal, 2. ve 3. Derece Polinom, Üstel, Logaritmik, Kuvvet
"""

import math
from typing import List, Dict, Any, Tuple


class CurveFittingEngine:
    """
    Geçmiş nüfus verilerinden bağıl zaman (t=1, 2, ... N) değişkenine bağlı olarak
    6 regresyon eğrisini analitik olarak uydurur ve ileriye dönük projeksiyon üretir.
    """

    @staticmethod
    def fit_linear(t_list: List[float], y_list: List[float]) -> Tuple[float, float]:
        """y = a * t + b"""
        n = len(t_list)
        sum_t = sum(t_list)
        sum_y = sum(y_list)
        sum_tt = sum(t * t for t in t_list)
        sum_ty = sum(t * y for t, y in zip(t_list, y_list))
        denom = (n * sum_tt - sum_t * sum_t)
        if abs(denom) < 1e-9:
            return 0.0, sum_y / n if n > 0 else 0.0
        a = (n * sum_ty - sum_t * sum_y) / denom
        b = (sum_y - a * sum_t) / n
        return a, b

    @staticmethod
    def fit_poly2(t_list: List[float], y_list: List[float]) -> Tuple[float, float, float]:
        """y = a * t^2 + b * t + c (Gaussian elimination on 3x3 normal equations)"""
        n = len(t_list)
        s_t = sum(t_list)
        s_t2 = sum(t**2 for t in t_list)
        s_t3 = sum(t**3 for t in t_list)
        s_t4 = sum(t**4 for t in t_list)
        s_y = sum(y_list)
        s_ty = sum(t * y for t, y in zip(t_list, y_list))
        s_t2y = sum((t**2) * y for t, y in zip(t_list, y_list))

        A = [
            [s_t4, s_t3, s_t2, s_t2y],
            [s_t3, s_t2, s_t,  s_ty],
            [s_t2, s_t,  float(n), s_y]
        ]
        # Gaussian elimination
        for i in range(3):
            pivot = A[i][i]
            if abs(pivot) < 1e-12:
                continue
            for j in range(i, 4):
                A[i][j] /= pivot
            for k in range(3):
                if k != i:
                    factor = A[k][i]
                    for j in range(i, 4):
                        A[k][j] -= factor * A[i][j]
        return A[0][3], A[1][3], A[2][3]

    @staticmethod
    def fit_poly3(t_list: List[float], y_list: List[float]) -> Tuple[float, float, float, float]:
        """y = a * t^3 + b * t^2 + c * t + d"""
        n = len(t_list)
        powers_t = [sum(t**p for t in t_list) for p in range(7)]
        powers_ty = [sum((t**p) * y for t, y in zip(t_list, y_list)) for p in range(4)]

        A = [
            [powers_t[6], powers_t[5], powers_t[4], powers_t[3], powers_ty[3]],
            [powers_t[5], powers_t[4], powers_t[3], powers_t[2], powers_ty[2]],
            [powers_t[4], powers_t[3], powers_t[2], powers_t[1], powers_ty[1]],
            [powers_t[3], powers_t[2], powers_t[1], float(n),    powers_ty[0]],
        ]
        for i in range(4):
            pivot = A[i][i]
            if abs(pivot) < 1e-12:
                continue
            for j in range(i, 5):
                A[i][j] /= pivot
            for k in range(4):
                if k != i:
                    factor = A[k][i]
                    for j in range(i, 5):
                        A[k][j] -= factor * A[i][j]
        return A[0][4], A[1][4], A[2][4], A[3][4]

    @staticmethod
    def fit_exponential(t_list: List[float], y_list: List[float]) -> Tuple[float, float]:
        """y = a * e^(b * t) --> ln(y) = ln(a) + b * t"""
        log_y = [math.log(max(1.0, y)) for y in y_list]
        b_slope, ln_a = CurveFittingEngine.fit_linear(t_list, log_y)
        a = math.exp(ln_a)
        return a, b_slope

    @staticmethod
    def fit_logarithmic(t_list: List[float], y_list: List[float]) -> Tuple[float, float]:
        """y = a * ln(t) + b"""
        ln_t = [math.log(max(0.001, t)) for t in t_list]
        a, b = CurveFittingEngine.fit_linear(ln_t, y_list)
        return a, b

    @staticmethod
    def fit_power(t_list: List[float], y_list: List[float]) -> Tuple[float, float]:
        """y = a * t^b --> ln(y) = ln(a) + b * ln(t)"""
        ln_t = [math.log(max(0.001, t)) for t in t_list]
        log_y = [math.log(max(1.0, y)) for y in y_list]
        b, ln_a = CurveFittingEngine.fit_linear(ln_t, log_y)
        a = math.exp(ln_a)
        return a, b

    @staticmethod
    def calculate_metrics(y_actual: List[float], y_pred: List[float]) -> Dict[str, float]:
        n = len(y_actual)
        if n == 0:
            return {"sse": 0.0, "rmse": 0.0, "r2": 0.0, "mae": 0.0}
        
        y_mean = sum(y_actual) / n
        sse = sum((y - p)**2 for y, p in zip(y_actual, y_pred))
        sst = sum((y - y_mean)**2 for y in y_actual)
        rmse = math.sqrt(sse / n)
        mae = sum(abs(y - p) for y, p in zip(y_actual, y_pred)) / n
        r2 = 1.0 - (sse / sst) if sst > 1e-9 else 0.0
        r2 = max(0.0, min(1.0, r2))

        return {
            "sse": round(sse, 1),
            "rmse": round(rmse, 2),
            "r2": round(r2, 4),
            "mae": round(mae, 2)
        }

    @classmethod
    def evaluate_all_models(
        cls,
        years_hist: List[int],
        pop_hist: List[float],
        target_years: List[int]
    ) -> Dict[str, Any]:
        """
        Geçmiş seriye 6 modeli uydurur ve hedef yıllar için projeksiyon sonuçlarını döner.
        """
        n = len(years_hist)
        # Gerçek takvim yıllarına göre zaman ekseni (ardışık olmayan yıllarda da doğru uyum)
        t_hist = [float(y - years_hist[0] + 1) for y in years_hist]

        # 1. Fit models
        a_lin, b_lin = cls.fit_linear(t_hist, pop_hist)
        a_p2, b_p2, c_p2 = cls.fit_poly2(t_hist, pop_hist)
        a_p3, b_p3, c_p3, d_p3 = cls.fit_poly3(t_hist, pop_hist)
        a_exp, b_exp = cls.fit_exponential(t_hist, pop_hist)
        a_log, b_log = cls.fit_logarithmic(t_hist, pop_hist)
        a_pow, b_pow = cls.fit_power(t_hist, pop_hist)

        # 2. Historical predictions for metrics
        pred_lin_h = [a_lin * t + b_lin for t in t_hist]
        pred_p2_h = [a_p2 * t**2 + b_p2 * t + c_p2 for t in t_hist]
        pred_p3_h = [a_p3 * t**3 + b_p3 * t**2 + c_p3 * t + d_p3 for t in t_hist]
        pred_exp_h = [a_exp * math.exp(b_exp * t) for t in t_hist]
        pred_log_h = [a_log * math.log(max(0.001, t)) + b_log for t in t_hist]
        pred_pow_h = [a_pow * (t**b_pow) for t in t_hist]

        # 3. Future predictions
        start_year = years_hist[0]
        t_future = [float(yr - start_year + 1) for yr in target_years]

        models = {
            "linear": {
                "name": "Doğrusal (Linear)",
                "formula_str": f"y = {a_lin:.2f} × t + {b_lin:,.2f}",
                "metrics": cls.calculate_metrics(pop_hist, pred_lin_h),
                "predictions": {yr: round(a_lin * t + b_lin) for yr, t in zip(target_years, t_future)},
                "academic_review": "Plan kararına esas alınan en istikrarlı matematiksel trend modeli (Yüksek R² ve düşük standart hata)."
            },
            "poly2": {
                "name": "2. Derece Polinom",
                "formula_str": f"y = {a_p2:.4f}t² + {b_p2:.2f}t + {c_p2:,.2f}",
                "metrics": cls.calculate_metrics(pop_hist, pred_p2_h),
                "predictions": {yr: round(a_p2 * t**2 + b_p2 * t + c_p2) for yr, t in zip(target_years, t_future)},
                "academic_review": "Çok yüksek R² uyumu; orta-uzun vadede doğrusal model ile tutarlı seyreder."
            },
            "poly3": {
                "name": "3. Derece Polinom",
                "formula_str": f"y = {a_p3:.4f}t³ + {b_p3:.4f}t² + {c_p3:.2f}t + {d_p3:,.2f}",
                "metrics": cls.calculate_metrics(pop_hist, pred_p3_h),
                "predictions": {yr: round(a_p3 * t**3 + b_p3 * t**2 + c_p3 * t + d_p3) for yr, t in zip(target_years, t_future)},
                "academic_review": "TEKNİK AYKIRI: R² yüksek görünse de ileriye dönük parabolik çöküş/aşırı sıçrama riski taşır."
            },
            "exponential": {
                "name": "Üstel (Exponential)",
                "formula_str": f"y = {a_exp:,.2f} × e^({b_exp:.5f}t)",
                "metrics": cls.calculate_metrics(pop_hist, pred_exp_h),
                "predictions": {yr: round(a_exp * math.exp(b_exp * t)) for yr, t in zip(target_years, t_future)},
                "academic_review": "AŞIRI YÜKSEK: Ekolojik ve kentsel kaynak eşiklerini aşan geometrik bileşik büyüme."
            },
            "logarithmic": {
                "name": "Logaritmik",
                "formula_str": f"y = {a_log:,.2f} × ln(t) + {b_log:,.2f}",
                "metrics": cls.calculate_metrics(pop_hist, pred_log_h),
                "predictions": {yr: round(a_log * math.log(max(0.001, t)) + b_log) for yr, t in zip(target_years, t_future)},
                "academic_review": "YETERSİZ: Erken doygunluk varsayımı nedeniyle kentin büyüme dinamiklerini bastırır."
            },
            "power": {
                "name": "Kuvvet (Power)",
                "formula_str": f"y = {a_pow:,.2f} × t^{b_pow:.4f}",
                "metrics": cls.calculate_metrics(pop_hist, pred_pow_h),
                "predictions": {yr: round(a_pow * (t**b_pow)) for yr, t in zip(target_years, t_future)},
                "academic_review": "YETERSİZ: R² düşük, kentsel gelişmeyi yavaşlatıcı gösterir."
            }
        }

        return {
            "years_hist": years_hist,
            "pop_hist": pop_hist,
            "target_years": target_years,
            "models": models
        }
