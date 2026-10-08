import pandas as pd
import os
import glob
import streamlit as st
import re

TRADEMAP_FOLDER = "TradeMap_Data"

def load_trade_data():
    all_data = []
    if not os.path.exists(TRADEMAP_FOLDER):
        return pd.DataFrame()
        
    files = glob.glob(os.path.join(TRADEMAP_FOLDER, "*.csv")) + glob.glob(os.path.join(TRADEMAP_FOLDER, "*.txt"))
    
    for f in files:
        df = None
        for enc in ['utf-8-sig', 'windows-1256', 'utf-8', 'latin1']:
            for sep in [',', '\t', ';']:
                try:
                    temp_df = pd.read_csv(f, sep=sep, encoding=enc, dtype=str, on_bad_lines='skip', index_col=False)
                    if len(temp_df.columns) >= 7: 
                        df = temp_df
                        break
                except:
                    continue
            if df is not None:
                break
                
        if df is not None and not df.empty:
            cols = list(df.columns)
            
            r_col = cols[1]  
            p_col = cols[3]  
            pr_col = cols[5] 
            
            year_cols = []
            year_map = {}
            unit_str = "" # 🎯 المستشعر الجديد لالتقاط وحدة القياس
            
            for c in cols[6:]:
                # البحث عن السنة والوحدة (مثل: 2001 (USD))
                match_with_unit = re.search(r'^(\d{4})\s*\((.*?)\)', str(c).strip())
                if match_with_unit:
                    year_cols.append(c)
                    year_map[c] = int(match_with_unit.group(1))
                    if not unit_str:
                        unit_str = match_with_unit.group(2) # التقاط (USD) أو (Tons)
                else:
                    # الخطة البديلة إذا كانت السنة رقماً فقط
                    match_year_only = re.search(r'^(\d{4})', str(c).strip())
                    if match_year_only:
                        year_cols.append(c)
                        year_map[c] = int(match_year_only.group(1))
                        if not unit_str:
                            unit_str = "غير محدد"
                    
            if year_cols:
                melted = pd.melt(df, id_vars=[r_col, p_col, pr_col], value_vars=year_cols, var_name="y_raw", value_name="القيمة")
                
                melted = melted.rename(columns={
                    r_col: "الدولة المصدرة",
                    p_col: "الدولة المستوردة",
                    pr_col: "المحصول"
                })
                
                # 🎯 دمج الوحدة مع اسم المحصول لكي يظهر بوضوح للمحلل الاقتصادي
                if unit_str and unit_str != "غير محدد":
                    indicator = "قيمة" if "usd" in unit_str.lower() else ("كمية" if "ton" in unit_str.lower() else "مؤشر")
                    melted["المحصول"] = melted["المحصول"].astype(str) + f" [{indicator}: {unit_str}]"
                
                melted["السنة"] = melted["y_raw"].map(year_map)
                melted["القيمة"] = pd.to_numeric(melted["القيمة"].astype(str).str.replace(',', '').str.replace(' ', ''), errors='coerce')
                melted = melted.dropna(subset=["القيمة"])
                
                if not melted.empty:
                    all_data.append(melted[["الدولة المصدرة", "الدولة المستوردة", "المحصول", "السنة", "القيمة"]])

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()

def get_tm_reporters():
    df = load_trade_data()
    if not df.empty:
        return sorted(list(df["الدولة المصدرة"].unique()))
    return ["لا توجد بيانات"]

def get_tm_partners():
    df = load_trade_data()
    if not df.empty:
        return sorted(list(df["الدولة المستوردة"].unique()))
    return ["لا توجد بيانات"]

def get_tm_products():
    df = load_trade_data()
    if not df.empty:
        return sorted(list(df["المحصول"].unique()))
    return ["لا توجد بيانات"]

def fetch_trademap_data(reporter, partner, product, start_year, end_year):
    df = load_trade_data()
    if not df.empty:
        mask = (df["الدولة المصدرة"] == reporter) & (df["الدولة المستوردة"] == partner) & (df["المحصول"] == product)
        filtered = df[mask].copy()
        if not filtered.empty:
            filtered = filtered[(filtered["السنة"] >= start_year) & (filtered["السنة"] <= end_year)]
            if not filtered.empty:
                res = filtered[["السنة", "القيمة"]].copy()
                res["المتغير"] = f"TradeMap: {product}"
                return res
    return pd.DataFrame()