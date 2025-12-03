import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="เว็บดูดวง AI", layout="centered")
st.title("เว็บดูดวงด้วย Gemini AI ✨")

# --- ฟอร์มกรอกข้อมูลผู้ใช้ ---
with st.form("user_form"):
    name = st.text_input("ชื่อของคุณ")
    dob = st.date_input("วันเกิด")
    time_of_birth = st.text_input("เวลาเกิด (เช่น 02:45)")
    question = st.text_area("คำถามเกี่ยวกับดวงชะตาของคุณ")
    api_key = st.text_input("กรอก Gemini API Key ของคุณ (AIzaSy...)", type="password")
    
    submitted = st.form_submit_button("ถามดวง")

if submitted:
    if not all([name, dob, time_of_birth, question, api_key]):
        st.warning("กรุณากรอกทุกช่องให้ครบ")
    else:
        # --- เตรียมข้อความที่จะส่งให้ Gemini ---
        prompt = f"""
        ชื่อ: {name}
        วันเกิด: {dob.strftime('%d/%m/%Y')}
        เวลาเกิด: {time_of_birth}
        
        คำถาม: {question}
        
        กรุณาตอบคำถามเกี่ยวกับดวงชะตาของผู้ใช้
        """

        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        data =  {
    "contents": [{
        "parts": [{
            "text": prompt
        }]
    }]
}
        response = requests.post(url,json=data)
        print(response.json())

    #try:
            # ส่ง request ไป Gemini API
           # response = requests.post(f"{url}?key={api_key}", json=payload, headers=headers, timeout=15)
           # response.raise_for_status()
           # data = response.json()
            
            # ดึงคำตอบ
            #answer = data.get("candidates", [{}])[0].get("content", "ไม่พบคำตอบจาก Gemini")
            
            # แสดงผลในเว็บ
            #st.success("คำตอบจาก Gemini AI:")
           # st.markdown(f"💫 {answer}")

       # except requests.exceptions.HTTPError as errh:
           # st.error(f"HTTP Error: {errh}")
        #except requests.exceptions.ConnectionError as errc:
           # st.error(f"Connection Error: {errc}")
       # except requests.exceptions.Timeout as errt:
           # st.error(f"Timeout Error: {errt}")
       # except Exception as e:
           # st.error(f"เกิดข้อผิดพลาด: {e}")"""