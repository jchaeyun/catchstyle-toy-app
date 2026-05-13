import streamlit as st
import google.generativeai as genai

API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)

st.title("지원되는 모델 목록")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            st.write(m.name)
except Exception as e:
    st.error(f"목록을 불러오는 중 오류 발생: {e}")
