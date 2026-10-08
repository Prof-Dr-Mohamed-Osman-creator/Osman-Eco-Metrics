import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

import config
from router import process_request
from api_worldbank import fetch_all_countries, fetch_worldbank_data
from api_faostat import get_fao_countries, get_fao_crops, get_fao_indicators, fetch_agricultural_data
from api_trademap import get_tm_reporters, get_tm_partners, get_tm_products, fetch_trademap_data
from api_comtrade import get_comtrade_countries, get_comtrade_flows, get_comtrade_products, get_hs_code, fetch_comtrade_data

# استدعاء دوالك الأساسية التي برمجناها
try:
    from api_worldbank import fetch_all_countries, fetch_worldbank_data
except ImportError:
    pass # سيتم تجاوز الخطأ مؤقتاً لتجنب توقف المنصة إذا كان هناك تعديل في الملفات

# ==========================================
# 🧠 إعدادات الصفحة والذاكرة المركزية
# ==========================================
st.set_page_config(page_title="Osman Eco-Metrics System", page_icon="📊", layout="wide")

if 'smart_memory' not in st.session_state:
    st.session_state['smart_memory'] = None

# ==========================================
# 🚀 القائمة الجانبية (الأجنحة)
# ==========================================
st.sidebar.title("🚀 أجنحة المختبر الرقمي")
st.sidebar.markdown("---")

