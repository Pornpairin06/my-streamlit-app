import streamlit as st
import requests
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="MysticStar",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    /* Background หมู่ดาว */
    .stApp {
        background: radial-gradient(ellipse at bottom, #1a1a2e 0%, #0f0f1e 100%);
        color: #ffffff;
        background-image: url('https://static.thairath.co.th/media/PZnhTOtr5D3rd9oc97Dle3eYpO4IIFDAjc2SdH2Ps199kVj.jpg'); /* ตัวอย่างดาว */
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* ปรับ Card ของ Streamlit */
    .stButton>button {
        background-color: #8a2be2;
        color: white;
        border-radius: 10px;
        height: 40px;
        width: 100%;
        font-size: 16px;
    }

    .stTextInput>div>div>input {
        background-color: #f3e6ff;
        color: #000000;
    }

    .stSelectbox>div>div>div>select {
        background-color: #f3e6ff;
        color: #000000;
    }

    h1, h2, h3, h4, h5 {
        color: #dda0dd;
    }

    /* เปลี่ยนสี label ของ input */
    label, .stTextInput>label, .stTextArea>label, .stSelectbox>label {
        color: white;
        font-weight: bold;
    }

    .crystal-ball {
    width: 200px;
    height: 200px;
    margin: auto;
    margin-bottom: 20px;
    border-radius: 50%;
    position: relative;
    background: radial-gradient(circle at 30% 30%, #ffffff66, #8a2be2cc, #000000dd);
    box-shadow:
        0 0 25px #c084f5,
        0 0 50px #a855f7,
        inset 0 0 30px #ffffff44;
    
    /* อนิเมชันรวมเพื่อให้ดูเหมือนมีพลัง */
    animation: float 4s ease-in-out infinite alternate,
               rotateGlow 12s linear infinite;
    }

    .crystal-ball::before {
    content: "";
    position: absolute;
    top: 10%;
    left: 10%;
    width: 80%;
    height: 80%;
    border-radius: 50%;
    background: radial-gradient(circle, #ffffff33, #ffffff00);
    animation: innerSpin 6s linear infinite;
    }

    @keyframes float {
    0% { transform: translateY(0px); }
    100% { transform: translateY(-12px); }
    }

    @keyframes rotateGlow {
    0% { box-shadow:
            0 0 25px #c084f5,
            0 0 50px #a855f7,
            inset 0 0 30px #ffffff44; }
    50% { box-shadow:
            0 0 35px #d8b4fe,
            0 0 70px #c084f5,
            inset 0 0 40px #ffffff66; }
    100% { box-shadow:
            0 0 25px #c084f5,
            0 0 50px #a855f7,
            inset 0 0 30px #ffffff44; }
    }

    @keyframes innerSpin {
    0% { transform: rotate(0deg); filter: blur(2px); }
    100% { transform: rotate(360deg); filter: blur(4px); }
    }
   </style>

   <div class="crystal-ball"></div>
    """,
    unsafe_allow_html=True)

st.title("🔮 MysticStar - เว็บพยากรณ์ดวงชะตายุคใหม่")

# Sidebar API Key
st.sidebar.header("API Key ของ Google Gemini(2.0 Flash)")
api_key = st.sidebar.text_input("ใส่ API Key ของคุณ", type="password")

# Input จากผู้ใช้
name = st.text_input("ชื่อ")
col1, col2, col3 = st.columns(3)

with col1:
    day = st.selectbox("วันเกิด", list(range(1,32)))
with col2:
    month = st.selectbox("เดือนเกิด", ["มกราคม","กุมภาพันธ์","มีนาคม","เมษายน","พฤษภาคม","มิถุนายน",
                                       "กรกฎาคม","สิงหาคม","กันยายน","ตุลาคม","พฤศจิกายน","ธันวาคม"])
with col3:
    year = st.selectbox("ปีเกิด (ค.ศ.)", list(range(1950, date.today().year+1)))

dob = f"{day:02d}/{month}/{year}"
time_of_birth = st.text_input("เวลาเกิด (เช่น 12:00)")
question = st.text_area("คำถามที่อยากถาม")

if st.button("ดูดวง"):
    if not (name and time_of_birth and question and api_key):
        st.warning("กรุณากรอกทุกช่องให้ครบถ้วน รวมถึง API Key")
    else:
        st.info("กรุณาตั้งจิตอธิษฐานและรอผลคำทำนายซักครู่...")

        # prompt
        prompt = f"ชื่อ: {name}\nวันเกิด: {dob}\nเวลาเกิด: {time_of_birth}\nคำถาม: {question}\nกรุณาตอบคำถามด้วยหลักโหราศาสตร์ไทย พร้อมให้คำแนะนำ ขอไม่เกิน 500 คำ"

        model_name = "gemini-2.0-flash" 
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 500
            }
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                answer = response.json()['candidates'][0]['content']['parts'][0]['text']
            else:
                answer = f"เกิดข้อผิดพลาด {response.status_code}:\n{response.text}"

        except Exception as e:
            answer = f"เกิดข้อผิดพลาดในการเชื่อมต่อ API: {e}"

        # แสดงผล-
        st.subheader("คำทำนายของคุณ:")
        st.markdown(f"<div style='background-color:#9370DB;padding:15px;border-radius:10px'>{answer}</div>", unsafe_allow_html=True)

        df = pd.DataFrame({
            "ชื่อ": [name],
            "วันเกิด": [dob],
            "เวลาเกิด": [time_of_birth],
            "คำถาม": [question],
            "คำทำนาย": [answer]
        })
        st.subheader("สรุปคำทำนายของคุณ")
        st.table(df.T.style.set_properties(**{
    'color': 'white',
    'background-color': '#4B0082',
    'white-space': 'normal',
    'word-wrap': 'break-word'
}))
        # ปุ่มดาวน์โหลด
        csv_data = df.to_csv(index=False)
        st.download_button(
    label="ดาวน์โหลดผลคำทำนาย",
    data=csv_data,
    file_name="horoscope.csv",
    mime="text/csv"
)

        # ปุ่มแชร์คำทำนาย
        st.subheader("คัดลอกผลคำทำนายไปแชร์ได้เลย!")
        share_text = answer.replace('"', '\\"') 
