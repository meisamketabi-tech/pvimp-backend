/* AUTO-GENERATED FROM WORKBOOK - DO NOT EDIT MANUALLY */
export type VaccinationKpiRow = {
  county: string;
  annualTarget: number | null;
  periodTarget: number | null;
  actual: number | null;
  annualAchievement: number | null;
  periodAchievement: number | null;
};

export type VaccinationKpiIndicator = {
  id: string;
  categoryId: string;
  categoryLabel: string;
  sheet: string;
  title: string;
  indicator: string;
  livestockGroup: string;
  sourcePeriodMonths: number;
  sourceAsOf: string;
  rows: readonly VaccinationKpiRow[];
};

export type VaccinationKpiCategory = {
  id: string;
  title: string;
  description: string;
};

export const vaccinationKpiSource = {
  "sourceWorkbook": "عملکرد واکسيناسيون، پايش و مراقبت استان و شهرستان.xlsx",
  "generatedAt": "2026-08-15T16:54:54.318628",
  "sourcePeriodMonths": 4,
  "sourceAsOf": "1405/05/01",
  "categories": [
    {
      "id": "infectious",
      "title": "الف- عملکرد مبارزه با بیماری‌های واگیر",
      "description": "واکسن‌های بیماری‌های واگیر مطابق ساختار شیت‌های منبع"
    },
    {
      "id": "zoonotic",
      "title": "ب- عملکرد مبارزه با بیماری‌های مشترک",
      "description": "واکسیناسیون بیماری‌های مشترک مطابق ساختار شیت‌های منبع"
    },
    {
      "id": "surveillance",
      "title": "ج- عملکرد پایش و مراقبت بیماری‌های مشترک",
      "description": "پایش، مراقبت، خونگیری و آزمون‌های بیماری‌های مشترک"
    }
  ],
  "indicators": [
    {
      "id": "آبله-عملکرد-واکسیناسیون-آبله-گوسفندی-شهرستان",
      "categoryId": "infectious",
      "categoryLabel": "الف- عملکرد مبارزه با بیماری‌های واگیر",
      "sheet": "آبله",
      "title": "عملکرد واکسیناسیون آبله گوسفندی شهرستان",
      "indicator": "آبله گوسفندی",
      "livestockGroup": "دام سبک",
      "sourcePeriodMonths": 4,
      "sourceAsOf": "1405/05/01",
      "rows": [
        {
          "county": "ابهر",
          "annualTarget": 106176.0,
          "periodTarget": 95176.0,
          "actual": 80060.0,
          "annualAchievement": 75.4,
          "periodAchievement": 84.12
        },
        {
          "county": "ایجرود",
          "annualTarget": 70400.0,
          "periodTarget": 70400.0,
          "actual": 72180.0,
          "annualAchievement": 102.53,
          "periodAchievement": 102.53
        },
        {
          "county": "خدابنده",
          "annualTarget": 196384.0,
          "periodTarget": 196384.0,
          "actual": 211649.0,
          "annualAchievement": 107.77,
          "periodAchievement": 107.77
        },
        {
          "county": "خرمدره",
          "annualTarget": 17380.0,
          "periodTarget": 17380.0,
          "actual": 21811.0,
          "annualAchievement": 125.49,
          "periodAchievement": 125.49
        },
        {
          "county": "زنجان",
          "annualTarget": 235419.0,
          "periodTarget": 235419.0,
          "actual": 103422.0,
          "annualAchievement": 43.93,
          "periodAchievement": 43.93
        },
        {
          "county": "سلطانیه",
          "annualTarget": 66870.0,
          "periodTarget": 55324.0,
          "actual": 46813.0,
          "annualAchievement": 70.01,
          "periodAchievement": 84.62
        },
        {
          "county": "طارم",
          "annualTarget": 55226.0,
          "periodTarget": 12826.0,
          "actual": 58036.0,
          "annualAchievement": 105.09,
          "periodAchievement": 452.49
        },
        {
          "county": "ماهنشان",
          "annualTarget": 130808.0,
          "periodTarget": 90539.0,
          "actual": 72282.0,
          "annualAchievement": 55.26,
          "periodAchievement": 79.84
        }
      ]
    },
    {
      "id": "آبله-عملکرد-واکسیناسیون-آبله-بزی-شهرستان",
      "categoryId": "infectious",
      "categoryLabel": "الف- عملکرد مبارزه با بیماری‌های واگیر",
      "sheet": "آبله",
      "title": "عملکرد واکسیناسیون آبله بزی شهرستان",
      "indicator": "آبله بزی",
      "livestockGroup": "دام سبک",
      "sourcePeriodMonths": 4,
      "sourceAsOf": "1405/05/01",
      "rows": [
        {
          "county": "ابهر",
          "annualTarget": 10920.0,
          "periodTarget": 10920.0,
          "actual": 6092.0,
          "annualAchievement": 55.79,
          "periodAchievement": 55.79
        },
        {
          "county": "ایجرود",
          "annualTarget": 1480.0,
          "periodTarget": 1480.0,
          "actual": 1110.0,
          "annualAchievement": 75.0,
          "periodAchievement": 75.0
        },
        {
          "county": "خدابنده",
          "annualTarget": 6646.0,
          "periodTarget": 6646.0,
          "actual": 6755.0,
          "annualAchievement": 101.64,
          "periodAchievement": 101.64
        },
        {
          "county": "خرمدره",
          "annualTarget": 969.0,
          "periodTarget": 969.0,
          "actual": 685.0,
          "annualAchievement": 70.69,
          "periodAchievement": 70.69
        },
        {
          "county": "زنجان",
          "annualTarget": 40373.0,
          "periodTarget": 40373.0,
          "actual": 12034.0,
          "annualAchievement": 29.81,
          "periodAchievement": 29.81
        },
        {
          "county": "سلطانیه",
          "annualTarget": 4492.0,
          "periodTarget": 3600.0,
          "actual": 2115.0,
          "annualAchievement": 47.08,
          "periodAchievement": 58.75
        },
        {
          "county": "طارم",
          "annualTarget": 14354.0,
          "periodTarget": 2734.0,
          "actual": 9665.0,
          "annualAchievement": 67.33,
          "periodAchievement": 353.51
        },
        {
          "county": "ماهنشان",
          "annualTarget": 19968.0,
          "periodTarget": 13318.0,
          "actual": 10514.0,
          "annualAchievement": 52.65,
          "periodAchievement": 78.95
        }
      ]
    },
    {
      "id": "آبله-عملکرد-واکسیناسیون-آبله-بزی-وارداتی-شهرستان",
      "categoryId": "infectious",
      "categoryLabel": "الف- عملکرد مبارزه با بیماری‌های واگیر",
      "sheet": "آبله",
      "title": "عملکرد واکسیناسیون آبله بزی(وارداتی) شهرستان",
      "indicator": "آبله بزی(وارداتی)",
      "livestockGroup": "دام سبک",
      "sourcePeriodMonths": 4,
      "sourceAsOf": "1405/05/01",
      "rows": [
        {
          "county": "ابهر",
          "annualTarget": 0.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": null,
          "periodAchievement": null
        },
        {
          "county": "ایجرود",
          "annualTarget": 0.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": null,
          "periodAchievement": null
        },
        {
          "county": "خدابنده",
          "annualTarget": 50.0,
          "periodTarget": 50.0,
          "actual": 0.0,
          "annualAchievement": 0.0,
          "periodAchievement": 0.0
        },
        {
          "county": "خرمدره",
          "annualTarget": 0.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": null,
          "periodAchievement": null
        },
        {
          "county": "زنجان",
          "annualTarget": 0.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": null,
          "periodAchievement": null
        },
        {
          "county": "سلطانیه",
          "annualTarget": 100.0,
          "periodTarget": 100.0,
          "actual": 0.0,
          "annualAchievement": 0.0,
          "periodAchievement": 0.0
        },
        {
          "county": "طارم",
          "annualTarget": 0.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": null,
          "periodAchievement": null
        },
        {
          "county": "ماهنشان",
          "annualTarget": 0.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": null,
          "periodAchievement": null
        }
      ]
    },
    {
      "id": "بروسلوز-دام-سبک-عملکرد-واکسیناسیون-بروسلوز-بره-REV1-شهرستان",
      "categoryId": "zoonotic",
      "categoryLabel": "ب- عملکرد مبارزه با بیماری‌های مشترک",
      "sheet": "بروسلوز دام سبک",
      "title": "عملکرد واکسیناسیون بروسلوز بره REV1 شهرستان",
      "indicator": "بروسلوز بره REV1",
      "livestockGroup": "دام سبک",
      "sourcePeriodMonths": 4,
      "sourceAsOf": "1405/05/01",
      "rows": [
        {
          "county": "ابهر",
          "annualTarget": 26347.0,
          "periodTarget": 18105.0,
          "actual": 26101.0,
          "annualAchievement": 99.07,
          "periodAchievement": 144.16
        },
        {
          "county": "ایجرود",
          "annualTarget": 17173.0,
          "periodTarget": 9654.0,
          "actual": 9204.0,
          "annualAchievement": 53.6,
          "periodAchievement": 95.34
        },
        {
          "county": "خدابنده",
          "annualTarget": 43882.0,
          "periodTarget": 36882.0,
          "actual": 39836.0,
          "annualAchievement": 90.78,
          "periodAchievement": 108.01
        },
        {
          "county": "خرمدره",
          "annualTarget": 4128.0,
          "periodTarget": 3200.0,
          "actual": 5736.0,
          "annualAchievement": 138.95,
          "periodAchievement": 179.25
        },
        {
          "county": "زنجان",
          "annualTarget": 64353.0,
          "periodTarget": 53500.0,
          "actual": 22373.0,
          "annualAchievement": 34.77,
          "periodAchievement": 41.82
        },
        {
          "county": "سلطانیه",
          "annualTarget": 15476.0,
          "periodTarget": 13700.0,
          "actual": 4711.0,
          "annualAchievement": 30.44,
          "periodAchievement": 34.39
        },
        {
          "county": "طارم",
          "annualTarget": 14305.0,
          "periodTarget": 10200.0,
          "actual": 5116.0,
          "annualAchievement": 35.76,
          "periodAchievement": 50.16
        },
        {
          "county": "ماهنشان",
          "annualTarget": 32210.0,
          "periodTarget": 25840.0,
          "actual": 10660.0,
          "annualAchievement": 33.1,
          "periodAchievement": 41.25
        }
      ]
    },
    {
      "id": "بروسلوز-دام-سبک-عملکرد-واکسیناسیون-بروسلوز-میش-REV1-شهرستان",
      "categoryId": "zoonotic",
      "categoryLabel": "ب- عملکرد مبارزه با بیماری‌های مشترک",
      "sheet": "بروسلوز دام سبک",
      "title": "عملکرد واکسیناسیون بروسلوز میش REV1 شهرستان",
      "indicator": "بروسلوز میش REV1",
      "livestockGroup": "دام سبک",
      "sourcePeriodMonths": 4,
      "sourceAsOf": "1405/05/01",
      "rows": [
        {
          "county": "ابهر",
          "annualTarget": 65867.0,
          "periodTarget": 45262.0,
          "actual": 17089.0,
          "annualAchievement": 25.94,
          "periodAchievement": 37.76
        },
        {
          "county": "ایجرود",
          "annualTarget": 43433.0,
          "periodTarget": 25137.5,
          "actual": 41866.0,
          "annualAchievement": 96.39,
          "periodAchievement": 166.55
        },
        {
          "county": "خدابنده",
          "annualTarget": 120042.0,
          "periodTarget": 102205.0,
          "actual": 96907.0,
          "annualAchievement": 80.73,
          "periodAchievement": 94.82
        },
        {
          "county": "خرمدره",
          "annualTarget": 10321.0,
          "periodTarget": 8000.0,
          "actual": 11565.0,
          "annualAchievement": 112.05,
          "periodAchievement": 144.56
        },
        {
          "county": "زنجان",
          "annualTarget": 165632.5,
          "periodTarget": 138500.0,
          "actual": 24363.0,
          "annualAchievement": 14.71,
          "periodAchievement": 17.59
        },
        {
          "county": "سلطانیه",
          "annualTarget": 37960.0,
          "periodTarget": 34750.0,
          "actual": 2827.0,
          "annualAchievement": 7.45,
          "periodAchievement": 8.14
        },
        {
          "county": "طارم",
          "annualTarget": 35762.5,
          "periodTarget": 25500.0,
          "actual": 13509.0,
          "annualAchievement": 37.77,
          "periodAchievement": 52.98
        },
        {
          "county": "ماهنشان",
          "annualTarget": 82187.0,
          "periodTarget": 66350.0,
          "actual": 21801.0,
          "annualAchievement": 26.53,
          "periodAchievement": 32.86
        }
      ]
    },
    {
      "id": "بروسلوز-دام-سنگین-عملکرد-واکسیناسیون-FD-IRIBA-شهرستان",
      "categoryId": "zoonotic",
      "categoryLabel": "ب- عملکرد مبارزه با بیماری‌های مشترک",
      "sheet": "بروسلوز دام سنگین",
      "title": "عملکرد واکسیناسیون FD IRIBA شهرستان",
      "indicator": "FD IRIBA",
      "livestockGroup": "سایر",
      "sourcePeriodMonths": 4,
      "sourceAsOf": "1405/05/01",
      "rows": [
        {
          "county": "ابهر",
          "annualTarget": 2565.0,
          "periodTarget": 1815.0,
          "actual": 162.0,
          "annualAchievement": 6.32,
          "periodAchievement": 8.93
        },
        {
          "county": "ایجرود",
          "annualTarget": 1413.0,
          "periodTarget": 0.0,
          "actual": 514.0,
          "annualAchievement": 36.38,
          "periodAchievement": null
        },
        {
          "county": "خدابنده",
          "annualTarget": 2816.0,
          "periodTarget": 2816.0,
          "actual": 1142.0,
          "annualAchievement": 40.55,
          "periodAchievement": 40.55
        },
        {
          "county": "خرمدره",
          "annualTarget": 3250.0,
          "periodTarget": 1100.0,
          "actual": 1130.0,
          "annualAchievement": 34.77,
          "periodAchievement": 102.73
        },
        {
          "county": "زنجان",
          "annualTarget": 4948.0,
          "periodTarget": 2050.0,
          "actual": 656.0,
          "annualAchievement": 13.26,
          "periodAchievement": 32.0
        },
        {
          "county": "سلطانیه",
          "annualTarget": 1242.0,
          "periodTarget": 235.0,
          "actual": 215.0,
          "annualAchievement": 17.31,
          "periodAchievement": 91.49
        },
        {
          "county": "طارم",
          "annualTarget": 1312.0,
          "periodTarget": 1312.0,
          "actual": 1319.0,
          "annualAchievement": 100.53,
          "periodAchievement": 100.53
        },
        {
          "county": "ماهنشان",
          "annualTarget": 1298.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": 0.0,
          "periodAchievement": null
        }
      ]
    },
    {
      "id": "بروسلوز-دام-سنگین-عملکرد-واکسیناسیون-RD-IRIBA-شهرستان",
      "categoryId": "zoonotic",
      "categoryLabel": "ب- عملکرد مبارزه با بیماری‌های مشترک",
      "sheet": "بروسلوز دام سنگین",
      "title": "عملکرد واکسیناسیون RD IRIBA شهرستان",
      "indicator": "RD IRIBA",
      "livestockGroup": "سایر",
      "sourcePeriodMonths": 4,
      "sourceAsOf": "1405/05/01",
      "rows": [
        {
          "county": "ابهر",
          "annualTarget": 5230.0,
          "periodTarget": 3899.0,
          "actual": 280.0,
          "annualAchievement": 5.35,
          "periodAchievement": 7.18
        },
        {
          "county": "ایجرود",
          "annualTarget": 2827.0,
          "periodTarget": 0.0,
          "actual": 892.0,
          "annualAchievement": 31.55,
          "periodAchievement": null
        },
        {
          "county": "خدابنده",
          "annualTarget": 5472.0,
          "periodTarget": 5472.0,
          "actual": 3648.0,
          "annualAchievement": 66.67,
          "periodAchievement": 66.67
        },
        {
          "county": "خرمدره",
          "annualTarget": 4269.0,
          "periodTarget": 560.0,
          "actual": 388.0,
          "annualAchievement": 9.09,
          "periodAchievement": 69.29
        },
        {
          "county": "زنجان",
          "annualTarget": 9996.0,
          "periodTarget": 3950.0,
          "actual": 2153.0,
          "annualAchievement": 21.54,
          "periodAchievement": 54.51
        },
        {
          "county": "سلطانیه",
          "annualTarget": 2481.0,
          "periodTarget": 698.0,
          "actual": 916.0,
          "annualAchievement": 36.92,
          "periodAchievement": 131.23
        },
        {
          "county": "طارم",
          "annualTarget": 2624.0,
          "periodTarget": 2624.0,
          "actual": 2732.0,
          "annualAchievement": 104.12,
          "periodAchievement": 104.12
        },
        {
          "county": "ماهنشان",
          "annualTarget": 2644.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": 0.0,
          "periodAchievement": null
        }
      ]
    },
    {
      "id": "شاربن-عملکرد-واکسیناسیون-شاربن-دام-سبک-شهرستان",
      "categoryId": "infectious",
      "categoryLabel": "الف- عملکرد مبارزه با بیماری‌های واگیر",
      "sheet": "شاربن",
      "title": "عملکرد واکسیناسیون شاربن دام سبک شهرستان",
      "indicator": "شاربن دام سبک",
      "livestockGroup": "دام سبک",
      "sourcePeriodMonths": 4,
      "sourceAsOf": "1405/05/01",
      "rows": [
        {
          "county": "ابهر",
          "annualTarget": 14000.0,
          "periodTarget": 14000.0,
          "actual": 13062.0,
          "annualAchievement": 93.3,
          "periodAchievement": 93.3
        },
        {
          "county": "ایجرود",
          "annualTarget": 21000.0,
          "periodTarget": 21000.0,
          "actual": 0.0,
          "annualAchievement": 0.0,
          "periodAchievement": 0.0
        },
        {
          "county": "خدابنده",
          "annualTarget": 89800.0,
          "periodTarget": 89800.0,
          "actual": 113942.0,
          "annualAchievement": 126.88,
          "periodAchievement": 126.88
        },
        {
          "county": "خرمدره",
          "annualTarget": 16200.0,
          "periodTarget": 16200.0,
          "actual": 22095.0,
          "annualAchievement": 136.39,
          "periodAchievement": 136.39
        },
        {
          "county": "زنجان",
          "annualTarget": 220000.0,
          "periodTarget": 0.0,
          "actual": 41007.0,
          "annualAchievement": 18.64,
          "periodAchievement": null
        },
        {
          "county": "سلطانیه",
          "annualTarget": 2500.0,
          "periodTarget": 2500.0,
          "actual": 5263.0,
          "annualAchievement": 210.52,
          "periodAchievement": 210.52
        },
        {
          "county": "طارم",
          "annualTarget": 60000.0,
          "periodTarget": 20000.0,
          "actual": 65376.0,
          "annualAchievement": 108.96,
          "periodAchievement": 326.88
        },
        {
          "county": "ماهنشان",
          "annualTarget": 50000.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": 0.0,
          "periodAchievement": null
        }
      ]
    },
    {
      "id": "شاربن-عملکرد-واکسیناسیون-شاربن-گاو-و-گوساله-شهرستان",
      "categoryId": "infectious",
      "categoryLabel": "الف- عملکرد مبارزه با بیماری‌های واگیر",
      "sheet": "شاربن",
      "title": "عملکرد واکسیناسیون شاربن گاو و گوساله شهرستان",
      "indicator": "شاربن گاو و گوساله",
      "livestockGroup": "دام سنگین",
      "sourcePeriodMonths": 4,
      "sourceAsOf": "1405/05/01",
      "rows": [
        {
          "county": "ابهر",
          "annualTarget": 2000.0,
          "periodTarget": 2000.0,
          "actual": 224.0,
          "annualAchievement": 11.2,
          "periodAchievement": 11.2
        },
        {
          "county": "ایجرود",
          "annualTarget": 1500.0,
          "periodTarget": 1500.0,
          "actual": 0.0,
          "annualAchievement": 0.0,
          "periodAchievement": 0.0
        },
        {
          "county": "خدابنده",
          "annualTarget": 8000.0,
          "periodTarget": 0.0,
          "actual": 3711.0,
          "annualAchievement": 46.39,
          "periodAchievement": null
        },
        {
          "county": "خرمدره",
          "annualTarget": 5800.0,
          "periodTarget": 1000.0,
          "actual": 1800.0,
          "annualAchievement": 31.03,
          "periodAchievement": 180.0
        },
        {
          "county": "زنجان",
          "annualTarget": 13821.0,
          "periodTarget": 3900.0,
          "actual": 5472.0,
          "annualAchievement": 39.59,
          "periodAchievement": 140.31
        },
        {
          "county": "سلطانیه",
          "annualTarget": 850.0,
          "periodTarget": 850.0,
          "actual": 559.0,
          "annualAchievement": 65.76,
          "periodAchievement": 65.76
        },
        {
          "county": "طارم",
          "annualTarget": 4309.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": 0.0,
          "periodAchievement": null
        },
        {
          "county": "ماهنشان",
          "annualTarget": 980.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": 0.0,
          "periodAchievement": null
        }
      ]
    },
    {
      "id": "شاربن-عملکرد-واکسیناسیون-تک-سمی-شهرستان",
      "categoryId": "infectious",
      "categoryLabel": "الف- عملکرد مبارزه با بیماری‌های واگیر",
      "sheet": "شاربن",
      "title": "عملکرد واکسیناسیون تک سمی شهرستان",
      "indicator": "تک سمی",
      "livestockGroup": "تک سمی",
      "sourcePeriodMonths": 4,
      "sourceAsOf": "1405/05/01",
      "rows": [
        {
          "county": "ابهر",
          "annualTarget": 111.0,
          "periodTarget": 111.0,
          "actual": 80.0,
          "annualAchievement": 72.07,
          "periodAchievement": 72.07
        },
        {
          "county": "ایجرود",
          "annualTarget": 40.0,
          "periodTarget": 40.0,
          "actual": 0.0,
          "annualAchievement": 0.0,
          "periodAchievement": 0.0
        },
        {
          "county": "خدابنده",
          "annualTarget": 60.0,
          "periodTarget": 60.0,
          "actual": 30.0,
          "annualAchievement": 50.0,
          "periodAchievement": 50.0
        },
        {
          "county": "خرمدره",
          "annualTarget": 130.0,
          "periodTarget": 60.0,
          "actual": 131.0,
          "annualAchievement": 100.77,
          "periodAchievement": 218.33
        },
        {
          "county": "زنجان",
          "annualTarget": 400.0,
          "periodTarget": 0.0,
          "actual": 53.0,
          "annualAchievement": 13.25,
          "periodAchievement": null
        },
        {
          "county": "سلطانیه",
          "annualTarget": 43.0,
          "periodTarget": 15.0,
          "actual": 19.0,
          "annualAchievement": 44.19,
          "periodAchievement": 126.67
        },
        {
          "county": "طارم",
          "annualTarget": 60.0,
          "periodTarget": 0.0,
          "actual": 57.0,
          "annualAchievement": 95.0,
          "periodAchievement": null
        },
        {
          "county": "ماهنشان",
          "annualTarget": 0.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": null,
          "periodAchievement": null
        }
      ]
    },
    {
      "id": "PPR-عملکرد-واکسیناسیون-PPR-شهرستان",
      "categoryId": "infectious",
      "categoryLabel": "الف- عملکرد مبارزه با بیماری‌های واگیر",
      "sheet": "PPR",
      "title": "عملکرد واکسیناسیون PPR شهرستان",
      "indicator": "PPR",
      "livestockGroup": "سایر",
      "sourcePeriodMonths": 4,
      "sourceAsOf": "1405/05/01",
      "rows": [
        {
          "county": "ابهر",
          "annualTarget": 81000.0,
          "periodTarget": 57000.0,
          "actual": 2570.0,
          "annualAchievement": 3.17,
          "periodAchievement": 4.51
        },
        {
          "county": "ایجرود",
          "annualTarget": 30000.0,
          "periodTarget": 15000.0,
          "actual": 2535.0,
          "annualAchievement": 8.45,
          "periodAchievement": 16.9
        },
        {
          "county": "خدابنده",
          "annualTarget": 233427.0,
          "periodTarget": 122427.0,
          "actual": 89528.0,
          "annualAchievement": 38.35,
          "periodAchievement": 73.13
        },
        {
          "county": "خرمدره",
          "annualTarget": 20730.0,
          "periodTarget": 10000.0,
          "actual": 13533.0,
          "annualAchievement": 65.28,
          "periodAchievement": 135.33
        },
        {
          "county": "زنجان",
          "annualTarget": 245000.0,
          "periodTarget": 180000.0,
          "actual": 7625.0,
          "annualAchievement": 3.11,
          "periodAchievement": 4.24
        },
        {
          "county": "سلطانیه",
          "annualTarget": 32602.0,
          "periodTarget": 18602.0,
          "actual": 17016.0,
          "annualAchievement": 52.19,
          "periodAchievement": 91.47
        },
        {
          "county": "طارم",
          "annualTarget": 70600.0,
          "periodTarget": 55600.0,
          "actual": 14801.0,
          "annualAchievement": 20.96,
          "periodAchievement": 26.62
        },
        {
          "county": "ماهنشان",
          "annualTarget": 177538.0,
          "periodTarget": 92616.0,
          "actual": 53474.0,
          "annualAchievement": 30.12,
          "periodAchievement": 57.74
        }
      ]
    },
    {
      "id": "هاری-عملکرد-واکسیناسیون-هاری-شهرستان",
      "categoryId": "zoonotic",
      "categoryLabel": "ب- عملکرد مبارزه با بیماری‌های مشترک",
      "sheet": "هاری",
      "title": "عملکرد واکسیناسیون هاری شهرستان",
      "indicator": "هاری",
      "livestockGroup": "سایر",
      "sourcePeriodMonths": 4,
      "sourceAsOf": "1405/05/01",
      "rows": [
        {
          "county": "ابهر",
          "annualTarget": 2089.0,
          "periodTarget": 100.0,
          "actual": 247.0,
          "annualAchievement": 11.82,
          "periodAchievement": 247.0
        },
        {
          "county": "ایجرود",
          "annualTarget": 887.0,
          "periodTarget": 300.0,
          "actual": 240.0,
          "annualAchievement": 27.06,
          "periodAchievement": 80.0
        },
        {
          "county": "خدابنده",
          "annualTarget": 1700.0,
          "periodTarget": 800.0,
          "actual": 371.0,
          "annualAchievement": 21.82,
          "periodAchievement": 46.38
        },
        {
          "county": "خرمدره",
          "annualTarget": 190.0,
          "periodTarget": 30.0,
          "actual": 133.0,
          "annualAchievement": 70.0,
          "periodAchievement": 443.33
        },
        {
          "county": "زنجان",
          "annualTarget": 3650.0,
          "periodTarget": 710.0,
          "actual": 1670.0,
          "annualAchievement": 45.75,
          "periodAchievement": 235.21
        },
        {
          "county": "سلطانیه",
          "annualTarget": 872.0,
          "periodTarget": 400.0,
          "actual": 283.0,
          "annualAchievement": 32.45,
          "periodAchievement": 70.75
        },
        {
          "county": "طارم",
          "annualTarget": 590.0,
          "periodTarget": 300.0,
          "actual": 113.0,
          "annualAchievement": 19.15,
          "periodAchievement": 37.67
        },
        {
          "county": "ماهنشان",
          "annualTarget": 630.0,
          "periodTarget": 190.0,
          "actual": 152.0,
          "annualAchievement": 24.13,
          "periodAchievement": 80.0
        }
      ]
    },
    {
      "id": "لمپی-اسکین-عملکرد-واکسیناسیون-لمپی-اسکین-شهرستان-واکسن-رایگان-دولتی",
      "categoryId": "infectious",
      "categoryLabel": "الف- عملکرد مبارزه با بیماری‌های واگیر",
      "sheet": "لمپی اسکین",
      "title": "عملکرد واکسیناسیون لمپی اسکین شهرستان (واکسن رایگان دولتی)",
      "indicator": "لمپی اسکین شهرستان (واکسن رایگان دولتی)",
      "livestockGroup": "سایر",
      "sourcePeriodMonths": 4,
      "sourceAsOf": "1405/05/01",
      "rows": [
        {
          "county": "ابهر",
          "annualTarget": 6149.0,
          "periodTarget": 0.0,
          "actual": 270.0,
          "annualAchievement": 4.39,
          "periodAchievement": null
        },
        {
          "county": "ایجرود",
          "annualTarget": 5654.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": 0.0,
          "periodAchievement": null
        },
        {
          "county": "خدابنده",
          "annualTarget": 10364.0,
          "periodTarget": 0.0,
          "actual": 3492.0,
          "annualAchievement": 33.69,
          "periodAchievement": null
        },
        {
          "county": "خرمدره",
          "annualTarget": 1610.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": 0.0,
          "periodAchievement": null
        },
        {
          "county": "زنجان",
          "annualTarget": 17411.0,
          "periodTarget": 3900.0,
          "actual": 6161.0,
          "annualAchievement": 35.39,
          "periodAchievement": 157.97
        },
        {
          "county": "سلطانیه",
          "annualTarget": 3386.0,
          "periodTarget": 3386.0,
          "actual": 3015.0,
          "annualAchievement": 89.04,
          "periodAchievement": 89.04
        },
        {
          "county": "طارم",
          "annualTarget": 5246.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": 0.0,
          "periodAchievement": null
        },
        {
          "county": "ماهنشان",
          "annualTarget": 5193.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": 0.0,
          "periodAchievement": null
        }
      ]
    },
    {
      "id": "تب-برفکی-خارج-از-فاز-عملکرد-واکسیناسیون-تب-برفکی-دام-سبک-شهرستان-واکسن-رایگان-دولتی",
      "categoryId": "infectious",
      "categoryLabel": "الف- عملکرد مبارزه با بیماری‌های واگیر",
      "sheet": "تب برفکی خارج از فاز",
      "title": "عملکرد واکسیناسیون تب برفکی دام سبک شهرستان (واکسن رایگان دولتی)",
      "indicator": "تب برفکی دام سبک شهرستان (واکسن رایگان دولتی)",
      "livestockGroup": "دام سبک",
      "sourcePeriodMonths": 4,
      "sourceAsOf": "1405/05/01",
      "rows": [
        {
          "county": "ابهر",
          "annualTarget": 250000.0,
          "periodTarget": 0.0,
          "actual": 5910.0,
          "annualAchievement": 2.36,
          "periodAchievement": null
        },
        {
          "county": "ایجرود",
          "annualTarget": 151730.0,
          "periodTarget": 0.0,
          "actual": 4799.0,
          "annualAchievement": 3.16,
          "periodAchievement": null
        },
        {
          "county": "خدابنده",
          "annualTarget": 438818.0,
          "periodTarget": 0.0,
          "actual": 8644.0,
          "annualAchievement": 1.97,
          "periodAchievement": null
        },
        {
          "county": "خرمدره",
          "annualTarget": 41284.0,
          "periodTarget": 0.0,
          "actual": 860.0,
          "annualAchievement": 2.08,
          "periodAchievement": null
        },
        {
          "county": "زنجان",
          "annualTarget": 600000.0,
          "periodTarget": 0.0,
          "actual": 44615.0,
          "annualAchievement": 7.44,
          "periodAchievement": null
        },
        {
          "county": "سلطانیه",
          "annualTarget": 159836.0,
          "periodTarget": 0.0,
          "actual": 8361.0,
          "annualAchievement": 5.23,
          "periodAchievement": null
        },
        {
          "county": "طارم",
          "annualTarget": 66527.0,
          "periodTarget": 0.0,
          "actual": 9845.0,
          "annualAchievement": 14.8,
          "periodAchievement": null
        },
        {
          "county": "ماهنشان",
          "annualTarget": 316744.0,
          "periodTarget": 0.0,
          "actual": 66208.0,
          "annualAchievement": 20.9,
          "periodAchievement": null
        }
      ]
    },
    {
      "id": "تب-برفکی-خارج-از-فاز-عملکرد-واکسیناسیون-تب-برفکی-دام-سنگین-شهرستان-واکسن-رایگان-دولتی",
      "categoryId": "infectious",
      "categoryLabel": "الف- عملکرد مبارزه با بیماری‌های واگیر",
      "sheet": "تب برفکی خارج از فاز",
      "title": "عملکرد واکسیناسیون تب برفکی دام سنگین شهرستان (واکسن رایگان دولتی)",
      "indicator": "تب برفکی دام سنگین شهرستان (واکسن رایگان دولتی)",
      "livestockGroup": "دام سنگین",
      "sourcePeriodMonths": 4,
      "sourceAsOf": "1405/05/01",
      "rows": [
        {
          "county": "ابهر",
          "annualTarget": 12980.0,
          "periodTarget": 0.0,
          "actual": 405.0,
          "annualAchievement": 3.12,
          "periodAchievement": null
        },
        {
          "county": "ایجرود",
          "annualTarget": 11936.0,
          "periodTarget": 0.0,
          "actual": 60.0,
          "annualAchievement": 0.5,
          "periodAchievement": null
        },
        {
          "county": "خدابنده",
          "annualTarget": 21384.0,
          "periodTarget": 0.0,
          "actual": 1384.0,
          "annualAchievement": 6.47,
          "periodAchievement": null
        },
        {
          "county": "خرمدره",
          "annualTarget": 3286.0,
          "periodTarget": 0.0,
          "actual": 649.0,
          "annualAchievement": 19.75,
          "periodAchievement": null
        },
        {
          "county": "زنجان",
          "annualTarget": 33189.0,
          "periodTarget": 0.0,
          "actual": 684.0,
          "annualAchievement": 2.06,
          "periodAchievement": null
        },
        {
          "county": "سلطانیه",
          "annualTarget": 6936.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": 0.0,
          "periodAchievement": null
        },
        {
          "county": "طارم",
          "annualTarget": 7539.0,
          "periodTarget": 0.0,
          "actual": 1937.0,
          "annualAchievement": 25.69,
          "periodAchievement": null
        },
        {
          "county": "ماهنشان",
          "annualTarget": 10964.0,
          "periodTarget": 0.0,
          "actual": 241.0,
          "annualAchievement": 2.2,
          "periodAchievement": null
        }
      ]
    },
    {
      "id": "تست-سل،-بروسلوز-و-مشمشه-عملکرد-تست-سل-شهرستان",
      "categoryId": "surveillance",
      "categoryLabel": "ج- عملکرد پایش و مراقبت بیماری‌های مشترک",
      "sheet": "تست سل، بروسلوز و مشمشه",
      "title": "عملکرد تست سل شهرستان",
      "indicator": "تست سل",
      "livestockGroup": "دام سنگین",
      "sourcePeriodMonths": 4,
      "sourceAsOf": "1405/05/01",
      "rows": [
        {
          "county": "ابهر",
          "annualTarget": 3316.0,
          "periodTarget": 859.0,
          "actual": 915.0,
          "annualAchievement": 27.59,
          "periodAchievement": 106.52
        },
        {
          "county": "ایجرود",
          "annualTarget": 0.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": null,
          "periodAchievement": null
        },
        {
          "county": "خدابنده",
          "annualTarget": 400.0,
          "periodTarget": 0.0,
          "actual": 9.0,
          "annualAchievement": 2.25,
          "periodAchievement": null
        },
        {
          "county": "خرمدره",
          "annualTarget": 4540.0,
          "periodTarget": 4300.0,
          "actual": 4270.0,
          "annualAchievement": 94.05,
          "periodAchievement": 99.3
        },
        {
          "county": "زنجان",
          "annualTarget": 2244.0,
          "periodTarget": 429.0,
          "actual": 491.0,
          "annualAchievement": 21.88,
          "periodAchievement": 114.45
        },
        {
          "county": "سلطانیه",
          "annualTarget": 2220.0,
          "periodTarget": 830.0,
          "actual": 284.0,
          "annualAchievement": 12.79,
          "periodAchievement": 34.22
        },
        {
          "county": "طارم",
          "annualTarget": 0.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": null,
          "periodAchievement": null
        },
        {
          "county": "ماهنشان",
          "annualTarget": 0.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": null,
          "periodAchievement": null
        }
      ]
    },
    {
      "id": "تست-سل،-بروسلوز-و-مشمشه-عملکرد-تست-بروسلوز-شهرستان",
      "categoryId": "surveillance",
      "categoryLabel": "ج- عملکرد پایش و مراقبت بیماری‌های مشترک",
      "sheet": "تست سل، بروسلوز و مشمشه",
      "title": "عملکرد  تست بروسلوز شهرستان",
      "indicator": "تست بروسلوز",
      "livestockGroup": "سایر",
      "sourcePeriodMonths": 4,
      "sourceAsOf": "1405/05/01",
      "rows": [
        {
          "county": "ابهر",
          "annualTarget": 1880.0,
          "periodTarget": 440.0,
          "actual": 893.0,
          "annualAchievement": 47.5,
          "periodAchievement": 202.95
        },
        {
          "county": "ایجرود",
          "annualTarget": 0.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": null,
          "periodAchievement": null
        },
        {
          "county": "خدابنده",
          "annualTarget": 320.0,
          "periodTarget": 0.0,
          "actual": 9.0,
          "annualAchievement": 2.81,
          "periodAchievement": null
        },
        {
          "county": "خرمدره",
          "annualTarget": 6260.0,
          "periodTarget": 3500.0,
          "actual": 2965.0,
          "annualAchievement": 47.36,
          "periodAchievement": 84.71
        },
        {
          "county": "زنجان",
          "annualTarget": 1280.0,
          "periodTarget": 244.0,
          "actual": 217.0,
          "annualAchievement": 16.95,
          "periodAchievement": 88.93
        },
        {
          "county": "سلطانیه",
          "annualTarget": 1304.0,
          "periodTarget": 501.0,
          "actual": 100.0,
          "annualAchievement": 7.67,
          "periodAchievement": 19.96
        },
        {
          "county": "طارم",
          "annualTarget": 0.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": null,
          "periodAchievement": null
        },
        {
          "county": "ماهنشان",
          "annualTarget": 0.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": null,
          "periodAchievement": null
        }
      ]
    },
    {
      "id": "تست-سل،-بروسلوز-و-مشمشه-عملکرد-تست-مشمشه-شهرستان",
      "categoryId": "surveillance",
      "categoryLabel": "ج- عملکرد پایش و مراقبت بیماری‌های مشترک",
      "sheet": "تست سل، بروسلوز و مشمشه",
      "title": "عملکرد تست مشمشه شهرستان",
      "indicator": "تست مشمشه",
      "livestockGroup": "تک سمی",
      "sourcePeriodMonths": 4,
      "sourceAsOf": "1405/05/01",
      "rows": [
        {
          "county": "ابهر",
          "annualTarget": 80.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": 0.0,
          "periodAchievement": null
        },
        {
          "county": "ایجرود",
          "annualTarget": 0.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": null,
          "periodAchievement": null
        },
        {
          "county": "خدابنده",
          "annualTarget": 20.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": 0.0,
          "periodAchievement": null
        },
        {
          "county": "خرمدره",
          "annualTarget": 134.0,
          "periodTarget": 67.0,
          "actual": 58.0,
          "annualAchievement": 43.28,
          "periodAchievement": 86.57
        },
        {
          "county": "زنجان",
          "annualTarget": 462.0,
          "periodTarget": 231.0,
          "actual": 153.0,
          "annualAchievement": 33.12,
          "periodAchievement": 66.23
        },
        {
          "county": "سلطانیه",
          "annualTarget": 84.0,
          "periodTarget": 42.0,
          "actual": 15.0,
          "annualAchievement": 17.86,
          "periodAchievement": 35.71
        },
        {
          "county": "طارم",
          "annualTarget": 0.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": null,
          "periodAchievement": null
        },
        {
          "county": "ماهنشان",
          "annualTarget": 0.0,
          "periodTarget": 0.0,
          "actual": 0.0,
          "annualAchievement": null,
          "periodAchievement": null
        }
      ]
    }
  ]
} as const;

export const vaccinationKpiCategories = vaccinationKpiSource.categories as readonly VaccinationKpiCategory[];
export const vaccinationKpiIndicators = vaccinationKpiSource.indicators as readonly VaccinationKpiIndicator[];
