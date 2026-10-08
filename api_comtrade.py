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

def fetch_comtrade_data(reporter_name, partner_name, flow_name, hs_code, start_year, end_year, api_key):
    if not api_key:
        st.error("⚠ يرجى إدخال مفتاح الأمم المتحدة.")
        return pd.DataFrame()
        
    reporter_code = COMTRADE_COUNTRIES.get(reporter_name, "818")
    partner_code = COMTRADE_COUNTRIES.get(partner_name, "0")
    flow_code = FLOWS.get(flow_name, "X")
    
    all_years = list(range(start_year, end_year + 1))
    chunk_size = 5
    year_chunks = [all_years[i:i + chunk_size] for i in range(0, len(all_years), chunk_size)]
    
    url = "https://comtradeapi.un.org/data/v1/get/C/A/HS"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key.strip()
    }
    
    all_data = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, chunk in enumerate(year_chunks):
        years_str = ",".join([str(y) for y in chunk])
        status_text.text(f"جاري سحب بيانات السنوات: {years_str} ...")
        
        # تجهيز الطلب الأساسي
        params = {
            "reporterCode": reporter_code,
            "partner2Code": "0",
            "cmdCode": str(hs_code).strip(),
            "flowCode": flow_code,
            "period": years_str,
            "motCode": "0",
            "customsCode": "C00"
        }
        
        # 🎯 السر هنا: إذا أراد كل الدول، لا نرسل شرط (partnerCode) نهائياً ليتم سحب العالم كله
        if partner_code != "all":
            params["partnerCode"] = partner_code
            
        try:
            response = requests.get(url, headers=headers, params=params, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                if "data" in data and len(data["data"]) > 0:
                    df_chunk = pd.DataFrame(data["data"])
                    all_data.append(df_chunk)
            elif response.status_code == 400:
                # صندوق الاعتراف الأسود لكشف أي خطأ مستقبلي
                st.error("❌ خادم الأمم المتحدة يرفض الطلب. إليك اعتراف الخادم الدقيق:")
                st.code(response.text)
                progress_bar.empty()
                status_text.empty()
                return pd.DataFrame()
            elif response.status_code == 401:
                st.error("⛔ المفتاح غير صالح.")
                progress_bar.empty()
                status_text.empty()
                return pd.DataFrame()
                
            time.sleep(1.5)
        except Exception:
            pass
            
        progress_bar.progress((idx + 1) / len(year_chunks))
        
    progress_bar.empty()
    status_text.empty()
    
    if all_data:
        df = pd.concat(all_data, ignore_index=True)
        if "primaryValue" in df.columns and "partnerDesc" in df.columns:
            df_clean = df[["period", "partnerDesc", "primaryValue"]].copy()
            df_clean.rename(columns={"period": "السنة", "primaryValue": "القيمة"}, inplace=True)
            df_clean["السنة"] = df_clean["السنة"].astype(int)
            
            direction = "إلى" if flow_code == "X" else "من"
            
            if partner_name == "جميع الدول فردياً (All Partners)":
                df_clean["المتغير"] = f"{reporter_name.split()[0]} {direction} " + df_clean["partnerDesc"]
            else:
                df_clean["المتغير"] = f"{reporter_name.split()[0]} {direction} {partner_name.split()[0]}"
                
            df_clean = df_clean.sort_values(by=["السنة", "القيمة"], ascending=[True, False]).reset_index(drop=True)
            return df_clean
    return pd.DataFrame()