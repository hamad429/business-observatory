import streamlit as st
import pandas as pd
import urllib.parse
import json
import xml.etree.ElementTree as ET
import requests

# 1. إعدادات الصفحة الرئيسية
st.set_page_config(page_title="المرصد الشامل لبيئة الأعمال", page_icon="📡", layout="wide")

# 2. ضبط التنسيق والمحاذاة الشاملة ومنع انقلاب النصوص
st.markdown("""
    <style>
    /* محاذاة التطبيق لليمين */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    
    /* محاذاة الخانات والقوائم والجدول */
    div[data-baseweb="input"], input, textarea, .stDataFrame {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* بطاقات المنصات الحكومية */
    .portal-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        text-align: right;
        direction: rtl;
    }
    
    .portal-card h4 {
        color: #1e293b;
        margin-top: 0;
        margin-bottom: 6px;
        font-size: 1.1rem;
    }
    
    .portal-card p {
        color: #64748b;
        margin-bottom: 10px;
        font-size: 0.95rem;
    }
    
    .portal-link {
        display: inline-block;
        color: #2563eb;
        font-weight: bold;
        text-decoration: none;
        direction: ltr;
    }
    </style>
""", unsafe_allow_html=True)

# 3. إعدادات الشريط الجانبي ومفتاح الذكاء الاصطناعي
st.sidebar.title("⚙️ إعدادات النظام")
user_api_key = st.sidebar.text_input(
    "ضع مفتاح Gemini API الخاص بك هنا:", 
    type="password", 
    help="أدخل المفتاح الذي استخرجته من Google AI Studio لتفعيل التحليلات المباشرة."
)

api_key = user_api_key.strip()

def ask_ai(prompt):
    """دالة الاتصال بالذكاء الاصطناعي عبر المفتاح المدخل"""
    if not api_key:
        return "⚠️ يرجى إدخال مفتاح Gemini API الخاص بك في القائمة الجانبية (⚙️ إعدادات النظام) لتفعيل تحليلات الذكاء الاصطناعي."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        res_json = response.json()
        if response.status_code == 200:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            err = res_json.get('error', {}).get('message', 'خطأ في المفتاح أو الخدمة')
            return f"❌ خطأ من الذكاء الاصطناعي: {err}"
    except Exception as e:
        return f"❌ تعذر الاتصال بالسيرفر: {str(e)}"

# 4. واجهة المرصد الرئيسية
st.title("📡 المرصد الشامل لمرئيات ومتغيرات بيئة الأعمال والقطاع الأجنبي")
st.write("رادار مباشر يرصد التحديات الميدانية والقرارات والبيانات المفتوحة للقطاع الخاص الأجنبي في المملكة.")

search_query = st.text_input("🔍 اكتب القطاع أو التحدي للتفتيش والتحليل الحقيقي:", value="الخدمات اللوجستية")

# تبويبات المسميات المعتمدة
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📰 مرصد الأخبار ومنصات التواصل الاجتماعي", 
    "🏛️ قاعدة البيانات المفتوحة", 
    "📊 القوائم المالية", 
    "💬 منصة استطلاع", 
    "💡 التحديات المحتملة"
])

# ----- التبويب 1: مرصد الأخبار ومنصات التواصل الاجتماعي -----
with tab1:
    st.subheader("📰 مرصد الصحف ومنصات التواصل الاجتماعي (X & LinkedIn)")
    
    # 1. الأخبار والصحف
    encoded_query = urllib.parse.quote(f"{search_query} السعودية استثمار")
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ar&gl=SA&ceid=SA:ar"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(rss_url, headers=headers, timeout=7)
        root = ET.fromstring(res.text)
        items = root.findall('.//item')
        if items:
            st.success(f"✅ تم سحب {len(items[:6])} خبر وتغطية إعلامية مباشرة من الصحف والمجلات:")
            for item in items[:6]:
                title = item.find('title').text if item.find('title') is not None else "بدون عنوان"
                link = item.find('link').text if item.find('link') is not None else "#"
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else "غير محدد"
                with st.expander(f"📌 {title}"):
                    st.write(f"**تاريخ النشر:** {pub_date}")
                    st.markdown(f"🔗 **رابط التغطية الصحفية:** [{link}]({link})")
        else:
            st.warning("لا توجد تغطيات إعلامية حديثة بكلمة البحث الحالية.")
    except Exception as e:
        st.error(f"تعذر جلب الأخبار الصحفية: {e}")
        
    st.write("---")
    st.write("**📱 البحث المباشر في المنصات الاجتماعية لقطاع:** " + f"**{search_query}**")
    
    encoded_social = urllib.parse.quote(f"{search_query} السعودية")
    x_search_url = f"https://x.com/search?q={encoded_social}&f=live"
    linkedin_search_url = f"https://www.linkedin.com/search/results/content/?keywords={encoded_social}"
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"🔗 **[🔍 تفتيش منشورات وتغريدات منصة X حياً]({x_search_url})**")
    with col2:
        st.markdown(f"🔗 **[🔍 تفتيش تحليلات ومقالات منصة LinkedIn حياً]({linkedin_search_url})**")

