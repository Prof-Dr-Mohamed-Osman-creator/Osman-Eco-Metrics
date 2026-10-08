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

# 1. إعدادات الصفحة
st.set_page_config(page_title="Osman Eco-Metrics System", page_icon="📊", layout="wide")

# ==========================================
# 🧠 تأسيس الذاكرة المركزية للمنصة (Session State)
# ==========================================
if 'smart_memory' not in st.session_state:
    st.session_state['smart_memory'] = None  # الذاكرة فارغة في البداية

# 2. القائمة الجانبية
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

# 3. برمجة محتوى الأجنحة

if app_mode == "🏠 الصفحة الرئيسية":
    st.markdown("<h1 style='color: #2E86C1; text-align: center;'>📊 Osman Eco-Metrics System</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #34495E; text-align: center;'>المدرسة الإيكو-ديناميكية الرقمية | مختبر القياس المتعدد الشامل</h3>", unsafe_allow_html=True)
    st.info("👈 يرجى اختيار جناح التحليل من القائمة الجانبية.")

# ==========================================
# 🕸️ الجناح الأول: رادار الحصاد الآلي
# ==========================================
elif app_mode == "🕸️ رادار الحصاد الآلي للبيانات":
    st.markdown("<h1 style='color: #E67E22;'>🕸️ رادار الحصاد الآلي للبيانات</h1>", unsafe_allow_html=True)
    st.write("سيقوم الرادار بجلب البيانات الحية وحفظها مباشرة في **(ذاكرة المنصة)** ليقوم الذكاء الاصطناعي بتحليلها.")
    
    # 👈 هنا أضفنا قواعد بيانات الأمم المتحدة للقائمة!
    source = st.selectbox("اختر المنظمة الدولية:", [
        "البنك الدولي (World Bank)", 
        "منظمة الأغذية والزراعة (FAO)",
        "الأمم المتحدة - خريطة التجارة (TradeMap)",
        "الأمم المتحدة - كومتريد (UN Comtrade)"
    ])
    
    if st.button("بدء الحصاد 📡"):
        with st.spinner("جاري الاتصال بالسيرفرات الدولية وسحب البيانات..."):
            try:
                # محاكاة مؤقتة للبيانات لحين تفعيل الدوال الأساسية
                if source == "البنك الدولي (World Bank)":
                    df_result = pd.DataFrame({
                        "السنة": [2021, 2022, 2023],
                        "الناتج المحلي الإجمالي (مصر)": [404.14, 478.23, 395.93] 
                    })
                elif source == "منظمة الأغذية والزراعة (FAO)":
                    df_result = pd.DataFrame({
                        "المحصول": ["قمح", "أرز", "ذرة"],
                        "الإنتاج (مليون طن)": [9.0, 4.8, 7.5],
                        "السنة": [2023, 2023, 2023]
                    })
                elif source == "الأمم المتحدة - خريطة التجارة (TradeMap)":
                    df_result = pd.DataFrame({
                        "المحصول": ["فراولة (مجمدة)", "فاصوليا خضراء", "بصل"],
                        "مؤشر الاختراق السوقي": [0.85, 0.72, 0.65],
                        "كفاءة التصدير (%)": [88, 75, 80]
                    })
                elif source == "الأمم المتحدة - كومتريد (UN Comtrade)":
                    df_result = pd.DataFrame({
                        "كود HS": ["070190", "121291"],
                        "السلعة": ["بطاطس", "بنجر السكر"],
                        "قيمة الصادرات (ألف دولار)": [250000, 150000],
                        "السنة": [2023, 2023]
                    })
                
                # إيداع البيانات في الذاكرة المركزية
                st.session_state['smart_memory'] = df_result
                
                st.success("✅ تمت العملية بنجاح! تم التقاط البيانات وإيداعها في ذاكرة المنصة.")
                st.dataframe(df_result)
                st.info("الآن.. اذهب إلى جناح (المساعد الذكي Gemini) لتجعله يكتب تقريراً عن هذه الأرقام!")
                
            except Exception as e:
                st.error(f"حدث خطأ في الاتصال: {e}")
# ==========================================
# ✨ الجناح الثاني: المساعد الذكي وصياغة التقارير
# ==========================================
elif app_mode == "✨ المساعد الذكي وصياغة التقارير (Gemini AI)":
    st.markdown("<h1 style='color: #9B59B6;'>✨ المساعد الذكي (Gemini AI) وصياغة التقارير</h1>", unsafe_allow_html=True)
    
    # التحقق من ذاكرة المنصة
    if st.session_state['smart_memory'] is not None:
        st.success("🧠 عظيم! لقد وجدتُ بيانات مخزنة في الذاكرة قادمة من (رادار الحصاد).")
        st.write("البيانات الحالية:")
        st.dataframe(st.session_state['smart_memory'])
        
        if st.button("📝 توليد تقرير علمي عن هذه البيانات 🪄"):
            try:
                import google.generativeai as genai
                api_key = st.secrets["GEMINI_API_KEY"]
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-pro-latest')
                
                # تحويل الجدول إلى نص ليفهمه الذكاء الاصطناعي
                data_string = st.session_state['smart_memory'].to_string()
                
                with st.spinner("جاري صياغة التقرير الأكاديمي بناءً على بيانات الرادار..."):
                    prompt = f"""
                    أنت خبير اقتصادي وإحصائي في "المدرسة الإيكو-ديناميكية".
                    إليك هذا الجدول الإحصائي الذي تم سحبه من المنظمات الدولية:
                    {data_string}
                    
                    قم بكتابة تقرير أكاديمي رصين يحلل هذه الأرقام، واذكر دلالاتها الاقتصادية المحتملة بلغة علمية دقيقة.
                    """
                    response = model.generate_content(prompt)
                    
                st.success("اكتمل التقرير!")
                st.write(response.text)
                
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
    st.write("جاري ربط الخوارزميات وبناء هذا الجناح...")
