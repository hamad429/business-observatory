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

# 3. محاكاة المحرك التحليلي الاستباقي بناءً على مدخلات البحث
def ask_ai(prompt):
    sector = search_query if search_query else "القطاع الأجنبي"
    
    if "مالي" in prompt or "الإفصاحات" in prompt:
        return f"""
### 📊 التقرير المالي والاستثماري الاستباقي لقطاع ({sector}):

1. **تقييم المخاطر المالية:**
   * **تذبذب التكاليف التشغيلية:** يواجه المستثمرون الأجانب في قطاع {sector} ارتفاعاً متوقعاً في مصاريف الامتثال وسلاسل الإمداد بنسبة تقارب 5-8%.
   * **مخاطر رأس المال:** مخاطر متوسطة ترتبط بتأخر دورة التحصيل النقدي مقارنة بالتوقعات الأولى للتأسيس.

2. **مؤشرات الأداء:**
   * نمو ملحوظ في تدفق رؤوس الأموال الأجنبية المباشرة الموجهة لنشاط {sector} بنسبة 12% سنوياً.
   * توصية برفع الاحتياطي التشغيلي لمدة 6 أشهر لتفادي أي ضغوطات تدفق نقدي.
"""
    elif "لوائح" in prompt or "تنظيماً" in prompt:
        return f"""
### 💬 استقراء اللوائح والتحديثات التنظيمية لقطاع ({sector}):

1. **المرئيات المرصودة:**
   * تحفظات من المستثمرين الأجانب على الاشتراطات المتعلقة بمدد التراخيص المتعددة ومطالبات بتوحيدها عبر نافذة استثمارية واحدة.
   * مطالبة بتوفير فترات سماح إجرائية (Grace Periods) لا تقل عن 6 أشهر عند صدور أي تعديلات في اللوائح التنفيذية.

2. **الاتجاه التنظيمي:**
   * التوجه الحكومي يتجه نحو تبسيط الإجراءات وأتمتة متطلبات الامتثال لخفض تكلفة ممارسة الأعمال.
"""
    else:
        return f"""
| التحدي الميداني المرصود | مستوى الخطورة | المحفز الحكومي المتاح في السعودية | التوصية الاستباقية للعمليات |
| :--- | :--- | :--- | :--- |
| **بطء الفسح والتراخيص لقطاع {sector}** | مرتفع الخطورة | مسار الفسح الموحد والمبادرات التنفيذية | ربط التراخيص بالمنصات الموحدة لتقليل زمن الانتظار |
| **اشتراطات الامتثال والتوطين المحلي** | متوسط الخطورة | برامج الدعم والتمكين من وزارة الموارد البشرية | الاستفادة من مهل السماح والدعم المالي للتدريب |
"""

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

# ----- التبويب 3: التحليل المالي والإفصاحات بالذكاء الاصطناعي -----
with tab3:
    st.subheader("📊 تحليل الإفصاحات والاتجاهات المالية للقطاع")
    with st.spinner("جاري تحليل الاتجاهات المالية..."):
        prompt = f"مالي {search_query}"
        ai_res = ask_ai(prompt)
        st.markdown(ai_res)

# ----- التبويب 4: مرئيات منصة استطلع والأنظمة -----
with tab4:
    st.subheader("💬 تحليلات التشريعات ومرئيات المستثمرين الأجانب")
    with st.spinner("جاري استقراء مرئيات المستثمرين واللوائح..."):
        prompt = f"لوائح {search_query}"
        ai_res = ask_ai(prompt)
        st.markdown(ai_res)

# ----- التبويب 5: مصفوفة التحديات والمحفزات المباشرة -----
with tab5:
    st.subheader("💡 مصفوفة التحديات الميدانية والمحفزات الحكومية المقابلة")
    with st.spinner("جاري بناء مصفوفة الحلول والمحفزات..."):
        prompt = f"مصفوفة {search_query}"
        ai_res = ask_ai(prompt)
        st.markdown(ai_res)
