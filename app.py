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
                # هذا السطر يجب أن يكون موجوداً ومزاحاً للداخل تحت else
                st.error("لم يتم العثور على بيانات مطابقة." if selected_lang == "العربية" else "No matching data found.")
# ==========================================
# 📈 الشاشة البصرية: رسم البيانات المحصودة مباشرة
# ==========================================
    if 'smart_memory' in st.session_state and isinstance(st.session_state['smart_memory'], pd.DataFrame) and not st.session_state['smart_memory'].empty:
                import plotly.express as px  # 👈 الاستدعاء السحري الذي كان مفقوداً!
                import pandas as pd
                
                st.markdown("---")
                st.markdown("<h3 style='color: #2E86C1;'>📈 النظرة البصرية السريعة / Quick Data Visualization</h3>", unsafe_allow_html=True)
                
                df_harvested = st.session_state['smart_memory'].copy()
                
                # المحول الذكي الإجباري: لاكتشاف الأرقام المتخفية
                for col in df_harvested.columns:
                    num_col = pd.to_numeric(df_harvested[col], errors='coerce')
                    if num_col.notna().sum() > 0:
                        if num_col.notna().sum() >= (len(df_harvested) * 0.3):
                            df_harvested[col] = num_col
    
                # استخراج الأعمدة
                numeric_cols_harvest = df_harvested.select_dtypes(include=['float64', 'int64']).columns.tolist()
                time_cols = [col for col in df_harvested.columns if any(keyword in col.lower() for keyword in ['year', 'date', 'time', 'سنة', 'عام', 'تاريخ'])]
                x_axis_default = time_cols[0] if time_cols else df_harvested.columns[0]
    
                if len(numeric_cols_harvest) > 0:
                    # إعداد قائمة أنواع الرسوم البيانية باللغتين
                    if selected_lang == "English":
                        chart_types = ["Line Chart 📈", "Bar Chart 📊", "Scatter Plot ⏺️", "Area Chart ⛰️", "Pie Chart 🥧"]
                        chart_label = "🎨 Select Chart Type:"
                    else:
                        chart_types = ["رسم خطي 📈", "أعمدة بيانية 📊", "شكل انتشار ⏺️", "مساحة متراكمة ⛰️", "دائرة نسبية 🥧"]
                        chart_label = "🎨 اختر نوع الرسم البياني:"
                        
                    chart_choice = st.selectbox(chart_label, chart_types)
                    st.markdown("---")
                    
                    hc1, hc2 = st.columns(2)
                    x_axis = hc1.selectbox("📍 اختر المتغير للمحور الأفقي / X-Axis Variable:", df_harvested.columns.tolist(), index=df_harvested.columns.tolist().index(x_axis_default))
                    y_axis = hc2.selectbox("📊 اختر المتغير للمحور الرأسي / Y-Axis Variable:", numeric_cols_harvest)
                    
                    tc1, tc2 = st.columns(2)
                    custom_x_name = tc1.text_input("✏️ اكتب اسماً مخصصاً للمحور الأفقي (اختياري) / Custom X Name:")
                    custom_y_name = tc2.text_input("✏️ اكتب اسماً مخصصاً للمحور الرأسي (اختياري) / Custom Y Name:")
                    
                    final_x_title = custom_x_name if custom_x_name.strip() != "" else x_axis
                    final_y_title = custom_y_name if custom_y_name.strip() != "" else y_axis
                    
                    chart_title = f"Data Visualization: {final_y_title} vs {final_x_title}" if selected_lang == "English" else f"التمثيل البصري: ({final_y_title}) مقابل ({final_x_title})"
    
                    try:
                        # رسم الخرائط
                        if "Line" in chart_choice or "خطي" in chart_choice:
                            fig_harvest = px.line(df_harvested, x=x_axis, y=y_axis, markers=True, title=chart_title)
                            fig_harvest.update_traces(line_color='#E74C3C')
                        elif "Bar" in chart_choice or "أعمدة" in chart_choice:
                            fig_harvest = px.bar(df_harvested, x=x_axis, y=y_axis, title=chart_title)
                            fig_harvest.update_traces(marker_color='#E74C3C')
                        elif "Scatter" in chart_choice or "انتشار" in chart_choice:
                            fig_harvest = px.scatter(df_harvested, x=x_axis, y=y_axis, title=chart_title)
                            fig_harvest.update_traces(marker_color='#E74C3C', marker_size=10)
                        elif "Area" in chart_choice or "مساحة" in chart_choice:
                            fig_harvest = px.area(df_harvested, x=x_axis, y=y_axis, title=chart_title)
                            fig_harvest.update_traces(line_color='#E74C3C')
                        elif "Pie" in chart_choice or "دائرة" in chart_choice:
                            fig_harvest = px.pie(df_harvested, names=x_axis, values=y_axis, title=chart_title, hole=0.3)
                        
                        if "Pie" not in chart_choice and "دائرة" not in chart_choice:
                            fig_harvest.update_layout(xaxis_title=final_x_title, yaxis_title=final_y_title, plot_bgcolor='rgba(240, 242, 246, 0.5)')
                        
                        st.plotly_chart(fig_harvest, use_container_width=True)
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء محاولة الرسم البياني: {e}")
                else:
                    st.warning("⚠️ لا توجد بيانات رقمية صالحة للرسم في هذا الجدول." if selected_lang == "العربية" else "⚠️ No valid numeric data found for visualization.")