# ----- التبويب 2: قاعدة البيانات المفتوحة -----
with tab2:
    st.subheader("🏛️ قاعدة البيانات المفتوحة الحكومية (360°)")
    
    encoded_search = urllib.parse.quote(search_query)
    direct_gov_url = f"https://open.gov.sa/ar/datasets?query={encoded_search}"
    
    st.info(f"🔎 نتائج البحث والوصول السريع المخصص لقطاع: **{search_query}**")
    st.markdown(f"🔗 **[اضغط هنا للوصول المباشر لحزم البيانات المفتوحة الخاصة بـ ({search_query}) على منصة open.gov.sa]({direct_gov_url})**")
    
    st.write("---")
    st.write("**📌 المنصات والبوابات الحكومية المعتمدة للبيانات المفتوحة:**")
    
    portals = [
        {"name": "البوابة الوطنية للبيانات المفتوحة (Open Data Portal)", "desc": "المحرك الموحد لجميع حزم البيانات المفتوحة الصادرة عن أكثر من 170 جهة حكومية", "url": "https://open.gov.sa/ar"},
        {"name": "الهيئة العامة للإحصاء (GASTAT)", "desc": "المصدر الرسمي لمؤشرات التجارة الخارجية، الاقتصاد، والقوى العاملة والمسوح الوطنية", "url": "https://www.stats.gov.sa/ar"},
        {"name": "وزارة التجارة - بوابة البيانات المفتوحة", "desc": "بيانات السجلات التجارية، الشركات الأجنبية والمؤسسات والتراخيص التجارية", "url": "https://mc.gov.sa/ar/eservices/open-data/Pages/default.aspx"},
        {"name": "وزارة الاستثمار (Invest Saudi)", "desc": "منصة الاستثمار الوطنية والتقارير الاقتصادية والفرص الاستثمارية الأجنبية", "url": "https://investsaudi.sa/ar"},
        {"name": "الهيئة العامة للغذاء والدواء (SFDA)", "desc": "سجلات التراخيص، المصانع، الأدوية، الأغذية والأجهزة الطبية المعتمدة", "url": "https://sfda.gov.sa/ar/open-data"},
        {"name": "وزارة الصناعة والثروة المعدنية", "desc": "بيانات المصانع المنتجة، التراخيص الصناعية والتعدينية والمناطق اللوجستية", "url": "https://mim.gov.sa/mim/opendata.html"},
        {"name": "وزارة النقل والخدمات اللوجستية", "desc": "مؤشرات الأداء اللوجستي، حركة الشحن، الطرق، الموانئ وسلاسل الإمداد", "url": "https://mot.gov.sa/ar/OpenData/Pages/default.aspx"},
        {"name": "البنك المركزي السعودي (SAMA)", "desc": "البيانات الإحصائية للنظام المصرفي، التمويل، التأمين ومؤشرات الاقتصاد الكلي", "url": "https://www.sama.gov.sa/ar-sa/EconomicReports/Pages/Statistics.aspx"},
        {"name": "وزارة المالية - البيانات المفتوحة", "desc": "تقارير الميزانية العامة، الأداء المالي والقطاعات المالية الوطنية", "url": "https://www.mof.gov.sa/opendata/Pages/default.aspx"},
        {"name": "وزارة البيئة والمياه والزراعة", "desc": "بيانات الإنتاج الزراعي، الحيازات، التصاريف البيئية والمشاريع المائية", "url": "https://mewa.gov.sa/ar/InformationCenter/ResearchsAndStudies/Pages/OpenData.aspx"},
        {"name": "وزارة الموارد البشرية والتنمية الاجتماعية", "desc": "مؤشرات سوق العمل، نسب التوطين، برامج الدعم وتراخيص الكوادر", "url": "https://hrsd.gov.sa/ar/open-data"},
        {"name": "منصة استطلع (Istitlaa)", "desc": "المنصة الموحدة لاستطلاع آراء العموم والمستثمرين في اللوائح والأنظمة الحكومية", "url": "https://istitlaa.ncc.gov.sa/ar"},
        {"name": "منصة اعتماد (Etimad)", "desc": "بوابة المنافسات والمشتريات الحكومية والفرص التشغيلية للمشاريع", "url": "https://login.etimad.sa/account/login"},
        {"name": "الهيئة العامة للموانئ (موانئ)", "desc": "إحصائيات حركة الحاويات، السفن، والخدمات الملاحية واللوجستية في الموانئ", "url": "https://mawani.gov.sa/ar-sa/pages/opendata.aspx"},
        {"name": "الهيئة العامة للطيران المدني (GACA)", "desc": "حركة الشحن الجوي، المطارات، وتراخيص الناقلات والخدمات الجوية", "url": "https://gaca.gov.sa/web/ar-sa/page/open-data"},
        {"name": "وزارة البلدية والإسكان (منصة بلدي)", "desc": "الرخص البلدية، الأنشطة المعتمدة، والتخطيط العمراني والأراضي", "url": "https://balady.gov.sa/"},
        {"name": "وزارة الاتصالات وتقنية المعلومات", "desc": "مؤشرات البنية التحتية الرقمية، قطاع التقنية والذكاء الاصطناعي", "url": "https://mcit.gov.sa/ar/open-data"},
        {"name": "وزارة الطاقة", "desc": "مؤشرات الطاقة، التراخيص التشغيلية ومشاريع الطاقة المتجددة", "url": "https://www.moenergy.gov.sa/ar/Pages/OpenData.aspx"},
        {"name": "وزارة السياحة", "desc": "إحصائيات الحركة السياحية، تراخيص الفنادق والتنقل والاستثمار السياحي", "url": "https://mt.gov.sa/ar/open-data"},
        {"name": "هيئة الزكاة والضريبة والجمارك (ZATCA)", "desc": "الأنظمة الجمركية، الفسح الجمركي، وضوابط الاستيراد والتصدير", "url": "https://zatca.gov.sa/ar/OpenData/Pages/default.aspx"}
    ]
    
    for portal in portals:
        st.markdown(f"""
        <div class="portal-card">
            <h4>🏛️ {portal['name']}</h4>
            <p>{portal['desc']}</p>
            <a href="{portal['url']}" target="_blank" class="portal-link">🔗 اضغط هنا للانتقال المباشر للمنصة</a>
        </div>
        """, unsafe_allow_html=True)

