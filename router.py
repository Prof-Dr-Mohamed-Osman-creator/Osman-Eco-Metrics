# ==========================================
# ملف: router.py
# الوظيفة: الموجه الذكي (المايسترو) لتوزيع الطلبات
# النظام: Osman Eco-Metrics System
# ==========================================

import pandas as pd
import config
from api_worldbank import fetch_worldbank_data

def get_indicator_metadata(sector, indicator_name):
    """البحث عن تفاصيل المتغير داخل ملف الإعدادات"""
    try:
        return config.DATA_ROUTING_MAP[sector][indicator_name]
    except KeyError:
        return None

def process_request(sector, indicator_name, country_name, start_year, end_year):
    """توجيه الطلب للمحرك المناسب بناءً على المصدر المكتوب في الخريطة"""
    
    # 1. جلب كود الدولة من ملف الإعدادات
    country_code = config.SUPPORTED_COUNTRIES.get(country_name, "EGY")
    
    # 2. جلب بيانات المتغير (المصدر والكود)
    meta = get_indicator_metadata(sector, indicator_name)
    if not meta:
        print(f"⚠️ المتغير '{indicator_name}' غير مسجل في خريطة النظام.")
        return pd.DataFrame()
        
    source = meta["source"]
    source_code = meta["source_code"]
    
    # 3. التوجيه الفعلي (Routing)
    print(f"🔄 جاري توجيه '{indicator_name}' إلى محرك: {source.upper()}...")
    
    if source == "worldbank":
        # تشغيل كود البنك الدولي
        return fetch_worldbank_data(country_code, source_code, start_year, end_year)
        
    elif source == "fao":
        # تشغيل كود منظمة الأغذية والزراعة
        return fetch_faostat_data(country_name, indicator_name, "الإنتاج", start_year, end_year)
        
    else:
        print(f"⚠️ المحرك '{source}' قيد التطوير (مثل TradeMap أو الوزارات) ولم يتم تفعيله بعد.")
        return pd.DataFrame()

# ==========================================
# منطقة الاختبار (Test Zone)
# ==========================================
if __name__ == "__main__":
    print("🚀 تشغيل الموجه الذكي (Router)...\n")
    
    # الموجه الذكي سيقوم الآن بتنفيذ طلبين مختلفين تماماً من مصدرين مختلفين!
    
    # الطلب الأول: الميزان التجاري (اقتصاد كلي - من البنك الدولي)
    df_wb = process_request("التجارة الخارجية", "الميزان التجاري", "مصر", 2019, 2023)
    print("\n📊 نتيجة البنك الدولي:")
    print(df_wb.head() if not df_wb.empty else "لا توجد بيانات")
    
    print("\n" + "="*50 + "\n")
    
    # الطلب الثاني: إنتاج القمح (زراعة - من الفاو)
    df_fao = process_request("القطاع الزراعي والموارد", "إنتاج القمح", "مصر", 2019, 2023)
    print("🌾 نتيجة منظمة الأغذية والزراعة:")
    print(df_fao.head() if not df_fao.empty else "لا توجد بيانات")