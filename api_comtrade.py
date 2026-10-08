import requests
import pandas as pd
import streamlit as st
import time

# 🌍 قاعدة بيانات الدول الشاملة
COMTRADE_COUNTRIES = {
    "العالم ككتلة واحدة (World)": "0",
    "جميع الدول فردياً (All Partners)": "all",
    "مصر (Egypt)": "818",
    "السعودية (Saudi Arabia)": "682",
    "الإمارات (UAE)": "784",
    "الكويت (Kuwait)": "414",
    "قطر (Qatar)": "634",
    "البحرين (Bahrain)": "048",
    "عمان (Oman)": "512",
    "العراق (Iraq)": "368",
    "الأردن (Jordan)": "400",
    "لبنان (Lebanon)": "422",
    "سوريا (Syria)": "760",
    "فلسطين (Palestine)": "275",
    "اليمن (Yemen)": "887",
    "السودان (Sudan)": "729",
    "ليبيا (Libya)": "434",
    "تونس (Tunisia)": "788",
    "الجزائر (Algeria)": "012",
    "المغرب (Morocco)": "504",
    "موريتانيا (Mauritania)": "478",
    
    "الولايات المتحدة (USA)": "840",
    "الصين (China)": "156",
    "روسيا (Russia)": "643",
    "الهند (India)": "356",
    "اليابان (Japan)": "392",
    "ألمانيا (Germany)": "276",
    "بريطانيا (UK)": "826",
    "فرنسا (France)": "250",
    "إيطاليا (Italy)": "380",
    "إسبانيا (Spain)": "724",
    "البرازيل (Brazil)": "076",
    "تركيا (Türkiye)": "792"
}

# 🌾 قاعدة بيانات المحاصيل والمنتجات الاستراتيجية
COMTRADE_PRODUCTS = {
    "إجمالي التجارة (جميع السلع)": "TOTAL",
    "بطاطس طازجة أو مبردة": "0701",
    "طماطم طازجة أو مبردة": "0702",
    "بصل وثوم وكرات": "0703",
    "فاصوليا خضراء": "070820",
    "فراولة طازجة": "081010",
    "بنجر السكر": "121291",
    "قمح ومسليين": "1001",
    "ذرة شامية": "1005",
    "أرز": "1006",
    "موالح (برتقال ويوسفي)": "0805",
    "عنب طازج أو مجفف": "0806",
    "بطيخ وشمام": "0807",
    "تمور وتين ومانجو": "0804",
    "فول صويا": "1201",
    "أسمدة (كافة الأنواع)": "31"
}

FLOWS = {
    "صادرات (Exports)": "X",
    "واردات (Imports)": "M"
}

def get_comtrade_countries():
    return list(COMTRADE_COUNTRIES.keys())

def get_comtrade_flows():
    return list(FLOWS.keys())

def get_comtrade_products():
    return list(COMTRADE_PRODUCTS.keys())

def get_hs_code(product_name):
    return COMTRADE_PRODUCTS.get(product_name, "TOTAL")

def fetch_comtrade_data(countries, products, start_year, end_year, api_key, flow_code, target_metric):
    import pandas as pd
    import requests
    import streamlit as st

    # 1. تحضير السنوات (من سنة البداية لسنة النهاية)
    years = ",".join([str(y) for y in range(start_year, end_year + 1)])
    
    # 2. تحضير الدول والسلع
    country_str = ",".join(countries)
    product_str = ",".join(products)
    
    # 3. بناء رابط الاستدعاء وتضمين (كود التدفق: صادرات أو واردات)
    url = f"https://comtradeapi.un.org/data/v1/get/C/A/HS?reporterCode={country_str}&partnerCode=0&cmdCode={product_str}&period={years}&flowCode={flow_code}"
    
    headers = {'Ocp-Apim-Subscription-Key': api_key}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                df = pd.DataFrame(data['data'])
                
                # 4. تصفية الأعمدة بناءً على "المتغير الاقتصادي" المطلوب
                columns_to_keep = ['reporterDesc', 'cmdCode', 'cmdDesc', 'period']
                if target_metric == "القيمة بالدولار (Trade Value)":
                    columns_to_keep.append('primaryValue')
                elif target_metric == "الكمية / الوزن الصافي (Net Weight)":
                    columns_to_keep.append('netWgt')
                else:
                    columns_to_keep.extend(['primaryValue', 'netWgt'])
                    
                # الاحتفاظ بالأعمدة المتاحة فقط لعدم حدوث أخطاء
                final_cols = [c for c in columns_to_keep if c in df.columns]
                return df[final_cols]
            else:
                return pd.DataFrame()
        else:
            st.error(f"خطأ في الاتصال بسيرفر الأمم المتحدة: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"خطأ برمجي أثناء المعالجة: {e}")
        return pd.DataFrame()
