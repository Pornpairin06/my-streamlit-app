import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from io import BytesIO

try:
    from openai import OpenAI
except:
    OpenAI = None

# -------------------------------
# Page configuration + purple theme
# -------------------------------
st.set_page_config(page_title="🔮 Mystic Purple Astrology", layout="wide")

st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(180deg, #f3e8ff, #d8b4fe, #a855f7, #3b0764);
    color: white;
}
.stSidebar {
    background: linear-gradient(180deg, #3b0764, #6d28d9);
}
h1, h2, h3 {
    text-shadow: 0 2px 8px rgba(0,0,0,0.35);
}
</style>
""",
    unsafe_allow_html=True,
)

# -------------------------------
# Sidebar (single)
# -------------------------------
st.sidebar.title("🔐 API Key")
openai_key = st.sidebar.text_input("OpenAI API Key", type="password")

# -------------------------------
# Helpers
# -------------------------------
def init_client(key):
    if not key or OpenAI is None:
        return None
    try:
        return OpenAI(api_key=key)
    except:
        return None

client = init_client(openai_key)


def build_prompt(row, style):
    return (
        f"You are a mystical astrologer. Provide a {style.lower()} horoscope.
"
        f"Name: {row.get('Name','')}
"
        f"Birthdate: {row.get('Birthdate','')}
"
        f"Time: {row.get('Time','')}
"
        f"Focus: {row.get('Question','')}
"
        "Sections: Summary, Love, Career, Health, Advice."
    )


def ai_call(client, prompt, model):
    if not client:
        return "(กรุณาใส่ API Key ใน sidebar)"
    try:
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
        )
        return r.choices[0].message.content
    except Exception as e:
        return str(e)

# -------------------------------
# Main Page
# -------------------------------
st.title("🔮 Mystic Purple — เว็บดูดวง AI")
st.write("กรอกข้อมูลหรืออัปโหลดไฟล์ แล้วให้ AI ทำนายให้คุณ ✨")

st.markdown("---")

# Input mode
input_mode = st.radio("เลือกรูปแบบกรอกข้อมูล", ["กรอกเอง", "อัปโหลดไฟล์ (CSV/Excel)"])
user_df = None

if input_mode == "กรอกเอง":
    with st.form("form_input"):
        name = st.text_input("ชื่อ")
        birth = st.date_input("วันเกิด")
        time = st.time_input("เวลาเกิด", None)
        q = st.text_area("คำถามที่อยากให้เน้น", "")
        s = st.form_submit_button("เพิ่มข้อมูล")
        if s:
            user_df = pd.DataFrame([
                {
                    "Name": name,
                    "Birthdate": birth.strftime("%Y-%m-%d"),
                    "Time": time.strftime("%H:%M") if time else "",
                    "Question": q,
                }
            ])
else:
    file = st.file_uploader("อัปโหลด CSV/Excel", type=["csv", "xlsx"])
    if file:
        if file.name.endswith("csv"):
            user_df = pd.read_csv(file)
        else:
            user_df = pd.read_excel(file)
        st.success("โหลดไฟล์สำเร็จ ✨")

# -------------------------------
# Data editor
# -------------------------------
if user_df is not None:
    st.subheader("ข้อมูลที่ใช้ทำนาย (แก้ไขได้)")
    user_df = st.data_editor(user_df, num_rows="dynamic")

# -------------------------------
# Generate prediction
# -------------------------------
if user_df is not None and st.button("🔮 สร้างคำทำนาย"):
    st.header("✨ ผลคำทำนาย")

    results = []
    progress = st.progress(0)
    total = len(user_df)

    for i, row in user_df.iterrows():
        prompt = build_prompt(row, "Detailed")
        reading = ai_call(client, prompt, model_choice)
        results.append({
            "Name": row.get("Name", ""),
            "Reading": reading,
            "Model": model_choice,
            "GeneratedAt": datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'),
        })
        progress.progress((i + 1) / total)

    result_df = pd.DataFrame(results)

    st.subheader("ผลลัพธ์ทั้งหมด")
    st.dataframe(result_df)

    # Expanders
    for i, r in result_df.iterrows():
        with st.expander(f"🔎 ดูคำทำนายของ {r['Name']}"):
        st.markdown(r["Reading"])
        st.caption(f"Model:{r['Model']}|{r['GeneratedAt']}")

    # -------------------------------
    # SHARE BUTTON (แทนดาวน์โหลดไฟล์)
    # -------------------------------
    st.markdown("---")
    st.subheader("📤 แชร์ผลลัพธ์")

    share_text = "".join(
        [f"{r['Name']} — {r['Reading']}" for _, r in result_df.iterrows()]
    )

    st.text_area("คัดลอกข้อความด้านล่างเพื่อแชร์", share_text, height=200)

    st.success("คัดลอกเพื่อแชร์ได้เลย ✨")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("สร้างด้วย Streamlit x OpenAI | Mystic Purple Theme 💜")