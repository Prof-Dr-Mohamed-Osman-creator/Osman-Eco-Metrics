# ==========================================
# ملف: config.py
# الوظيفة: الإعدادات المركزية وخريطة توجيه البيانات
# النظام: Osman Eco-Metrics System
# ==========================================

SYSTEM_NAME = "Osman Eco-Metrics System"
VERSION = "1.0 - Core Architecture"

# خريطة توجيه المتغيرات إلى مصادرها
DATA_ROUTING_MAP = {
    
    "القطاع الزراعي والموارد": {
        "إنتاج القمح": {"source": "fao", "method": "api", "source_code": "2511"},
        "تكاليف التشغيل للإنتاج": {"source": "agri_ministry_eg", "method": "scraping", "source_code": None},
        "البصمة المائية": {"source": "fao", "method": "api", "source_code": "6732"}
    },
    
    "التجارة الخارجية": {
        "صادرات الفراولة المجمدة": {"source": "trademap", "method": "api", "source_code": "081110"},
        "الميزة التنافسية (RCA)": {"source": "un_comtrade", "method": "api", "source_code": "RCA_INDEX"},
        "الميزان التجاري": {"source": "worldbank", "method": "api", "source_code": "NE.RSB.GNFS.CD"}
    },
    
    "القطاع الحقيقي والمالي": {
        "معدل التضخم": {"source": "capmas", "method": "scraping", "source_code": None},
        "الناتج المحلي الإجمالي": {"source": "worldbank", "method": "api", "source_code": "NY.GDP.MKTP.CD"},
        "أسعار الفائدة": {"source": "cbe", "method": "scraping", "source_code": None}
    }
}

# قائمة الدول المدعومة مبدئياً
SUPPORTED_COUNTRIES = {
    "مصر": "EGY",
    "السعودية": "SAU",
    "الولايات المتحدة": "USA",
    "الأسواق الأوروبية": "EU"
}