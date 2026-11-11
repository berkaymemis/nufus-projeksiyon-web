# -*- coding: utf-8 -*-
"""
Turkey District-Level Economic Base Multipliers (BM_LQ and BM_MG)
Prof. Dr. K. Mert Cubukcu (2011) Veri Tabani
"The spatial distribution of economic base multipliers: A GIS and spatial statistics-based cluster analysis"
ITU Journal, 8(2), 49-62.
Turkiye Geneli 81 Il ve 923 Ilcenin Resmi Carpan Degerleri
"""

from typing import Dict, Any, List, Optional
import os, csv, re

CITATION_CUBUKCU_2011 = "Cubukcu, K. M. (2011). The spatial distribution of economic base multipliers: A GIS and spatial statistics-based cluster analysis. ITU Journal, 8(2), 49-62."
CITATION_KUZIP_2026 = "Cubukcu, K. M., ve Ayalp, E. (2026). Kuzey Izmir Mekansal Gelisme Perspektifi (KUZIP) Sentez Raporu. Dokuz Eylul Universitesi ve Izmir Kalkinma Ajansi (IZKA)."

# Turkiye Geneli Resmi 923 Ilce Carpan Veri Tabani (Mert Cubukcu, 2011)
DISTRICT_BASE_MULTIPLIERS: Dict[str, Dict[str, Dict[str, Any]]] = {
  "ADANA": {
    "ALADAG": {
      "bm_lq": 2.512,
      "bm_mg": 2.196,
      "pop_2000": 6674
    },
    "CEYHAN": {
      "bm_lq": 3.058,
      "bm_mg": 2.411,
      "pop_2000": 108602
    },
    "FEKE": {
      "bm_lq": 2.981,
      "bm_mg": 2.91,
      "pop_2000": 4632
    },
    "IMAMOGLU": {
      "bm_lq": 4.782,
      "bm_mg": 3.2,
      "pop_2000": 30428
    },
    "KARAISALI": {
      "bm_lq": 2.745,
      "bm_mg": 2.106,
      "pop_2000": 6883
    },
    "KARATAS": {
      "bm_lq": 3.316,
      "bm_mg": 1.642,
      "pop_2000": 9189
    },
    "KOZAN": {
      "bm_lq": 2.804,
      "bm_mg": 2.036,
      "pop_2000": 75833
    },
    "POZANTI": {
      "bm_lq": 2.133,
      "bm_mg": 1.644,
      "pop_2000": 9627
    },
    "SAIMBEYLI": {
      "bm_lq": 2.243,
      "bm_mg": 2.265,
      "pop_2000": 5198
    },
    "SEYHAN": {
      "bm_lq": 2.144,
      "bm_mg": 2.577,
      "pop_2000": 807934
    },
    "TUFANBEYLI": {
      "bm_lq": 3.374,
      "bm_mg": 3.298,
      "pop_2000": 5332
    },
    "YUMURTALIK": {
      "bm_lq": 2.301,
      "bm_mg": 1.647,
      "pop_2000": 4745
    },
    "YUREGIR": {
      "bm_lq": 2.166,
      "bm_mg": 2.854,
      "pop_2000": 322776
    }
  },
  "ADIYAMAN": {
    "ADIYAMAN MERKEZ": {
      "bm_lq": 2.546,
      "bm_mg": 2.628,
      "pop_2000": 178538
    },
    "BESNI": {
      "bm_lq": 3.248,
      "bm_mg": 2.719,
      "pop_2000": 36123
    },
    "CELIKHAN": {
      "bm_lq": 4.05,
      "bm_mg": 1.844,
      "pop_2000": 11306
    },
    "GERGER": {
      "bm_lq": 3.774,
      "bm_mg": 2.227,
      "pop_2000": 4223
    },
    "GOLBASI": {
      "bm_lq": 2.565,
      "bm_mg": 2.521,
      "pop_2000": 28656
    },
    "KAHTA": {
      "bm_lq": 3.331,
      "bm_mg": 2.848,
      "pop_2000": 60689
    },
    "SAMSAT": {
      "bm_lq": 4.274,
      "bm_mg": 1.652,
      "pop_2000": 6917
    },
    "SINCIK": {
      "bm_lq": 5.392,
      "bm_mg": 2.013,
      "pop_2000": 5274
    },
    "TUT": {
      "bm_lq": 3.958,
      "bm_mg": 2.257,
      "pop_2000": 7213
    }
  },
  "AFYON": {
    "AFYON MERKEZ": {
      "bm_lq": 2.133,
      "bm_mg": 2.3,
      "pop_2000": 128516
    },
    "BASMAKCI": {
      "bm_lq": 3.972,
      "bm_mg": 2.806,
      "pop_2000": 7816
    },
    "BAYAT": {
      "bm_lq": 6.323,
      "bm_mg": 2.248,
      "pop_2000": 4702
    },
    "BOLVADIN": {
      "bm_lq": 2.983,
      "bm_mg": 2.049,
      "pop_2000": 52398
    },
    "CAY": {
      "bm_lq": 3.012,
      "bm_mg": 3.555,
      "pop_2000": 18137
    },
    "COBANLAR": {
      "bm_lq": 4.017,
      "bm_mg": 2.381,
      "pop_2000": 8315
    },
    "DAZKIRI": {
      "bm_lq": 2.655,
      "bm_mg": 3.644,
      "pop_2000": 6555
    },
    "DINAR": {
      "bm_lq": 2.801,
      "bm_mg": 2.659,
      "pop_2000": 35424
    },
    "EMIRDAG": {
      "bm_lq": 1.971,
      "bm_mg": 1.811,
      "pop_2000": 20508
    },
    "EVCILER": {
      "bm_lq": 8.013,
      "bm_mg": 2.074,
      "pop_2000": 5134
    },
    "HOCALAR": {
      "bm_lq": 3.065,
      "bm_mg": 2.075,
      "pop_2000": 2646
    },
    "IHSANIYE": {
      "bm_lq": 3.094,
      "bm_mg": 3.401,
      "pop_2000": 4466
    },
    "ISCEHISAR": {
      "bm_lq": 1.789,
      "bm_mg": 1.408,
      "pop_2000": 10542
    },
    "KIZILOREN": {
      "bm_lq": 4.795,
      "bm_mg": 2.252,
      "pop_2000": 2556
    },
    "SANDIKLI": {
      "bm_lq": 2.952,
      "bm_mg": 2.203,
      "pop_2000": 37804
    },
    "SINCANLI": {
      "bm_lq": 3.117,
      "bm_mg": 2.853,
      "pop_2000": 5826
    },
    "SUHUT": {
      "bm_lq": 3.754,
      "bm_mg": 1.477,
      "pop_2000": 13630
    },
    "SULTANDAGI": {
      "bm_lq": 2.925,
      "bm_mg": 2.098,
      "pop_2000": 6893
    }
  },
  "AĞRI": {
    "AGRI MERKEZ": {
      "bm_lq": 2.03,
      "bm_mg": 2.691,
      "pop_2000": 79764
    },
    "DIYADIN": {
      "bm_lq": 2.608,
      "bm_mg": 1.719,
      "pop_2000": 13320
    },
    "DOGUBEYAZIT": {
      "bm_lq": 1.923,
      "bm_mg": 2.755,
      "pop_2000": 56261
    },
    "ELESKIRT": {
      "bm_lq": 1.763,
      "bm_mg": 2.127,
      "pop_2000": 15339
    },
    "HAMUR": {
      "bm_lq": 1.698,
      "bm_mg": 2.729,
      "pop_2000": 3865
    },
    "PATNOS": {
      "bm_lq": 2.081,
      "bm_mg": 2.226,
      "pop_2000": 71829
    },
    "TASLICAY": {
      "bm_lq": 2.238,
      "bm_mg": 2.306,
      "pop_2000": 5180
    },
    "TUTAK": {
      "bm_lq": 2.258,
      "bm_mg": 2.148,
      "pop_2000": 6751
    }
  },
  "AMASYA": {
    "AMASYA MERKEZ": {
      "bm_lq": 1.963,
      "bm_mg": 2.484,
      "pop_2000": 74393
    },
    "GOYNUCEK": {
      "bm_lq": 2.408,
      "bm_mg": 2.171,
      "pop_2000": 2776
    },
    "GUMUSHACIKOY": {
      "bm_lq": 3.602,
      "bm_mg": 1.717,
      "pop_2000": 14057
    },
    "HAMAMOZU": {
      "bm_lq": 3.301,
      "bm_mg": 1.978,
      "pop_2000": 1511
    },
    "MERZIFON": {
      "bm_lq": 2.096,
      "bm_mg": 2.385,
      "pop_2000": 45613
    },
    "SULUOVA": {
      "bm_lq": 2.67,
      "bm_mg": 2.049,
      "pop_2000": 42715
    },
    "TASOVA": {
      "bm_lq": 2.4,
      "bm_mg": 1.986,
      "pop_2000": 15556
    }
  },
  "ANKARA": {
    "AKYURT": {
      "bm_lq": 2.416,
      "bm_mg": 2.556,
      "pop_2000": 8069
    },
    "ALTINDAG": {
      "bm_lq": 2.084,
      "bm_mg": 2.804,
      "pop_2000": 400023
    },
    "AYAS": {
      "bm_lq": 2.26,
      "bm_mg": 2.358,
      "pop_2000": 7839
    },
    "BALA": {
      "bm_lq": 2.412,
      "bm_mg": 3.052,
      "pop_2000": 6616
    },
    "BEYPAZARI": {
      "bm_lq": 3.384,
      "bm_mg": 1.919,
      "pop_2000": 34441
    },
    "CAMLIDERE": {
      "bm_lq": 2.006,
      "bm_mg": 1.56,
      "pop_2000": 6303
    },
    "CANKAYA": {
      "bm_lq": 1.88,
      "bm_mg": 2.026,
      "pop_2000": 758490
    },
    "CUBUK": {
      "bm_lq": 2.187,
      "bm_mg": 2.397,
      "pop_2000": 46605
    },
    "ELMADAG": {
      "bm_lq": 2.228,
      "bm_mg": 2.637,
      "pop_2000": 22518
    },
    "ETIMESGUT": {
      "bm_lq": 1.994,
      "bm_mg": 2.138,
      "pop_2000": 169615
    },
    "EVREN": {
      "bm_lq": 3.421,
      "bm_mg": 1.758,
      "pop_2000": 4363
    },
    "GOLBASI": {
      "bm_lq": 1.991,
      "bm_mg": 3.267,
      "pop_2000": 35308
    },
    "GUDUL": {
      "bm_lq": 2.972,
      "bm_mg": 2.093,
      "pop_2000": 5806
    },
    "HAYMANA": {
      "bm_lq": 2.494,
      "bm_mg": 2.381,
      "pop_2000": 11313
    },
    "KALECIK": {
      "bm_lq": 4.059,
      "bm_mg": 1.714,
      "pop_2000": 11965
    },
    "KAZAN": {
      "bm_lq": 2.446,
      "bm_mg": 1.926,
      "pop_2000": 15871
    },
    "KECIOREN": {
      "bm_lq": 2.08,
      "bm_mg": 2.971,
      "pop_2000": 625167
    },
    "KIZILCAHAMAM": {
      "bm_lq": 2.081,
      "bm_mg": 2.087,
      "pop_2000": 16195
    },
    "MAMAK": {
      "bm_lq": 2.078,
      "bm_mg": 2.773,
      "pop_2000": 412771
    },
    "NALLIHAN": {
      "bm_lq": 2.133,
      "bm_mg": 1.905,
      "pop_2000": 17181
    },
    "POLATLI": {
      "bm_lq": 2.39,
      "bm_mg": 2.281,
      "pop_2000": 79992
    },
    "SEREFLIKOCHISAR": {
      "bm_lq": 2.654,
      "bm_mg": 2.57,
      "pop_2000": 42083
    },
    "SINCAN": {
      "bm_lq": 2.094,
      "bm_mg": 2.207,
      "pop_2000": 267879
    },
    "YENIMAHALLE": {
      "bm_lq": 2.085,
      "bm_mg": 2.321,
      "pop_2000": 534109
    }
  },
  "ANTALYA": {
    "AKSEKI": {
      "bm_lq": 3.008,
      "bm_mg": 1.951,
      "pop_2000": 10563
    },
    "ALANYA": {
      "bm_lq": 1.953,
      "bm_mg": 2.616,
      "pop_2000": 88346
    },
    "ANTALYA MERKEZ": {
      "bm_lq": 2.166,
      "bm_mg": 2.421,
      "pop_2000": 603190
    },
    "ELMALI": {
      "bm_lq": 3.239,
      "bm_mg": 2.401,
      "pop_2000": 14561
    },
    "FINIKE": {
      "bm_lq": 2.748,
      "bm_mg": 1.912,
      "pop_2000": 9746
    },
    "GAZIPASA": {
      "bm_lq": 4.038,
      "bm_mg": 2.096,
      "pop_2000": 16536
    },
    "GUNDOGMUS": {
      "bm_lq": 3.182,
      "bm_mg": 2.196,
      "pop_2000": 5021
    },
    "IBRADI": {
      "bm_lq": 8.805,
      "bm_mg": 1.607,
      "pop_2000": 6991
    },
    "KALE": {
      "bm_lq": 5.153,
      "bm_mg": 1.612,
      "pop_2000": 13900
    },
    "KAS": {
      "bm_lq": 1.912,
      "bm_mg": 2.228,
      "pop_2000": 6361
    },
    "KEMER": {
      "bm_lq": 1.781,
      "bm_mg": 1.617,
      "pop_2000": 17255
    },
    "KORKUTELI": {
      "bm_lq": 2.63,
      "bm_mg": 3.319,
      "pop_2000": 16431
    },
    "KUMLUCA": {
      "bm_lq": 8.855,
      "bm_mg": 1.913,
      "pop_2000": 25081
    },
    "MANAVGAT": {
      "bm_lq": 1.94,
      "bm_mg": 1.882,
      "pop_2000": 71679
    },
    "SERIK": {
      "bm_lq": 2.55,
      "bm_mg": 3.472,
      "pop_2000": 30579
    }
  },
  "ARTVİN": {
    "ARDANUC": {
      "bm_lq": 2.339,
      "bm_mg": 2.356,
      "pop_2000": 5278
    },
    "ARHAVI": {
      "bm_lq": 2.202,
      "bm_mg": 1.809,
      "pop_2000": 14079
    },
    "ARTVIN MERKEZ": {
      "bm_lq": 1.79,
      "bm_mg": 2.47,
      "pop_2000": 23157
    },
    "BORCKA": {
      "bm_lq": 1.926,
      "bm_mg": 2.002,
      "pop_2000": 9008
    },
    "HOPA": {
      "bm_lq": 2.125,
      "bm_mg": 1.939,
      "pop_2000": 15445
    },
    "MURGUL": {
      "bm_lq": 2.165,
      "bm_mg": 1.692,
      "pop_2000": 3801
    },
    "SAVSAT": {
      "bm_lq": 2.021,
      "bm_mg": 2.701,
      "pop_2000": 7325
    },
    "YUSUFELI": {
      "bm_lq": 1.947,
      "bm_mg": 1.705,
      "pop_2000": 6105
    }
  },
  "AYDIN": {
    "AYDIN MERKEZ": {
      "bm_lq": 2.183,
      "bm_mg": 3.774,
      "pop_2000": 143267
    },
    "BOZDOGAN": {
      "bm_lq": 3.736,
      "bm_mg": 2.289,
      "pop_2000": 8300
    },
    "BUHARKENT": {
      "bm_lq": 4.847,
      "bm_mg": 2.312,
      "pop_2000": 7074
    },
    "CINE": {
      "bm_lq": 2.54,
      "bm_mg": 1.584,
      "pop_2000": 17867
    },
    "DIDIM": {
      "bm_lq": 2.09,
      "bm_mg": 3.227,
      "pop_2000": 25699
    },
    "GERMENCIK": {
      "bm_lq": 3.442,
      "bm_mg": 2.041,
      "pop_2000": 11596
    },
    "INCIRLIOVA": {
      "bm_lq": 3.24,
      "bm_mg": 2.905,
      "pop_2000": 17548
    },
    "KARACASU": {
      "bm_lq": 3.026,
      "bm_mg": 3.191,
      "pop_2000": 5915
    },
    "KARPUZLU": {
      "bm_lq": 3.576,
      "bm_mg": 2.302,
      "pop_2000": 2318
    },
    "KOCARLI": {
      "bm_lq": 8.686,
      "bm_mg": 1.684,
      "pop_2000": 8927
    },
    "KOSK": {
      "bm_lq": 3.179,
      "bm_mg": 2.239,
      "pop_2000": 8349
    },
    "KUSADASI": {
      "bm_lq": 1.899,
      "bm_mg": 2.772,
      "pop_2000": 47661
    },
    "KUYUCAK": {
      "bm_lq": 4.507,
      "bm_mg": 1.951,
      "pop_2000": 7282
    },
    "NAZILLI": {
      "bm_lq": 2.47,
      "bm_mg": 2.16,
      "pop_2000": 105665
    },
    "SOKE": {
      "bm_lq": 2.959,
      "bm_mg": 3.831,
      "pop_2000": 62384
    },
    "SULTANHISAR": {
      "bm_lq": 7.333,
      "bm_mg": 2.146,
      "pop_2000": 6256
    },
    "YENIPAZAR": {
      "bm_lq": 11.2,
      "bm_mg": 2.034,
      "pop_2000": 7006
    }
  },
  "BALIKESİR": {
    "AYVALIK": {
      "bm_lq": 2.405,
      "bm_mg": 1.929,
      "pop_2000": 31986
    },
    "BALIKESIR MERKEZ": {
      "bm_lq": 2.119,
      "bm_mg": 4.498,
      "pop_2000": 215436
    },
    "BALYA": {
      "bm_lq": 2.475,
      "bm_mg": 3.464,
      "pop_2000": 1916
    },
    "BANDIRMA": {
      "bm_lq": 2.318,
      "bm_mg": 2.604,
      "pop_2000": 97419
    },
    "BIGADIC": {
      "bm_lq": 2.519,
      "bm_mg": 3.067,
      "pop_2000": 14550
    },
    "BURHANIYE": {
      "bm_lq": 2.414,
      "bm_mg": 1.554,
      "pop_2000": 31227
    },
    "DURSUNBEY": {
      "bm_lq": 2.404,
      "bm_mg": 2.016,
      "pop_2000": 14654
    },
    "EDREMIT": {
      "bm_lq": 2.252,
      "bm_mg": 2.535,
      "pop_2000": 39202
    },
    "ERDEK": {
      "bm_lq": 2.21,
      "bm_mg": 1.349,
      "pop_2000": 18626
    },
    "GOMEC": {
      "bm_lq": 3.683,
      "bm_mg": 2.69,
      "pop_2000": 4122
    },
    "GONEN": {
      "bm_lq": 2.277,
      "bm_mg": 1.601,
      "pop_2000": 36263
    },
    "HAVRAN": {
      "bm_lq": 3.334,
      "bm_mg": 2.15,
      "pop_2000": 10122
    },
    "IVRINDI": {
      "bm_lq": 2.66,
      "bm_mg": 2.575,
      "pop_2000": 5772
    },
    "KEPSUT": {
      "bm_lq": 3.394,
      "bm_mg": 1.625,
      "pop_2000": 5545
    },
    "MANYAS": {
      "bm_lq": 2.744,
      "bm_mg": 1.748,
      "pop_2000": 5455
    },
    "MARMARA": {
      "bm_lq": 3.42,
      "bm_mg": 2.791,
      "pop_2000": 2215
    },
    "SAVASTEPE": {
      "bm_lq": 2.962,
      "bm_mg": 2.206,
      "pop_2000": 10288
    },
    "SINDIRGI": {
      "bm_lq": 2.857,
      "bm_mg": 2.328,
      "pop_2000": 10492
    },
    "SUSURLUK": {
      "bm_lq": 2.244,
      "bm_mg": 2.571,
      "pop_2000": 22305
    }
  },
  "BİLECİK": {
    "BILECIK MERKEZ": {
      "bm_lq": 2.011,
      "bm_mg": 1.612,
      "pop_2000": 34105
    },
    "BOZUYUK": {
      "bm_lq": 2.159,
      "bm_mg": 2.038,
      "pop_2000": 47469
    },
    "GOLPAZARI": {
      "bm_lq": 3.513,
      "bm_mg": 3.037,
      "pop_2000": 7002
    },
    "INHISAR": {
      "bm_lq": 6.182,
      "bm_mg": 1.636,
      "pop_2000": 2318
    },
    "OSMANELI": {
      "bm_lq": 2.608,
      "bm_mg": 2.071,
      "pop_2000": 12814
    },
    "PAZARYERI": {
      "bm_lq": 2.644,
      "bm_mg": 1.848,
      "pop_2000": 6659
    },
    "SOGUT": {
      "bm_lq": 1.928,
      "bm_mg": 2.122,
      "pop_2000": 12644
    },
    "YENIPAZAR": {
      "bm_lq": 2.745,
      "bm_mg": 2.86,
      "pop_2000": 1369
    }
  },
  "BİNGÖL": {
    "ADAKLI": {
      "bm_lq": 1.476,
      "bm_mg": 2.334,
      "pop_2000": 3370
    },
    "BINGOL MERKEZ": {
      "bm_lq": 1.84,
      "bm_mg": 1.803,
      "pop_2000": 68876
    },
    "GENC": {
      "bm_lq": 2.03,
      "bm_mg": 2.809,
      "pop_2000": 18345
    },
    "KARLIOVA": {
      "bm_lq": 1.862,
      "bm_mg": 2.898,
      "pop_2000": 8761
    },
    "KIGI": {
      "bm_lq": 1.531,
      "bm_mg": 1.411,
      "pop_2000": 4684
    },
    "SOLHAN": {
      "bm_lq": 2.517,
      "bm_mg": 1.525,
      "pop_2000": 14325
    },
    "YAYLADERE": {
      "bm_lq": 1.736,
      "bm_mg": 1.411,
      "pop_2000": 3136
    },
    "YEDISU": {
      "bm_lq": 1.566,
      "bm_mg": 1.903,
      "pop_2000": 1973
    }
  },
  "BİTLİS": {
    "ADILCEVAZ": {
      "bm_lq": 3.565,
      "bm_mg": 1.549,
      "pop_2000": 35174
    },
    "AHLAT": {
      "bm_lq": 3.369,
      "bm_mg": 2.422,
      "pop_2000": 34787
    },
    "BITLIS MERKEZ": {
      "bm_lq": 2.501,
      "bm_mg": 3.446,
      "pop_2000": 44923
    },
    "GUROYMAK": {
      "bm_lq": 3.107,
      "bm_mg": 2.903,
      "pop_2000": 22521
    },
    "HIZAN": {
      "bm_lq": 3.137,
      "bm_mg": 1.828,
      "pop_2000": 11067
    },
    "MUTKI": {
      "bm_lq": 1.559,
      "bm_mg": 2.21,
      "pop_2000": 4291
    },
    "TATVAN": {
      "bm_lq": 1.999,
      "bm_mg": 2.024,
      "pop_2000": 66748
    }
  },
  "BOLU": {
    "BOLU MERKEZ": {
      "bm_lq": 2.173,
      "bm_mg": 4.489,
      "pop_2000": 84565
    },
    "DORTDIVAN": {
      "bm_lq": 2.731,
      "bm_mg": 1.614,
      "pop_2000": 3335
    },
    "GEREDE": {
      "bm_lq": 2.204,
      "bm_mg": 1.815,
      "pop_2000": 25188
    },
    "GOYNUK": {
      "bm_lq": 2.849,
      "bm_mg": 1.745,
      "pop_2000": 4984
    },
    "KIBRISCIK": {
      "bm_lq": 2.457,
      "bm_mg": 2.778,
      "pop_2000": 2549
    },
    "MENGEN": {
      "bm_lq": 2.196,
      "bm_mg": 1.718,
      "pop_2000": 5411
    },
    "MUDURNU": {
      "bm_lq": 2.555,
      "bm_mg": 1.666,
      "pop_2000": 5955
    },
    "SEBEN": {
      "bm_lq": 3.823,
      "bm_mg": 3.391,
      "pop_2000": 4334
    },
    "YENICAGA": {
      "bm_lq": 2.205,
      "bm_mg": 2.162,
      "pop_2000": 6364
    }
  },
  "BURDUR": {
    "AGLASUN": {
      "bm_lq": 5.98,
      "bm_mg": 2.608,
      "pop_2000": 4738
    },
    "ALTINYAYLA": {
      "bm_lq": 3.248,
      "bm_mg": 1.779,
      "pop_2000": 4173
    },
    "BUCAK": {
      "bm_lq": 2.367,
      "bm_mg": 3.182,
      "pop_2000": 28833
    },
    "BURDUR MERKEZ": {
      "bm_lq": 2.182,
      "bm_mg": 2.785,
      "pop_2000": 63363
    },
    "CAVDIR": {
      "bm_lq": 3.727,
      "bm_mg": 2.3,
      "pop_2000": 4739
    },
    "CELTIKCI": {
      "bm_lq": 5.198,
      "bm_mg": 1.993,
      "pop_2000": 2534
    },
    "GOLHISAR": {
      "bm_lq": 3.779,
      "bm_mg": 1.247,
      "pop_2000": 12434
    },
    "KARAMANLI": {
      "bm_lq": 4.721,
      "bm_mg": 1.457,
      "pop_2000": 5000
    },
    "KEMER": {
      "bm_lq": 6.959,
      "bm_mg": 2.779,
      "pop_2000": 2262
    },
    "TEFENNI": {
      "bm_lq": 2.711,
      "bm_mg": 2.233,
      "pop_2000": 5398
    },
    "YESILOVA": {
      "bm_lq": 2.393,
      "bm_mg": 2.133,
      "pop_2000": 6423
    }
  },
  "BURSA": {
    "BUYUKORHAN": {
      "bm_lq": 2.955,
      "bm_mg": 2.39,
      "pop_2000": 3603
    },
    "GEMLIK": {
      "bm_lq": 2.206,
      "bm_mg": 2.77,
      "pop_2000": 63710
    },
    "GURSU": {
      "bm_lq": 2.364,
      "bm_mg": 1.718,
      "pop_2000": 21518
    },
    "HARMANCIK": {
      "bm_lq": 2.707,
      "bm_mg": 2.634,
      "pop_2000": 3560
    },
    "INEGOL": {
      "bm_lq": 2.129,
      "bm_mg": 2.606,
      "pop_2000": 105959
    },
    "IZNIK": {
      "bm_lq": 3.976,
      "bm_mg": 1.555,
      "pop_2000": 20169
    },
    "KARACABEY": {
      "bm_lq": 2.663,
      "bm_mg": 2.805,
      "pop_2000": 40624
    },
    "KELES": {
      "bm_lq": 2.123,
      "bm_mg": 1.961,
      "pop_2000": 3636
    },
    "KESTEL": {
      "bm_lq": 2.154,
      "bm_mg": 2.17,
      "pop_2000": 27496
    },
    "M.KEMALPASA": {
      "bm_lq": 2.423,
      "bm_mg": 2.86,
      "pop_2000": 46731
    },
    "MUDANYA": {
      "bm_lq": 2.18,
      "bm_mg": 2.101,
      "pop_2000": 20682
    },
    "NILUFER": {
      "bm_lq": 2.112,
      "bm_mg": 2.703,
      "pop_2000": 136311
    },
    "ORHANELI": {
      "bm_lq": 2.192,
      "bm_mg": 1.667,
      "pop_2000": 8071
    },
    "ORHANGAZI": {
      "bm_lq": 2.324,
      "bm_mg": 2.236,
      "pop_2000": 44426
    },
    "OSMANGAZI": {
      "bm_lq": 2.101,
      "bm_mg": 2.685,
      "pop_2000": 579127
    },
    "YENISEHIR": {
      "bm_lq": 3.407,
      "bm_mg": 3.295,
      "pop_2000": 26068
    },
    "YILDIRIM": {
      "bm_lq": 2.095,
      "bm_mg": 3.573,
      "pop_2000": 479249
    }
  },
  "ÇANAKKALE": {
    "AYVACIK": {
      "bm_lq": 3.109,
      "bm_mg": 2.498,
      "pop_2000": 6475
    },
    "BAYRAMIC": {
      "bm_lq": 3.828,
      "bm_mg": 2.105,
      "pop_2000": 11988
    },
    "BIGA": {
      "bm_lq": 2.194,
      "bm_mg": 2.482,
      "pop_2000": 27549
    },
    "BOZCAADA": {
      "bm_lq": 2.597,
      "bm_mg": 2.058,
      "pop_2000": 2427
    },
    "CAN": {
      "bm_lq": 2.143,
      "bm_mg": 1.665,
      "pop_2000": 28878
    },
    "CANAKKALE MERKEZ": {
      "bm_lq": 2.03,
      "bm_mg": 2.202,
      "pop_2000": 75810
    },
    "ECEABAT": {
      "bm_lq": 4.153,
      "bm_mg": 2.259,
      "pop_2000": 4778
    },
    "EZINE": {
      "bm_lq": 2.35,
      "bm_mg": 2.133,
      "pop_2000": 13309
    },
    "GELIBOLU": {
      "bm_lq": 2.122,
      "bm_mg": 2.54,
      "pop_2000": 23127
    },
    "GOKCEADA": {
      "bm_lq": 1.596,
      "bm_mg": 1.521,
      "pop_2000": 7254
    },
    "LAPSEKI": {
      "bm_lq": 2.663,
      "bm_mg": 2.19,
      "pop_2000": 8489
    },
    "YENICE": {
      "bm_lq": 2.531,
      "bm_mg": 1.525,
      "pop_2000": 5487
    }
  },
  "ÇANKIRI": {
    "ATKARACALAR": {
      "bm_lq": 3.017,
      "bm_mg": 1.86,
      "pop_2000": 5468
    },
    "BAYRAMOREN": {
      "bm_lq": 3.433,
      "bm_mg": 1.88,
      "pop_2000": 2697
    },
    "CANKIRI MERKEZ": {
      "bm_lq": 2.212,
      "bm_mg": 2.09,
      "pop_2000": 62508
    },
    "CERKES": {
      "bm_lq": 2.599,
      "bm_mg": 1.895,
      "pop_2000": 15536
    },
    "ELDIVAN": {
      "bm_lq": 2.859,
      "bm_mg": 2.261,
      "pop_2000": 5708
    },
    "ILGAZ": {
      "bm_lq": 2.206,
      "bm_mg": 3.263,
      "pop_2000": 11236
    },
    "KIZILIRMAK": {
      "bm_lq": 5.692,
      "bm_mg": 2.492,
      "pop_2000": 3008
    },
    "KORGUN": {
      "bm_lq": 2.999,
      "bm_mg": 2.685,
      "pop_2000": 6031
    },
    "KURSUNLU": {
      "bm_lq": 2.594,
      "bm_mg": 2.259,
      "pop_2000": 11569
    },
    "ORTA": {
      "bm_lq": 1.902,
      "bm_mg": 1.947,
      "pop_2000": 6045
    },
    "SABANOZU": {
      "bm_lq": 2.698,
      "bm_mg": 2.0,
      "pop_2000": 5996
    },
    "YAPRAKLI": {
      "bm_lq": 3.013,
      "bm_mg": 1.932,
      "pop_2000": 5384
    }
  },
  "ÇORUM": {
    "ALACA": {
      "bm_lq": 2.909,
      "bm_mg": 1.596,
      "pop_2000": 24983
    },
    "BAYAT": {
      "bm_lq": 2.337,
      "bm_mg": 1.92,
      "pop_2000": 7381
    },
    "BOGAZKALE": {
      "bm_lq": 2.394,
      "bm_mg": 2.206,
      "pop_2000": 1970
    },
    "CORUM MERKEZ": {
      "bm_lq": 2.227,
      "bm_mg": 3.55,
      "pop_2000": 161321
    },
    "DODURGA": {
      "bm_lq": 2.187,
      "bm_mg": 2.296,
      "pop_2000": 3431
    },
    "ISKILIP": {
      "bm_lq": 2.452,
      "bm_mg": 1.609,
      "pop_2000": 19648
    },
    "KARGI": {
      "bm_lq": 3.155,
      "bm_mg": 2.301,
      "pop_2000": 5728
    },
    "LACIN": {
      "bm_lq": 2.657,
      "bm_mg": 2.088,
      "pop_2000": 2153
    },
    "MECITOZU": {
      "bm_lq": 5.906,
      "bm_mg": 1.988,
      "pop_2000": 5787
    },
    "OGUZLAR": {
      "bm_lq": 3.795,
      "bm_mg": 1.6,
      "pop_2000": 4678
    },
    "ORTAKOY": {
      "bm_lq": 2.91,
      "bm_mg": 2.567,
      "pop_2000": 3349
    },
    "OSMANCIK": {
      "bm_lq": 2.875,
      "bm_mg": 2.801,
      "pop_2000": 28423
    },
    "SUNGURLU": {
      "bm_lq": 2.543,
      "bm_mg": 2.204,
      "pop_2000": 35397
    },
    "UGURLUDAG": {
      "bm_lq": 5.586,
      "bm_mg": 2.942,
      "pop_2000": 7648
    }
  },
  "DENİZLİ": {
    "ACIPAYAM": {
      "bm_lq": 2.342,
      "bm_mg": 1.903,
      "pop_2000": 9956
    },
    "AKKOY": {
      "bm_lq": 11.401,
      "bm_mg": 1.94,
      "pop_2000": 2716
    },
    "BABADAG": {
      "bm_lq": 1.976,
      "bm_mg": 1.682,
      "pop_2000": 4832
    },
    "BAKLAN": {
      "bm_lq": 3.448,
      "bm_mg": 2.802,
      "pop_2000": 2737
    },
    "BEKILLI": {
      "bm_lq": 2.651,
      "bm_mg": 2.19,
      "pop_2000": 3931
    },
    "BEYAGAC": {
      "bm_lq": 12.254,
      "bm_mg": 2.114,
      "pop_2000": 2789
    },
    "BOZKURT": {
      "bm_lq": 2.312,
      "bm_mg": 1.844,
      "pop_2000": 4191
    },
    "BULDAN": {
      "bm_lq": 2.397,
      "bm_mg": 1.986,
      "pop_2000": 13986
    },
    "CAL": {
      "bm_lq": 3.322,
      "bm_mg": 1.946,
      "pop_2000": 4926
    },
    "CAMELI": {
      "bm_lq": 3.454,
      "bm_mg": 2.868,
      "pop_2000": 2740
    },
    "CARDAK": {
      "bm_lq": 2.184,
      "bm_mg": 2.204,
      "pop_2000": 5649
    },
    "CIVRIL": {
      "bm_lq": 2.645,
      "bm_mg": 3.038,
      "pop_2000": 13749
    },
    "DENIZLI MERKEZ": {
      "bm_lq": 2.09,
      "bm_mg": 3.341,
      "pop_2000": 275480
    },
    "GUNEY": {
      "bm_lq": 9.602,
      "bm_mg": 2.204,
      "pop_2000": 6277
    },
    "HONAZ": {
      "bm_lq": 3.795,
      "bm_mg": 2.27,
      "pop_2000": 7442
    },
    "KALE": {
      "bm_lq": 4.159,
      "bm_mg": 2.295,
      "pop_2000": 7189
    },
    "SARAYKOY": {
      "bm_lq": 3.795,
      "bm_mg": 1.816,
      "pop_2000": 17760
    },
    "SERINHISAR": {
      "bm_lq": 7.282,
      "bm_mg": 1.274,
      "pop_2000": 15864
    },
    "TAVAS": {
      "bm_lq": 2.239,
      "bm_mg": 1.684,
      "pop_2000": 11700
    }
  },
  "DİYARBAKIR": {
    "BISMIL": {
      "bm_lq": 3.404,
      "bm_mg": 2.21,
      "pop_2000": 61182
    },
    "CERMIK": {
      "bm_lq": 2.505,
      "bm_mg": 2.302,
      "pop_2000": 15843
    },
    "CINAR": {
      "bm_lq": 3.784,
      "bm_mg": 2.182,
      "pop_2000": 13282
    },
    "CUNGUS": {
      "bm_lq": 1.892,
      "bm_mg": 2.195,
      "pop_2000": 4708
    },
    "DICLE": {
      "bm_lq": 1.674,
      "bm_mg": 1.529,
      "pop_2000": 9861
    },
    "DIYARBAKIR MERKEZ": {
      "bm_lq": 2.04,
      "bm_mg": 2.399,
      "pop_2000": 545983
    },
    "EGIL": {
      "bm_lq": 2.138,
      "bm_mg": 1.874,
      "pop_2000": 4827
    },
    "ERGANI": {
      "bm_lq": 2.304,
      "bm_mg": 2.047,
      "pop_2000": 47333
    },
    "HANI": {
      "bm_lq": 2.03,
      "bm_mg": 1.608,
      "pop_2000": 10918
    },
    "HAZRO": {
      "bm_lq": 2.228,
      "bm_mg": 1.603,
      "pop_2000": 6189
    },
    "KOCAKOY": {
      "bm_lq": 2.472,
      "bm_mg": 3.496,
      "pop_2000": 5678
    },
    "KULP": {
      "bm_lq": 1.845,
      "bm_mg": 2.226,
      "pop_2000": 15825
    },
    "LICE": {
      "bm_lq": 1.472,
      "bm_mg": 1.607,
      "pop_2000": 11927
    },
    "SILVAN": {
      "bm_lq": 2.349,
      "bm_mg": 2.686,
      "pop_2000": 64136
    }
  },
  "EDİRNE": {
    "EDIRNE MERKEZ": {
      "bm_lq": 2.205,
      "bm_mg": 2.594,
      "pop_2000": 119298
    },
    "ENEZ": {
      "bm_lq": 2.881,
      "bm_mg": 3.917,
      "pop_2000": 3941
    },
    "HAVSA": {
      "bm_lq": 2.557,
      "bm_mg": 2.016,
      "pop_2000": 8081
    },
    "IPSALA": {
      "bm_lq": 2.476,
      "bm_mg": 1.854,
      "pop_2000": 8471
    },
    "KESAN": {
      "bm_lq": 2.239,
      "bm_mg": 2.114,
      "pop_2000": 42755
    },
    "LALAPASA": {
      "bm_lq": 1.69,
      "bm_mg": 1.412,
      "pop_2000": 2270
    },
    "MERIC": {
      "bm_lq": 3.086,
      "bm_mg": 2.134,
      "pop_2000": 3382
    },
    "SULEOGLU": {
      "bm_lq": 1.407,
      "bm_mg": 1.31,
      "pop_2000": 6548
    },
    "UZUNKOPRU": {
      "bm_lq": 2.312,
      "bm_mg": 2.072,
      "pop_2000": 36162
    }
  },
  "ELAZIĞ": {
    "AGIN": {
      "bm_lq": 2.58,
      "bm_mg": 2.157,
      "pop_2000": 3590
    },
    "ALACAKAYA": {
      "bm_lq": 1.889,
      "bm_mg": 1.588,
      "pop_2000": 4034
    },
    "ARICAK": {
      "bm_lq": 1.582,
      "bm_mg": 2.153,
      "pop_2000": 4478
    },
    "BASKIL": {
      "bm_lq": 2.449,
      "bm_mg": 2.546,
      "pop_2000": 11772
    },
    "ELAZIG MERKEZ": {
      "bm_lq": 2.066,
      "bm_mg": 2.447,
      "pop_2000": 266495
    },
    "KARAKOCAN": {
      "bm_lq": 1.783,
      "bm_mg": 1.743,
      "pop_2000": 23994
    },
    "KEBAN": {
      "bm_lq": 1.816,
      "bm_mg": 2.55,
      "pop_2000": 5962
    },
    "KOVANCILAR": {
      "bm_lq": 2.404,
      "bm_mg": 2.806,
      "pop_2000": 21255
    },
    "MADEN": {
      "bm_lq": 1.926,
      "bm_mg": 1.619,
      "pop_2000": 7159
    },
    "PALU": {
      "bm_lq": 2.731,
      "bm_mg": 2.949,
      "pop_2000": 10103
    },
    "SIVRICE": {
      "bm_lq": 2.211,
      "bm_mg": 2.426,
      "pop_2000": 5432
    }
  },
  "ERZİNCAN": {
    "CAYIRLI": {
      "bm_lq": 7.212,
      "bm_mg": 1.423,
      "pop_2000": 6547
    },
    "ERZINCAN MERKEZ": {
      "bm_lq": 1.905,
      "bm_mg": 2.285,
      "pop_2000": 107175
    },
    "ILIC": {
      "bm_lq": 2.354,
      "bm_mg": 2.092,
      "pop_2000": 2361
    },
    "KEMAH": {
      "bm_lq": 2.047,
      "bm_mg": 2.525,
      "pop_2000": 2862
    },
    "KEMALIYE": {
      "bm_lq": 2.13,
      "bm_mg": 2.787,
      "pop_2000": 2243
    },
    "OTLUKBELI": {
      "bm_lq": 4.822,
      "bm_mg": 1.977,
      "pop_2000": 3479
    },
    "REFAHIYE": {
      "bm_lq": 1.855,
      "bm_mg": 1.882,
      "pop_2000": 6034
    },
    "TERCAN": {
      "bm_lq": 2.876,
      "bm_mg": 2.27,
      "pop_2000": 11207
    },
    "UZUMLU": {
      "bm_lq": 6.232,
      "bm_mg": 2.02,
      "pop_2000": 30298
    }
  },
  "ERZURUM": {
    "ASKALE": {
      "bm_lq": 1.777,
      "bm_mg": 1.647,
      "pop_2000": 15548
    },
    "CAT": {
      "bm_lq": 1.946,
      "bm_mg": 2.281,
      "pop_2000": 7169
    },
    "ERZURUM MERKEZ": {
      "bm_lq": 1.956,
      "bm_mg": 2.606,
      "pop_2000": 361235
    },
    "HINIS": {
      "bm_lq": 2.614,
      "bm_mg": 1.803,
      "pop_2000": 27504
    },
    "HORASAN": {
      "bm_lq": 2.151,
      "bm_mg": 2.556,
      "pop_2000": 16151
    },
    "ILICA": {
      "bm_lq": 2.11,
      "bm_mg": 2.012,
      "pop_2000": 12893
    },
    "ISPIR": {
      "bm_lq": 2.223,
      "bm_mg": 3.106,
      "pop_2000": 11188
    },
    "KARACOBAN": {
      "bm_lq": 3.076,
      "bm_mg": 2.321,
      "pop_2000": 12683
    },
    "KARAYAZI": {
      "bm_lq": 2.478,
      "bm_mg": 1.692,
      "pop_2000": 6749
    },
    "KOPRUKOY": {
      "bm_lq": 5.063,
      "bm_mg": 1.889,
      "pop_2000": 3712
    },
    "NARMAN": {
      "bm_lq": 2.635,
      "bm_mg": 2.639,
      "pop_2000": 9025
    },
    "OLTU": {
      "bm_lq": 1.997,
      "bm_mg": 2.635,
      "pop_2000": 23064
    },
    "OLUR": {
      "bm_lq": 2.587,
      "bm_mg": 3.382,
      "pop_2000": 3271
    },
    "PASINLER": {
      "bm_lq": 2.395,
      "bm_mg": 2.643,
      "pop_2000": 22787
    },
    "PAZARYOLU": {
      "bm_lq": 4.096,
      "bm_mg": 1.619,
      "pop_2000": 4826
    },
    "SENKAYA": {
      "bm_lq": 2.025,
      "bm_mg": 1.893,
      "pop_2000": 3676
    },
    "TEKMAN": {
      "bm_lq": 2.373,
      "bm_mg": 2.232,
      "pop_2000": 6350
    },
    "TORTUM": {
      "bm_lq": 1.955,
      "bm_mg": 1.929,
      "pop_2000": 7905
    },
    "UZUNDERE": {
      "bm_lq": 2.43,
      "bm_mg": 2.354,
      "pop_2000": 4815
    }
  },
  "ESKİŞEHİR": {
    "ALPU": {
      "bm_lq": 8.238,
      "bm_mg": 1.848,
      "pop_2000": 5708
    },
    "BEYLIKOVA": {
      "bm_lq": 5.305,
      "bm_mg": 2.775,
      "pop_2000": 5420
    },
    "CIFTELER": {
      "bm_lq": 3.257,
      "bm_mg": 2.357,
      "pop_2000": 11883
    },
    "ESKISEHIR MERKEZ": {
      "bm_lq": 2.136,
      "bm_mg": 4.513,
      "pop_2000": 482793
    },
    "GUNYUZU": {
      "bm_lq": 6.206,
      "bm_mg": 1.903,
      "pop_2000": 4737
    },
    "HAN": {
      "bm_lq": 7.796,
      "bm_mg": 2.068,
      "pop_2000": 2050
    },
    "INONU": {
      "bm_lq": 2.85,
      "bm_mg": 1.558,
      "pop_2000": 5180
    },
    "MAHMUDIYE": {
      "bm_lq": 3.468,
      "bm_mg": 3.561,
      "pop_2000": 5141
    },
    "MIHALGAZI": {
      "bm_lq": 2.945,
      "bm_mg": 1.982,
      "pop_2000": 7613
    },
    "MIHALICCIK": {
      "bm_lq": 2.35,
      "bm_mg": 2.697,
      "pop_2000": 4706
    },
    "SARICAKAYA": {
      "bm_lq": 13.494,
      "bm_mg": 1.68,
      "pop_2000": 7942
    },
    "SEYITGAZI": {
      "bm_lq": 3.439,
      "bm_mg": 1.94,
      "pop_2000": 3281
    },
    "SIVRIHISAR": {
      "bm_lq": 2.426,
      "bm_mg": 2.024,
      "pop_2000": 10574
    }
  },
  "GAZİANTEP": {
    "ARABAN": {
      "bm_lq": 9.36,
      "bm_mg": 1.596,
      "pop_2000": 10666
    },
    "ISLAHIYE": {
      "bm_lq": 2.363,
      "bm_mg": 1.836,
      "pop_2000": 38770
    },
    "KARKAMIS": {
      "bm_lq": 1.984,
      "bm_mg": 2.213,
      "pop_2000": 4412
    },
    "NIZIP": {
      "bm_lq": 2.211,
      "bm_mg": 1.804,
      "pop_2000": 71629
    },
    "NURDAGI": {
      "bm_lq": 2.611,
      "bm_mg": 2.31,
      "pop_2000": 10866
    },
    "OGUZELI": {
      "bm_lq": 2.787,
      "bm_mg": 1.55,
      "pop_2000": 11527
    },
    "SAHINBEY": {
      "bm_lq": 2.107,
      "bm_mg": 3.481,
      "pop_2000": 498159
    },
    "SEHITKAMIL": {
      "bm_lq": 2.116,
      "bm_mg": 2.729,
      "pop_2000": 355354
    },
    "YAVUZELI": {
      "bm_lq": 4.628,
      "bm_mg": 2.044,
      "pop_2000": 7743
    }
  },
  "GİRESUN": {
    "ALUCRA": {
      "bm_lq": 2.567,
      "bm_mg": 2.549,
      "pop_2000": 14365
    },
    "BULANCAK": {
      "bm_lq": 2.263,
      "bm_mg": 3.733,
      "pop_2000": 32182
    },
    "CAMOLUK": {
      "bm_lq": 3.661,
      "bm_mg": 1.807,
      "pop_2000": 4192
    },
    "CANAKCI": {
      "bm_lq": 2.566,
      "bm_mg": 2.117,
      "pop_2000": 6644
    },
    "DERELI": {
      "bm_lq": 2.46,
      "bm_mg": 1.739,
      "pop_2000": 8124
    },
    "DOGANKENT": {
      "bm_lq": 2.335,
      "bm_mg": 2.176,
      "pop_2000": 3789
    },
    "ESPIYE": {
      "bm_lq": 2.999,
      "bm_mg": 2.041,
      "pop_2000": 12990
    },
    "EYNESIL": {
      "bm_lq": 2.998,
      "bm_mg": 2.779,
      "pop_2000": 10667
    },
    "GIRESUN MERKEZ": {
      "bm_lq": 2.137,
      "bm_mg": 2.336,
      "pop_2000": 83636
    },
    "GORELE": {
      "bm_lq": 2.432,
      "bm_mg": 1.91,
      "pop_2000": 27214
    },
    "GUCE": {
      "bm_lq": 7.191,
      "bm_mg": 1.656,
      "pop_2000": 3461
    },
    "KESAP": {
      "bm_lq": 2.266,
      "bm_mg": 2.635,
      "pop_2000": 9475
    },
    "PIRAZIZ": {
      "bm_lq": 3.005,
      "bm_mg": 1.662,
      "pop_2000": 9416
    },
    "S.KARAHISAR": {
      "bm_lq": 3.01,
      "bm_mg": 1.863,
      "pop_2000": 36713
    },
    "TIREBOLU": {
      "bm_lq": 2.618,
      "bm_mg": 2.302,
      "pop_2000": 16112
    },
    "YAGLIDERE": {
      "bm_lq": 2.989,
      "bm_mg": 2.314,
      "pop_2000": 4336
    }
  },
  "GÜMÜŞHANE": {
    "GUMUSHANE MERKEZ": {
      "bm_lq": 1.943,
      "bm_mg": 1.229,
      "pop_2000": 30270
    },
    "KELKIT": {
      "bm_lq": 3.164,
      "bm_mg": 2.407,
      "pop_2000": 19090
    },
    "KOSE": {
      "bm_lq": 2.659,
      "bm_mg": 2.612,
      "pop_2000": 8153
    },
    "KURTUN": {
      "bm_lq": 2.509,
      "bm_mg": 2.409,
      "pop_2000": 3488
    },
    "SIRAN": {
      "bm_lq": 2.567,
      "bm_mg": 1.985,
      "pop_2000": 11977
    },
    "TORUL": {
      "bm_lq": 2.086,
      "bm_mg": 2.466,
      "pop_2000": 4592
    }
  },
  "HAKKARİ": {
    "CUKURCA": {
      "bm_lq": 1.253,
      "bm_mg": 1.454,
      "pop_2000": 7471
    },
    "HAKKARI MERKEZ": {
      "bm_lq": 1.625,
      "bm_mg": 1.864,
      "pop_2000": 58145
    },
    "SEMDINLI": {
      "bm_lq": 1.364,
      "bm_mg": 1.58,
      "pop_2000": 14177
    },
    "YUKSEKOVA": {
      "bm_lq": 1.692,
      "bm_mg": 1.667,
      "pop_2000": 59662
    }
  },
  "HATAY": {
    "ALTINOZU": {
      "bm_lq": 2.988,
      "bm_mg": 3.038,
      "pop_2000": 5352
    },
    "BELEN": {
      "bm_lq": 2.214,
      "bm_mg": 3.047,
      "pop_2000": 18646
    },
    "DORTYOL": {
      "bm_lq": 2.462,
      "bm_mg": 2.694,
      "pop_2000": 53597
    },
    "ERZIN": {
      "bm_lq": 4.225,
      "bm_mg": 1.709,
      "pop_2000": 25879
    },
    "HASSA": {
      "bm_lq": 3.092,
      "bm_mg": 1.551,
      "pop_2000": 9071
    },
    "HATAY MERKEZ": {
      "bm_lq": 2.159,
      "bm_mg": 3.717,
      "pop_2000": 144910
    },
    "ISKENDERUN": {
      "bm_lq": 2.12,
      "bm_mg": 3.309,
      "pop_2000": 159149
    },
    "KIRIKHAN": {
      "bm_lq": 3.337,
      "bm_mg": 1.741,
      "pop_2000": 63615
    },
    "KUMLU": {
      "bm_lq": 5.828,
      "bm_mg": 1.619,
      "pop_2000": 6629
    },
    "REYHANLI": {
      "bm_lq": 2.895,
      "bm_mg": 2.041,
      "pop_2000": 52135
    },
    "SAMANDAG": {
      "bm_lq": 2.702,
      "bm_mg": 3.697,
      "pop_2000": 34641
    },
    "YAYLADAGI": {
      "bm_lq": 1.846,
      "bm_mg": 2.217,
      "pop_2000": 7717
    }
  },
  "ISPARTA": {
    "AKSU": {
      "bm_lq": 2.78,
      "bm_mg": 2.624,
      "pop_2000": 3532
    },
    "ATABEY": {
      "bm_lq": 2.336,
      "bm_mg": 2.338,
      "pop_2000": 9703
    },
    "EGIRDIR": {
      "bm_lq": 1.862,
      "bm_mg": 1.743,
      "pop_2000": 16905
    },
    "GELENDOST": {
      "bm_lq": 6.239,
      "bm_mg": 1.702,
      "pop_2000": 7321
    },
    "GONEN": {
      "bm_lq": 2.367,
      "bm_mg": 1.73,
      "pop_2000": 10826
    },
    "ISPARTA MERKEZ": {
      "bm_lq": 2.093,
      "bm_mg": 2.532,
      "pop_2000": 148496
    },
    "KECIBORLU": {
      "bm_lq": 2.61,
      "bm_mg": 2.025,
      "pop_2000": 10390
    },
    "SARKIKARAAGAC": {
      "bm_lq": 2.546,
      "bm_mg": 2.138,
      "pop_2000": 24502
    },
    "SENIRKENT": {
      "bm_lq": 2.681,
      "bm_mg": 1.813,
      "pop_2000": 13698
    },
    "SUTCULER": {
      "bm_lq": 2.155,
      "bm_mg": 2.186,
      "pop_2000": 3636
    },
    "ULUBORLU": {
      "bm_lq": 3.006,
      "bm_mg": 2.303,
      "pop_2000": 11717
    },
    "YALVAC": {
      "bm_lq": 2.367,
      "bm_mg": 1.629,
      "pop_2000": 35316
    },
    "YENISARBADEMLI": {
      "bm_lq": 2.762,
      "bm_mg": 2.079,
      "pop_2000": 5519
    }
  },
  "MERSİN (İÇEL)": {
    "ANAMUR": {
      "bm_lq": 2.4,
      "bm_mg": 2.133,
      "pop_2000": 49948
    },
    "AYDINCIK": {
      "bm_lq": 7.839,
      "bm_mg": 1.778,
      "pop_2000": 7941
    },
    "BOZYAZI": {
      "bm_lq": 5.025,
      "bm_mg": 2.128,
      "pop_2000": 26314
    },
    "CAMLIYAYLA": {
      "bm_lq": 3.173,
      "bm_mg": 3.362,
      "pop_2000": 8806
    },
    "ERDEMLI": {
      "bm_lq": 3.455,
      "bm_mg": 2.19,
      "pop_2000": 40175
    },
    "GULNAR": {
      "bm_lq": 2.586,
      "bm_mg": 1.594,
      "pop_2000": 10503
    },
    "MERSIN (ICEL) MERKEZ": {
      "bm_lq": 2.2,
      "bm_mg": 2.796,
      "pop_2000": 537842
    },
    "MUT": {
      "bm_lq": 2.913,
      "bm_mg": 1.87,
      "pop_2000": 36482
    },
    "SILIFKE": {
      "bm_lq": 2.772,
      "bm_mg": 2.142,
      "pop_2000": 64827
    },
    "TARSUS": {
      "bm_lq": 2.647,
      "bm_mg": 2.07,
      "pop_2000": 216382
    }
  },
  "İSTANBUL": {
    "ADALAR": {
      "bm_lq": 2.094,
      "bm_mg": 2.613,
      "pop_2000": 17760
    },
    "AVCILAR": {
      "bm_lq": 2.07,
      "bm_mg": 3.113,
      "pop_2000": 233749
    },
    "BAGCILAR": {
      "bm_lq": 1.935,
      "bm_mg": 2.372,
      "pop_2000": 556519
    },
    "BAHCELIEVLER": {
      "bm_lq": 2.065,
      "bm_mg": 2.951,
      "pop_2000": 478623
    },
    "BAKIRKOY": {
      "bm_lq": 1.968,
      "bm_mg": 3.334,
      "pop_2000": 208398
    },
    "BAYRAMPASA": {
      "bm_lq": 2.019,
      "bm_mg": 2.738,
      "pop_2000": 246006
    },
    "BESIKTAS": {
      "bm_lq": 2.007,
      "bm_mg": 2.702,
      "pop_2000": 190813
    },
    "BEYKOZ": {
      "bm_lq": 2.079,
      "bm_mg": 2.54,
      "pop_2000": 172291
    },
    "BEYOGLU": {
      "bm_lq": 2.065,
      "bm_mg": 3.144,
      "pop_2000": 231900
    },
    "BUYUKCEKMECE": {
      "bm_lq": 2.114,
      "bm_mg": 1.742,
      "pop_2000": 35860
    },
    "CATALCA": {
      "bm_lq": 2.277,
      "bm_mg": 2.647,
      "pop_2000": 15779
    },
    "EMINONU": {
      "bm_lq": 2.041,
      "bm_mg": 2.106,
      "pop_2000": 55635
    },
    "ESENLER": {
      "bm_lq": 2.034,
      "bm_mg": 2.846,
      "pop_2000": 380709
    },
    "EYUP": {
      "bm_lq": 2.063,
      "bm_mg": 2.323,
      "pop_2000": 235116
    },
    "FATIH": {
      "bm_lq": 2.034,
      "bm_mg": 3.491,
      "pop_2000": 403508
    },
    "GAZIOSMANPASA": {
      "bm_lq": 1.94,
      "bm_mg": 2.926,
      "pop_2000": 658756
    },
    "GUNGOREN": {
      "bm_lq": 2.048,
      "bm_mg": 2.393,
      "pop_2000": 272950
    },
    "KADIKOY": {
      "bm_lq": 2.064,
      "bm_mg": 2.026,
      "pop_2000": 663299
    },
    "KAGITHANE": {
      "bm_lq": 2.064,
      "bm_mg": 2.842,
      "pop_2000": 345239
    },
    "KARTAL": {
      "bm_lq": 2.076,
      "bm_mg": 4.059,
      "pop_2000": 337390
    },
    "KUCUKCEKMECE": {
      "bm_lq": 2.071,
      "bm_mg": 2.834,
      "pop_2000": 593520
    },
    "MALTEPE": {
      "bm_lq": 2.065,
      "bm_mg": 3.758,
      "pop_2000": 355384
    },
    "PENDIK": {
      "bm_lq": 2.074,
      "bm_mg": 4.303,
      "pop_2000": 384668
    },
    "SARIYER": {
      "bm_lq": 2.11,
      "bm_mg": 2.616,
      "pop_2000": 219032
    },
    "SILE": {
      "bm_lq": 2.152,
      "bm_mg": 2.594,
      "pop_2000": 10262
    },
    "SILIVRI": {
      "bm_lq": 2.255,
      "bm_mg": 2.613,
      "pop_2000": 44530
    },
    "SISLI": {
      "bm_lq": 2.063,
      "bm_mg": 3.048,
      "pop_2000": 270674
    },
    "SULTANBEYLI": {
      "bm_lq": 2.073,
      "bm_mg": 2.142,
      "pop_2000": 175700
    },
    "TUZLA": {
      "bm_lq": 2.11,
      "bm_mg": 3.787,
      "pop_2000": 107883
    },
    "UMRANIYE": {
      "bm_lq": 2.072,
      "bm_mg": 4.225,
      "pop_2000": 440859
    },
    "USKUDAR": {
      "bm_lq": 2.064,
      "bm_mg": 2.342,
      "pop_2000": 495118
    },
    "ZEYTINBURNU": {
      "bm_lq": 2.021,
      "bm_mg": 2.341,
      "pop_2000": 247669
    }
  },
  "İZMİR": {
    "ALIAGA": {
      "bm_lq": 2.11,
      "bm_mg": 2.006,
      "pop_2000": 37537
    },
    "BALCOVA": {
      "bm_lq": 2.163,
      "bm_mg": 1.846,
      "pop_2000": 66877
    },
    "BAYINDIR": {
      "bm_lq": 8.39,
      "bm_mg": 1.456,
      "pop_2000": 15870
    },
    "BERGAMA": {
      "bm_lq": 2.698,
      "bm_mg": 2.637,
      "pop_2000": 52173
    },
    "BEYDAG": {
      "bm_lq": 3.304,
      "bm_mg": 1.998,
      "pop_2000": 5521
    },
    "BORNOVA": {
      "bm_lq": 2.083,
      "bm_mg": 4.799,
      "pop_2000": 391128
    },
    "BUCA": {
      "bm_lq": 2.08,
      "bm_mg": 2.282,
      "pop_2000": 308661
    },
    "CESME": {
      "bm_lq": 2.082,
      "bm_mg": 2.73,
      "pop_2000": 25257
    },
    "CIGLI": {
      "bm_lq": 2.091,
      "bm_mg": 2.28,
      "pop_2000": 106740
    },
    "DIKILI": {
      "bm_lq": 2.899,
      "bm_mg": 2.155,
      "pop_2000": 12552
    },
    "FOCA": {
      "bm_lq": 1.66,
      "bm_mg": 1.896,
      "pop_2000": 14604
    },
    "GAZIEMIR": {
      "bm_lq": 2.05,
      "bm_mg": 2.804,
      "pop_2000": 70035
    },
    "GUZELBAHCE": {
      "bm_lq": 2.566,
      "bm_mg": 2.277,
      "pop_2000": 14924
    },
    "KARABURUN": {
      "bm_lq": 1.85,
      "bm_mg": 2.092,
      "pop_2000": 2932
    },
    "KARSIYAKA": {
      "bm_lq": 2.084,
      "bm_mg": 4.883,
      "pop_2000": 438430
    },
    "KEMALPASA": {
      "bm_lq": 2.337,
      "bm_mg": 1.743,
      "pop_2000": 25448
    },
    "KINIK": {
      "bm_lq": 8.233,
      "bm_mg": 1.614,
      "pop_2000": 13136
    },
    "KIRAZ": {
      "bm_lq": 2.629,
      "bm_mg": 1.597,
      "pop_2000": 10001
    },
    "KONAK": {
      "bm_lq": 2.077,
      "bm_mg": 2.026,
      "pop_2000": 781363
    },
    "MENDERES": {
      "bm_lq": 3.078,
      "bm_mg": 1.229,
      "pop_2000": 16792
    },
    "MENEMEN": {
      "bm_lq": 2.398,
      "bm_mg": 2.041,
      "pop_2000": 46079
    },
    "NARLIDERE": {
      "bm_lq": 2.032,
      "bm_mg": 2.453,
      "pop_2000": 54107
    },
    "ODEMIS": {
      "bm_lq": 3.08,
      "bm_mg": 2.411,
      "pop_2000": 61896
    },
    "SEFERIHISAR": {
      "bm_lq": 2.546,
      "bm_mg": 1.724,
      "pop_2000": 17526
    },
    "SELCUK": {
      "bm_lq": 2.849,
      "bm_mg": 2.413,
      "pop_2000": 25414
    },
    "TIRE": {
      "bm_lq": 3.271,
      "bm_mg": 2.295,
      "pop_2000": 42988
    },
    "TORBALI": {
      "bm_lq": 2.619,
      "bm_mg": 1.849,
      "pop_2000": 38099
    },
    "URLA": {
      "bm_lq": 2.306,
      "bm_mg": 2.492,
      "pop_2000": 36579
    }
  },
  "KARS": {
    "AKYAKA": {
      "bm_lq": 2.232,
      "bm_mg": 2.251,
      "pop_2000": 3400
    },
    "ARPACAY": {
      "bm_lq": 2.299,
      "bm_mg": 2.476,
      "pop_2000": 4453
    },
    "DIGOR": {
      "bm_lq": 1.786,
      "bm_mg": 2.276,
      "pop_2000": 2708
    },
    "KAGIZMAN": {
      "bm_lq": 1.77,
      "bm_mg": 2.159,
      "pop_2000": 21685
    },
    "KARS MERKEZ": {
      "bm_lq": 2.0,
      "bm_mg": 2.294,
      "pop_2000": 78473
    },
    "SARIKAMIS": {
      "bm_lq": 1.642,
      "bm_mg": 1.617,
      "pop_2000": 23236
    },
    "SELIM": {
      "bm_lq": 2.712,
      "bm_mg": 2.074,
      "pop_2000": 4393
    },
    "SUSUZ": {
      "bm_lq": 2.128,
      "bm_mg": 1.988,
      "pop_2000": 3797
    }
  },
  "KASTAMONU": {
    "ABANA": {
      "bm_lq": 2.233,
      "bm_mg": 1.793,
      "pop_2000": 3590
    },
    "AGLI": {
      "bm_lq": 6.405,
      "bm_mg": 1.883,
      "pop_2000": 3074
    },
    "ARAC": {
      "bm_lq": 2.149,
      "bm_mg": 2.001,
      "pop_2000": 5696
    },
    "AZDAVAY": {
      "bm_lq": 2.2,
      "bm_mg": 2.042,
      "pop_2000": 3502
    },
    "BOZKURT": {
      "bm_lq": 2.297,
      "bm_mg": 2.254,
      "pop_2000": 5451
    },
    "CATALZEYTIN": {
      "bm_lq": 2.398,
      "bm_mg": 2.585,
      "pop_2000": 3410
    },
    "CIDE": {
      "bm_lq": 2.11,
      "bm_mg": 2.941,
      "pop_2000": 5834
    },
    "DADAY": {
      "bm_lq": 2.464,
      "bm_mg": 2.098,
      "pop_2000": 4625
    },
    "DEVREKANI": {
      "bm_lq": 3.27,
      "bm_mg": 1.854,
      "pop_2000": 6174
    },
    "DOGANYURT": {
      "bm_lq": 2.874,
      "bm_mg": 3.016,
      "pop_2000": 1470
    },
    "HANONU": {
      "bm_lq": 3.032,
      "bm_mg": 1.881,
      "pop_2000": 2451
    },
    "IHSANGAZI": {
      "bm_lq": 11.228,
      "bm_mg": 2.12,
      "pop_2000": 3127
    },
    "INEBOLU": {
      "bm_lq": 2.061,
      "bm_mg": 2.543,
      "pop_2000": 9486
    },
    "KASTAMONU MERKEZ": {
      "bm_lq": 2.113,
      "bm_mg": 2.436,
      "pop_2000": 64606
    },
    "KURE": {
      "bm_lq": 1.892,
      "bm_mg": 2.371,
      "pop_2000": 3880
    },
    "PINARBASI": {
      "bm_lq": 2.591,
      "bm_mg": 2.02,
      "pop_2000": 2270
    },
    "SENPAZAR": {
      "bm_lq": 3.029,
      "bm_mg": 2.182,
      "pop_2000": 2682
    },
    "SEYDILER": {
      "bm_lq": 3.276,
      "bm_mg": 4.053,
      "pop_2000": 3254
    },
    "TASKOPRU": {
      "bm_lq": 2.571,
      "bm_mg": 1.522,
      "pop_2000": 16181
    },
    "TOSYA": {
      "bm_lq": 2.508,
      "bm_mg": 1.883,
      "pop_2000": 23257
    }
  },
  "KAYSERİ": {
    "AKKISLA": {
      "bm_lq": 2.45,
      "bm_mg": 2.328,
      "pop_2000": 3265
    },
    "BUNYAN": {
      "bm_lq": 2.347,
      "bm_mg": 2.498,
      "pop_2000": 12510
    },
    "DEVELI": {
      "bm_lq": 2.312,
      "bm_mg": 1.914,
      "pop_2000": 35084
    },
    "FELAHIYE": {
      "bm_lq": 3.703,
      "bm_mg": 3.512,
      "pop_2000": 6015
    },
    "HACILAR": {
      "bm_lq": 2.046,
      "bm_mg": 2.09,
      "pop_2000": 19655
    },
    "INCESU": {
      "bm_lq": 2.516,
      "bm_mg": 3.243,
      "pop_2000": 8511
    },
    "KOCASINAN": {
      "bm_lq": 2.119,
      "bm_mg": 4.297,
      "pop_2000": 272939
    },
    "MELIKGAZI": {
      "bm_lq": 2.101,
      "bm_mg": 4.133,
      "pop_2000": 263453
    },
    "OZVATAN": {
      "bm_lq": 2.669,
      "bm_mg": 2.092,
      "pop_2000": 7105
    },
    "PINARBASI": {
      "bm_lq": 2.598,
      "bm_mg": 1.946,
      "pop_2000": 12075
    },
    "SARIOGLAN": {
      "bm_lq": 3.067,
      "bm_mg": 1.742,
      "pop_2000": 5245
    },
    "SARIZ": {
      "bm_lq": 3.1,
      "bm_mg": 2.246,
      "pop_2000": 4404
    },
    "TALAS": {
      "bm_lq": 2.098,
      "bm_mg": 2.797,
      "pop_2000": 34879
    },
    "TOMARZA": {
      "bm_lq": 2.336,
      "bm_mg": 2.687,
      "pop_2000": 10963
    },
    "YAHYALI": {
      "bm_lq": 2.749,
      "bm_mg": 3.044,
      "pop_2000": 22665
    },
    "YESILHISAR": {
      "bm_lq": 6.991,
      "bm_mg": 1.519,
      "pop_2000": 13586
    }
  },
  "KIRKLARELİ": {
    "BABAESKI": {
      "bm_lq": 2.214,
      "bm_mg": 2.491,
      "pop_2000": 25559
    },
    "DEMIRKOY": {
      "bm_lq": 2.642,
      "bm_mg": 2.362,
      "pop_2000": 4855
    },
    "KIRKLARELI MERKEZ": {
      "bm_lq": 2.204,
      "bm_mg": 4.377,
      "pop_2000": 53221
    },
    "KOFCAZ": {
      "bm_lq": 1.733,
      "bm_mg": 1.671,
      "pop_2000": 1538
    },
    "LULEBURGAZ": {
      "bm_lq": 2.163,
      "bm_mg": 3.689,
      "pop_2000": 79002
    },
    "PEHLIVANKOY": {
      "bm_lq": 3.591,
      "bm_mg": 2.064,
      "pop_2000": 3136
    },
    "PINARHISAR": {
      "bm_lq": 2.076,
      "bm_mg": 1.992,
      "pop_2000": 11263
    },
    "VIZE": {
      "bm_lq": 2.257,
      "bm_mg": 1.47,
      "pop_2000": 10628
    }
  },
  "KIRŞEHİR": {
    "AKCAKENT": {
      "bm_lq": 2.155,
      "bm_mg": 2.592,
      "pop_2000": 1268
    },
    "AKPINAR": {
      "bm_lq": 2.905,
      "bm_mg": 2.212,
      "pop_2000": 3696
    },
    "BOZTEPE": {
      "bm_lq": 8.464,
      "bm_mg": 2.369,
      "pop_2000": 5022
    },
    "CICEKDAGI": {
      "bm_lq": 2.397,
      "bm_mg": 2.67,
      "pop_2000": 6683
    },
    "KAMAN": {
      "bm_lq": 2.425,
      "bm_mg": 2.292,
      "pop_2000": 27962
    },
    "KIRSEHIR MERKEZ": {
      "bm_lq": 2.219,
      "bm_mg": 3.75,
      "pop_2000": 88105
    },
    "MUCUR": {
      "bm_lq": 3.375,
      "bm_mg": 1.779,
      "pop_2000": 14676
    }
  },
  "KOCAELİ": {
    "DERINCE": {
      "bm_lq": 2.113,
      "bm_mg": 2.473,
      "pop_2000": 93997
    },
    "GEBZE": {
      "bm_lq": 2.149,
      "bm_mg": 2.102,
      "pop_2000": 253487
    },
    "GOLCUK": {
      "bm_lq": 2.025,
      "bm_mg": 1.846,
      "pop_2000": 55790
    },
    "KANDIRA": {
      "bm_lq": 2.058,
      "bm_mg": 2.656,
      "pop_2000": 12641
    },
    "KARAMURSEL": {
      "bm_lq": 2.164,
      "bm_mg": 2.227,
      "pop_2000": 29353
    },
    "KOCAELI MERKEZ": {
      "bm_lq": 2.15,
      "bm_mg": 2.6,
      "pop_2000": 195699
    },
    "KORFEZ": {
      "bm_lq": 2.112,
      "bm_mg": 2.466,
      "pop_2000": 81938
    }
  },
  "KONYA": {
    "AHIRLI": {
      "bm_lq": 5.365,
      "bm_mg": 2.786,
      "pop_2000": 5685
    },
    "AKOREN": {
      "bm_lq": 3.643,
      "bm_mg": 2.992,
      "pop_2000": 10946
    },
    "AKSEHIR": {
      "bm_lq": 2.379,
      "bm_mg": 2.787,
      "pop_2000": 60226
    },
    "ALTINEKIN": {
      "bm_lq": 5.861,
      "bm_mg": 1.57,
      "pop_2000": 9145
    },
    "BEYSEHIR": {
      "bm_lq": 2.432,
      "bm_mg": 3.107,
      "pop_2000": 41312
    },
    "BOZKIR": {
      "bm_lq": 2.211,
      "bm_mg": 2.91,
      "pop_2000": 10483
    },
    "CELTIK": {
      "bm_lq": 8.91,
      "bm_mg": 1.898,
      "pop_2000": 4692
    },
    "CIHANBEYLI": {
      "bm_lq": 3.549,
      "bm_mg": 2.961,
      "pop_2000": 18306
    },
    "CUMRA": {
      "bm_lq": 5.673,
      "bm_mg": 1.629,
      "pop_2000": 42308
    },
    "DERBENT": {
      "bm_lq": 6.32,
      "bm_mg": 2.108,
      "pop_2000": 7440
    },
    "DEREBUCAK": {
      "bm_lq": 2.899,
      "bm_mg": 2.016,
      "pop_2000": 5072
    },
    "DOGANHISAR": {
      "bm_lq": 2.724,
      "bm_mg": 3.067,
      "pop_2000": 9756
    },
    "EMIRGAZI": {
      "bm_lq": 8.769,
      "bm_mg": 2.287,
      "pop_2000": 8524
    },
    "EREGLI": {
      "bm_lq": 2.583,
      "bm_mg": 2.223,
      "pop_2000": 82633
    },
    "GUNEYSINIR": {
      "bm_lq": 3.011,
      "bm_mg": 2.69,
      "pop_2000": 10217
    },
    "HADIM": {
      "bm_lq": 3.094,
      "bm_mg": 2.376,
      "pop_2000": 16620
    },
    "HALKAPINAR": {
      "bm_lq": 3.689,
      "bm_mg": 1.781,
      "pop_2000": 2021
    },
    "HUYUK": {
      "bm_lq": 2.53,
      "bm_mg": 1.721,
      "pop_2000": 8472
    },
    "ILGIN": {
      "bm_lq": 2.528,
      "bm_mg": 1.611,
      "pop_2000": 26698
    },
    "KADINHANI": {
      "bm_lq": 2.819,
      "bm_mg": 2.602,
      "pop_2000": 14816
    },
    "KARAPINAR": {
      "bm_lq": 6.483,
      "bm_mg": 2.593,
      "pop_2000": 35285
    },
    "KARATAY": {
      "bm_lq": 2.29,
      "bm_mg": 3.758,
      "pop_2000": 183677
    },
    "KULU": {
      "bm_lq": 2.758,
      "bm_mg": 1.594,
      "pop_2000": 28024
    },
    "MERAM": {
      "bm_lq": 2.175,
      "bm_mg": 3.721,
      "pop_2000": 231386
    },
    "SARAYONU": {
      "bm_lq": 3.189,
      "bm_mg": 2.281,
      "pop_2000": 10386
    },
    "SELCUKLU": {
      "bm_lq": 2.12,
      "bm_mg": 2.887,
      "pop_2000": 327627
    },
    "SEYDISEHIR": {
      "bm_lq": 2.268,
      "bm_mg": 1.964,
      "pop_2000": 48372
    },
    "TASKENT": {
      "bm_lq": 3.178,
      "bm_mg": 1.643,
      "pop_2000": 10779
    },
    "TUZLUKCU": {
      "bm_lq": 9.181,
      "bm_mg": 2.622,
      "pop_2000": 5845
    },
    "YALIHUYUK": {
      "bm_lq": 3.413,
      "bm_mg": 1.93,
      "pop_2000": 5330
    },
    "YUNAK": {
      "bm_lq": 3.688,
      "bm_mg": 2.145,
      "pop_2000": 12734
    }
  },
  "KÜTAHYA": {
    "ALTINTAS": {
      "bm_lq": 2.743,
      "bm_mg": 1.767,
      "pop_2000": 6375
    },
    "ASLANAPA": {
      "bm_lq": 3.156,
      "bm_mg": 2.117,
      "pop_2000": 2348
    },
    "CAVDARHISAR": {
      "bm_lq": 4.797,
      "bm_mg": 1.917,
      "pop_2000": 4687
    },
    "DOMANIC": {
      "bm_lq": 2.1,
      "bm_mg": 1.904,
      "pop_2000": 4673
    },
    "DUMLUPINAR": {
      "bm_lq": 3.192,
      "bm_mg": 2.075,
      "pop_2000": 3310
    },
    "EMET": {
      "bm_lq": 2.078,
      "bm_mg": 1.309,
      "pop_2000": 19350
    },
    "GEDIZ": {
      "bm_lq": 2.398,
      "bm_mg": 1.297,
      "pop_2000": 19375
    },
    "HISARCIK": {
      "bm_lq": 2.418,
      "bm_mg": 3.239,
      "pop_2000": 6321
    },
    "KUTAHYA MERKEZ": {
      "bm_lq": 2.092,
      "bm_mg": 2.142,
      "pop_2000": 166665
    },
    "PAZARLAR": {
      "bm_lq": 5.105,
      "bm_mg": 1.85,
      "pop_2000": 5455
    },
    "SAPHANE": {
      "bm_lq": 2.919,
      "bm_mg": 1.921,
      "pop_2000": 4671
    },
    "SIMAV": {
      "bm_lq": 2.529,
      "bm_mg": 2.093,
      "pop_2000": 28415
    },
    "TAVSANLI": {
      "bm_lq": 2.027,
      "bm_mg": 1.666,
      "pop_2000": 47224
    }
  },
  "MALATYA": {
    "AKCADAG": {
      "bm_lq": 6.184,
      "bm_mg": 1.854,
      "pop_2000": 13432
    },
    "ARAPKIR": {
      "bm_lq": 2.61,
      "bm_mg": 1.626,
      "pop_2000": 10180
    },
    "ARGUVAN": {
      "bm_lq": 2.152,
      "bm_mg": 2.099,
      "pop_2000": 2730
    },
    "BATTALGAZI": {
      "bm_lq": 4.625,
      "bm_mg": 1.652,
      "pop_2000": 15154
    },
    "DARENDE": {
      "bm_lq": 2.426,
      "bm_mg": 2.876,
      "pop_2000": 13908
    },
    "DOGANSEHIR": {
      "bm_lq": 3.44,
      "bm_mg": 2.919,
      "pop_2000": 13517
    },
    "DOGANYOL": {
      "bm_lq": 5.859,
      "bm_mg": 2.053,
      "pop_2000": 5360
    },
    "HEKIMHAN": {
      "bm_lq": 2.915,
      "bm_mg": 1.846,
      "pop_2000": 13206
    },
    "KALE": {
      "bm_lq": 7.457,
      "bm_mg": 2.44,
      "pop_2000": 3966
    },
    "KULUNCAK": {
      "bm_lq": 5.362,
      "bm_mg": 1.896,
      "pop_2000": 6101
    },
    "MALATYA MERKEZ": {
      "bm_lq": 2.24,
      "bm_mg": 2.664,
      "pop_2000": 381081
    },
    "POTURGE": {
      "bm_lq": 3.181,
      "bm_mg": 1.588,
      "pop_2000": 4795
    },
    "YAZIHAN": {
      "bm_lq": 4.737,
      "bm_mg": 2.119,
      "pop_2000": 4285
    },
    "YESILYURT": {
      "bm_lq": 2.402,
      "bm_mg": 2.649,
      "pop_2000": 11998
    }
  },
  "MANİSA": {
    "AHMETLI": {
      "bm_lq": 4.566,
      "bm_mg": 2.612,
      "pop_2000": 11011
    },
    "AKHISAR": {
      "bm_lq": 2.926,
      "bm_mg": 2.458,
      "pop_2000": 81510
    },
    "ALASEHIR": {
      "bm_lq": 3.126,
      "bm_mg": 2.514,
      "pop_2000": 39590
    },
    "DEMIRCI": {
      "bm_lq": 2.388,
      "bm_mg": 1.612,
      "pop_2000": 21230
    },
    "GOLMARMARA": {
      "bm_lq": 9.924,
      "bm_mg": 1.52,
      "pop_2000": 11205
    },
    "GORDES": {
      "bm_lq": 4.69,
      "bm_mg": 2.649,
      "pop_2000": 10809
    },
    "KIRKAGAC": {
      "bm_lq": 1.907,
      "bm_mg": 1.741,
      "pop_2000": 25093
    },
    "KOPRUBASI": {
      "bm_lq": 4.316,
      "bm_mg": 3.518,
      "pop_2000": 5049
    },
    "KULA": {
      "bm_lq": 2.473,
      "bm_mg": 1.864,
      "pop_2000": 24217
    },
    "MANISA MERKEZ": {
      "bm_lq": 2.257,
      "bm_mg": 2.851,
      "pop_2000": 214345
    },
    "SALIHLI": {
      "bm_lq": 2.537,
      "bm_mg": 2.268,
      "pop_2000": 83137
    },
    "SARIGOL": {
      "bm_lq": 6.845,
      "bm_mg": 2.176,
      "pop_2000": 12043
    },
    "SARUHANLI": {
      "bm_lq": 5.621,
      "bm_mg": 2.265,
      "pop_2000": 13025
    },
    "SELENDI": {
      "bm_lq": 2.906,
      "bm_mg": 1.742,
      "pop_2000": 8095
    },
    "SOMA": {
      "bm_lq": 1.988,
      "bm_mg": 1.994,
      "pop_2000": 60674
    },
    "TURGUTLU": {
      "bm_lq": 2.974,
      "bm_mg": 2.769,
      "pop_2000": 93727
    }
  },
  "KAHRAMANMARAŞ": {
    "AFSIN": {
      "bm_lq": 2.105,
      "bm_mg": 2.643,
      "pop_2000": 35834
    },
    "ANDIRIN": {
      "bm_lq": 2.445,
      "bm_mg": 2.934,
      "pop_2000": 8311
    },
    "CAGLAYANCERIT": {
      "bm_lq": 7.726,
      "bm_mg": 1.711,
      "pop_2000": 12642
    },
    "EKINOZU": {
      "bm_lq": 4.016,
      "bm_mg": 2.479,
      "pop_2000": 6880
    },
    "ELBISTAN": {
      "bm_lq": 2.423,
      "bm_mg": 1.939,
      "pop_2000": 71500
    },
    "GOKSUN": {
      "bm_lq": 2.686,
      "bm_mg": 2.595,
      "pop_2000": 30232
    },
    "KAHRAMANMARAS MERKEZ": {
      "bm_lq": 2.24,
      "bm_mg": 2.145,
      "pop_2000": 326198
    },
    "NURHAK": {
      "bm_lq": 3.529,
      "bm_mg": 2.464,
      "pop_2000": 8118
    },
    "PAZARCIK": {
      "bm_lq": 2.753,
      "bm_mg": 2.971,
      "pop_2000": 24374
    },
    "TURKOGLU": {
      "bm_lq": 3.599,
      "bm_mg": 2.513,
      "pop_2000": 11918
    }
  },
  "MARDİN": {
    "DARGECIT": {
      "bm_lq": 2.066,
      "bm_mg": 1.692,
      "pop_2000": 16541
    },
    "DERIK": {
      "bm_lq": 2.537,
      "bm_mg": 1.835,
      "pop_2000": 19806
    },
    "KIZILTEPE": {
      "bm_lq": 2.226,
      "bm_mg": 2.759,
      "pop_2000": 113143
    },
    "MARDIN MERKEZ": {
      "bm_lq": 1.948,
      "bm_mg": 2.199,
      "pop_2000": 65072
    },
    "MAZIDAGI": {
      "bm_lq": 2.043,
      "bm_mg": 1.838,
      "pop_2000": 11194
    },
    "MIDYAT": {
      "bm_lq": 2.117,
      "bm_mg": 1.55,
      "pop_2000": 56669
    },
    "NUSAYBIN": {
      "bm_lq": 2.139,
      "bm_mg": 1.848,
      "pop_2000": 74110
    },
    "OMERLI": {
      "bm_lq": 2.198,
      "bm_mg": 2.183,
      "pop_2000": 7197
    },
    "SAVUR": {
      "bm_lq": 2.295,
      "bm_mg": 2.743,
      "pop_2000": 7817
    },
    "YESILLI": {
      "bm_lq": 2.267,
      "bm_mg": 1.618,
      "pop_2000": 19700
    }
  },
  "MUĞLA": {
    "BODRUM": {
      "bm_lq": 1.836,
      "bm_mg": 2.234,
      "pop_2000": 32227
    },
    "DALAMAN": {
      "bm_lq": 2.388,
      "bm_mg": 1.393,
      "pop_2000": 17607
    },
    "DATCA": {
      "bm_lq": 2.206,
      "bm_mg": 4.725,
      "pop_2000": 8108
    },
    "FETHIYE": {
      "bm_lq": 2.195,
      "bm_mg": 1.996,
      "pop_2000": 50689
    },
    "KAVAKLIDERE": {
      "bm_lq": 2.545,
      "bm_mg": 1.704,
      "pop_2000": 3432
    },
    "KOYCEGIZ": {
      "bm_lq": 1.983,
      "bm_mg": 1.824,
      "pop_2000": 7523
    },
    "MARMARIS": {
      "bm_lq": 1.779,
      "bm_mg": 2.058,
      "pop_2000": 28660
    },
    "MILAS": {
      "bm_lq": 2.122,
      "bm_mg": 3.084,
      "pop_2000": 38063
    },
    "MUGLA MERKEZ": {
      "bm_lq": 1.961,
      "bm_mg": 1.606,
      "pop_2000": 43845
    },
    "ORTACA": {
      "bm_lq": 2.576,
      "bm_mg": 1.541,
      "pop_2000": 16923
    },
    "ULA": {
      "bm_lq": 2.244,
      "bm_mg": 1.748,
      "pop_2000": 5257
    },
    "YATAGAN": {
      "bm_lq": 2.158,
      "bm_mg": 1.31,
      "pop_2000": 16007
    }
  },
  "MUŞ": {
    "BULANIK": {
      "bm_lq": 8.524,
      "bm_mg": 1.98,
      "pop_2000": 24020
    },
    "HASKOY": {
      "bm_lq": 6.142,
      "bm_mg": 2.226,
      "pop_2000": 21342
    },
    "KORKUT": {
      "bm_lq": 3.429,
      "bm_mg": 2.042,
      "pop_2000": 6135
    },
    "MALAZGIRT": {
      "bm_lq": 2.059,
      "bm_mg": 2.219,
      "pop_2000": 23697
    },
    "MUS MERKEZ": {
      "bm_lq": 2.257,
      "bm_mg": 2.445,
      "pop_2000": 67927
    },
    "VARTO": {
      "bm_lq": 2.381,
      "bm_mg": 1.726,
      "pop_2000": 16382
    }
  },
  "NEVŞEHİR": {
    "ACIGOL": {
      "bm_lq": 3.429,
      "bm_mg": 3.164,
      "pop_2000": 6702
    },
    "AVANOS": {
      "bm_lq": 2.209,
      "bm_mg": 3.064,
      "pop_2000": 11921
    },
    "DERINKUYU": {
      "bm_lq": 4.202,
      "bm_mg": 1.248,
      "pop_2000": 11092
    },
    "GULSEHIR": {
      "bm_lq": 3.012,
      "bm_mg": 1.998,
      "pop_2000": 9377
    },
    "HACIBEKTAS": {
      "bm_lq": 2.344,
      "bm_mg": 1.533,
      "pop_2000": 7274
    },
    "KOZAKLI": {
      "bm_lq": 3.03,
      "bm_mg": 3.232,
      "pop_2000": 7755
    },
    "NEVSEHIR MERKEZ": {
      "bm_lq": 2.186,
      "bm_mg": 2.811,
      "pop_2000": 67864
    },
    "URGUP": {
      "bm_lq": 2.238,
      "bm_mg": 1.294,
      "pop_2000": 14538
    }
  },
  "NİĞDE": {
    "ALTUNHISAR": {
      "bm_lq": 4.927,
      "bm_mg": 1.636,
      "pop_2000": 3839
    },
    "BOR": {
      "bm_lq": 2.456,
      "bm_mg": 1.718,
      "pop_2000": 29804
    },
    "CAMARDI": {
      "bm_lq": 3.117,
      "bm_mg": 2.371,
      "pop_2000": 4086
    },
    "CIFTLIK": {
      "bm_lq": 5.151,
      "bm_mg": 2.173,
      "pop_2000": 4627
    },
    "NIGDE MERKEZ": {
      "bm_lq": 2.217,
      "bm_mg": 2.411,
      "pop_2000": 78088
    },
    "ULUKISLA": {
      "bm_lq": 2.446,
      "bm_mg": 1.546,
      "pop_2000": 6368
    }
  },
  "ORDU": {
    "AKKUS": {
      "bm_lq": 3.014,
      "bm_mg": 3.36,
      "pop_2000": 8768
    },
    "AYBASTI": {
      "bm_lq": 3.538,
      "bm_mg": 2.622,
      "pop_2000": 14326
    },
    "CAMAS": {
      "bm_lq": 6.056,
      "bm_mg": 1.648,
      "pop_2000": 10047
    },
    "CATALPINAR": {
      "bm_lq": 5.578,
      "bm_mg": 1.703,
      "pop_2000": 10265
    },
    "CAYBASI": {
      "bm_lq": 7.196,
      "bm_mg": 1.945,
      "pop_2000": 4810
    },
    "FATSA": {
      "bm_lq": 2.355,
      "bm_mg": 3.346,
      "pop_2000": 63721
    },
    "GOLKOY": {
      "bm_lq": 3.783,
      "bm_mg": 2.853,
      "pop_2000": 24162
    },
    "GULYALI": {
      "bm_lq": 3.377,
      "bm_mg": 2.079,
      "pop_2000": 5245
    },
    "GURGENTEPE": {
      "bm_lq": 7.994,
      "bm_mg": 1.901,
      "pop_2000": 18313
    },
    "IKIZCE": {
      "bm_lq": 8.77,
      "bm_mg": 1.908,
      "pop_2000": 10427
    },
    "KABADUZ": {
      "bm_lq": 2.617,
      "bm_mg": 2.688,
      "pop_2000": 4018
    },
    "KABATAS": {
      "bm_lq": 4.836,
      "bm_mg": 2.527,
      "pop_2000": 9211
    },
    "KORGAN": {
      "bm_lq": 4.048,
      "bm_mg": 1.778,
      "pop_2000": 15587
    },
    "KUMRU": {
      "bm_lq": 3.619,
      "bm_mg": 1.476,
      "pop_2000": 18057
    },
    "MESUDIYE": {
      "bm_lq": 2.24,
      "bm_mg": 1.962,
      "pop_2000": 5665
    },
    "ORDU MERKEZ": {
      "bm_lq": 2.194,
      "bm_mg": 3.022,
      "pop_2000": 112525
    },
    "PERSEMBE": {
      "bm_lq": 3.132,
      "bm_mg": 2.6,
      "pop_2000": 10804
    },
    "ULUBEY": {
      "bm_lq": 4.407,
      "bm_mg": 2.04,
      "pop_2000": 9128
    },
    "UNYE": {
      "bm_lq": 2.32,
      "bm_mg": 2.683,
      "pop_2000": 61552
    }
  },
  "RİZE": {
    "ARDESEN": {
      "bm_lq": 2.366,
      "bm_mg": 2.506,
      "pop_2000": 45392
    },
    "CAMLIHEMSIN": {
      "bm_lq": 2.087,
      "bm_mg": 2.325,
      "pop_2000": 2354
    },
    "CAYELI": {
      "bm_lq": 2.417,
      "bm_mg": 3.222,
      "pop_2000": 22546
    },
    "DEREPAZARI": {
      "bm_lq": 2.416,
      "bm_mg": 1.759,
      "pop_2000": 6172
    },
    "FINDIKLI": {
      "bm_lq": 3.027,
      "bm_mg": 1.622,
      "pop_2000": 11043
    },
    "GUNEYSU": {
      "bm_lq": 3.06,
      "bm_mg": 1.992,
      "pop_2000": 4914
    },
    "HEMSIN": {
      "bm_lq": 4.299,
      "bm_mg": 2.3,
      "pop_2000": 3262
    },
    "IKIZDERE": {
      "bm_lq": 2.362,
      "bm_mg": 2.53,
      "pop_2000": 2384
    },
    "IYIDERE": {
      "bm_lq": 4.745,
      "bm_mg": 1.529,
      "pop_2000": 5466
    },
    "KALKANDERE": {
      "bm_lq": 4.344,
      "bm_mg": 1.615,
      "pop_2000": 8886
    },
    "PAZAR": {
      "bm_lq": 2.811,
      "bm_mg": 1.987,
      "pop_2000": 14682
    },
    "RIZE MERKEZ": {
      "bm_lq": 2.2,
      "bm_mg": 4.176,
      "pop_2000": 78144
    }
  },
  "SAKARYA": {
    "AKYAZI": {
      "bm_lq": 2.202,
      "bm_mg": 1.719,
      "pop_2000": 23192
    },
    "FERIZLI": {
      "bm_lq": 2.556,
      "bm_mg": 3.914,
      "pop_2000": 12379
    },
    "GEYVE": {
      "bm_lq": 2.724,
      "bm_mg": 1.456,
      "pop_2000": 17318
    },
    "HENDEK": {
      "bm_lq": 2.276,
      "bm_mg": 2.622,
      "pop_2000": 28537
    },
    "KARAPURCEK": {
      "bm_lq": 2.856,
      "bm_mg": 1.692,
      "pop_2000": 4186
    },
    "KARASU": {
      "bm_lq": 2.447,
      "bm_mg": 1.565,
      "pop_2000": 24672
    },
    "KAYNARCA": {
      "bm_lq": 2.511,
      "bm_mg": 2.844,
      "pop_2000": 5064
    },
    "KOCAALI": {
      "bm_lq": 2.783,
      "bm_mg": 3.431,
      "pop_2000": 13793
    },
    "PAMUKOVA": {
      "bm_lq": 2.372,
      "bm_mg": 2.126,
      "pop_2000": 13200
    },
    "SAKARYA MERKEZ": {
      "bm_lq": 2.189,
      "bm_mg": 3.325,
      "pop_2000": 283752
    },
    "SAPANCA": {
      "bm_lq": 2.13,
      "bm_mg": 1.393,
      "pop_2000": 21727
    },
    "SOGUTLU": {
      "bm_lq": 6.59,
      "bm_mg": 1.597,
      "pop_2000": 7858
    },
    "TARAKLI": {
      "bm_lq": 2.935,
      "bm_mg": 2.351,
      "pop_2000": 4146
    }
  },
  "SAMSUN": {
    "19 MAYIS": {
      "bm_lq": 2.654,
      "bm_mg": 1.899,
      "pop_2000": 8928
    },
    "ALACAM": {
      "bm_lq": 4.023,
      "bm_mg": 2.52,
      "pop_2000": 11950
    },
    "ASARCIK": {
      "bm_lq": 2.249,
      "bm_mg": 2.078,
      "pop_2000": 1926
    },
    "AYVACIK": {
      "bm_lq": 4.935,
      "bm_mg": 1.578,
      "pop_2000": 5650
    },
    "BAFRA": {
      "bm_lq": 2.276,
      "bm_mg": 2.857,
      "pop_2000": 83733
    },
    "CARSAMBA": {
      "bm_lq": 2.207,
      "bm_mg": 1.794,
      "pop_2000": 49189
    },
    "HAVZA": {
      "bm_lq": 2.299,
      "bm_mg": 2.221,
      "pop_2000": 19385
    },
    "KAVAK": {
      "bm_lq": 2.301,
      "bm_mg": 1.593,
      "pop_2000": 7871
    },
    "LADIK": {
      "bm_lq": 2.275,
      "bm_mg": 1.618,
      "pop_2000": 9098
    },
    "SALIPAZARI": {
      "bm_lq": 4.405,
      "bm_mg": 2.254,
      "pop_2000": 6303
    },
    "SAMSUN MERKEZ": {
      "bm_lq": 2.09,
      "bm_mg": 2.796,
      "pop_2000": 363180
    },
    "TEKKEKOY": {
      "bm_lq": 2.323,
      "bm_mg": 2.787,
      "pop_2000": 15071
    },
    "TERME": {
      "bm_lq": 2.623,
      "bm_mg": 1.348,
      "pop_2000": 25052
    },
    "VEZIRKOPRU": {
      "bm_lq": 2.436,
      "bm_mg": 1.645,
      "pop_2000": 23211
    },
    "YAKAKENT": {
      "bm_lq": 4.398,
      "bm_mg": 2.601,
      "pop_2000": 4707
    }
  },
  "SİİRT": {
    "AYDINLAR": {
      "bm_lq": 1.929,
      "bm_mg": 2.114,
      "pop_2000": 2981
    },
    "BAYKAN": {
      "bm_lq": 1.814,
      "bm_mg": 1.598,
      "pop_2000": 8883
    },
    "ERUH": {
      "bm_lq": 1.506,
      "bm_mg": 1.679,
      "pop_2000": 7226
    },
    "KURTALAN": {
      "bm_lq": 2.301,
      "bm_mg": 1.871,
      "pop_2000": 24865
    },
    "PERVARI": {
      "bm_lq": 1.994,
      "bm_mg": 2.322,
      "pop_2000": 5737
    },
    "SIIRT MERKEZ": {
      "bm_lq": 1.862,
      "bm_mg": 2.252,
      "pop_2000": 98281
    },
    "SIRVAN": {
      "bm_lq": 2.066,
      "bm_mg": 2.118,
      "pop_2000": 5549
    }
  },
  "SİNOP": {
    "AYANCIK": {
      "bm_lq": 2.533,
      "bm_mg": 3.947,
      "pop_2000": 10919
    },
    "BOYABAT": {
      "bm_lq": 2.216,
      "bm_mg": 2.093,
      "pop_2000": 24681
    },
    "DIKMEN": {
      "bm_lq": 1.821,
      "bm_mg": 2.592,
      "pop_2000": 1402
    },
    "DURAGAN": {
      "bm_lq": 2.276,
      "bm_mg": 2.683,
      "pop_2000": 9725
    },
    "ERFELEK": {
      "bm_lq": 2.132,
      "bm_mg": 2.247,
      "pop_2000": 3659
    },
    "GERZE": {
      "bm_lq": 2.185,
      "bm_mg": 1.806,
      "pop_2000": 10013
    },
    "SARAYDUZU": {
      "bm_lq": 3.701,
      "bm_mg": 2.249,
      "pop_2000": 3407
    },
    "SINOP MERKEZ": {
      "bm_lq": 2.069,
      "bm_mg": 1.617,
      "pop_2000": 30502
    },
    "TURKELI": {
      "bm_lq": 2.272,
      "bm_mg": 1.615,
      "pop_2000": 6977
    }
  },
  "SİVAS": {
    "AKINCILAR": {
      "bm_lq": 5.595,
      "bm_mg": 1.705,
      "pop_2000": 4982
    },
    "ALTINYAYLA": {
      "bm_lq": 6.743,
      "bm_mg": 1.905,
      "pop_2000": 4867
    },
    "DIVRIGI": {
      "bm_lq": 2.238,
      "bm_mg": 1.688,
      "pop_2000": 14429
    },
    "DOGANSAR": {
      "bm_lq": 7.118,
      "bm_mg": 2.598,
      "pop_2000": 4004
    },
    "GEMEREK": {
      "bm_lq": 3.463,
      "bm_mg": 2.308,
      "pop_2000": 12589
    },
    "GOLOVA": {
      "bm_lq": 4.248,
      "bm_mg": 1.584,
      "pop_2000": 4120
    },
    "GURUN": {
      "bm_lq": 2.158,
      "bm_mg": 1.768,
      "pop_2000": 11294
    },
    "HAFIK": {
      "bm_lq": 2.057,
      "bm_mg": 1.799,
      "pop_2000": 5526
    },
    "IMRANLI": {
      "bm_lq": 2.119,
      "bm_mg": 1.697,
      "pop_2000": 7316
    },
    "KANGAL": {
      "bm_lq": 2.391,
      "bm_mg": 1.885,
      "pop_2000": 12099
    },
    "KOYULHISAR": {
      "bm_lq": 1.943,
      "bm_mg": 2.563,
      "pop_2000": 5706
    },
    "SARKISLA": {
      "bm_lq": 2.277,
      "bm_mg": 1.608,
      "pop_2000": 20654
    },
    "SIVAS MERKEZ": {
      "bm_lq": 2.123,
      "bm_mg": 4.848,
      "pop_2000": 251776
    },
    "SUSEHRI": {
      "bm_lq": 2.619,
      "bm_mg": 2.478,
      "pop_2000": 25137
    },
    "ULAS": {
      "bm_lq": 2.2,
      "bm_mg": 1.773,
      "pop_2000": 3390
    },
    "YILDIZELI": {
      "bm_lq": 3.973,
      "bm_mg": 2.261,
      "pop_2000": 16070
    },
    "ZARA": {
      "bm_lq": 2.442,
      "bm_mg": 3.798,
      "pop_2000": 17845
    }
  },
  "TEKİRDAĞ": {
    "CERKEZKOY": {
      "bm_lq": 2.013,
      "bm_mg": 2.09,
      "pop_2000": 41638
    },
    "CORLU": {
      "bm_lq": 2.123,
      "bm_mg": 2.551,
      "pop_2000": 141525
    },
    "HAYRABOLU": {
      "bm_lq": 2.483,
      "bm_mg": 1.967,
      "pop_2000": 18812
    },
    "MALKARA": {
      "bm_lq": 2.394,
      "bm_mg": 2.965,
      "pop_2000": 24898
    },
    "MARMARAEREGLISI": {
      "bm_lq": 2.334,
      "bm_mg": 1.432,
      "pop_2000": 8779
    },
    "MURATLI": {
      "bm_lq": 2.261,
      "bm_mg": 1.941,
      "pop_2000": 18571
    },
    "SARAY": {
      "bm_lq": 2.105,
      "bm_mg": 1.743,
      "pop_2000": 17769
    },
    "SARKOY": {
      "bm_lq": 2.623,
      "bm_mg": 1.922,
      "pop_2000": 16194
    },
    "TEKIRDAG MERKEZ": {
      "bm_lq": 2.194,
      "bm_mg": 3.822,
      "pop_2000": 107191
    }
  },
  "TOKAT": {
    "ALMUS": {
      "bm_lq": 2.205,
      "bm_mg": 1.767,
      "pop_2000": 6197
    },
    "ARTOVA": {
      "bm_lq": 1.998,
      "bm_mg": 2.196,
      "pop_2000": 5610
    },
    "BASCIFTLIK": {
      "bm_lq": 4.956,
      "bm_mg": 1.899,
      "pop_2000": 5971
    },
    "ERBAA": {
      "bm_lq": 2.434,
      "bm_mg": 1.501,
      "pop_2000": 45595
    },
    "NIKSAR": {
      "bm_lq": 2.518,
      "bm_mg": 2.956,
      "pop_2000": 44808
    },
    "PAZAR": {
      "bm_lq": 4.08,
      "bm_mg": 1.586,
      "pop_2000": 5301
    },
    "RESADIYE": {
      "bm_lq": 2.374,
      "bm_mg": 2.054,
      "pop_2000": 16389
    },
    "SULUSARAY": {
      "bm_lq": 5.126,
      "bm_mg": 1.641,
      "pop_2000": 4160
    },
    "TOKAT MERKEZ": {
      "bm_lq": 2.197,
      "bm_mg": 2.804,
      "pop_2000": 113100
    },
    "TURHAL": {
      "bm_lq": 2.512,
      "bm_mg": 2.797,
      "pop_2000": 95536
    },
    "YESILYURT": {
      "bm_lq": 2.676,
      "bm_mg": 2.212,
      "pop_2000": 6455
    },
    "ZILE": {
      "bm_lq": 3.259,
      "bm_mg": 2.491,
      "pop_2000": 52640
    }
  },
  "TRABZON": {
    "AKCAABAT": {
      "bm_lq": 2.366,
      "bm_mg": 2.12,
      "pop_2000": 39102
    },
    "ARAKLI": {
      "bm_lq": 2.259,
      "bm_mg": 1.657,
      "pop_2000": 22506
    },
    "ARSIN": {
      "bm_lq": 2.318,
      "bm_mg": 2.91,
      "pop_2000": 13038
    },
    "BESIKDUZU": {
      "bm_lq": 2.609,
      "bm_mg": 2.156,
      "pop_2000": 29766
    },
    "CARSIBASI": {
      "bm_lq": 2.988,
      "bm_mg": 1.532,
      "pop_2000": 8532
    },
    "CAYKARA": {
      "bm_lq": 2.963,
      "bm_mg": 2.044,
      "pop_2000": 5829
    },
    "DERNEKPAZARI": {
      "bm_lq": 2.867,
      "bm_mg": 3.341,
      "pop_2000": 5108
    },
    "DUZKOY": {
      "bm_lq": 2.797,
      "bm_mg": 2.491,
      "pop_2000": 6863
    },
    "HAYRAT": {
      "bm_lq": 4.164,
      "bm_mg": 2.066,
      "pop_2000": 7665
    },
    "KOPRUBASI": {
      "bm_lq": 2.858,
      "bm_mg": 1.892,
      "pop_2000": 4998
    },
    "MACKA": {
      "bm_lq": 2.066,
      "bm_mg": 1.689,
      "pop_2000": 11060
    },
    "OF": {
      "bm_lq": 2.503,
      "bm_mg": 2.227,
      "pop_2000": 25478
    },
    "SALPAZARI": {
      "bm_lq": 3.047,
      "bm_mg": 2.274,
      "pop_2000": 7591
    },
    "SURMENE": {
      "bm_lq": 2.771,
      "bm_mg": 2.337,
      "pop_2000": 17063
    },
    "TONYA": {
      "bm_lq": 9.006,
      "bm_mg": 2.488,
      "pop_2000": 12666
    },
    "TRABZON MERKEZ": {
      "bm_lq": 2.033,
      "bm_mg": 2.626,
      "pop_2000": 214949
    },
    "VAKFIKEBIR": {
      "bm_lq": 2.187,
      "bm_mg": 1.611,
      "pop_2000": 33394
    },
    "YOMRA": {
      "bm_lq": 2.684,
      "bm_mg": 1.903,
      "pop_2000": 13346
    }
  },
  "TUNCELİ": {
    "CEMISGEZEK": {
      "bm_lq": 1.901,
      "bm_mg": 2.079,
      "pop_2000": 3685
    },
    "HOZAT": {
      "bm_lq": 1.349,
      "bm_mg": 1.247,
      "pop_2000": 6589
    },
    "MAZGIRT": {
      "bm_lq": 1.637,
      "bm_mg": 2.085,
      "pop_2000": 2707
    },
    "NAZIMIYE": {
      "bm_lq": 1.364,
      "bm_mg": 1.679,
      "pop_2000": 2915
    },
    "OVACIK": {
      "bm_lq": 1.407,
      "bm_mg": 1.491,
      "pop_2000": 5909
    },
    "PERTEK": {
      "bm_lq": 2.687,
      "bm_mg": 2.379,
      "pop_2000": 5737
    },
    "PULUMUR": {
      "bm_lq": 1.679,
      "bm_mg": 1.777,
      "pop_2000": 1893
    },
    "TUNCELI MERKEZ": {
      "bm_lq": 1.567,
      "bm_mg": 1.948,
      "pop_2000": 25041
    }
  },
  "ŞANLIURFA": {
    "AKCAKALE": {
      "bm_lq": 3.173,
      "bm_mg": 1.583,
      "pop_2000": 32114
    },
    "BIRECIK": {
      "bm_lq": 2.501,
      "bm_mg": 2.507,
      "pop_2000": 40054
    },
    "BOZOVA": {
      "bm_lq": 2.596,
      "bm_mg": 2.338,
      "pop_2000": 19848
    },
    "CEYLANPINAR": {
      "bm_lq": 2.124,
      "bm_mg": 2.181,
      "pop_2000": 44258
    },
    "HALFETI": {
      "bm_lq": 2.223,
      "bm_mg": 2.252,
      "pop_2000": 2766
    },
    "HARRAN": {
      "bm_lq": 3.667,
      "bm_mg": 1.411,
      "pop_2000": 8784
    },
    "HILVAN": {
      "bm_lq": 7.31,
      "bm_mg": 1.411,
      "pop_2000": 16094
    },
    "SANLIURFA MERKEZ": {
      "bm_lq": 2.394,
      "bm_mg": 4.628,
      "pop_2000": 385588
    },
    "SIVEREK": {
      "bm_lq": 3.33,
      "bm_mg": 2.035,
      "pop_2000": 126820
    },
    "SURUC": {
      "bm_lq": 3.285,
      "bm_mg": 2.143,
      "pop_2000": 44421
    },
    "VIRANSEHIR": {
      "bm_lq": 2.904,
      "bm_mg": 2.14,
      "pop_2000": 121382
    }
  },
  "UŞAK": {
    "BANAZ": {
      "bm_lq": 2.327,
      "bm_mg": 2.054,
      "pop_2000": 16212
    },
    "ESME": {
      "bm_lq": 2.419,
      "bm_mg": 1.994,
      "pop_2000": 11615
    },
    "KARAHALLI": {
      "bm_lq": 2.102,
      "bm_mg": 1.708,
      "pop_2000": 5243
    },
    "SIVASLI": {
      "bm_lq": 2.523,
      "bm_mg": 1.894,
      "pop_2000": 6837
    },
    "ULUBEY": {
      "bm_lq": 2.841,
      "bm_mg": 2.671,
      "pop_2000": 5132
    },
    "USAK MERKEZ": {
      "bm_lq": 2.103,
      "bm_mg": 3.397,
      "pop_2000": 137001
    }
  },
  "VAN": {
    "BAHCESARAY": {
      "bm_lq": 3.119,
      "bm_mg": 1.839,
      "pop_2000": 3524
    },
    "BASKALE": {
      "bm_lq": 1.479,
      "bm_mg": 1.607,
      "pop_2000": 14114
    },
    "CALDIRAN": {
      "bm_lq": 1.969,
      "bm_mg": 1.532,
      "pop_2000": 12841
    },
    "CATAK": {
      "bm_lq": 1.668,
      "bm_mg": 1.692,
      "pop_2000": 5892
    },
    "EDREMIT": {
      "bm_lq": 2.412,
      "bm_mg": 1.953,
      "pop_2000": 6481
    },
    "ERCIS": {
      "bm_lq": 2.134,
      "bm_mg": 2.709,
      "pop_2000": 70881
    },
    "GEVAS": {
      "bm_lq": 1.98,
      "bm_mg": 1.923,
      "pop_2000": 10988
    },
    "GURPINAR": {
      "bm_lq": 1.49,
      "bm_mg": 1.504,
      "pop_2000": 6211
    },
    "MURADIYE": {
      "bm_lq": 2.95,
      "bm_mg": 2.1,
      "pop_2000": 19702
    },
    "OZALP": {
      "bm_lq": 1.704,
      "bm_mg": 1.946,
      "pop_2000": 6997
    },
    "SARAY": {
      "bm_lq": 1.575,
      "bm_mg": 1.773,
      "pop_2000": 4881
    },
    "VAN MERKEZ": {
      "bm_lq": 1.995,
      "bm_mg": 2.069,
      "pop_2000": 284464
    }
  },
  "YOZGAT": {
    "AKDAGMADENI": {
      "bm_lq": 2.461,
      "bm_mg": 2.219,
      "pop_2000": 20312
    },
    "AYDINCIK": {
      "bm_lq": 3.158,
      "bm_mg": 1.839,
      "pop_2000": 6437
    },
    "BOGAZLIYAN": {
      "bm_lq": 7.152,
      "bm_mg": 1.811,
      "pop_2000": 29719
    },
    "CANDIR": {
      "bm_lq": 9.81,
      "bm_mg": 2.11,
      "pop_2000": 13449
    },
    "CAYIRALAN": {
      "bm_lq": 3.288,
      "bm_mg": 2.249,
      "pop_2000": 14046
    },
    "CEKEREK": {
      "bm_lq": 2.33,
      "bm_mg": 1.762,
      "pop_2000": 12339
    },
    "KADISEHRI": {
      "bm_lq": 3.49,
      "bm_mg": 2.103,
      "pop_2000": 5200
    },
    "SARAYKENT": {
      "bm_lq": 3.51,
      "bm_mg": 2.254,
      "pop_2000": 9224
    },
    "SARIKAYA": {
      "bm_lq": 3.039,
      "bm_mg": 3.147,
      "pop_2000": 22102
    },
    "SEFAATLI": {
      "bm_lq": 3.622,
      "bm_mg": 1.987,
      "pop_2000": 13728
    },
    "SORGUN": {
      "bm_lq": 2.423,
      "bm_mg": 2.194,
      "pop_2000": 53884
    },
    "YENIFAKILI": {
      "bm_lq": 13.999,
      "bm_mg": 1.922,
      "pop_2000": 8558
    },
    "YERKOY": {
      "bm_lq": 2.695,
      "bm_mg": 1.847,
      "pop_2000": 32228
    },
    "YOZGAT MERKEZ": {
      "bm_lq": 2.156,
      "bm_mg": 2.234,
      "pop_2000": 73930
    }
  },
  "ZONGULDAK": {
    "ALAPLI": {
      "bm_lq": 2.121,
      "bm_mg": 1.678,
      "pop_2000": 18487
    },
    "CAYCUMA": {
      "bm_lq": 2.113,
      "bm_mg": 1.705,
      "pop_2000": 18734
    },
    "DEVREK": {
      "bm_lq": 2.057,
      "bm_mg": 2.34,
      "pop_2000": 21360
    },
    "EREGLI": {
      "bm_lq": 2.126,
      "bm_mg": 2.475,
      "pop_2000": 79486
    },
    "GOKCEBEY": {
      "bm_lq": 2.186,
      "bm_mg": 2.476,
      "pop_2000": 7939
    },
    "ZONGULDAK MERKEZ": {
      "bm_lq": 1.896,
      "bm_mg": 2.691,
      "pop_2000": 104276
    }
  },
  "AKSARAY": {
    "AGACOREN": {
      "bm_lq": 3.08,
      "bm_mg": 2.278,
      "pop_2000": 4983
    },
    "AKSARAY MERKEZ": {
      "bm_lq": 2.243,
      "bm_mg": 2.366,
      "pop_2000": 129949
    },
    "ESKIL": {
      "bm_lq": 2.885,
      "bm_mg": 1.229,
      "pop_2000": 22125
    },
    "GULAGAC": {
      "bm_lq": 3.164,
      "bm_mg": 1.982,
      "pop_2000": 4672
    },
    "GUZELYURT": {
      "bm_lq": 2.135,
      "bm_mg": 1.887,
      "pop_2000": 3775
    },
    "ORTAKOY": {
      "bm_lq": 2.779,
      "bm_mg": 1.781,
      "pop_2000": 26961
    },
    "SARIYAHSI": {
      "bm_lq": 4.97,
      "bm_mg": 2.985,
      "pop_2000": 7751
    }
  },
  "BAYBURT": {
    "AYDINTEPE": {
      "bm_lq": 2.843,
      "bm_mg": 2.214,
      "pop_2000": 7010
    },
    "BAYBURT MERKEZ": {
      "bm_lq": 2.014,
      "bm_mg": 2.826,
      "pop_2000": 32285
    },
    "DEMIROZU": {
      "bm_lq": 2.727,
      "bm_mg": 2.024,
      "pop_2000": 2061
    }
  },
  "KARAMAN": {
    "AYRANCI": {
      "bm_lq": 3.691,
      "bm_mg": 2.077,
      "pop_2000": 3153
    },
    "BASYAYLA": {
      "bm_lq": 6.22,
      "bm_mg": 1.683,
      "pop_2000": 5514
    },
    "ERMENEK": {
      "bm_lq": 2.233,
      "bm_mg": 1.491,
      "pop_2000": 15509
    },
    "KARAMAN MERKEZ": {
      "bm_lq": 2.402,
      "bm_mg": 2.205,
      "pop_2000": 105384
    },
    "KAZIMKARABEKIR": {
      "bm_lq": 6.036,
      "bm_mg": 2.281,
      "pop_2000": 3634
    },
    "SARIVELILER": {
      "bm_lq": 7.546,
      "bm_mg": 2.509,
      "pop_2000": 6718
    }
  },
  "KIRIKKALE": {
    "BAHSILI": {
      "bm_lq": 2.417,
      "bm_mg": 2.45,
      "pop_2000": 5790
    },
    "BALISEYH": {
      "bm_lq": 2.21,
      "bm_mg": 2.066,
      "pop_2000": 3344
    },
    "CELEBI": {
      "bm_lq": 3.256,
      "bm_mg": 3.451,
      "pop_2000": 3333
    },
    "DELICE": {
      "bm_lq": 2.772,
      "bm_mg": 1.819,
      "pop_2000": 10512
    },
    "KARAKECILI": {
      "bm_lq": 4.669,
      "bm_mg": 3.855,
      "pop_2000": 7851
    },
    "KESKIN": {
      "bm_lq": 3.619,
      "bm_mg": 1.584,
      "pop_2000": 34827
    },
    "KIRIKKALE MERKEZ": {
      "bm_lq": 2.148,
      "bm_mg": 3.556,
      "pop_2000": 205078
    },
    "SULAKYURT": {
      "bm_lq": 4.775,
      "bm_mg": 1.909,
      "pop_2000": 6344
    },
    "YAHSIHAN": {
      "bm_lq": 1.996,
      "bm_mg": 2.146,
      "pop_2000": 8215
    }
  },
  "BATMAN": {
    "BATMAN MERKEZ": {
      "bm_lq": 2.385,
      "bm_mg": 2.277,
      "pop_2000": 246678
    },
    "BESIRI": {
      "bm_lq": 2.364,
      "bm_mg": 1.683,
      "pop_2000": 8554
    },
    "GERCUS": {
      "bm_lq": 1.933,
      "bm_mg": 2.134,
      "pop_2000": 8451
    },
    "HASANKEYF": {
      "bm_lq": 2.033,
      "bm_mg": 2.04,
      "pop_2000": 3669
    },
    "KOZLUK": {
      "bm_lq": 3.144,
      "bm_mg": 2.026,
      "pop_2000": 27109
    },
    "SASON": {
      "bm_lq": 2.735,
      "bm_mg": 1.777,
      "pop_2000": 9705
    }
  },
  "ŞIRNAK": {
    "BEYTUSSEBAP": {
      "bm_lq": 1.32,
      "bm_mg": 1.529,
      "pop_2000": 6633
    },
    "CIZRE": {
      "bm_lq": 1.867,
      "bm_mg": 2.468,
      "pop_2000": 69591
    },
    "GUCLUKONAK": {
      "bm_lq": 1.558,
      "bm_mg": 1.655,
      "pop_2000": 4111
    },
    "IDIL": {
      "bm_lq": 1.912,
      "bm_mg": 1.717,
      "pop_2000": 19123
    },
    "SILOPI": {
      "bm_lq": 1.781,
      "bm_mg": 2.659,
      "pop_2000": 51199
    },
    "SIRNAK MERKEZ": {
      "bm_lq": 1.549,
      "bm_mg": 2.027,
      "pop_2000": 52743
    },
    "ULUDERE": {
      "bm_lq": 1.634,
      "bm_mg": 1.905,
      "pop_2000": 7928
    }
  },
  "BARTIN": {
    "AMASRA": {
      "bm_lq": 1.775,
      "bm_mg": 1.53,
      "pop_2000": 6338
    },
    "BARTIN MERKEZ": {
      "bm_lq": 2.1,
      "bm_mg": 2.929,
      "pop_2000": 35992
    },
    "KURUCASILE": {
      "bm_lq": 2.188,
      "bm_mg": 1.97,
      "pop_2000": 2074
    },
    "ULUS": {
      "bm_lq": 2.146,
      "bm_mg": 1.767,
      "pop_2000": 3598
    }
  },
  "ARDAHAN": {
    "ARDAHAN MERKEZ": {
      "bm_lq": 1.854,
      "bm_mg": 2.125,
      "pop_2000": 17274
    },
    "CILDIR": {
      "bm_lq": 1.689,
      "bm_mg": 2.452,
      "pop_2000": 2415
    },
    "DAMAL": {
      "bm_lq": 2.068,
      "bm_mg": 1.615,
      "pop_2000": 2571
    },
    "GOLE": {
      "bm_lq": 1.675,
      "bm_mg": 1.432,
      "pop_2000": 10478
    },
    "HANAK": {
      "bm_lq": 5.521,
      "bm_mg": 1.84,
      "pop_2000": 4432
    },
    "POSOF": {
      "bm_lq": 1.825,
      "bm_mg": 2.376,
      "pop_2000": 2555
    }
  },
  "IĞDIR": {
    "ARALIK": {
      "bm_lq": 2.065,
      "bm_mg": 1.921,
      "pop_2000": 8115
    },
    "IGDIR MERKEZ": {
      "bm_lq": 2.101,
      "bm_mg": 1.846,
      "pop_2000": 59880
    },
    "KARAKOYUNLU": {
      "bm_lq": 5.193,
      "bm_mg": 1.844,
      "pop_2000": 4760
    },
    "TUZLUCA": {
      "bm_lq": 2.671,
      "bm_mg": 3.507,
      "pop_2000": 8827
    }
  },
  "YALOVA": {
    "ALTINOVA": {
      "bm_lq": 2.388,
      "bm_mg": 2.3,
      "pop_2000": 3231
    },
    "ARMUTLU": {
      "bm_lq": 2.376,
      "bm_mg": 1.912,
      "pop_2000": 4221
    },
    "CIFTLIKKOY": {
      "bm_lq": 2.219,
      "bm_mg": 2.823,
      "pop_2000": 9622
    },
    "CINARCIK": {
      "bm_lq": 2.052,
      "bm_mg": 1.899,
      "pop_2000": 8953
    },
    "TERMAL": {
      "bm_lq": 2.07,
      "bm_mg": 2.024,
      "pop_2000": 2516
    },
    "YALOVA MERKEZ": {
      "bm_lq": 2.182,
      "bm_mg": 2.786,
      "pop_2000": 70118
    }
  },
  "KARABÜK": {
    "EFLANI": {
      "bm_lq": 2.936,
      "bm_mg": 2.105,
      "pop_2000": 3897
    },
    "ESKIPAZAR": {
      "bm_lq": 2.357,
      "bm_mg": 2.457,
      "pop_2000": 8457
    },
    "KARABUK MERKEZ": {
      "bm_lq": 2.101,
      "bm_mg": 2.033,
      "pop_2000": 100749
    },
    "OVACIK": {
      "bm_lq": 2.256,
      "bm_mg": 2.403,
      "pop_2000": 1728
    },
    "SAFRANBOLU": {
      "bm_lq": 2.112,
      "bm_mg": 2.123,
      "pop_2000": 31697
    },
    "YENICE": {
      "bm_lq": 2.405,
      "bm_mg": 2.187,
      "pop_2000": 11228
    }
  },
  "KİLİS": {
    "ELBEYLI": {
      "bm_lq": 2.544,
      "bm_mg": 2.249,
      "pop_2000": 2077
    },
    "KILIS MERKEZ": {
      "bm_lq": 2.38,
      "bm_mg": 3.079,
      "pop_2000": 70670
    },
    "MUSABEYLI": {
      "bm_lq": 3.283,
      "bm_mg": 2.988,
      "pop_2000": 1555
    },
    "POLATELI": {
      "bm_lq": 3.075,
      "bm_mg": 2.592,
      "pop_2000": 683000
    }
  },
  "OSMANİYE": {
    "BAHCE": {
      "bm_lq": 2.285,
      "bm_mg": 1.608,
      "pop_2000": 18411
    },
    "DUZICI": {
      "bm_lq": 2.53,
      "bm_mg": 1.555,
      "pop_2000": 39097
    },
    "HASANBEYLI": {
      "bm_lq": 2.488,
      "bm_mg": 3.792,
      "pop_2000": 4766
    },
    "KADIRLI": {
      "bm_lq": 2.619,
      "bm_mg": 2.646,
      "pop_2000": 65227
    },
    "OSMANIYE MERKEZ": {
      "bm_lq": 2.308,
      "bm_mg": 2.649,
      "pop_2000": 173977
    },
    "SUMBAS": {
      "bm_lq": 5.25,
      "bm_mg": 2.191,
      "pop_2000": 2103
    },
    "TOPRAKKALE": {
      "bm_lq": 2.472,
      "bm_mg": 1.942,
      "pop_2000": 8413
    }
  },
  "DÜZCE": {
    "AKCAKOCA": {
      "bm_lq": 2.414,
      "bm_mg": 2.517,
      "pop_2000": 25560
    },
    "CILIMLI": {
      "bm_lq": 3.239,
      "bm_mg": 3.1,
      "pop_2000": 7147
    },
    "CUMAYERI": {
      "bm_lq": 2.454,
      "bm_mg": 1.633,
      "pop_2000": 7434
    },
    "DUZCE MERKEZ": {
      "bm_lq": 2.228,
      "bm_mg": 2.171,
      "pop_2000": 56649
    },
    "GOLYAKA": {
      "bm_lq": 2.687,
      "bm_mg": 2.215,
      "pop_2000": 8572
    },
    "GUMUSOVA": {
      "bm_lq": 2.414,
      "bm_mg": 2.283,
      "pop_2000": 12103
    },
    "KAYNASLI": {
      "bm_lq": 2.108,
      "bm_mg": 1.929,
      "pop_2000": 9439
    },
    "YIGILCA": {
      "bm_lq": 2.711,
      "bm_mg": 2.295,
      "pop_2000": 3728
    }
  }
}


