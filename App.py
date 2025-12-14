import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="موقعي الذكي")

# العنوان
st.title("مساعدي الذكي 🤖")

# إحضار المفتاح من الإعدادات الآمنة
try:
    # سنستخدم المفتاح الذي وضعناه سراً في الخطوة القادمة
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash') 

    # واجهة الشات
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("اكتب سؤالك هنا..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    # هذه الرسالة تظهر لو نسيت وضع المفتاح السري في الخطوة التالية
    st.error("يرجى التأكد من وضع مفتاح API الخاص بك بشكل صحيح في الإعدادات السرية.")
  
