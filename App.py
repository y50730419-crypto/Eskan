
import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="حاسبة الإسكان - واجهة مخصصة", layout="centered")
st.title("🏡 حاسبة الإسكان المصرية 📊")

# إحضار المفتاح واسم الموديل من الإعدادات الآمنة
try:
    # مفتاح API واسم الموديل من ملف Secrets (الملف السري)
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model_name = st.secrets["CUSTOM_MODEL_NAME"]
    model = genai.GenerativeModel(model_name)

    st.header("1. البيانات المالية الأساسية")

    # حقول إدخال البيانات المالية
    prepaid = st.number_input("المدفوعات ما قبل الاستلام (المقدم)", min_value=0, value=46700, step=100)
    down_payment = st.number_input("دفعة الاستلام (المقدم الثاني)", min_value=0, value=50000, step=100)
    current_installment = st.number_input("القسط الشهري الحالي", min_value=0, value=1300, step=50)

    st.header("2. مدة القسط والدعم")

    subsidy = st.number_input("قيمة الدعم المخصوم (اختياري)", min_value=0, value=0, step=100)
    annual_increase_rate = st.slider("نسبة الزيادة السنوية (%)", min_value=0.0, max_value=20.0, value=7.0, step=0.5)
    remaining_period = st.number_input("المدة المتبقية على القسط (بالسنوات)", min_value=1, value=20, step=1)

    # زر إرسال
    if st.button("احسب الجدول الزمني والتحليل"):
        if current_installment <= 0:
            st.warning("الرجاء إدخال قيمة صحيحة للقسط الشهري الحالي.")
        else:
            # تجميع كل بيانات المستخدم في سؤال واحد للنموذج
            prompt_data = f"""
            أنت آلة حاسبة الإسكان المخصصة. بناءً على البيانات التالية، قم بتحليل الموقف المالي للمستخدم وحساب الجدول الزمني الكامل والنهائي لسداد الوحدة (المتبقي من القرض، الإجمالي المدفوع، قيمة القسط بعد الزيادة).
            * المدفوعات السابقة (المقدم الأول): {prepaid} جنيه.
            * دفعة الاستلام (المقدم الثاني): {down_payment} جنيه.
            * القسط الشهري الحالي: {current_installment} جنيه.
            * قيمة الدعم المخصوم: {subsidy} جنيه.
            * نسبة الزيادة السنوية للقسط: {annual_increase_rate}%.
            * المدة المتبقية على القرض (المطلوب حسابها): {remaining_period} سنوات.
            """
            
            with st.spinner("جاري تحليل بيانات حاسبة الإسكان..."):
                response = model.generate_content(prompt_data)
                st.success("✅ تحليل حاسبة الإسكان:")
                st.markdown(response.text)

except KeyError:
    st.error("خطأ في الإعدادات: يرجى التأكد من أن المفتاح السري (GOOGLE_API_KEY) واسم الموديل (CUSTOM_MODEL_NAME) مضبوطان بشكل صحيح في قائمة الأسرار.")
except Exception as e:
    st.error(f"حدث خطأ أثناء تشغيل حاسبة الإسكان. يرجى التحقق من المفتاح السري والإعدادات. الخطأ: {e}")
