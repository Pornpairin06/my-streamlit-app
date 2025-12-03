import streamlit as st
import requests

st.title("🔮 เว็บดูดวง Gemini 2.0 Flash")

name = st.text_input("ชื่อ")
dob = st.date_input("วันเกิด")
time_of_birth = st.text_input("เวลาเกิด (เช่น 02:45)")
question = st.text_area("คำถามที่อยากถาม")
api_key = st.text_input("API Key", type="password")

if st.button("ส่งคำถาม"):
    if not (name and dob and time_of_birth and question and api_key):
        st.warning("กรุณากรอกทุกช่อง")
    else:
        # --- prompt เป็น single string ไม่มี indent ---
        prompt = {"text": f"ชื่อ: {name}\nวันเกิด: {dob.strftime('%d/%m/%Y')}\nเวลาเกิด: {time_of_birth}\nคำถาม: {question}\nกรุณาตอบคำถามเกี่ยวกับดวงชะตาของผู้ใช้"}

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateText?key={api_key}"

        data = {
            "prompt": prompt,
            "temperature": 0.7,
            "maxOutputTokens": 500
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                answer = response.json()['candidates'][0]['output']
                st.subheader("คำตอบจาก AI:")
                st.write(answer)
            else:
                st.error(f"เกิดข้อผิดพลาด {response.status_code}")
                st.text(response.text)
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อ API: {e}")


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