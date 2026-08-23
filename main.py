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

# 3. مفتاح الذكاء الاصطناعي الحقيقي الخاص بك
api_key = "AQ.Ab8RN6JO7Umu9mZsx05Ip_Se8UdqV8twMlvcVbKFVzgPTDu76w"

def ask_ai(prompt):
    """دالة اتصال حقيقية ومباشرة بنموذج الذكاء الاصطناعي"""
    if not api_key:
        return "❌ لا يوجد مفتاح مثبت."
    
    # إرسال الطلب حياً لموديل الذكاء الاصطناعي
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
            return f"❌ خطأ حقيقي من سيرفر الذكاء الاصطناعي: {err}"
    except Exception as e:
        return f"❌ تعذر الاتصال بالسيرفر: {str(e)}"

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
        res = requests.get(rss_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
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

# ----- التبويب 2: ربط حي مع بوابة البيانات المفتوحة السعودية -----
with tab2:
    st.subheader("🏛️ نتائج الحزم التفاعلية المباشرة من (open.gov.sa)")
    gov_api = f"https://open.gov.sa/api/3/action/package_search?q={urllib.parse.quote(search_query)}&rows=10"
    try:
        res = requests.get(gov_api, headers={'User-Agent': 'Mozilla/5.0'}, timeout=6)
        data = res.json()
        results = data.get('result', {}).get('results', [])
        
        if results:
            clean_data = []
            for r in results:
                org = r.get('organization', {})
                org_title = org.get('title') if org else "جهة حكومية"
                clean_data.append({
                    "عنوان حزمة البيانات المفتوحة": r.get('title'),
                    "الجهة الحكومية المصدرة": org_title,
                    "عدد الموارد والملفات": r.get('num_resources', 0),
                    "رابط الوصول المباشر": f"https://open.gov.sa/dataset/{r.get('name')}"
                })
            st.dataframe(pd.DataFrame(clean_data), use_container_width=True)
        else:
            st.info("لم يتم العثور على حزم بيانات مفتوحة مرتبطة مباشرة بهذه الكلمة حالياً في البوابة الوطنية.")
    except Exception:
        st.warning("تعذر الاتصال المباشر برابط API المنصة الوطنية للبيانات المفتوحة حالياً.")

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
