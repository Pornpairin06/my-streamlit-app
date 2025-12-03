import streamlit as st
import requests
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="เว็บดูดวง",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- ใช้ CSS สำหรับธีมสีและ background หมู่ดาว ---
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
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔮 MysticStar - เว็บพยากรณ์ดวงชะตายุคใหม่")

# --- Sidebar API Key ---
st.sidebar.header("API Key ของ Google Gemini(2.0 Flash)")
api_key = st.sidebar.text_input("ใส่ API Key ของคุณ", type="password")

# --- Input จากผู้ใช้ ---
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

# --- ปุ่มส่งคำถาม ---
if st.button("ดูดวง"):
    if not (name and time_of_birth and question and api_key):
        st.warning("กรุณากรอกทุกช่องให้ครบ")
    else:
        st.info("กรุณาตั้งจิตอธิษฐานและรอผลคำทำนายซักครู่...")

        # --- prompt ---
        prompt = f"ชื่อ: {name}\nวันเกิด: {dob}\nเวลาเกิด: {time_of_birth}\nคำถาม: {question}\nกรุณาตอบคำถามเกี่ยวกับดวงชะตาของผู้ใช้"

        # --- URL Gemini 2.0 Flash (ถ้า enable) ---
        model_name = "gemini-2.0-flash"  # ต้อง enable จริงในบัญชีของคุณ
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateText?key={api_key}"

        data = {
            "prompt": {"text": prompt},
            "temperature": 0.7,
            "maxOutputTokens": 500
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                answer = response.json()['candidates'][0]['output']
            else:
                answer = f"เกิดข้อผิดพลาด {response.status_code}:\n{response.text}"

        except Exception as e:
            answer = f"เกิดข้อผิดพลาดในการเชื่อมต่อ API: {e}"

        # --- แสดงผลแบบสวย ๆ ---
        st.subheader("คำทำนายของคุณ:")
        st.markdown(f"<div style='background-color:#9370DB;padding:15px;border-radius:10px'>{answer}</div>", unsafe_allow_html=True)

        # --- เก็บผลใน dataframe ---
        df = pd.DataFrame({
            "ชื่อ": [name],
            "วันเกิด": [dob],
            "เวลาเกิด": [time_of_birth],
            "คำถาม": [question],
            "คำทำนาย": [answer]
        })
        st.subheader("สรุปคำทำนายของคุณ")
        st.dataframe(df)