def _norm_tr(s: str) -> str:
    if not s:
        return ""
    s = s.strip().upper()
    for tr, en in [("İ", "I"), ("I", "I"), ("Ğ", "G"), ("Ü", "U"), ("Ş", "S"), ("Ö", "O"), ("Ç", "C")]:
        s = s.replace(tr, en)
    return s


def get_all_provinces() -> List[str]:
    """Tum illerin alfabetik listesini doner."""
    return sorted(list(DISTRICT_BASE_MULTIPLIERS.keys()))


def get_districts_by_province(province: str) -> List[str]:
    """Belirtilen ile ait ilcelerin listesini doner."""
    p_norm = _norm_tr(province)
    for pk, dists in DISTRICT_BASE_MULTIPLIERS.items():
        if _norm_tr(pk) == p_norm:
            return sorted(list(dists.keys()))
    return []


def get_district_info(province: str, district: str) -> Optional[Dict[str, Any]]:
    """Belirtilen il ve ilcenin LQ, MG ve nufus bilgilerini doner."""
    p_norm = _norm_tr(province)
    d_norm = _norm_tr(district)

    for pk, dists in DISTRICT_BASE_MULTIPLIERS.items():
        if _norm_tr(pk) == p_norm:
            for dk, info in dists.items():
                if _norm_tr(dk) == d_norm:
                    return info
            return None
    return None


