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

# 2. القائمة الجانبية
st.sidebar.title("🚀 أجنحة المختبر الرقمي")
st.sidebar.markdown("---")

app_mode = st.sidebar.radio(
    "اختر الجناح المطلوب:",
    [
        "🏠 الصفحة الرئيسية",
        "📖 موسوعة المدرسة الإيكو-ديناميكية",
        "🕸️ رادار الحصاد الآلي للبيانات",
        "📂 بوابة البيانات الشاملة (استبيانات وسلاسل)",
        "📊 الإحصاء الوصفي وتوزيع البيانات",
        "🧠 القياس النفسي وتأكيد المقاييس (Psychometrics)",
        "📈 الإحصاء الاستدلالي (Parametric & Non-Parametric)",
        "📉 النماذج القياسية والتنبؤ (Econometrics)",
        "⚙️ بحوث العمليات (Operations Research)",
        "🤖 محاكي فاقد ما بعد الحصاد (Machine Learning)",
        "🌍 مرصد التنافسية التصديرية والبصمة المائية",
        "🎓 أكاديمية التدريب والدورات",
        "💬 مجتمع الباحثين (تواصل ومناقشات)",
        "✨ المساعد الذكي وصياغة التقارير (Gemini AI)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.success("Designed by: Prof. Dr. Mohamed Osman (Egypt) © 2026")

# 3. برمجة محتوى الأجنحة بالألوان الزاهية (HTML Injection)

if app_mode == "🏠 الصفحة الرئيسية":
    st.markdown("<h1 style='color: #2E86C1; text-align: center;'>📊 Osman Eco-Metrics System</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #34495E; text-align: center;'>المدرسة الإيكو-ديناميكية الرقمية | مختبر القياس المتعدد الشامل</h3>", unsafe_allow_html=True)
    st.markdown("---")
    st.info("👈 يرجى اختيار جناح التحليل من القائمة الجانبية للبدء بالتحليق في سماء البيانات.")

elif app_mode == "🕸️ رادار الحصاد الآلي للبيانات":
    st.markdown("<h1 style='color: #E67E22;'>🕸️ رادار الحصاد الآلي للبيانات</h1>", unsafe_allow_html=True)
    st.write("أداة ذكية تتصل بقواعد البيانات العالمية لجلب أحدث الإحصاءات وتحديث المؤشرات داخل المنصة تلقائياً.")
    st.selectbox("اختر مصدر البيانات:", ["FAO", "البنك الدولي", "الجهاز المركزي للإحصاء"])

elif app_mode == "🎓 أكاديمية التدريب والدورات":
    st.markdown("<h1 style='color: #8E44AD;'>🎓 أكاديمية التدريب والدورات</h1>", unsafe_allow_html=True)
    st.write("منصة التعليم التفاعلي للباحثين والطلاب.")
    st.selectbox("اختر الدورة:", ["نظريات التنمية الاقتصادية", "تطبيقات بايثون القياسية"])

elif app_mode == "📖 موسوعة المدرسة الإيكو-ديناميكية":
    st.markdown("<h1 style='color: #D4AC0D;'>📖 موسوعة المدرسة الإيكو-ديناميكية</h1>", unsafe_allow_html=True)
    st.warning("هذا الجناح قيد الإعداد المكتبي وسيمثل الثورة النظرية القادمة في علم الاقتصاد.")

elif app_mode == "📂 بوابة البيانات الشاملة (استبيانات وسلاسل)":
    st.markdown("<h1 style='color: #16A085;'>📂 بوابة البيانات الشاملة</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("قم برفع ملف البيانات هنا", type=["csv", "xlsx"])

elif app_mode == "🤖 محاكي فاقد ما بعد الحصاد (Machine Learning)":
    st.markdown("<h1 style='color: #C0392B;'>🤖 محاكي فاقد ما بعد الحصاد</h1>", unsafe_allow_html=True)
    st.write("تطبيق النماذج الهجينة للتعلم الآلي لتقدير الفاقد الزراعي.")

elif app_mode == "🌍 مرصد التنافسية التصديرية والبصمة المائية":
    st.markdown("<h1 style='color: #27AE60;'>🌍 مرصد التنافسية والبصمة المائية</h1>", unsafe_allow_html=True)
    st.write("لوحات تفاعلية لقياس الاختراق السوقي وكفاءة التصدير للمحاصيل المصرية.")

elif app_mode == "💬 مجتمع الباحثين (تواصل ومناقشات)":
    st.markdown("<h1 style='color: #2980B9;'>💬 مجتمع الباحثين</h1>", unsafe_allow_html=True)
    st.text_area("شارك استفسارك أو بياناتك مع المجتمع:")

elif app_mode == "✨ المساعد الذكي وصياغة التقارير (Gemini AI)":
    st.markdown("<h1 style='color: #9B59B6;'>✨ المساعد الذكي (Gemini AI) وصياغة التقارير</h1>", unsafe_allow_html=True)
    st.write("هنا يتواجد رفيقك العلمي الرقمي! أدخل نتائجك الإحصائية، وسيقوم الذكاء الاصطناعي بصياغتها في تقرير أكاديمي رصين وترجمتها لأي لغة.")
    st.text_area("أدخل أرقامك أو نتائجك الإحصائية هنا:")
    st.button("توليد التقرير العلمي 🪄")

else:
    st.markdown(f"<h1 style='color: #7F8C8D;'>{app_mode}</h1>", unsafe_allow_html=True)
    st.write("جاري بناء الخوارزميات الدقيقة لهذا الجناح...")
