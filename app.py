import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

import config
from router import process_request
from api_worldbank import fetch_all_countries, fetch_worldbank_data
from api_faostat import get_fao_countries, get_fao_crops, get_fao_indicators, fetch_agricultural_data
from api_trademap import get_tm_reporters, get_tm_partners, get_tm_products, fetch_trademap_data
from api_comtrade import get_comtrade_countries, get_comtrade_flows, get_comtrade_products, get_hs_code, fetch_comtrade_data

# ==========================================
# إعدادات الصفحة
# ==========================================
st.set_page_config(page_title="Osman Eco-Metrics System", page_icon="🌍", layout="wide")

st.title("📊 Osman Eco-Metrics System")
st.subheader("المدرسة الإيكو-ديناميكية الرقمية | مختبر القياس المتعدد")
st.markdown("---")

@st.cache_data
def load_local_indicators(lang_code):
    file_name = "wb_indicators_ar.csv" if lang_code == "ar" else "wb_indicators_en.csv"
    try:
        df = pd.read_csv(file_name)
        return dict(zip(df["اسم المتغير"], df["كود المتغير"]))
    except Exception as e:
        return {"GDP": "NY.GDP.MKTP.CD"}

@st.cache_data
def load_wb_countries(lang):
    return fetch_all_countries(lang)

@st.cache_data(show_spinner=False)
def fetch_data_cached(source, param1, param2, start, end, param3="", param4="", param5=""):
    if source == "dynamic_wb":
        return fetch_worldbank_data(param1, param2, start, end)
    elif source == "fao_agri":
        return fetch_agricultural_data(param3, param1, param2, start, end)
    elif source == "trademap":
        return fetch_trademap_data(param1, param2, param3, start, end)
    elif source == "comtrade":
        return fetch_comtrade_data(param1, param2, param3, param4, start, end, param5)
    else:
        return process_request(param1, param2, param3, start, end)

if 'is_analyzing' not in st.session_state:
    st.session_state.is_analyzing = False

# ==========================================
# لوحة التحكم الجانبية
# ==========================================
with st.sidebar:
    st.markdown("### ⚙ لوحة التحكم")
    lang_choice = st.radio("لغة المؤشرات:", ["العربية", "English"], horizontal=True)
    lang_code = "ar" if lang_choice == "العربية" else "en"
    
    wb_indicators_dict = load_local_indicators(lang_code)
    wb_countries_dict = load_wb_countries(lang_code)
    
    st.markdown("---")
    st.markdown("**1. تحديد سلة المتغيرات**")
    
    sector_options = ["🌍 الفهرس الشامل للبنك الدولي", "🌱 البيانات الزراعية (FAO)", "🚢 بيانات التجارة الدولية (Trade Map)", "🇺🇳 مصفوفة الأمم المتحدة الحية (UN Comtrade)"] + list(config.DATA_ROUTING_MAP.keys())
    sector = st.selectbox("القطاع الاقتصادي:", sector_options)
    
    if sector == "🌍 الفهرس الشامل للبنك الدولي":
        indicator_names = st.multiselect("اختر المتغيرات:", list(wb_indicators_dict.keys()), max_selections=5)
        source_type = "dynamic_wb"
        
    elif sector == "🌱 البيانات الزراعية (FAO)":
        selected_crops = st.multiselect("اختر المحاصيل الاستراتيجية:", get_fao_crops())
        selected_indicators = st.multiselect("اختر المؤشرات الزراعية:", get_fao_indicators())
        indicator_names = [f"{c} - {i}" for c in selected_crops for i in selected_indicators]
        source_type = "fao_agri"
        
    elif sector == "🚢 بيانات التجارة الدولية (Trade Map)":
        country_name = st.selectbox("الدولة المصدرة:", get_tm_reporters())
        tm_partner = st.selectbox("الدولة المستوردة:", get_tm_partners())
        selected_tm_products = st.multiselect("اختر المنتجات:", get_tm_products())
        indicator_names = [f"TradeMap: {p}" for p in selected_tm_products]
        source_type = "trademap"
        
    elif sector == "🇺🇳 مصفوفة الأمم المتحدة الحية (UN Comtrade)":
        un_api_key = "71a6e635d5c922fc7f8a4b2659819edb"
        
        c1, c2 = st.columns(2)
        comtrade_reporter = c1.selectbox("الدولة:", get_comtrade_countries())
        comtrade_partner = c2.selectbox("الشريك التجاري:", get_comtrade_countries(), index=1)
        
        comtrade_flow = st.radio("نوع التدفق:", get_comtrade_flows(), horizontal=True)
        comtrade_name = st.selectbox("المحصول / المنتج:", get_comtrade_products())
        comtrade_hs = get_hs_code(comtrade_name)
        
        flow_ar = "صادرات" if "Exports" in comtrade_flow else "واردات"
        indicator_names = [f"UN Comtrade: {flow_ar} {comtrade_name} ({comtrade_hs}) [القيمة: USD]"]
        source_type = "comtrade"
        
    else:
        single_ind = st.selectbox("المتغير التحليلي:", list(config.DATA_ROUTING_MAP[sector].keys()))
        indicator_names = [single_ind]
        source_type = "static_router"
        
    st.markdown("**2. النطاق الزمني والمكاني**")
    if source_type == "dynamic_wb":
        country_name = st.selectbox("الدولة المستهدفة:", list(wb_countries_dict.keys()))
    elif source_type == "fao_agri":
        country_name = st.selectbox("الدولة المستهدفة:", get_fao_countries())
    elif source_type in ["trademap", "comtrade"]:
        pass 
    else:
        country_name = st.selectbox("الدولة المستهدفة:", list(config.SUPPORTED_COUNTRIES.keys()))
        
    start_year, end_year = st.slider("الفترة الزمنية:", 1960, 2026, (2000, 2023))
    
    st.markdown("---")
    run_button = st.button("🚀 بناء النماذج القياسية", use_container_width=True)
    if run_button and len(indicator_names) > 0:
        st.session_state.is_analyzing = True
        
    st.markdown("---")
    st.info("👨‍🏫 **Founder:** Prof.Dr. Mohamed Osman (Egypt)")