# ----- التبويب 3: القوائم المالية -----
with tab3:
    st.subheader("📊 تحليل القوائم المالية والاتجاهات الاستثمارية بالذكاء الاصطناعي")
    if not api_key:
        st.info("⚠️ فضلاً ضع مفتاح Gemini API في الخانة الجانبية لتنشيط التقرير المالي.")
    else:
        with st.spinner("جاري الاتصال بالذكاء الاصطناعي لتوليد تحليل القوائم المالية..."):
            prompt = f"قدم تحليلاً استباقياً للقوائم المالية والإفصاحات لقطاع '{search_query}' في السعودية للشركات الأجنبية، واذكر أهم 3 مخاطر مالية وتأثيرها على رأس المال."
            ai_res = ask_ai(prompt)
            st.markdown(ai_res)

# ----- التبويب 4: منصة استطلاع -----
with tab4:
    st.subheader("💬 تحليلات التشريعات ومرئيات المستثمرين عبر منصة استطلاع")
    
    encoded_istitlaa = urllib.parse.quote(search_query)
    istitlaa_url = f"https://istitlaa.ncc.gov.sa/ar/Pages/search.aspx?k={encoded_istitlaa}"
    st.markdown(f"🔗 **[اضغط هنا للتفتيش المباشر على مشروعات اللوائح والأنظمة بقطاع ({search_query}) في منصة استطلاع]({istitlaa_url})**")
    st.write("---")
    
    if not api_key:
        st.info("⚠️ فضلاً ضع مفتاح Gemini API في الخانة الجانبية لتنشيط استقراء اللوائح والمرئيات.")
    else:
        with st.spinner("جاري استقراء لوائح منصة استطلاع والأنظمة والمرئيات..."):
            prompt = f"بصفتك خبيراً تنظيماً، استقرئ التحديات التنظيمية واللوائح الحكومية المطروحة في منصة استطلاع بالسعودية المتعلقة بقطاع '{search_query}' والآراء المتوقعة للمستثمرين الأجانب."
            ai_res = ask_ai(prompt)
            st.markdown(ai_res)

# ----- التبويب 5: التحديات المحتملة -----
with tab5:
    st.subheader("💡 مصفوفة التحديات المحتملة والمحفزات الحكومية المقابلة")
    if not api_key:
        st.info("⚠️ فضلاً ضع مفتاح Gemini API في الخانة الجانبية لتنشيط مصفوفة التحديات المحتملة.")
    else:
        with st.spinner("جاري صياغة مصفوفة التحديات المحتملة والحلول..."):
            prompt = f"قم بصياغة جدول ماركداون يحتوي على: (التحدي الميداني المحتمل، مستوى الخطورة، المحفز الحكومي المتاح في السعودية، والتوصية الاستباقية) للقطاع التالي: {search_query}"
            ai_res = ask_ai(prompt)
            st.markdown(ai_res)
