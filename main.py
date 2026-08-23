import streamlit as st
import pandas as pd
import urllib.parse
import json
import xml.etree.ElementTree as ET
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="المرصد الشامل لبيئة الأعمال", page_icon="📡", layout="wide")

# 2. ضبط محاذاة الصفحة بالكامل لليمين (RTL)
st.markdown("""
    <style>
    body, div, p, h1, h2, h3, h4, span, label, input {
        direction: rtl !important;
        text-align: right !important;
    }
    .stDataFrame {
        direction: rtl !important;
    }
    .stTextInput input {
        direction: rtl !important;
        text-align: right !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. مفتاح الذكاء الاصطناعي
api_key = "AQ.Ab8RN6JO7Umu9mZsx05Ip_Se8UdqV8twMlvcVbKFVzgPTDu76w"

def ask_ai(prompt):
    """دالة اتصال بنموذج الذكاء الاصطناعي الحقيقي"""
    if not api_key:
        return "❌ لا يوجد مفتاح مثبت."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        res_json = response.json()
        if response.status_code == 200:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            err = res_json.get('error', {}).get('message', 'خطأ في الاستجابة')
            return f"❌ خطأ من الذكاء الاصطناعي: {err}"
    except Exception as e:
        return f"❌ تعذر الاتصال: {str(e)}"

# 4. واجهة المرصد الرئيسية
st.title("📡 المرصد الشامل لمرئيات ومتغيرات بيئة الأعمال والقطاع الأجنبي")
st.write("رادار مباشر يرصد التحديات الميدانية والقرارات والبيانات المفتوحة للقطاع الخاص الأجنبي في المملكة.")

search_query = st.text_input("🔍 اكتب القطاع أو التحدي للتفتيش والتحليل الحقيقي:", value="الخدمات اللوجستية")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📰 مرصد الإعلام المباشر", 
    "🏛️ البيانات المفتوحة الحية (open.gov.sa)", 
    "📊 تحليل الإفصاحات بالذكاء الاصطناعي", 
    "💬 استطلاع اللوائح والأنظمة", 
    "💡 التحديات المحتملة"
])

# ----- التبويب 1: رادار الأخبار الحية -----
with tab1:
    st.subheader("📰 أحدث الأخبار والقرارات الرسمية الحية")
    encoded_query = urllib.parse.quote(f"{search_query} السعودية استثمار")
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ar&gl=SA&ceid=SA:ar"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(rss_url, headers=headers, timeout=7)
        root = ET.fromstring(res.text)
        items = root.findall('.//item')
        if items:
            st.success(f"✅ تم سحب {len(items[:8])} خبراً حياً ومباشراً من المصادر:")
            for item in items[:8]:
                title = item.find('title').text if item.find('title') is not None else "بدون عنوان"
                link = item.find('link').text if item.find('link') is not None else "#"
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else "غير محدد"
                with st.expander(f"📌 {title}"):
                    st.write(f"**تاريخ النشر:** {pub_date}")
                    st.markdown(f"🔗 **رابط الخبر المباشر:** [{link}]({link})")
        else:
            st.warning("لا توجد أخبار حديثة مسجلة بكلمة البحث الحالية.")
    except Exception as e:
        st.error(f"تعذر جلب الأخبار الحية: {e}")

# ----- التبويب 2: محرك الروابط المباشرة للبيانات المفتوحة -----
with tab2:
    st.subheader("🏛️ دليل الوصول المباشر لحزم البيانات المفتوحة (open.gov.sa)")
    
    encoded_search = urllib.parse.quote(search_query)
    direct_gov_url = f"https://open.gov.sa/dataset?q={encoded_search}"
    
    st.info(f"🔎 البحث الحالي مخصص لقطاع: **{search_query}**")
    st.markdown(f"🔗 **[اضغط هنا للوصول المباشر لحزم البيانات المفتوحة الخاصة بـ ({search_query}) على منصة open.gov.sa]({direct_gov_url})**")
    
    st.write("---")
    st.write("**📌 الروابط المباشرة لأهم المنصات الوطنية للبيانات المفتوحة:**")
    
    # جدول الروابط المباشرة الموثوقة
    portal_data = [
        {"الجهة / المنصة": "البوابة الوطنية للبيانات المفتوحة", "الوصف": "المحرك الموحد لكافة حزم البيانات الحكومية", "رابط الوصول المباشر": "https://open.gov.sa/"},
        {"الجهة العامة للإحصاء (Gastat)", "الوصف": "مؤشرات التجارة الخارجية، الاقتصاد، والقوى العاملة", "رابط الوصول المباشر": "https://www.stats.gov.sa/ar/page/259"},
        {"وزارة التجارة - البيانات المفتوحة", "الوصف": "بيانات السجلات التجارية، الشركات الأجنبية والمؤسسات", "رابط الوصول المباشر": "https://mc.gov.sa/ar/eservices/open-data/Pages/default.aspx"},
        {"وزارة الاستثمار - استثمر في السعودية", "الوصف": "التقارير الاقتصادية والفرص الاستثمارية الأجنبية", "رابط الوصول المباشر": "https://investsaudi.sa/ar/"},
        {"الهيئة العامة للغذة والدواء (SFDA)", "الوصف": "بيانات التراخيص والمنتجات والمنشآت المعتمدة", "رابط الوصول المباشر": "https://sfda.gov.sa/ar/open-data"},
        {"وزارة الصناعة والثروة المعدنية", "الوصف": "بيانات المصانع، التراخيص الصناعية والمناطق اللوجستية", "رابط الوصول المباشر": "https://mim.gov.sa/mim/opendata.html"},
        {"وزارة النقل والخدمات اللوجستية", "الوصف": "مؤشرات الأداء اللوجستي، حركة الشحن والموانئ", "رابط الوصول المباشر": "https://mot.gov.sa/ar/OpenData/Pages/default.aspx"}
    ]
    
    df_portals = pd.DataFrame(portal_data)
    st.dataframe(df_portals, use_container_width=True)

# ----- التبويب 3: التحليل المالي بالذكاء الاصطناعي الحقيقي -----
with tab3:
    st.subheader("📊 تحليل الإفصاحات والاتجاهات المالية للقطاع")
    with st.spinner("جاري الاتصال بالذكاء الاصطناعي لتوليد التحليل المالي الحقيقي..."):
        prompt = f"قدم تحليلاً مالياً حقيقياً واستباقياً لقطاع '{search_query}' في السعودية للشركات الأجنبية، واذكر أهم 3 مخاطر مالية وتأثيرها على رأس المال."
        ai_res = ask_ai(prompt)
        st.markdown(ai_res)

# ----- التبويب 4: مرئيات اللوائح بالذكاء الاصطناعي الحقيقي -----
with tab4:
    st.subheader("💬 تحليلات التشريعات ومرئيات المستثمرين الأجانب")
    with st.spinner("جاري استقراء اللوائح عبر الذكاء الاصطناعي..."):
        prompt = f"بصفتك خبيراً تنظيماً، استقرئ التحديات التنظيمية واللوائح الحكومية المرتقبة في السعودية المتعلقة بقطاع '{search_query}' والآراء المتوقعة للمستثمرين الأجانب."
        ai_res = ask_ai(prompt)
        st.markdown(ai_res)

# ----- التبويب 5: مصفوفة التحديات والمحفزات بالذكاء الاصطناعي الحقيقي -----
with tab5:
    st.subheader("💡 مصفوفة التحديات الميدانية والمحفزات الحكومية المقابلة")
    with st.spinner("جاري صياغة مصفوفة الحلول بواسطة الذكاء الاصطناعي..."):
        prompt = f"قم بصياغة جدول ماركداون يحتوي على: (التحدي الميداني، مستوى الخطورة، المحفز الحكومي المتاح في السعودية، والتوصية الاستباقية) للقطاع التالي: {search_query}"
        ai_res = ask_ai(prompt)
        st.markdown(ai_res)
