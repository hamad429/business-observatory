import streamlit as st
import pandas as pd
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

st.set_page_config(page_title="المرصد الشامل لبيئة الأعمال", page_icon="📡", layout="wide")

st.title("📡 المرصد الشامل لمرئيات ومتغيرات بيئة الأعمال والقطاع الأجنبي")
st.write("رادار متكامل يرصد التحديات الميدانية والفرص الاستثمارية للقطاع الخاص الأجنبي في المملكة.")

search_query = st.text_input("🔍 شريط البحث والتفتيش التفاعلي (اكتب القطاع، الخبر، أو التحدي):", placeholder="مثال: الاستثمار، اللوجستي، الصحة، التعدين...")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📰 رادار الإعلام والويب حياً", 
    "🏛️ البيانات المفتوحة (open.gov.sa)", 
    "📊 القوائم الإفصاحية والمالية", 
    "💬 نبض منصة استطلع والشبكات", 
    "💡 مصفوفة التحديات والمحفزات"
])

with tab1:
    st.subheader("📰 التحديثات الإخبارية والقرارات الصادرة المباشرة")
    query_text = search_query if search_query else "الاستثمار الأجنبي السعودية"
    encoded_query = urllib.parse.quote(query_text)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ar&gl=SA&ceid=SA:ar"
    
    try:
        req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=5).read()
        root = ET.fromstring(html)
        items = root.findall('.//item')
        if items:
            st.success(f"✅ تم رصد {len(items[:8])} خبراً حقيقياً مباشراً:")
            for item in items[:8]:
                title = item.find('title').text if item.find('title') is not None else "خبر بدون عنوان"
                link = item.find('link').text if item.find('link') is not None else "#"
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else "غير محدد"
                with st.expander(f"📌 {title}"):
                    st.write(f"**تاريخ النشر:** {pub_date}")
                    st.markdown(f"🔗 **رابط التثبت المباشر من المصدر:** [{link}]({link})")
        else:
            st.warning("لم يتم رصد نتائج إخبارية لهذه الكلمة حالياً.")
    except Exception:
        st.info("جاري تحميل الأخبار الحية...")

with tab2:
    st.subheader("🏛️ حزم البيانات المفتوحة والتراخيص")
    sample_open = [
        {"حزمة البيانات": "بيانات السجلات التجارية الأجنبية النشطة", "الجهة المصدرة": "وزارة التجارة", "رابط الحزمة": "https://open.gov.sa/dataset/cr-foreign"},
        {"حزمة البيانات": "تراخيص الاستثمار الأجنبي المباشر", "الجهة المصدرة": "وزارة الاستثمار", "رابط الحزمة": "https://open.gov.sa/dataset/investment-licenses"}
    ]
    df_open = pd.DataFrame(sample_open)
    if search_query:
        df_open = df_open[df_open['حزمة البيانات'].str.contains(search_query, case=False, na=False)]
    st.dataframe(df_open, use_container_width=True)

with tab3:
    st.subheader("📊 مؤشرات الإفصاحات المالية وتغيرات رأس المال")
    financial_data = [
        {"الشركة / القطاع الأجنبي": "شركة الخدمات اللوجستية العالمية", "نوع الإفصاح": "إعادة هيكلة وتخفيض ميزانية", "المؤشر المالي": "تراجع الهامش التشغيلي بـ 4%", "مستوى التنبيه": "مرتفع الخطورة"},
        {"الشركة / القطاع الأجنبي": "مجموعة التقنية والحلول السحابية", "نوع الإفصاح": "زيادة رأس المال والامتثال", "المؤشر المالي": "نمو الإيرادات المحلية بـ 12%", "مستوى التنبيه": "منخفض"}
    ]
    df_fin = pd.DataFrame(financial_data)
    if search_query:
        df_fin = df_fin[df_fin['الشركة / القطاع الأجنبي'].str.contains(search_query, case=False, na=False)]
    st.dataframe(df_fin, use_container_width=True)

with tab4:
    st.subheader("💬 مرئيات منصة 'استطلع' ونبض الشبكات المهنية (LinkedIn)")
    social_data = [
        {"المنصة": "استطلع (NCC)", "مشروع اللائحة": "مشروع تعديل ضوابط التخليص الجمركي", "مرئيات المستثمرين الأجانب": "اعتراض على ارتفاع رسوم التخزين والتأخير", "الحالة": "تحت الدراسة"},
        {"المنصة": "شبكات مهنية (LinkedIn)", "مشروع اللائحة": "نقاشات توطين الوظائف الهندسية", "مرئيات المستثمرين الأجانب": "مطالبة بمهلة إضافية لاستقطاب الكفاءات", "الحالة": "رصد استباقي"}
    ]
    df_soc = pd.DataFrame(social_data)
    if search_query:
        df_soc = df_soc[df_soc['مشروع اللائحة'].str.contains(search_query, case=False, na=False)]
    st.dataframe(df_soc, use_container_width=True)

with tab5:
    st.subheader("💡 تحليل التحديات ومطابقة المحفزات الحكومية")
    matrix_data = [
        {"القطاع": "الخدمات اللوجستية", "التحدي المرصود": "تعدد جهات التراخيص وتأخر الفسح", "مستوى الخطورة": "مرتفع الخطورة", "المحفز الحكومي المتاح": "تفعيل مسار 'الفسح خلال 24 ساعة' بالزكاة والجمارك", "التوصية الاستباقية": "ربط رخصة النقل بالفسح الموحد"},
        {"القطاع": "التقنية والبيانات", "التحدي المرصود": "اشتراطات استضافة البيانات السحابية", "مستوى الخطورة": "متوسط الخطورة", "المحفز الحكومي المتاح": "برامج دعم السحابة المعتمدة من سدايا", "التوصية الاستباقية": "تقديم فترة سماح إجرائية لمدة 6 أشهر"}
    ]
    df_mat = pd.DataFrame(matrix_data)
    if search_query:
        df_mat = df_mat[df_mat['القطاع'].str.contains(search_query, case=False, na=False)]
    st.dataframe(df_mat, use_container_width=True)