def parse_custom_multiplier_file(filepath: str) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """
    Kullanicinin yukleyecegi yeni bir carpan dosyasini (.xls, .xlsx veya .csv) okur.
    Hocanin 'Yenisi hesaplaninca modellerine entegre ederler' gereksinimi icin.
    """
    res = {}
    if filepath.lower().endswith(".csv"):
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            header = [c.strip().upper() for c in next(reader, [])]
            il_idx = next((i for i, c in enumerate(header) if "IL" in c and "ILCE" not in c), 1)
            ilce_idx = next((i for i, c in enumerate(header) if "ILCE" in c), 2)
            lq_idx = next((i for i, c in enumerate(header) if "LQ" in c), 4)
            mg_idx = next((i for i, c in enumerate(header) if "MG" in c), 5)
            pop_idx = next((i for i, c in enumerate(header) if any(k in c for k in ["POP", "NUFUS"])), 6)

            for row in reader:
                if len(row) <= max(il_idx, ilce_idx): continue
                il = row[il_idx].strip().upper()
                ilce = row[ilce_idx].strip().upper()
                try:
                    lq = round(float(row[lq_idx].replace(",", ".")), 3) if len(row) > lq_idx else 2.5
                except Exception:
                    lq = 2.5
                try:
                    mg = round(float(row[mg_idx].replace(",", ".")), 3) if len(row) > mg_idx else 2.0
                except Exception:
                    mg = 2.0
                try:
                    pop = int(float(row[pop_idx].replace(",", "."))) if len(row) > pop_idx else 0
                except Exception:
                    pop = 0
                if il not in res: res[il] = {}
                res[il][ilce] = {"bm_lq": lq, "bm_mg": mg, "pop_2000": pop}
    return res
