import streamlit as st
import requests

st.set_page_config(page_title="เว็บดูดวง Gemini", page_icon="🔮")

st.title("🔮 เว็บดูดวง Gemini 2.0 Flash")

# --- ฟอร์มรับ input ---
name = st.text_input("ชื่อ")
dob = st.date_input("วันเกิด")
time_of_birth = st.text_input("เวลาเกิด (เช่น 02:45)")
question = st.text_area("คำถามที่อยากถาม")

api_key = st.text_input("API Key (Gemini 2.0 Flash)", type="password")

# --- ปุ่มส่งคำถาม ---
if st.button("ส่งคำถาม"):
    if not (name and dob and time_of_birth and question and api_key):
        st.warning("กรุณากรอกทุกช่อง")
    else:
        # --- สร้าง prompt ---
        prompt = f"""
ชื่อ: {name}
วันเกิด: {dob.strftime('%d/%m/%Y')}
เวลาเกิด: {time_of_birth}

คำถาม: {question}

กรุณาตอบคำถามเกี่ยวกับดวงชะตาของผู้ใช้
"""

        # --- ตั้ง URL ของ Gemini 2.0 Flash ---
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateText?key={api_key}"

        # --- body ของ request ---
        data = {
            "prompt": prompt,
            "temperature": 0.7,
            "maxOutputTokens": 500
        }

        # --- ส่ง request ---
        try:
            response = requests.post(url, json=data)
            
            if response.status_code == 200:
                res_json = response.json()
                # Gemini 2.0 Flash ส่งข้อความใน candidates[0].output
                answer = res_json['candidates'][0]['output']
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