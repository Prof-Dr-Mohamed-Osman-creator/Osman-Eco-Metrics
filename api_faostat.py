import pandas as pd
import os
import glob
import streamlit as st

FAO_FOLDER = "FAO_Data"

@st.cache_data
def get_fao_metadata():
    """قراءة ذكية وسريعة للقوائم المنسدلة بدون استهلاك الذاكرة"""
    countries = set()
    crops = set()
    indicators = set()
    
    if not os.path.exists(FAO_FOLDER):
        return ["يرجى إنشاء مجلد FAO_Data"], [], []
        
    all_files = glob.glob(os.path.join(FAO_FOLDER, "*.csv"))
    if not all_files:
        return ["لا توجد ملفات في المجلد"], [], []
        
    for file in all_files:
        try:
            # قراءة أسماء الأعمدة أولاً للتأكد
            cols = pd.read_csv(file, nrows=0, encoding="latin1").columns
            valid_cols = [c for c in ["Area", "Item", "Element"] if c in cols]
            
            if valid_cols:
                # قراءة الأعمدة الثلاثة فقط لتوفير 99% من الذاكرة
                df_meta = pd.read_csv(file, usecols=valid_cols, encoding="latin1")
                if "Area" in df_meta: countries.update(df_meta["Area"].dropna().unique())
                if "Item" in df_meta: crops.update(df_meta["Item"].dropna().unique())
                if "Element" in df_meta: indicators.update(df_meta["Element"].dropna().unique())
        except Exception as e:
            pass
            
    return sorted(list(countries)), sorted(list(crops)), sorted(list(indicators))

def get_fao_countries():
    countries, _, _ = get_fao_metadata()
    return countries if countries else ["لا توجد بيانات"]

def get_fao_crops():
    _, crops, _ = get_fao_metadata()
    return crops if crops else ["لا توجد بيانات"]

def get_fao_indicators():
    _, _, indicators = get_fao_metadata()
    return indicators if indicators else ["لا توجد بيانات"]

def fetch_agricultural_data(country_name, crop_name, indicator_name, start_year, end_year):
    """خوارزمية الحصاد بالتقطيع (Chunking) لمنع انهيار الذاكرة - مستوى احترافي"""
    result_list = []
    all_files = glob.glob(os.path.join(FAO_FOLDER, "*.csv"))
    
    for file in all_files:
        try:
            # قراءة الملف الضخم على دفعات (50 ألف صف في كل مرة)
            chunk_iter = pd.read_csv(file, encoding="latin1", chunksize=50000, low_memory=False)
            for chunk in chunk_iter:
                # فلترة الدفعة وهي صغيرة في الذاكرة
                mask = pd.Series(True, index=chunk.index)
                if "Area" in chunk.columns: mask = mask & (chunk["Area"] == country_name)
                if "Item" in chunk.columns: mask = mask & (chunk["Item"] == crop_name)
                if "Element" in chunk.columns: mask = mask & (chunk["Element"] == indicator_name)
                
                filtered = chunk[mask]
                if not filtered.empty:
                    # صهر الأجزاء المطلوبة فقط بدلاً من صهر الملف كله
                    year_cols = [c for c in filtered.columns if c.startswith('Y') and len(c) == 5 and c[1:].isdigit()]
                    id_vars = ["Area", "Item", "Element"]
                    avail_id_vars = [c for c in id_vars if c in filtered.columns]
                    
                    melted = pd.melt(filtered, id_vars=avail_id_vars, value_vars=year_cols, var_name="السنة", value_name="القيمة")
                    melted["السنة"] = melted["السنة"].str.replace('Y', '').astype(int)
                    
                    # تطبيق النطاق الزمني
                    melted = melted[(melted["السنة"] >= start_year) & (melted["السنة"] <= end_year)]
                    result_list.append(melted)
        except Exception as e:
            pass
            
    if result_list:
        final_df = pd.concat(result_list, ignore_index=True)
        final_df = final_df.dropna(subset=["القيمة"])
        if not final_df.empty:
            res = final_df[["السنة", "القيمة"]].copy()
            res["المتغير"] = f"{crop_name} - {indicator_name}"
            return res
            
    return pd.DataFrame()