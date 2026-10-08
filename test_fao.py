import pandas as pd
import os

print("="*50)
print("🔍 جاري فحص الملفات الزراعية في المجلد...")
print("="*50)

# طباعة كل الملفات التي تشبه الفاو في المجلد
files = os.listdir()
for f in files:
    if "fao" in f.lower() or "data" in f.lower() or "production" in f.lower():
        print(f"📄 الملف الموجود: {f}")

print("-" * 50)

# محاولة قراءة الملف
file_name = "FAOSTAT_data.csv"
try:
    print(f"⏳ جاري محاولة فتح {file_name} ...")
    df = pd.read_csv(file_name, encoding="latin1", nrows=5)
    print("✅ نجاح! تم قراءة الملف. الأعمدة الموجودة هي:")
    print(list(df.columns))
except FileNotFoundError:
    print(f"❌ خطأ: لم أتمكن من العثور على ملف باسم '{file_name}' بالضبط.")
except Exception as e:
    print(f"❌ خطأ غير معروف أثناء القراءة: {e}")