# ==========================================
# ملف: build_catalog.py
# الوظيفة: بناء الفهرس المزدوج (العربي النقي + الإنجليزي الشامل)
# ==========================================

import requests
import pandas as pd
import time

def fetch_catalog(lang_code, file_name):
    print(f"\n🚀 جاري سحب الفهرس للغة: {lang_code.upper()} ...")
    indicators = []
    page = 1
    per_page = 5000
    lang_path = "ar/" if lang_code == "ar" else ""
    
    while True:
        print(f"-> سحب الدفعة رقم {page} ...")
        url = f"http://api.worldbank.org/v2/{lang_path}indicator?format=json&per_page={per_page}&page={page}"
        
        try:
            response = requests.get(url, timeout=30)
            data = response.json()
            
            if len(data) > 1 and data[1]:
                for item in data[1]:
                    if item.get('name') and item.get('id'):
                        indicators.append({
                            "اسم المتغير": item['name'],
                            "كود المتغير": item['id']
                        })
                
                total_pages = data[0].get('pages', 1)
                if page >= total_pages:
                    break
                
                page += 1
                time.sleep(1) # استراحة قصيرة
            else:
                break
                
        except Exception as e:
            print(f"⚠️ خطأ في الدفعة {page}: {e}")
            break

    # حفظ الملف
    if indicators:
        df = pd.DataFrame(indicators)
        df = df.drop_duplicates(subset=["كود المتغير"])
        df = df.sort_values(by="اسم المتغير")
        df.to_csv(file_name, index=False, encoding="utf-8-sig")
        print(f"✅ اكتمل سحب {len(df)} متغير، وتم الحفظ في '{file_name}'.")

if __name__ == "__main__":
    print("=========================================")
    print("أداة بناء فهرس البنك الدولي المزدوج")
    print("=========================================")
    
    # 1. سحب الفهرس العربي
    fetch_catalog("ar", "wb_indicators_ar.csv")
    
    # 2. سحب الفهرس الإنجليزي (القاعدة الشاملة)
    fetch_catalog("en", "wb_indicators_en.csv")
    
    print("\n🎉 تمت العملية بالكامل بنجاح! المنصة الآن تمتلك الفهرس الشامل.")
    time.sleep(5)