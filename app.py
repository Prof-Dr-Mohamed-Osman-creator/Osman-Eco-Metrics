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
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 1. قائمة الدول الشاملة للسهولة (كما في البناء الأولي)
            comtrade_countries = {
                "مصر (Egypt)": "818", 
                "السعودية (Saudi Arabia)": "682", 
                "الإمارات (UAE)": "784", 
                "المغرب (Morocco)": "504", 
                "إسبانيا (Spain)": "724", 
                "تركيا (Turkey)": "792", 
                "أمريكا (USA)": "842", 
                "الصين (China)": "156", 
                "روسيا (Russia)": "643",
                "إيطاليا (Italy)": "380",
                "العالم (World)": "0"
            }
            selected_countries_names = st.multiselect(
                "🛒 اختر الدول المصدرة:", 
                options=list(comtrade_countries.keys()), 
                default=["مصر (Egypt)"],
                max_selections=10
            )
            selected_countries = [comtrade_countries[name] for name in selected_countries_names]

        with col2:
            # 2. قائمة المحاصيل بالاسم والكود (لإلغاء الإدخال اليدوي تماماً)
            comtrade_products = {
                "بطاطس طازجة أو مبردة (070190)": "070190",
                "بنجر السكر (121291)": "121291",
                "فراولة مجمدة (081110)": "081110",
                "فراولة طازجة (081010)": "081010",
                "فاصوليا خضراء (070820)": "070820",
                "بصل وثوم طازج (070310)": "070310",
                "طماطم طازجة أو مبردة (070200)": "070200",
                "قمح (100199)": "100199",
                "برتقال (080510)": "080510",
                "إجمالي الصادرات (TOTAL)": "TOTAL"
            }
            selected_commodities_names = st.multiselect(
                "🛒 اختر السلع (الاسم والكود):", 
                options=list(comtrade_products.keys()), 
                default=["بطاطس طازجة أو مبردة (070190)"],
                max_selections=10
            )
            selected_commodities = [comtrade_products[name] for name in selected_commodities_names]
            
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
                        # 3. جلب المفتاح السري بأمان
                        try:
                            comtrade_key = st.secrets["COMTRADE_API_KEY"]
                        except:
                            comtrade_key = "" # في حال لم تقم بإضافته بعد في إعدادات المنصة
                            
                        # 4. استدعاء الدالة مع تمرير كافة المتغيرات الناقصة (حسب رسالة الخطأ)
                        df_un_result = fetch_comtrade_data(
                            selected_countries, 
                            selected_commodities, 
                            start_year_un, 
                            end_year_un, 
                            comtrade_key
                        )
                        
                        if df_un_result is not None and not df_un_result.empty:
                            st.session_state['smart_memory'] = df_un_result
                            st.success(f"✅ تمت العملية بنجاح! تم سحب بيانات السلة.")
                            st.dataframe(df_un_result)
                            st.info("👈 بياناتك في الذاكرة الآن.. اذهب للمساعد الذكي لعمل تقرير الاختراق السوقي!")
                        else:
                            st.warning("الخادم لم يُرجع أي بيانات لهذه السلة في هذه السنوات.")
                    except TypeError as e:
                        st.error(f"عطل في ترتيب المتغيرات: {e}. (يرجى مراجعة ملف api_comtrade.py الخاص بك للتأكد من ترتيب استلام المتغيرات داخل الدالة).")
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