# ==========================================
# ✨ المساعد الذكي وصياغة التقارير
# ==========================================
elif page == t["ai_assistant"]:
    # إعداد نصوص اللغتين لمكتب المستشار
    if selected_lang == "English":
        ai_title = "✨ Gemini AI Assistant & Report Generation"
        ai_desc = "Welcome to the AI Office! Provide your secure API Key to let the algorithms read the 'Smart Memory' and draft professional eco-dynamic reports."
        key_label = "🔑 Safe Vault: Enter Gemini API Key (Stored securely during session):"
        context_label = "📝 What should the report focus on? (e.g., Analyze the economic growth trends...)"
        btn_gen = "Generate Analytical Report 🧠"
        empty_msg = "👈 The table is empty! Please fetch data via the Harvest Wing first."
        success_msg = "✅ Data is successfully loaded into the AI context!"
    else:
        ai_title = "✨ المساعد الذكي وصياغة التقارير (Gemini AI)"
        ai_desc = "مرحباً بك في مكتب المستشار! ضع مفتاحك في 'الخزينة' لتمكين النماذج اللغوية من قراءة الذاكرة الذكية وصياغة تقارير تحليلية دقيقة."
        key_label = "🔑 الخزينة الآمنة: أدخل مفتاح Gemini API (مُشفر ويحذف بانتهاء الجلسة):"
        context_label = "📝 ما هو التركيز الأساسي للتقرير؟ (مثال: قم بتحليل دلالات التشتت والنمو الاقتصادي لهذه البيانات...)"
        btn_gen = "توليد التقرير التحليلي 🧠"
        empty_msg = "👈 المائدة فارغة! يرجى جلب البيانات أولاً من جناح الحصاد الآلي."
        success_msg = "✅ البيانات مستقرة بنجاح في عقل الذكاء الاصطناعي!"

    # واجهة المكتب
    st.markdown(f"<h2 style='color: #8E44AD;'>{ai_title}</h2>", unsafe_allow_html=True)
    st.write(ai_desc)
    st.markdown("---")

    # 1. الخزينة 
    api_key = st.text_input(key_label, type="password")

    # 2. التحقق من الذاكرة
    if 'smart_memory' not in st.session_state or not isinstance(st.session_state['smart_memory'], pd.DataFrame) or st.session_state['smart_memory'].empty:
        st.info(empty_msg)
    else:
        df = st.session_state['smart_memory']
        st.success(success_msg)
        
        with st.expander("👀 إلقاء نظرة على البيانات المُرسلة للنموذج / View Data Context"):
            st.dataframe(df.head(), use_container_width=True)
            
        report_focus = st.text_area(context_label, height=100)
        
        if st.button(btn_gen):
            if not api_key:
                st.error("⚠️ يجب وضع المفتاح (API Key) في الخزينة أولاً!" if selected_lang == "العربية" else "⚠️ API Key is required!")
            elif not report_focus:
                st.warning("⚠️ يرجى إعطاء توجيه للمستشار حول موضوع التقرير." if selected_lang == "العربية" else "⚠️ Please provide report instructions.")
            else:
                with st.spinner("الخوارزميات تعتصر البيانات وتصيغ التقرير..." if selected_lang == "العربية" else "Generating report..."):
                    try:
                        import google.generativeai as genai
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-1.5-pro')
                        data_summary = df.describe().to_string()
                        prompt = f"أنت مستشار إحصائي واقتصادي في المدرسة الإيكو-ديناميكية.\nطلب الباحث: {report_focus}\nملخص البيانات:\n{data_summary}\nاكتب التقرير بلغة: {selected_lang}."
                        response = model.generate_content(prompt)
                        st.markdown("---")
                        st.markdown(f"<h3 style='color: #2E86C1;'>📄 التقرير النهائي / Final Report</h3>", unsafe_allow_html=True)
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"❌ حدث خطأ في الاتصال بالخزينة أو النموذج: {e}")

