import streamlit as st
import pandas as pd
import urllib.parse
import urllib.request
import json
import xml.etree.ElementTree as ET

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

# 3. تثبيت مفتاح الذكاء الاصطناعي برمجياً (ضع مفتاح Gemini الخاص بك هنا)
api_key = "YOUR_GEMINI_API_KEY"

def ask_ai(prompt):
    """دالة الربط المباشر مع الذكاء الاصطناعي عبر API"""
    if not api_key or api_key == "YOUR_GEMINI_API_KEY":
        return "⚠️ يرجى وضع مفتاح Gemini API في السطر 20 لتفعيل تحليلات الذكاء الاصطناعي المباشرة."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        result = json.loads(response.read().decode('utf-8'))
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"خطأ في الاتصال بالذكاء الاصطناعي: {str(e)}"

# 4. واجهة المرصد الرئيسية
st.title("📡 المرصد الشامل لمرئيات ومتغيرات بيئة الأعمال والقطاع الأجنبي")
st.write("رادار مباشر يرصد التحديات الميدانية والقرارات والبيانات المفتوحة للقطاع الخاص الأجنبي في المملكة.")

search_query = st.text_input("🔍 اكتب القطاع أو التحدي للتفتيش والتحليل الحقيقي:", value="الخدمات اللوجستية")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📰 مرصد الإعلام المباشر", 
    "🏛️ البيانات المفتوحة  (open.gov.sa)", 
    "📊 تحليل الإفصاحات بالذكاء الاصطناعي", 
    "💬 استطلاع اللوائح والأنظمة", 
    "💡  التحديات المحتملة"
])

# ----- التبويب 1: رادار الأخبار الحية -----
with tab1:
    st.subheader("📰 أحدث الأخبار والقرارات الرسمية الحية")
    encoded_query = urllib.parse.quote(f"{search_query} السعودية استثمار")
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ar&gl=SA&ceid=SA:ar"
    
    try:
        req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=5).read()
        root = ET.fromstring(html)
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
        req = urllib.request.Request(gov_api, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=6).read()
        data = json.loads(res.decode('utf-8'))
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

# ----- التبويب 3: التحليل المالي والإفصاحات بالذكاء الاصطناعي -----
with tab3:
    st.subheader("📊 تحليل الإفصاحات والاتجاهات المالية للقطاع")
    with st.spinner("جاري تحليل الاتجاهات المالية باستخدام الذكاء الاصطناعي..."):
        prompt = f"قم بتقديم تحليل مالي استباقي وموجز لقطاع '{search_query}' في السعودية للشركات الأجنبية، وذكر أهم 3 مخاطر مالية وتأثيرها على رأس المال بناءً على تحركات السوق الحالية."
        ai_res = ask_ai(prompt)
        st.markdown(ai_res)

# ----- التبويب 4: مرئيات منصة استطلع والأنظمة -----
with tab4:
    st.subheader("💬 تحليلات التشريعات ومرئيات المستثمرين الأجانب")
    with st.spinner("جاري استقراء مرئيات المستثمرين واللوائح..."):
        prompt = f"بصفتك خبيراً تنظيماً، استقرئ التحديات التنظيمية واللوائح الحكومية المرتقبة في السعودية المتعلقة بقطاع '{search_query}' والآراء المتوقعة للمستثمرين الأجانب."
        ai_res = ask_ai(prompt)
        st.markdown(ai_res)

# ----- التبويب 5: مصفوفة التحديات والمحفزات المباشرة -----
with tab5:
    st.subheader("💡 مصفوفة التحديات الميدانية والمحفزات الحكومية المقابلة")
    with st.spinner("جاري بناء مصفوفة الحلول والمحفزات..."):
        prompt = f"قم بصياغة جدول يحتوي على: (التحدي الميداني، مستوى الخطورة، المحفز الحكومي المتاح في السعودية، والتوصية الاستباقية) للقطاع التالي: {search_query}"
        ai_res = ask_ai(prompt)
        st.markdown(ai_res)
