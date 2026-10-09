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
import streamlit as st
import pandas as pd
# (باقي الاستدعاءات التي لديك في أعلى الملف تبقى كما هي)

# --- 1. مفتاح اختيار اللغة (Language Switcher) ---
# نجعل الإنجليزية في الفهرس 0 لتكون هي الافتراضية
st.sidebar.markdown("---")
selected_lang = st.sidebar.selectbox("🌐 Select Language / اختر اللغة", ["English", "العربية"], index=0)
st.sidebar.markdown("---")

# --- 2. القاموس اللغوي (Translation Dictionary) ---
lang_dict = {
    "English": {
        "sys_title": "Osman Eco-Metrics System",
        "sys_subtitle": "Digital Eco-Dynamic School | Comprehensive Metrics Lab",
        "sidebar_header": "🚀 Digital Lab Wings",
        "menu_title": "Select Wing:",
        "home": "🏠 Home Page",
        "harvest": "🕸️ Automated Data Harvest",
        "data_portal": "📁 Comprehensive Data Portal",
        "desc_stats": "📊 Descriptive Statistics & Distribution",
        "inferential_stats": "📈 Inferential Statistics (Parametric & Non-Parametric)",
        "econometrics": "📉 Econometrics & Forecasting",
        "ai_assistant": "✨ Gemini AI Assistant",
        "eco_encyclopedia": "📖 Eco-Dynamic Encyclopedia",
        "psychometrics": "🧠 Psychometrics",
        "operations_research": "⚙️ Operations Research",
        "machine_learning": "🤖 Post-Harvest Loss Simulator (ML)",
        "competitiveness": "🌍 Export Competitiveness & Water Footprint",
        "academy": "🎓 Training Academy",
        "community": "💬 Researchers Community"
    },
    "العربية": {
        "sys_title": "Osman Eco-Metrics System",
        "sys_subtitle": "المدرسة الإيكو-ديناميكية الرقمية | مختبر القياس المتعدد الشامل",
        "sidebar_header": "🚀 أجنحة المختبر الرقمي",
        "menu_title": "اختر الجناح المطلوب:",
        "home": "🏠 الصفحة الرئيسية",
        "harvest": "🕸️ رادار الحصاد الآلي للبيانات",
        "data_portal": "📁 بوابة البيانات الشاملة (استبيانات وسلاسل)",
        "desc_stats": "📊 الإحصاء الوصفي وتوزيع البيانات",
        "inferential_stats": "📈 الإحصاء الاستدلالي (Parametric & Non-Parametric)",
        "econometrics": "📉 النماذج القياسية والتنبؤ (Econometrics)",
        "ai_assistant": "✨ المساعد الذكي وصياغة التقارير (Gemini AI)",
        "eco_encyclopedia": "📖 موسوعة المدرسة الإيكو-ديناميكية",
        "psychometrics": "🧠 القياس النفسي وتأكيد المقاييس (Psychometrics)",
        "operations_research": "⚙️ بحوث العمليات (Operations Research)",
        "machine_learning": "🤖 محاكي فاقد ما بعد الحصاد (Machine Learning)",
        "competitiveness": "🌍 مرصد التنافسية التصديرية والبصمة المائية",
        "academy": "🎓 أكاديمية التدريب والدورات",
        "community": "💬 مجتمع الباحثين (تواصل ومناقشات)"
    }
}

# نخصص المتغير 't' ليحمل كلمات اللغة التي اختارها الباحث
t = lang_dict[selected_lang]

# --- 3. بناء القائمة الجانبية بجميع الأجنحة باللغة المختارة ---
st.sidebar.markdown(f"### {t['sidebar_header']}")

page = st.sidebar.radio(
    t["menu_title"],
    [
        t["home"], 
        t["harvest"], 
        t["data_portal"],
        t["desc_stats"],
        t["inferential_stats"],
        t["econometrics"],
        t["ai_assistant"],
        t["eco_encyclopedia"],
        t["psychometrics"],
        t["operations_research"],
        t["machine_learning"],
        t["competitiveness"],
        t["academy"],
        t["community"]
    ]
)

# --- 4. العناوين الرئيسية للمنصة باللغة المختارة ---
st.markdown(f"<h1 style='text-align: center; color: #2E86C1;'>📊 {t['sys_title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center; color: #5D6D7E;'>{t['sys_subtitle']}</h3>", unsafe_allow_html=True)
st.markdown("---")

st.sidebar.markdown("---")
st.sidebar.success("Designed by: Prof. Dr. Mohamed Osman (Egypt) © 2026")

# ==========================================
# 🏠 الجناح الرئيسي
# ==========================================
if page == t["home"]:
    # تم إزالة العناوين المكررة من هنا لأنها تظهر تلقائياً في أعلى الواجهة
    
    # رسالة إرشادية تتغير لغتها تلقائياً
    welcome_msg = "Please select an analytical wing from the sidebar to activate the algorithms." if selected_lang == "English" else "يرجى اختيار جناح التحليل من القائمة الجانبية لتفعيل الخوارزميات."
    
    st.info(f"👈 {welcome_msg}")

