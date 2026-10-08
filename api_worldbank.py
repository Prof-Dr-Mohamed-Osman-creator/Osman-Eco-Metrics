# ==========================================
# ملف: api_worldbank.py
# الوظيفة: محرك جلب البيانات من البنك الدولي
# ==========================================

import requests
import pandas as pd

def fetch_all_countries(lang="ar"):
    """جلب قائمة الدول"""
    lang_path = "ar/" if lang == "ar" else ""
    url = f"http://api.worldbank.org/v2/{lang_path}country?format=json&per_page=400"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        countries_dict = {}
        if len(data) > 1 and data[1]:
            for item in data[1]:
                if item.get('name') and item.get('id'):
                    countries_dict[item['name']] = item['id']
        return dict(sorted(countries_dict.items()))
    except:
        return {"جمهورية مصر العربية": "EGY", "العالم": "WLD"}

def fetch_worldbank_data(country_code, indicator_code, start_year, end_year, lang="ar"):
    """جلب السلسلة الزمنية (تم إزالة مسار اللغة من الرابط لضمان استرداد الأرقام دائماً)"""
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}"
    
    params = {
        "format": "json",
        "date": f"{start_year}:{end_year}",
        "per_page": 250
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        data = response.json()
        
        if len(data) > 1 and data[1] is not None:
            records = data[1]
            parsed_data = []
            
            for item in records:
                if item.get('value') is not None:
                    parsed_data.append({
                        "الدولة": item['country']['value'],
                        "السنة": item['date'],
                        "المتغير": item['indicator']['value'],
                        "القيمة": item['value']
                    })
            
            df = pd.DataFrame(parsed_data)
            if not df.empty:
                df["السنة"] = df["السنة"].astype(int)
                df = df.sort_values(by="السنة", ascending=True).reset_index(drop=True)
            return df
            
        return pd.DataFrame()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()