# ==========================================
# مختبر التحليل وقاعدة البيانات
# ==========================================
if st.session_state.is_analyzing and len(indicator_names) > 0:
    with st.spinner("جاري سحب وتوحيد المصفوفات من السيرفرات الدولية..."):
        df_merged = pd.DataFrame()
        
        for ind_name in indicator_names:
            if source_type == "dynamic_wb":
                df_temp = fetch_data_cached("dynamic_wb", wb_countries_dict[country_name], wb_indicators_dict[ind_name], start_year, end_year)
            elif source_type == "fao_agri":
                crop, ind = ind_name.split(" - ")
                df_temp = fetch_data_cached("fao_agri", crop, ind, start_year, end_year, country_name)
            elif source_type == "trademap":
                df_temp = fetch_data_cached("trademap", country_name, tm_partner, start_year, end_year, ind_name.replace("TradeMap: ", ""))
            elif source_type == "comtrade":
                df_temp = fetch_data_cached("comtrade", comtrade_reporter, comtrade_partner, start_year, end_year, comtrade_flow, comtrade_hs, un_api_key)
            else:
                df_temp = fetch_data_cached("static_router", sector, ind_name, start_year, end_year, country_name)
            
            if not df_temp.empty:
                if source_type == "comtrade" and "المتغير" in df_temp.columns:
                    df_temp["المتغير"] = comtrade_name + " (" + df_temp["المتغير"] + ")"
                    df_pivot = pd.pivot_table(df_temp, index="السنة", columns="المتغير", values="القيمة", aggfunc='sum').reset_index()
                    df_pivot["السنة"] = df_pivot["السنة"].astype(int)
                    if df_merged.empty:
                        df_merged = df_pivot
                    else:
                        df_merged = pd.merge(df_merged, df_pivot, on="السنة", how="outer")
                else:
                    df_temp = df_temp[["السنة", "القيمة"]].rename(columns={"القيمة": ind_name})
                    df_temp["السنة"] = df_temp["السنة"].astype(int)
                    if df_merged.empty:
                        df_merged = df_temp
                    else:
                        df_merged = pd.merge(df_merged, df_temp, on="السنة", how="outer")
        
        if not df_merged.empty:
            df_merged = df_merged.sort_values(by="السنة").reset_index(drop=True)
            st.success(f"✅ اكتمل بناء المصفوفة بنجاح!")
            
            tab_data, tab_lab = st.tabs(["📊 قاعدة البيانات", "🔬 مختبر الاقتصاد القياسي"])
            
            with tab_data:
                if source_type == "trademap":
                    display_title = f"{country_name} ➔ {tm_partner}"
                elif source_type == "comtrade":
                    if comtrade_partner == "جميع الدول فردياً (All Partners)":
                        display_title = f"{comtrade_reporter} ➔ جميع دول العالم (تحليل الأهمية النسبية)"
                    else:
                        display_title = f"{comtrade_reporter} ➔ {comtrade_partner}"
                else:
                    display_title = country_name
                    
                st.markdown(f"### 📈 التطور الزمني للمتغيرات ({display_title})")
                df_chart = df_merged.set_index("السنة")
                
                fig = px.line(df_chart, markers=True, title=f"تحليل تدفقات البيانات")
                fig.update_layout(xaxis_title="السنوات", yaxis_title="القيمة", xaxis=dict(type='category'))
                st.plotly_chart(fig, use_container_width=True)
                
                with st.expander("📂 عرض المصفوفة الزمنية (الجدول الرقمي)"):
                    st.dataframe(df_merged, use_container_width=True)
                    
            with tab_lab:
                st.markdown("### 🔬 مختبر التحليل القياسي")
                analysis_vars = [col for col in df_merged.columns if col != "السنة"]
                
                if len(analysis_vars) > 0:
                    df_clean = df_merged.dropna()
                    if len(df_clean) > 3:
                        st.markdown("#### 1️⃣ الإحصاء الوصفي (Descriptive Statistics)")
                        st.dataframe(df_clean[analysis_vars].describe().T, use_container_width=True)
                        
                        st.markdown("#### 2️⃣ اختبار استقرار السلاسل الزمنية (ADF Test)")
                        for var in analysis_vars:
                            try:
                                adf_test = adfuller(df_clean[var])
                                p_value = adf_test[1]
                                status = "مستقرة (Stationary)" if p_value < 0.05 else "غير مستقرة (Non-Stationary)"
                                st.write(f"- **{var}**: p-value = {p_value:.4f} ➔ **{status}**")
                            except:
                                st.write(f"- **{var}**: السلسلة أقصر من المطلوب لإجراء الاختبار.")
                                
                        st.markdown("#### 3️⃣ نمذجة الانحدار (OLS Regression)")
                        if len(analysis_vars) == 1:
                            st.info("بما أنك اخترت متغيراً واحداً، سيتم تقدير معادلة الاتجاه العام الزمني (Time Trend).")
                            y = df_clean[analysis_vars[0]]
                            X = sm.add_constant(df_clean["السنة"])
                            model = sm.OLS(y, X).fit()
                            st.code(model.summary().as_text())
                        elif len(analysis_vars) > 1:
                            c1, c2 = st.columns(2)
                            y_var = c1.selectbox("المتغير التابع (Y):", analysis_vars)
                            x_vars = c2.multiselect("المتغيرات المستقلة (X):", [v for v in analysis_vars if v != y_var], default=[v for v in analysis_vars if v != y_var][0:1])
                            
                            if x_vars:
                                y = df_clean[y_var]
                                X = sm.add_constant(df_clean[x_vars])
                                model = sm.OLS(y, X).fit()
                                st.code(model.summary().as_text())
                            else:
                                st.warning("يرجى اختيار متغير مستقل (X) واحد على الأقل لتشغيل النموذج.")
                    else:
                        st.warning("عدد المشاهدات غير كافٍ لإجراء التحليل القياسي بعد حذف القيم المفقودة.")
                else:
                    st.warning("لا توجد متغيرات كافية لإجراء التحليل.")

st.success("Osman Eco-Metrics System | Designed by: Prof.Dr. Mohamed Osman (Egypt) © 2026")