# ==========================================
# 🕸️ رادار الحصاد الآلي (النسخة الشاملة الحية)
# ==========================================
elif page == t["harvest"]:
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
# 5. التوجيه وفتح الأجنحة (Routing)
# ==========================================

if page == t["home"]:
    welcome_msg = "Please select an analytical wing from the sidebar to activate the algorithms." if selected_lang == "English" else "يرجى اختيار جناح التحليل من القائمة الجانبية لتفعيل الخوارزميات."
    st.info(f"👈 {welcome_msg}")

elif page == t["harvest"]:
    st.markdown("<h2 style='color: #2E86C1;'>🕸️ Automated Data Harvest | رادار الحصاد الآلي</h2>", unsafe_allow_html=True)
    # ⚠️ (اترك كود الحصاد الخاص بالبنك الدولي والأمم المتحدة هنا كما هو دون حذف) ⚠️

elif page == t["desc_stats"]:
    # --- قاموس الإحصاء الوصفي المدمج ---
    if selected_lang == "English":
        header_title = "📊 Descriptive Statistics & Distribution Tests"
        header_desc = "This wing provides a comprehensive suite of descriptive metrics, dispersion measures, and normality tests for the retrieved data."
        empty_msg = "👈 The table is currently empty! Please go to (Automated Data Harvest) to fetch data into the Smart Memory first."
        ready_msg = "✅ Data is ready on the analytical table!"
        select_col_msg = "🎯 Select the variable (column) to analyze:"
        btn_msg = "Serve Statistical Meal 🍽️"
        spinner_msg = "Algorithms are processing data and calculating metrics..."
        cat1, cat2, cat3, cat4 = "### 1️⃣ Central Tendency", "### 2️⃣ Dispersion", "### 3️⃣ Distribution Shape", "### 4️⃣ Kolmogorov-Smirnov Test (Normality)"
        m_mean, m_median, m_mode, m_geom, m_harm = "Mean", "Median", "Mode", "Geometric Mean", "Harmonic Mean"
        m_var, m_std, m_range, m_iqr, m_cv = "Variance", "Std Deviation", "Range", "IQR", "CV (%)"
        m_skew, m_kurt, m_mad = "Skewness", "Kurtosis", "Mean Abs Dev (MAD)"
        m_ks, m_pval = "K-S Statistic", "P-Value"
        ks_pass = "Result: Data follows a normal distribution (Fail to reject H0) ✅"
        ks_fail = "Result: Data does not follow a normal distribution (Reject H0) ❌"
        vis_title, hist_title, qq_title = "### 🎨 Data Visualization", "Histogram with Outliers Boxplot", "**Q-Q Plot for Normality**"
        no_num_msg = "The data in memory does not contain quantitative variables. Please check the data."
    else:
        header_title = "📊 مائدة الإحصاء الوصفي واختبارات التوزيع"
        header_desc = "يقدم هذا الجناح وجبة متكاملة من المقاييس الوصفية، مقاييس التشتت، واختبارات التوزيع الطبيعي للبيانات المستدعاة."
        empty_msg = "👈 المائدة فارغة حالياً! يرجى الذهاب إلى (رادار الحصاد) لجلب البيانات أولاً لتستقر في الذاكرة الذكية."
        ready_msg = "✅ البيانات جاهزة على المائدة البرمجية!"
        select_col_msg = "🎯 اختر المتغير (العمود) لتقديم وجبة الإحصاء الوصفي له:"
        btn_msg = "تقديم الوجبة الإحصائية 🍽️"
        spinner_msg = "الخوارزميات تقوم بطهي البيانات وحساب المقاييس..."
        cat1, cat2, cat3, cat4 = "### 1️⃣ مقبلات النزعة المركزية", "### 2️⃣ الطبق الرئيسي للتشتت", "### 3️⃣ شكل التوزيع", "### 4️⃣ اختبار كولومجروف-سميرنوف (الطبيعية)"
        m_mean, m_median, m_mode, m_geom, m_harm = "المتوسط الحسابي", "الوسيط", "المنوال", "المتوسط الهندسي", "المتوسط التوافقي"
        m_var, m_std, m_range, m_iqr, m_cv = "التباين", "الانحراف المعياري", "المدى", "الانحراف الربيعي (IQR)", "معامل الاختلاف (CV)"
        m_skew, m_kurt, m_mad = "الالتواء (Skewness)", "التفلطح (Kurtosis)", "الانحراف المتوسط"
        m_ks, m_pval = "إحصاء الاختبار (K-S)", "القيمة الاحتمالية (P-Value)"
        ks_pass = "نتيجة الاختبار: البيانات تتبع التوزيع الطبيعي (لا نرفض الفرض العدم) ✅"
        ks_fail = "نتيجة الاختبار: البيانات لا تتبع التوزيع الطبيعي (نرفض الفرض العدم) ❌"
        vis_title, hist_title, qq_title = "### 🎨 الرؤية البصرية للبيانات", "المدرج التكراري (Histogram) مع صندوق القيم الشاذة", "**رسم الـ Q-Q Plot للطبيعية**"
        no_num_msg = "البيانات الموجودة في الذاكرة لا تحتوي على متغيرات رقمية. يرجى التأكد من البيانات."

    # --- واجهة الجناح ---
    st.markdown(f"<h2 style='color: #2E86C1;'>{header_title}</h2>", unsafe_allow_html=True)
    st.write(header_desc)
    
    if 'smart_memory' not in st.session_state or st.session_state['smart_memory'].empty:
        st.info(empty_msg)
    else:
        df = st.session_state['smart_memory']
        st.success(ready_msg)
        
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        
        if len(numeric_cols) > 0:
            selected_col = st.selectbox(select_col_msg, numeric_cols)
            data_col = df[selected_col].dropna()
            
            if st.button(btn_msg):
                with st.spinner(spinner_msg):
                    import numpy as np
                    from scipy import stats
                    import plotly.express as px
                    import matplotlib.pyplot as plt
                    
                    # الحسابات الإحصائية
                    mean = np.mean(data_col)
                    median = np.median(data_col)
                    mode_result = stats.mode(data_col, keepdims=False)
                    mode = mode_result.mode if hasattr(mode_result, 'mode') else mode_result[0]
                    pos_data = data_col.loc[data_col > 0]
                    geom_mean = stats.gmean(pos_data) if not pos_data.empty else np.nan
                    harm_mean = stats.hmean(pos_data) if not pos_data.empty else np.nan
                    
                    data_range = np.ptp(data_col)
                    iqr = stats.iqr(data_col)
                    variance = np.var(data_col, ddof=1)
                    std_dev = np.std(data_col, ddof=1)
                    mad = (data_col - mean).abs().mean()
                    cv = (std_dev / mean) * 100 if mean != 0 else np.nan
                    
                    skewness = stats.skew(data_col)
                    kurtosis = stats.kurtosis(data_col)
                    
                    std_data = (data_col - mean) / std_dev
                    ks_stat, p_value = stats.kstest(std_data, 'norm')
                    
                    # العرض الديناميكي
                    st.markdown(cat1)
                    c1, c2, c3, c4, c5 = st.columns(5)
                    c1.metric(m_mean, f"{mean:.4f}")
                    c2.metric(m_median, f"{median:.4f}")
                    c3.metric(m_mode, f"{mode:.4f}")
                    c4.metric(m_geom, f"{geom_mean:.4f}")
                    c5.metric(m_harm, f"{harm_mean:.4f}")
                    
                    st.markdown(cat2)
                    d1, d2, d3, d4, d5 = st.columns(5)
                    d1.metric(m_var, f"{variance:.4f}")
                    d2.metric(m_std, f"{std_dev:.4f}")
                    d3.metric(m_range, f"{data_range:.4f}")
                    d4.metric(m_iqr, f"{iqr:.4f}")
                    d5.metric(m_cv, f"{cv:.2f}%")
                    
                    st.markdown(cat3)
                    s1, s2, s3 = st.columns(3)
                    s1.metric(m_skew, f"{skewness:.4f}")
                    s2.metric(m_kurt, f"{kurtosis:.4f}")
                    s3.metric(m_mad, f"{mad:.4f}")
                    
                    st.markdown(cat4)
                    k1, k2 = st.columns(2)
                    k1.metric(m_ks, f"{ks_stat:.4f}")
                    k2.metric(m_pval, f"{p_value:.4f}")
                    
                    if p_value > 0.05:
                        st.success(ks_pass)
                    else:
                        st.warning(ks_fail)
                        
                    st.markdown(vis_title)
                    vcol1, vcol2 = st.columns(2)
                    
                    with vcol1:
                        fig_hist = px.histogram(data_frame=df, x=selected_col, marginal="box", 
                                                title=hist_title, color_discrete_sequence=['#2E86C1'])
                        st.plotly_chart(fig_hist, use_container_width=True)
                        
                    with vcol2:
                        st.markdown(qq_title)
                        fig, ax = plt.subplots(figsize=(6, 4))
                        stats.probplot(data_col, dist="norm", plot=ax)
                        ax.set_title("")
                        ax.get_lines()[0].set_markerfacecolor('#2E86C1')
                        st.pyplot(fig)
        else:
            st.warning(no_num_msg)

# ==========================================
# باقي الأجنحة (مؤقتة لحين اكتمالها)
# ==========================================
else:
    st.markdown(f"<h2 style='color: #7F8C8D; text-align: center;'>{page}</h2>", unsafe_allow_html=True)
    
    if selected_lang == "English":
        st.info("🚧 Algorithms are currently being linked, and this wing is under construction...")
    else:
        st.info("🚧 جاري ربط الخوارزميات وبناء هذا الجناح...")
