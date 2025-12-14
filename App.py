
import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="حاسبة الإسكان الذكية")
st.title("حاسبة الإسكان المصرية 💰")

# إحضار المفتاح واسم الموديل من الإعدادات الآمنة
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

    # هنا يتم استخدام اسم الأداة المخصصة من الإعدادات السريعة
    model_name = st.secrets["CUSTOM_MODEL_NAME"] 
    model = genai.GenerativeModel(model_name) 

    # واجهة الشات/الإدخال
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("أدخل بيانات الإسكان أو سؤالك هنا..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

except KeyError:
    st.error("خطأ في الإعدادات: يرجى التأكد من وضع مفتاح API واسم الأداة (CUSTOM_MODEL_NAME) في قائمة الأسرار.")
except Exception as e:
    st.error(f"حدث خطأ أثناء الاتصال بأداة الإسكان. يرجى التحقق من اسم الأداة.")