# ==========================================
# 5. التوجيه وفتح الأجنحة (Routing) الاحصاء الوصفي
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
        
        # --- قاموس اختبار كاي ---
        chi_title = "🎲 Cross-Tabulation & Chi-Square Test"
        chi_desc = "Select two variables to generate a cross-tab and perform a Chi-Square test of independence."
        var1_label = "First Variable (Rows)"
        var2_label = "Second Variable (Columns)"
        chi_btn = "Run Chi-Square Test"
        res_crosstab = "Cross-Tabulation Table:"
        res_stat = "Chi-Square Value"
        res_pval = "P-Value"
        res_dof = "Degrees of Freedom"
        res_sig = "Result: Significant relationship exists (Reject H0) ❌"
        res_not_sig = "Result: No significant relationship (Fail to reject H0) ✅"
        chi_no_cat = "Not enough variables to perform the test."
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
        
        # --- قاموس اختبار كاي ---
        chi_title = "🎲 الجدول المزدوج واختبار كاي تربيع (Chi-Square)"
        chi_desc = "اختر متغيرين لإنشاء جدول التكرار المزدوج وإجراء اختبار الاستقلالية."
        var1_label = "المتغير الأول (الصفوف)"
        var2_label = "المتغير الثاني (الأعمدة)"
        chi_btn = "إجراء اختبار كاي تربيع"
        res_crosstab = "جدول التكرار المزدوج (Cross-Tab):"
        res_stat = "قيمة كاي تربيع"
        res_pval = "القيمة الاحتمالية (P-Value)"
        res_dof = "درجات الحرية"
        res_sig = "النتيجة: توجد علاقة معنوية بين المتغيرين (نرفض فرض العدم) ❌"
        res_not_sig = "النتيجة: لا توجد علاقة معنوية بين المتغيرين (لا نرفض فرض العدم) ✅"
        chi_no_cat = "لا يوجد عدد كافٍ من المتغيرات لإجراء الاختبار."

    # --- واجهة الجناح ---
    st.markdown(f"<h2 style='color: #2E86C1;'>{header_title}</h2>", unsafe_allow_html=True)
    st.write(header_desc)
    
    if 'smart_memory' not in st.session_state or not isinstance(st.session_state['smart_memory'], pd.DataFrame) or st.session_state['smart_memory'].empty:
        st.info(empty_msg)
    else:
        df = st.session_state['smart_memory']
        st.success(ready_msg)
        
        # ==========================================
        # 1️⃣ القسم الأول: الإحصاء الوصفي للمتغيرات الرقمية
        # ==========================================
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
        # 2️⃣ القسم الثاني: الجدول المزدوج واختبار كاي مع الرسم
        # ==========================================
        st.markdown("---")
        st.markdown(f"<h3 style='color: #2E86C1;'>{chi_title}</h3>", unsafe_allow_html=True)
        st.write(chi_desc)
        
        cat_cols = df.columns.tolist()
        
        if len(cat_cols) >= 2:
            col1, col2 = st.columns(2)
            var_1 = col1.selectbox(var1_label, cat_cols, key="chi_var1_select")
            var_2 = col2.selectbox(var2_label, cat_cols, key="chi_var2_select")
            
            if st.button(chi_btn, key="chi_run_button"):
                if var_1 == var_2:
                    st.warning("يرجى اختيار متغيرين مختلفين!" if selected_lang == "العربية" else "Please select two different variables!")
                else:
                    # بناء وعرض الجدول المزدوج
                    crosstab_df = pd.crosstab(df[var_1], df[var_2])
                    st.markdown(f"**{res_crosstab}**")
                    st.dataframe(crosstab_df, use_container_width=True)
                    
                    # إجراء الحساب الإحصائي
                    import scipy.stats as stats
                    chi2, p_val_chi, dof, expected = stats.chi2_contingency(crosstab_df)
                    
                    # عرض النتائج
                    c1, c2, c3 = st.columns(3)
                    c1.markdown(f"<div style='text-align: center; background-color: #f0f2f6; padding: 10px; border-radius: 5px;'><b>{res_stat}</b><br><span style='font-size: 1.2rem; color: #2E86C1;'>{chi2:.4f}</span></div>", unsafe_allow_html=True)
                    c2.markdown(f"<div style='text-align: center; background-color: #f0f2f6; padding: 10px; border-radius: 5px;'><b>{res_pval}</b><br><span style='font-size: 1.2rem; color: #2E86C1;'>{p_val_chi:.4f}</span></div>", unsafe_allow_html=True)
                    c3.markdown(f"<div style='text-align: center; background-color: #f0f2f6; padding: 10px; border-radius: 5px;'><b>{res_dof}</b><br><span style='font-size: 1.2rem; color: #2E86C1;'>{dof}</span></div>", unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # التفسير والقرار الإحصائي
                    if p_val_chi < 0.05:
                        st.warning(res_sig)
                    else:
                        st.success(res_not_sig)
                        
                    # 🎨 الرسم البياني التفاعلي
                    st.markdown("---")
                    st.markdown("### 📊 الرؤية البصرية للجدول المزدوج" if selected_lang == "العربية" else "### 📊 Cross-Tabulation Visualization")
                    
                    t_col, x_col, l_col = st.columns(3)
                    chart_title = t_col.text_input("عنوان الرسم" if selected_lang == "العربية" else "Chart Title", value=f"{var_1} vs {var_2}", key="c_title")
                    x_label = x_col.text_input("اسم المحور الأفقي (X)" if selected_lang == "العربية" else "X-Axis Label", value=var_1, key="c_xlab")
                    l_label = l_col.text_input("اسم مفتاح الألوان (Legend)" if selected_lang == "العربية" else "Legend Label", value=var_2, key="c_llab")
                    
                    import plotly.express as px
                    chart_df = crosstab_df.reset_index()
                    melted_df = chart_df.melt(id_vars=var_1, value_vars=crosstab_df.columns, var_name=var_2, value_name='Count')
                    
                    y_label = 'التكرار' if selected_lang == 'العربية' else 'Frequency / Count'
                    
                    fig_bar = px.bar(melted_df, x=var_1, y='Count', color=var_2, barmode='group',
                                 title=chart_title,
                                 labels={var_1: x_label, var_2: l_label, 'Count': y_label},
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
                    
                    fig_bar.update_layout(title_x=0.5, template="plotly_white", margin=dict(t=50, l=0, r=0, b=0))
                    st.plotly_chart(fig_bar, use_container_width=True)
                    
        else:
            st.info(chi_no_cat)
                        
        # ==========================================
        # 🎨 5. الرسم البياني التفاعلي للجدول المزدوج
        # ==========================================
        st.markdown("---")
        st.markdown("### 📊 الرؤية البصرية للجدول المزدوج" if selected_lang == "العربية" else "### 📊 Cross-Tabulation Visualization")
        
        # إعطاء الباحث حرية كتابة وتعديل أسماء المحاور والعنوان
        t_col, x_col, l_col = st.columns(3)
        chart_title = t_col.text_input("عنوان الرسم" if selected_lang == "العربية" else "Chart Title", value=f"{var_1} vs {var_2}", key="c_title")
        x_label = x_col.text_input("اسم المحور الأفقي (X)" if selected_lang == "العربية" else "X-Axis Label", value=var_1, key="c_xlab")
        l_label = l_col.text_input("اسم مفتاح الألوان (Legend)" if selected_lang == "العربية" else "Legend Label", value=var_2, key="c_llab")
        
        # تجهيز البيانات للرسم (تحويل الجدول المزدوج إلى صيغة مناسبة لـ Plotly)
        import plotly.express as px
        chart_df = crosstab_df.reset_index()
        melted_df = chart_df.melt(id_vars=var_1, value_vars=crosstab_df.columns, var_name=var_2, value_name='Count')
        
        y_label = 'التكرار' if selected_lang == 'العربية' else 'Frequency / Count'
        
        # رسم الأعمدة المجمعة (Grouped Bar Chart)
        fig_bar = px.bar(melted_df, x=var_1, y='Count', color=var_2, barmode='group',
                     title=chart_title,
                     labels={var_1: x_label, var_2: l_label, 'Count': y_label},
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        
        # تحسين شكل الرسم
        fig_bar.update_layout(title_x=0.5, template="plotly_white", margin=dict(t=50, l=0, r=0, b=0))
        st.plotly_chart(fig_bar, use_container_width=True)
        
else:
st.info(chi_no_cat)
                        
# ==========================================
# 📂 بوابة البيانات الشاملة (Comprehensive Data Portal)
# ==========================================
# الضربة الذكية: استخدام in لالتقاط الجناح حتى مع وجود إيموجي
elif "Comprehensive" in page or "الشاملة" in page:  
            if selected_lang == "English":
                portal_title = "📂 Comprehensive Data Portal"
                portal_desc = "Upload your dataset here. Once uploaded, the data will be securely saved in the 'Smart Memory' and instantly available across all analytical wings (Descriptive, Inferential, Psychometrics, AI Assistant, etc.)."
                upload_label = "📤 Upload your file (Supports CSV, Excel):"
                success_msg = "✅ Data successfully loaded into Smart Memory! You can now move to any other wing to analyze it."
                preview_title = "👀 Data Preview:"
                vars_title = "📌 Detected Variables (Columns):"
            else:
                portal_title = "📂 بوابة البيانات الشاملة (الرفع اليدوي)"
                portal_desc = "قم برفع ملف البيانات الخاص بك هنا (استبيانات، سلاسل زمنية، إلخ). بمجرد الرفع، ستستقر البيانات في 'الذاكرة الذكية' وتصبح متاحة فوراً للتحليل في جميع الأجنحة الأخرى (الإحصاء الوصفي، الاستدلالي، القياس النفسي، والمساعد الذكي)."
                upload_label = "📤 ارفع ملف البيانات (يدعم صيغ CSV و Excel):"
                success_msg = "✅ استقرت البيانات بنجاح في الذاكرة الذكية! يمكنك الآن الانتقال لأي جناح آخر للتحليل."
                preview_title = "👀 نظرة سريعة على البيانات:"
                vars_title = "📌 المتغيرات (الأعمدة) التي تم التعرف عليها:"

            st.markdown(f"<h2 style='color: #2E86C1;'>{portal_title}</h2>", unsafe_allow_html=True)
            st.write(portal_desc)
            st.markdown("---")

            uploaded_file = st.file_uploader(upload_label, type=['csv', 'xlsx', 'xls'])

            if uploaded_file is not None:
                with st.spinner("جاري تهيئة البيانات وحقنها في الذاكرة الذكية..." if selected_lang == "العربية" else "Loading data into Smart Memory..."):
                    try:
                        import pandas as pd
                        
                        if uploaded_file.name.endswith('.csv'):
                            df_uploaded = pd.read_csv(uploaded_file)
                        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                            df_uploaded = pd.read_excel(uploaded_file)
                        
                        st.session_state['smart_memory'] = df_uploaded
                        
                        st.success(success_msg)
                        
                        if selected_lang == "English":
                            st.info(f"📊 Dataset Shape: {df_uploaded.shape[0]} Rows, {df_uploaded.shape[1]} Columns.")
                        else:
                            st.info(f"📊 حجم البيانات: {df_uploaded.shape[0]} صف (مشاهدة)، و {df_uploaded.shape[1]} عمود (متغير).")

                        st.markdown(f"**{vars_title}**")
                        st.write(df_uploaded.columns.tolist())
                        
                        st.markdown(f"**{preview_title}**")
                        st.dataframe(df_uploaded.head(10), use_container_width=True)

                    except Exception as e:
                        st.error(f"❌ حدث خطأ أثناء قراءة الملف. تأكد من أن الملف غير تالف: {e}" if selected_lang == "العربية" else f"❌ Error reading file: {e}")

# ==========================================
# 📊 جناح الإحصاء الاستدلالي والاحتمالات (Inferential Statistics & Probabilities)
# ==========================================
elif "Inferential" in page or "الاستدلالي" in page:
            if selected_lang == "English":
                st.markdown("<h2 style='color: #2E86C1;'>📊 Inferential Statistics & Probabilities</h2>", unsafe_allow_html=True)
                st.write("Advanced statistical laboratory for hypothesis testing and relationship modeling.")
            else:
                st.markdown("<h2 style='color: #2E86C1;'>📊 الإحصاء الاستدلالي والاحتمالات</h2>", unsafe_allow_html=True)
                st.write("المختبر الإحصائي المتقدم لاختبار الفرضيات، التوزيعات الاحتمالية، ونمذجة العلاقات.")
            st.markdown("---")

            if 'smart_memory' not in st.session_state or not isinstance(st.session_state['smart_memory'], pd.DataFrame) or st.session_state['smart_memory'].empty:
                st.warning("⚠️ الذاكرة الذكية فارغة! يرجى جلب أو رفع البيانات أولاً." if selected_lang == "العربية" else "⚠️ Smart Memory is empty!")
            else:
                df_infer = st.session_state['smart_memory'].copy()
                st.success("✅ البيانات مستقرة وجاهزة للتحليل الاستدلالي!" if selected_lang == "العربية" else "✅ Data is ready for inferential analysis!")
                
                numeric_cols = df_infer.select_dtypes(include=['float64', 'int64']).columns.tolist()
                categorical_cols = df_infer.columns.tolist()

                st.markdown("### 🧬 تحديد مسار التحليل / Analysis Path")
                
                families = [
                    "اختر العائلة الإحصائية...",
                    "1. الفروق المعلمية (Parametric Tests)", 
                    "2. الاختبارات اللامعلمية (Non-Parametric Tests)",
                    "3. الارتباط والتوافق (Correlation)", 
                    "4. اختبارات التوزيع والاعتدالية (Normality Tests)",
                    "5. الاحتمالات والتوزيعات (Probabilities)",
                    "6. الانحدار الاستدلالي الأساسي (Basic Regression)"
                ] 
                
                family_choice = st.selectbox("اختر العائلة / Select Family:", families)
                st.markdown("---")

                try:
                    import pingouin as pg
                    import scipy.stats as stats
                    import plotly.express as px
                    import numpy as np
                    
# ==========================================
# 1. عائلة الفروق المعلمية (Parametric Tests)
# ==========================================
                    if "1" in family_choice:
                        st.markdown("### 🔬 مختبر الفروق المعلمية (Parametric Tests Laboratory)")
                        st.info("تفترض هذه الاختبارات اعتدالية التوزيع (البيانات تتبع التوزيع الطبيعي). يتم حساب أحجام الأثر (Effect Sizes) تلقائياً للمجلات العلمية.")
                        
                        para_test = st.selectbox("🎯 اختر الاختبار المعلمي الدقيق / Select specific test:", [
                            "1. اختبار T لعينة واحدة (One-Sample T-Test)",
                            "2. اختبار T لعينتين مستقلتين (Independent Samples T-Test)",
                            "3. اختبار T للعينات المترابطة (Paired Samples T-Test)",
                            "4. تحليل التباين الأحادي (One-Way ANOVA) مع Post-Hoc",
                            "5. تحليل التباين الثنائي (Two-Way ANOVA)"
                        ])
                        
                        st.markdown("---")
                        
                        # 1. اختبار T لعينة واحدة
                        if "One-Sample" in para_test:
                            col_to_test = st.selectbox("اختر المتغير المراد اختباره / Select Variable:", numeric_cols)
                            pop_mean = st.number_input("أدخل المتوسط المفترض للمجتمع (Test Value):", value=0.0)
                            if st.button("إجراء اختبار T لعينة واحدة / Run Test"):
                                res = pg.ttest(df_infer[col_to_test].dropna(), pop_mean)
                                st.success(f"📌 مقارنة متوسط [{col_to_test}] مع القيمة المعيارية ({pop_mean})")
                                st.dataframe(res, use_container_width=True)
                        
                        # 2. اختبار T لعينتين مستقلتين
                        elif "Independent" in para_test:
                            target_var = st.selectbox("المتغير التابع (الكمي) / Dependent Variable:", numeric_cols)
                            group_var = st.selectbox("متغير التجميع (الفئوي) / Grouping Variable:", categorical_cols)
                            if st.button("إجراء اختبار T المستقل / Run Test"):
                                groups = df_infer[group_var].dropna().unique()
                                if len(groups) == 2:
                                    g1 = df_infer[df_infer[group_var] == groups[0]][target_var].dropna()
                                    g2 = df_infer[df_infer[group_var] == groups[1]][target_var].dropna()
                                    st.success(f"📌 مقارنة [{target_var}] بين مجموعتي: ({groups[0]}) و ({groups[1]})")
                                    res_t = pg.ttest(g1, g2)
                                    st.dataframe(res_t, use_container_width=True)
                                else:
                                    st.error(f"⚠️ المتغير الفئوي [{group_var}] يحتوي على {len(groups)} مجموعات. هذا الاختبار يتطلب مجموعتين فقط!")
                        
                        # 3. اختبار T للعينات المترابطة (القبلي والبعدي)
                        elif "Paired" in para_test:
                            st.write("يُستخدم لمقارنة نفس العينة في فترتين (مثل: قبل وبعد تطبيق سياسة تسعيرية).")
                            var_pre = st.selectbox("المتغير الأول (القبلي) / Pre-Test Variable:", numeric_cols)
                            var_post = st.selectbox("المتغير الثاني (البعدي) / Post-Test Variable:", [c for c in numeric_cols if c != var_pre])
                            if st.button("إجراء اختبار T المترابط / Run Test"):
                                # تنظيف القيم المفقودة مع الحفاظ على الترابط
                                df_paired = df_infer[[var_pre, var_post]].dropna()
                                res_paired = pg.ttest(df_paired[var_pre], df_paired[var_post], paired=True)
                                st.success(f"📌 مقارنة مترابطة بين [{var_pre}] و [{var_post}]")
                                st.dataframe(res_paired, use_container_width=True)
                        # 4. تحليل التباين الأحادي (One-Way ANOVA)
                        elif "One-Way ANOVA" in para_test:
                            target_var = st.selectbox("المتغير التابع (الكمي) / Dependent Variable:", numeric_cols)
                            group_var = st.selectbox("متغير التجميع (الفئوي - أكثر من مجموعتين) / Grouping Variable:", categorical_cols)
                            if st.button("إجراء تحليل التباين / Run ANOVA"):
                                groups_count = df_infer[group_var].nunique()
                                if groups_count > 2:
                                    st.success(f"📌 تحليل تباين لـ [{target_var}] عبر {groups_count} مجموعات في [{group_var}]")
                                    res_anova = pg.anova(data=df_infer, dv=target_var, between=group_var)
                                    st.markdown("**📊 جدول تحليل التباين (ANOVA Table)**")
                                    st.dataframe(res_anova, use_container_width=True)
                                    
                                    # التعديل هنا: استخدام .values[0] لتجنب خطأ p-unc
                                    if res_anova['p_unc'].values[0] < 0.05:                                        st.warning("✨ نتيجة الأنوڤا دالة إحصائياً! إليك اختبار (توكي) لتحديد المجموعات المختلفة:")
                                    res_tukey = pg.pairwise_tukey(data=df_infer, dv=target_var, between=group_var)
                                    st.dataframe(res_tukey, use_container_width=True)
                                else:
                                    st.info("💡 لا توجد فروق دالة إحصائياً بين المجموعات الكلية، لذا لا حاجة لإجراء اختبارات بعدية (Post-Hoc).")
                            else:
                                st.warning("⚠️ المتغير الفئوي يحتوي على مجموعتين أو أقل، يُفضل استخدام اختبار T لعينتين مستقلتين.")
                                    
                       # 5. تحليل التباين الثنائي (Two-Way ANOVA)
                        elif "Two-Way ANOVA" in para_test:
                            st.write("لدراسة تأثير عاملين فئويين (متغيرين مستقلين) معاً والتفاعل بينهما على متغير كمي تابع.")
                            target_var = st.selectbox("المتغير التابع (الكمي) / Dependent Variable:", numeric_cols)
                            col1, col2 = st.columns(2)
                            with col1:
                                group_var1 = st.selectbox("العامل الأول / Factor 1:", categorical_cols)
                            with col2:
                                group_var2 = st.selectbox("العامل الثاني / Factor 2:", [c for c in categorical_cols if c != group_var1])
                                
                            if st.button("إجراء التباين الثنائي / Run Two-Way ANOVA"):
                                clean_df = df_infer.dropna(subset=[target_var, group_var1, group_var2])
                                
                                # التأكد من وجود أكثر من مجموعة في كل عامل لتجنب انهيار الخوارزمية
                                if clean_df[group_var1].nunique() > 1 and clean_df[group_var2].nunique() > 1:
                                    st.success(f"📌 دراسة تأثير [{group_var1}] و [{group_var2}] والتفاعل بينهما على [{target_var}]")
                                    res_two_way = pg.anova(data=clean_df, 
                                                           dv=target_var, 
                                                           between=[group_var1, group_var2])
                                    st.markdown("**📊 جدول تحليل التباين الثنائي (Two-Way ANOVA Table)**")
                                    st.dataframe(res_two_way, use_container_width=True)
                                    
                                    # التعديل الاستباقي: التفسير الذكي والآمن لقيم (p-unc) لكل صف لتجنب خطأ الفهرس
                                    st.markdown("**💡 التفسير الإحصائي الآمن للنتائج:**")
                                    for index, row in res_two_way.iterrows():
                                        source = row['Source']
                                        p_val = row['p-unc']
                                        if p_val < 0.05:
                                            st.warning(f"✨ التأثير الخاص بـ **{source}** دال إحصائياً (p-value = {p_val:.4f}).")
                                        else:
                                            st.info(f"⚪ التأثير الخاص بـ **{source}** غير دال إحصائياً (p-value = {p_val:.4f}).")
                                else:
                                    st.error("⚠️ يجب أن يحتوي كل عامل فئوي على مجموعتين على الأقل لإجراء التباين الثنائي.")
# ==========================================
# 2. عائلة الاختبارات اللامعلمية (Non-Parametric Tests)
# ==========================================
                    elif "2" in family_choice:
                        st.markdown("### 🧮 مختبر الاختبارات اللامعلمية (Non-Parametric Tests)")
                        st.info("تُستخدم كبديل قوي عندما لا تتبع البيانات التوزيع الطبيعي، أو للعينات الصغيرة، والمتغيرات الرتبية والفئوية.")
                        
                        non_para_test = st.selectbox("🎯 اختر الاختبار اللامعلمي الدقيق / Select specific test:", [
                            "1. اختبار مان-ويتني (Mann-Whitney U) - بديل T لعينتين مستقلتين",
                            "2. اختبار ويلكوكسون (Wilcoxon Signed-Rank) - بديل T للعينات المترابطة",
                            "3. اختبار كروسكال-واليس (Kruskal-Wallis) - بديل الأنوڤا للعينات المستقلة",
                            "4. اختبار فريدمان (Friedman Test) - للقياسات المتكررة / العينات المترابطة",
                            "5. اختبار مربع كاي (Chi-Square) - للاستقلالية والتوافق"
                        ])
                        
                        st.markdown("---")
                        
                        # 1. اختبار مان-ويتني
                        if "Mann-Whitney" in non_para_test:
                            target_var = st.selectbox("المتغير التابع (الكمي) / Dependent Variable:", numeric_cols)
                            group_var = st.selectbox("متغير التجميع (الفئوي - مجموعتين) / Grouping Variable:", categorical_cols)
                            if st.button("إجراء اختبار مان-ويتني / Run Test"):
                                groups = df_infer[group_var].dropna().unique()
                                if len(groups) == 2:
                                    g1 = df_infer[df_infer[group_var] == groups[0]][target_var].dropna()
                                    g2 = df_infer[df_infer[group_var] == groups[1]][target_var].dropna()
                                    st.success(f"📌 مقارنة الرتب لـ [{target_var}] بين: ({groups[0]}) و ({groups[1]})")
                                    res_mwu = pg.mwu(g1, g2)
                                    st.dataframe(res_mwu, use_container_width=True)
                                else:
                                    st.error("⚠️ يجب أن يحتوي متغير التجميع على مجموعتين فقط لهذا الاختبار!")
                        
                        # 2. اختبار ويلكوكسون (للعينات المترابطة)
                        elif "Wilcoxon" in non_para_test:
                            var_pre = st.selectbox("المتغير الأول (مثال: قبل) / First Variable:", numeric_cols)
                            var_post = st.selectbox("المتغير الثاني (مثال: بعد) / Second Variable:", [c for c in numeric_cols if c != var_pre])
                            if st.button("إجراء اختبار ويلكوكسون / Run Test"):
                                df_paired = df_infer[[var_pre, var_post]].dropna()
                                res_wilcoxon = pg.wilcoxon(df_paired[var_pre], df_paired[var_post])
                                st.success(f"📌 مقارنة الفروق المترابطة بين [{var_pre}] و [{var_post}]")
                                st.dataframe(res_wilcoxon, use_container_width=True)
                        
                       # 3. اختبار كروسكال-واليس (أكثر من مجموعتين)
                        elif "Kruskal-Wallis" in non_para_test:
                            target_var = st.selectbox("المتغير التابع (الكمي) / Dependent Variable:", numeric_cols)
                            group_var = st.selectbox("متغير التجميع (الفئوي) / Grouping Variable:", categorical_cols)
                            if st.button("إجراء اختبار كروسكال-واليس / Run Test"):
                                groups_count = df_infer[group_var].nunique()
                                if groups_count > 2:
                                    st.success(f"📌 تحليل الفروق اللامعلمية لـ [{target_var}] عبر {groups_count} مجموعات في [{group_var}]")
                                    res_kw = pg.kruskal(data=df_infer, dv=target_var, between=group_var)
                                    st.markdown("**📊 جدول كروسكال-واليس (Kruskal-Wallis H)**")
                                    st.dataframe(res_kw, use_container_width=True)
                                    
                                    # التعديل هنا: استخدام .values[0]
                                    if res_kw['p_unc'].values[0] < 0.05:
                                        st.warning("✨ توجد فروق دالة إحصائياً! إليك المقارنات الثنائية (Pairwise Mann-Whitney) لتحديد مصدر الاختلاف:")
                                        res_pw = pg.pairwise_tests(data=df_infer, dv=target_var, between=group_var, parametric=False)
                                        st.dataframe(res_pw, use_container_width=True)
                                else:
                                    st.warning("⚠️ عدد المجموعات 2 أو أقل، يُفضل استخدام اختبار مان-ويتني.")

                        # 4. اختبار فريدمان مع المقارنات المتعددة الذكية
                        elif "Friedman" in non_para_test:
                            st.write("يُستخدم لمقارنة 3 متغيرات مترابطة أو أكثر (مثل تقييمات لـ 3 سنوات متتالية لنفس العينة).")
                            selected_vars = st.multiselect("اختر 3 متغيرات كمية على الأقل / Select Variables:", numeric_cols)
                            if st.button("إجراء اختبار فريدمان / Run Test"):
                                if len(selected_vars) >= 3:
                                    import scipy.stats as stats
                                    import pandas as pd
                                    import itertools
                                    
                                    clean_data = df_infer[selected_vars].dropna()
                                    args = [clean_data[col] for col in selected_vars]
                                    stat, p_value = stats.friedmanchisquare(*args)
                                    
                                    res_friedman = pd.DataFrame({
                                        "الاختبار": ["Friedman Chi-Square"],
                                        "قيمة الإحصاء (Statistic)": [stat],
                                        "مستوى الدلالة (p-value)": [p_value]
                                    })
                                    st.success(f"📌 اختبار فريدمان للمتغيرات: {', '.join(selected_vars)}")
                                    st.dataframe(res_friedman, use_container_width=True)
                                    
                                    # إضافة المقارنات البعدية الذكية لفريدمان
                                    if p_value < 0.05:
                                        st.warning("✨ نتيجة فريدمان دالة إحصائياً! إليك المقارنات الثنائية (Post-Hoc Wilcoxon) بين كل متغيرين:")
                                        posthoc_res = []
                                        for var1, var2 in itertools.combinations(selected_vars, 2):
                                            res_w = pg.wilcoxon(clean_data[var1], clean_data[var2])
                                            posthoc_res.append({
                                                "المقارنة الثنائية": f"{var1} vs {var2}",
                                                "قيمة W": res_w['W-val'].values[0],
                                                "مستوى الدلالة (p-value)": res_w['p-val'].values[0]
                                            })
                                        st.dataframe(pd.DataFrame(posthoc_res), use_container_width=True)
                                else:
                                    st.error("⚠️ يرجى اختيار 3 متغيرات على الأقل لإجراء هذا الاختبار.")
                        
                        # 5. اختبار مربع كاي للاستقلالية
                        elif "Chi-Square" in non_para_test:
                            st.write("يقيس قوة الارتباط والاستقلالية بين متغيرين فئويين (Categorical).")
                            cat_var1 = st.selectbox("المتغير الفئوي الأول (صفوف) / Row Variable:", categorical_cols)
                            cat_var2 = st.selectbox("المتغير الفئوي الثاني (أعمدة) / Column Variable:", [c for c in categorical_cols if c != cat_var1])
                            if st.button("إجراء اختبار مربع كاي / Run Chi-Square"):
                                expected, observed, stats_res = pg.chi2_independence(data=df_infer, x=cat_var1, y=cat_var2)
                                st.success(f"📌 اختبار الاستقلالية بين [{cat_var1}] و [{cat_var2}]")
                                
                                st.markdown("**📊 نتائج الاختبار ومستوى الدلالة (Test Statistics)**")
                                st.dataframe(stats_res, use_container_width=True)
                                
                                st.markdown("**📉 جدول التكرارات المشاهدة (Observed Frequencies)**")
                                st.dataframe(observed, use_container_width=True)  
                    
                    
                    # 2. عائلة الارتباط
                    elif "2" in family_choice:
                        var_x = st.selectbox("المتغير الأول / Variable X:", numeric_cols)
                        var_y = st.selectbox("المتغير الثاني / Variable Y:", [c for c in numeric_cols if c != var_x])
                        corr_method = st.radio("نوع الارتباط / Correlation Type:", ["pearson", "spearman", "kendall"])
                        if st.button("إجراء الارتباط / Calculate"):
                            st.dataframe(pg.corr(df_infer[var_x], df_infer[var_y], method=corr_method), use_container_width=True)
                            fig = px.scatter(df_infer, x=var_x, y=var_y, trendline="ols", title=f"Correlation: {var_x} vs {var_y}")
                            st.plotly_chart(fig, use_container_width=True)

                    # 3. عائلة التوزيع والاعتدالية
                    elif "3" in family_choice:
                        st.markdown("**اختبارات شابيرو-ويلك للاعتدالية / Shapiro-Wilk Normality Test**")
                        cols_to_test = st.multiselect("اختر المتغيرات لاختبار اعتداليتها / Select Variables:", numeric_cols, default=[numeric_cols[0]] if numeric_cols else [])
                        if st.button("فحص التوزيع / Test Normality"):
                            normality_results = pg.normality(df_infer[cols_to_test])
                            st.dataframe(normality_results, use_container_width=True)
                            if len(cols_to_test) == 1:
                                fig = px.histogram(df_infer, x=cols_to_test[0], marginal="box", title=f"Distribution of {cols_to_test[0]}")
                                st.plotly_chart(fig, use_container_width=True)

                    # 4. عائلة الاحتمالات
                    elif "4" in family_choice:
                        st.markdown("**حساب القيم المعيارية والاحتمالات / Z-Scores & Probabilities**")
                        prob_var = st.selectbox("اختر المتغير لإنشاء التوزيع الطبيعي له / Select Variable:", numeric_cols)
                        target_val = st.number_input("أدخل القيمة لحساب احتمالها / Value to check probability for:", value=0.0)
                        if st.button("حساب الاحتمال / Calculate Probability"):
                            var_mean = df_infer[prob_var].mean()
                            var_std = df_infer[prob_var].std()
                            z_score = (target_val - var_mean) / var_std
                            p_value = stats.norm.cdf(z_score)
                            
                            st.success(f"📌 المتوسط (Mean): {var_mean:.4f} | الانحراف المعياري (Std): {var_std:.4f}")
                            st.info(f"📊 القيمة المعيارية (Z-Score): {z_score:.4f}")
                            st.warning(f"🎯 احتمال أن تكون القيم أقل من أو تساوي ({target_val}) هو: {p_value:.4%}")
                            st.warning(f"🎯 احتمال أن تكون القيم أكبر من ({target_val}) هو: {(1 - p_value):.4%}")

                    # 5. عائلة الانحدار
                    elif "5" in family_choice:
                        st.markdown("**الانحدار الخطي (بسيط / متعدد) | Linear Regression (Simple / Multiple)**")
                        dv = st.selectbox("المتغير التابع (Y) / Dependent Variable:", numeric_cols)
                        iv = st.multiselect("المتغيرات المستقلة (X) / Independent Variables:", [c for c in numeric_cols if c != dv])
                        
                        if st.button("تشغيل نموذج الانحدار / Run Regression Model") and iv:
                            import statsmodels.api as sm
                            import pandas as pd
                            
                            # تنظيف البيانات من القيم المفقودة لضمان دقة النموذج
                            df_reg = df_infer[[dv] + iv].dropna()
                            X = df_reg[iv]
                            Y = df_reg[dv]
                            
                            # إضافة القاطع (Intercept/Constant) وهو ضروري جداً في الاقتصاد القياسي
                            X = sm.add_constant(X)
                            
                            # بناء النموذج وتقديره
                            model = sm.OLS(Y, X).fit()
                            
                            # 1. عرض مؤشرات جودة النموذج الكلية (بما فيها قيمة F) في لوحة أنيقة
                            st.markdown("### 📈 مؤشرات جودة النموذج (Model Summary)")
                            col1, col2, col3, col4 = st.columns(4)
                            col1.metric("R-squared (R²)", f"{model.rsquared:.4f}")
                            col2.metric("Adj. R-squared", f"{model.rsquared_adj:.4f}")
                            col3.metric("F-statistic (قيمة ف)", f"{model.fvalue:.4f}")
                            col4.metric("Prob (F-statistic)", f"{model.f_pvalue:.4e}")
                            
                            # 2. عرض جدول معاملات الانحدار (T-tests)
                            st.markdown("### 🧮 معاملات الانحدار (Coefficients)")
                            results_df = pd.DataFrame({
                                "Coefficient (المعامل)": model.params,
                                "Std. Error (الخطأ المعياري)": model.bse,
                                "t-value (قيمة ت)": model.tvalues,
                                "P>|t| (مستوى الدلالة)": model.pvalues
                            })
                            st.dataframe(results_df, use_container_width=True)
                            
                            # 3. زر سحري لعرض التقرير الكلاسيكي الكامل (مثل EViews و SPSS)
                            with st.expander("📄 عرض التقرير القياسي الكامل (Full EViews/SPSS Style Summary)"):
                                st.text(model.summary().as_text())
                except ImportError:
                    st.error("⚠️ محركات pingouin أو scipy أو statsmodels غير مثبتة! يرجى إضافتها لملف requirements.txt.")
                except Exception as e:
                    st.error(f"❌ حدث خطأ في الحساب الإحصائي: {e}")
# ==========================================
# باقي الأجنحة (مؤقتة لحين اكتمالها)
# ==========================================
else:
            st.markdown(f"<h2 style='color: #7F8C8D; text-align: center;'>{page}</h2>", unsafe_allow_html=True)