app_mode = st.sidebar.radio(
    "اختر الجناح المطلوب:",
    [
        "🏠 الصفحة الرئيسية",
        "🕸️ رادار الحصاد الآلي للبيانات",
        "📂 بوابة البيانات الشاملة (استبيانات وسلاسل)",
        "📊 الإحصاء الوصفي وتوزيع البيانات",
        "📈 الإحصاء الاستدلالي (Parametric & Non-Parametric)",
        "📉 النماذج القياسية والتنبؤ (Econometrics)",
        "✨ المساعد الذكي وصياغة التقارير (Gemini AI)",
        "📖 موسوعة المدرسة الإيكو-ديناميكية",
        "🧠 القياس النفسي وتأكيد المقاييس (Psychometrics)",
        "⚙️ بحوث العمليات (Operations Research)",
        "🤖 محاكي فاقد ما بعد الحصاد (Machine Learning)",
        "🌍 مرصد التنافسية التصديرية والبصمة المائية",
        "🎓 أكاديمية التدريب والدورات",
        "💬 مجتمع الباحثين (تواصل ومناقشات)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.success("Designed by: Prof. Dr. Mohamed Osman (Egypt) © 2026")

# ==========================================
# 🏠 الجناح الرئيسي
# ==========================================
if app_mode == "🏠 الصفحة الرئيسية":
    st.markdown("<h1 style='color: #2E86C1; text-align: center;'>📊 Osman Eco-Metrics System</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #34495E; text-align: center;'>المدرسة الإيكو-ديناميكية الرقمية | مختبر القياس المتعدد الشامل</h3>", unsafe_allow_html=True)
    st.info("👈 يرجى اختيار جناح التحليل من القائمة الجانبية لتفعيل الخوارزميات.")

# ==========================================
# 🕸️ رادار الحصاد الآلي (النسخة الشاملة الحية)
# ==========================================
elif app_mode == "🕸️ رادار الحصاد الآلي للبيانات":
    st.markdown("<h1 style='color: #E67E22;'>🕸️ رادار الحصاد الآلي للبيانات</h1>", unsafe_allow_html=True)
    st.write("🌍 **وضع الاستكشاف الشامل:** الرادار متصل الآن بآلاف المتغيرات لجميع دول العالم.")
    
    source = st.selectbox("اختر المنظمة الدولية:", [
        "البنك الدولي (World Bank)", 
        "منظمة الأغذية والزراعة (FAO) - قيد التفعيل",
        "الأمم المتحدة - خريطة التجارة (TradeMap) - قيد التفعيل",
        "الأمم المتحدة - كومتريد (UN Comtrade)"
    ])
    
    if source == "البنك الدولي (World Bank)":
        # إضافة مفتاح اختيار اللغة
        lang = st.radio("🌐 لغة المؤشرات (Indicators Language):", ["العربية", "English"], horizontal=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                countries_dict = fetch_all_countries() 
                if isinstance(countries_dict, dict):
                    country_name = st.selectbox("اختر الدولة / Select Country:", list(countries_dict.keys()))
                    country_code = countries_dict[country_name]
                else:
                    country_code = st.selectbox("اختر كود الدولة:", countries_dict)
            except Exception as e:
                st.warning("جاري إعداد قائمة الدول...")
                country_code = st.text_input("أو أدخل كود الدولة يدوياً (مثال: EGY)", value="EGY")
                
        with col2:
            try:
                # قراءة الملف ديناميكياً بناءً على اختيار الباحث
                if lang == "العربية":
                    df_indicators = pd.read_csv("wb_indicators_ar.csv")
                    label_text = "ابحث واختر المؤشر (يوجد آلاف المؤشرات):"
                else:
                    df_indicators = pd.read_csv("wb_indicators_en.csv")
                    label_text = "Search & Select Indicator:"
                    
                indicator_name = st.selectbox(label_text, df_indicators.iloc[:, 0].tolist())
                indicator_code = df_indicators[df_indicators.iloc[:, 0] == indicator_name].iloc[0, 1]
            except Exception as e:
                st.warning(f"يرجى التأكد من مسار ملفات المؤشرات. الخطأ: {e}")
                indicator_code = st.text_input("أو أدخل كود المؤشر يدوياً:", value="NY.GDP.MKTP.CD")
                
        st.markdown("---")
        start_year, end_year = st.slider(
            "🗓️ حدد فترة السلسلة الزمنية / Select Time Period:", 
            min_value=1960, 
            max_value=2026, 
            value=(2000, 2023)
        )
                
        if st.button("بدء الحصاد الشامل 📡"):
            with st.spinner("جاري مسح قواعد البنك الدولي وسحب السلسلة الزمنية..."):
                try:
                    df_result = fetch_worldbank_data(country_code, indicator_code, start_year, end_year)
                    if df_result is not None and not df_result.empty:
                        st.session_state['smart_memory'] = df_result
                        st.success("✅ تمت العملية بنجاح! تم التقاط السلسلة الزمنية وحفظها في ذاكرة المنصة.")
                        st.dataframe(df_result)
                    else:
                        st.warning("عفواً، لا توجد بيانات مسجلة لهذا المؤشر في هذه الدولة للفترة المحددة.")
                except Exception as e:
                    st.error(f"حدث خطأ أثناء جلب البيانات: {e}")
                    
    elif source == "منظمة الأغذية والزراعة (FAO) - قيد التفعيل":
        st.info("جاري تجهيز دوال الحصاد الشامل لمنظمة الأغذية والزراعة (FAO).")
        
    elif source == "الأمم المتحدة - خريطة التجارة (TradeMap) - قيد التفعيل":
        st.info("جاري تجهيز دوال الحصاد لبيانات خريطة التجارة (TradeMap).")
        
    elif source == "الأمم المتحدة - كومتريد (UN Comtrade)":
        st.markdown("<h3 style='color: #2980B9;'>🇺🇳 رادار الأمم المتحدة (سلة التنافسية التصديرية الشاملة)</h3>", unsafe_allow_html=True)
        st.write("🌍 تم ربط الرادار بالأدلة الشاملة للأمم المتحدة (آلاف السلع والدول).")
        
        # --- الصف الأول: سلة الدول والسلع ---
        col1, col2 = st.columns(2)
        with col1:
            try:
                df_un_countries = pd.read_csv("comtrade_countries.csv")
                df_un_countries['Display'] = df_un_countries['Country_Name'].astype(str) + " (" + df_un_countries['Country_Code'].astype(str) + ")"
                un_countries_dict = dict(zip(df_un_countries['Display'], df_un_countries['Country_Code'].astype(str)))
                
                selected_countries_names = st.multiselect(
                    "🛒 اختر الدول (الشركاء/المنافسين):", 
                    options=list(un_countries_dict.keys()), 
                    default=["Egypt (818)"] if "Egypt (818)" in un_countries_dict else [],
                    max_selections=10
                )
                selected_countries = [un_countries_dict[name] for name in selected_countries_names]
            except:
                st.error("لم يتم العثور على ملف comtrade_countries.csv.")
                selected_countries = []

        with col2:
            try:
                df_un_products = pd.read_csv("comtrade_products.csv")
                df_un_products['Display'] = df_un_products['Product_Name'].astype(str) + " (" + df_un_products['HS_Code'].astype(str) + ")"
                un_products_dict = dict(zip(df_un_products['Display'], df_un_products['HS_Code'].astype(str)))
                
                selected_commodities_names = st.multiselect(
                    "🛒 ابحث واختر السلع (HS Codes):", 
                    options=list(un_products_dict.keys()), 
                    max_selections=10
                )
                selected_commodities = [un_products_dict[name] for name in selected_commodities_names]
            except:
                st.error("لم يتم العثور على ملف comtrade_products.csv.")
                selected_commodities = []
                
        # --- الصف الثاني: التدفق التجاري والمتغيرات ---
        st.markdown("---")
        col3, col4 = st.columns(2)
        with col3:
            trade_flow_name = st.selectbox(
                "🔄 التدفق التجاري (Trade Flow):", 
                ["صادرات (Exports)", "واردات (Imports)", "إعادة تصدير (Re-Exports)"]
            )
            if "صادرات" in trade_flow_name: flow_code = "X"
            elif "واردات" in trade_flow_name: flow_code = "M"
            else: flow_code = "RX"
        with col4:
            target_metric = st.selectbox(
                "📏 المتغير الاقتصادي (Metric):", 
                ["القيمة بالدولار (Trade Value)", "الكمية / الوزن الصافي (Net Weight)", "كلاهما (Value & Weight)"]
            )
            
        st.markdown("---")
        start_year_un, end_year_un = st.slider(
            "🗓️ حدد فترة السلسلة الزمنية للمقارنة:", 
            min_value=2010, 
            max_value=2026, 
            value=(2018, 2023),
            key="un_slider"
        )
        
        if st.button("بدء حصاد سلة الأمم المتحدة الشاملة 📡"):
            if len(selected_countries) > 0 and len(selected_commodities) > 0:
                with st.spinner("جاري الاتصال بقواعد بيانات UN Comtrade العالمية..."):
                    try:
                        try:
                            comtrade_key = st.secrets["COMTRADE_API_KEY"]
                        except:
                            comtrade_key = "" 
                        
                        # --- رادار فحص المفتاح السري المنسق برمجياً ---
                        if comtrade_key == "":
                            st.error("المنصة لا ترى المفتاح! تأكد من كتابة COMTRADE_API_KEY في الـ Secrets في إعدادات التطبيق.")
                        else:
                            st.success("✅ المنصة نجحت في قراءة المفتاح السري من الخزنة وتستعد للاتصال!")
                            
                            # استدعاء دالة الحصاد
                            df_un_result = fetch_comtrade_data(
                                selected_countries, 
                                selected_commodities, 
                                start_year_un, 
                                end_year_un, 
                                comtrade_key,
                                flow_code,       
                                target_metric    
                            )
                            
                            if df_un_result is not None and not df_un_result.empty:
                                st.session_state['smart_memory'] = df_un_result
                                st.success("🎉 تمت العملية بنجاح! تم سحب بيانات السلة من خوادم الأمم المتحدة.")
                                st.dataframe(df_un_result)
                            else:
                                st.warning("الخادم لم يُرجع أي بيانات لهذه السلة في هذه السنوات (قد يكون الخطأ 401 أو لا توجد داتا).")
                    
                    except TypeError as e:
                        st.error(f"يرجى تحديث دالة fetch_comtrade_data في ملف api_comtrade.py لتستقبل المتغيرات الجديدة. الخطأ: {e}")
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء جلب البيانات: {e}")
            else:
                st.warning("يرجى اختيار دولة واحدة وسلعة واحدة على الأقل.")
# ==========================================
# ✨ المساعد الذكي وصياغة التقارير
# ==========================================
elif app_mode == "✨ المساعد الذكي وصياغة التقارير (Gemini AI)":
    st.markdown("<h1 style='color: #9B59B6;'>✨ المساعد الذكي (Gemini AI) وصياغة التقارير</h1>", unsafe_allow_html=True)
    
    if st.session_state['smart_memory'] is not None:
        st.success("🧠 عظيم! لقد وجدتُ بيانات مخزنة في الذاكرة قادمة من (رادار الحصاد).")
        st.write("البيانات الحالية:")
        st.dataframe(st.session_state['smart_memory'])
        
        if st.button("📝 توليد تقرير علمي عن هذه البيانات 🪄"):
            try:
                import google.generativeai as genai
                api_key = st.secrets["GEMINI_API_KEY"]
                genai.configure(api_key=api_key)
                
                model = genai.GenerativeModel('gemini-3.8-flash')
                data_string = st.session_state['smart_memory'].to_string()
                
                prompt = f"""
                أنت خبير اقتصادي وإحصائي في "المدرسة الإيكو-ديناميكية".
                إليك هذا الجدول الإحصائي الذي تم سحبه من المنظمات الدولية:
                {data_string}
                
                قم بكتابة تقرير أكاديمي رصين يحلل هذه الأرقام، واذكر دلالاتها الاقتصادية المحتملة بلغة علمية دقيقة.
                """
                
                st.success("بدأت صياغة التقرير...")
                # إنشاء مربع نصي فارغ لنقوم بتحديثه لحظة بلحظة
                report_placeholder = st.empty()
                full_response = ""
                
                # تفعيل البث المباشر (stream=True)
                response = model.generate_content(prompt, stream=True)
                
                # طباعة الكلمات فور وصولها من السيرفر
                for chunk in response:
                    full_response += chunk.text
                    report_placeholder.markdown(full_response + "▌") # إضافة مؤشر الكتابة النابض
                
                # تثبيت النص النهائي
                report_placeholder.markdown(full_response)
                
            except Exception as e:
                st.error(f"النظام اكتشف الخطأ الحقيقي وهو: {e}")
    else:
        st.info("الذاكرة المركزية فارغة حالياً. اذهب أولاً إلى (رادار الحصاد الآلي) لجلب بيانات، أو أدخل نتائجك يدوياً بالأسفل.")
        
    st.markdown("---")
    user_input = st.text_area("أو أدخل نتائج أخرى يدوياً هنا:", height=150)
    if st.button("تحليل النص اليدوي"):
        st.warning("هذا الزر يعمل بنفس الآلية السابقة.. (سيتم برمجته لاحقاً)")

# ==========================================
# باقي الأجنحة (مؤقتة لحين اكتمالها)
# ==========================================
else:
    st.markdown(f"<h1 style='color: #7F8C8D;'>{app_mode}</h1>", unsafe_allow_html=True)
    st.write("...جاري ربط الخوارزميات وبناء هذا الجناح...")
