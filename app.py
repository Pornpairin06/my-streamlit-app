import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
import json
from datetime import date,time,datetime

# -------------------------------
# Page config + Theme
# -------------------------------
st.set_page_config(page_title="🔮 Mystic Purple Astrology", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #3b0764, #6d28d9, #a855f7);
    color: white;
}
.stSidebar {
    background: linear-gradient(180deg, #6d28d9, #3b0764);
    color: white;
}
h1, h2, h3 {
    text-shadow: 0 2px 8px rgba(0,0,0,0.35);
}
.stButton>button {
    background-color: #9d4edd;
    color: white;
    border: none;
}
.stButton>button:hover {
    background-color: #7b2cbf;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Sidebar: API Key
# -------------------------------
st.sidebar.title("กรุณาใส่ API KEY")
gemini_api_key = st.sidebar.text_input("Google Gemini API Key", type="password")

if gemini_api_key:
    genai.configure(gemini_api_key=gemini_api_key)

# -------------------------------
# Main Page
# -------------------------------
st.title("🔮 ดูดวงชะตาง่าย ๆ ผ่านเว็บแอป")

st.markdown("โปรดกรอกข้อมูลของคุณด้านล่าง จากนั้นกดปุ่มยืนยัน และรอคำทำนายโชคชะตา ✨")

# Input
with st.form("user_form"):
    name = st.text_input("ชื่อ")
    birth = st.date_input("วันเกิด",min_value=date(1950,1,1),max_value=date.today(),value=date(2025,1,1))
    time = st.time_input("เวลาเกิด", value=time(12,0),step=60)
    question = st.text_area("คำถามที่ต้องการจะถาม", "")
    submit = st.form_submit_button("ยืนยัน")
    
if submit:
   if not gemini_api_key:
        st.error("โปรดกรอก API KEY ในแถบด้านข้างก่อน!")
   elif not question.strip():
        st.error("กรุณากรอกคำถามที่ต้องการจะถาม")
   else:
      try:
          prompt = f"""
        You are a mystical astrologer. Provide a detailed horoscope.
        Name: {['Name']}
        Birthdate: {['Birthdate']}
        Time: {['Time']}
        Focus: {['Question']}
        Sections: Summary, Love, Career, Health, Advice.
        """
          model = genai.GenerativeModel("gemini-2.0-flash")
          response = model.generate_content(prompt)
          raw_text = response.text
          data = json.loads(raw_text)
          df = pd.DataFrame([data])
          st.header("✨ ผลคำทำนายของคุณ")
          st.dataframe(df)
      except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
    
    
   #results = []
    
    #for _, row in user_df.iterrows():
       # prompt = f"""
       # You are a mystical astrologer. Provide a detailed horoscope.
       # Name: {row['Name']}
       # Birthdate: {row['Birthdate']}
        #Time: {row['Time']}
        #Focus: {row['Question']}
        #Sections: Summary, Love, Career, Health, Advice.
       # """
"""reading = call_gemini(prompt, gemini_api_key)
        results.append({
            "Name": row["Name"],
            "Reading": reading,
            "GeneratedAt": datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
        })
    
    result_df = pd.DataFrame(results)
    st.dataframe(result_df)

    # -------------------------------
    # Download CSV
    # -------------------------------
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')
    
    csv = convert_df(result_df)
    st.download_button(
        label="📥 ดาวน์โหลดผลลัพธ์ เป็นไฟล์ CSV",
        data=csv,
        file_name='horoscope_results.csv',
        mime='text/csv'
    )
    
    # -------------------------------
    # Share text
    # -------------------------------
    st.subheader("📤 แชร์ผลลัพธ์ของคุณเลย!!")
    share_text = "\n\n".join([f"{r['Name']} — {r['Reading']}" for _, r in result_df.iterrows()])
    st.text_area("คัดลอกข้อความด้านล่างเพื่อแชร์", share_text, height=200)"""

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("สร้างด้วย Streamlit x Google Gemini API | Mystic Purple Theme 💜")