import streamlit as st
import google.generativeai as genai
from PIL import Image
import streamlit_analytics2 as streamlit_analytics

# 1. API 키 설정 (본인의 키로 교체하세요)
API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)

# 2. 토스 스타일 디자인 적용 (CSS)
st.set_page_config(page_title="패션 렌즈 MVP", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background-color: #f2f4f6; }
    .main { background-color: #f2f4f6; }
    /* 카드형 컨테이너 */
    .stImage, .stMarkdown {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        margin-bottom: 15px;
    }
    /* 토스 블루 버튼 */
    div.stButton > button {
        width: 100%;
        background-color: #3182f6;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 14px;
        font-weight: 700;
        font-size: 17px;
        transition: 0.2s;
    }
    div.stButton > button:hover { background-color: #1b64da; color: white; }
    /* 제목 스타일 */
    h1 { color: #191f28; font-size: 26px; font-weight: 900; margin-bottom: 5px; }
    p { color: #4e5968; }
    </style>
    """, unsafe_allow_html=True)

# 3. 분석 트래킹 시작 및 화면 UI 구성
with streamlit_analytics.track():
    st.title("패션 렌즈")
    st.write("사진 속 연예인이 입은 옷을 바로 찾아드릴게요.")

    # 업로드 섹션
    uploaded_file = st.file_uploader("", type=['jpg', 'png', 'jpeg'])

    if uploaded_file:
        # 이미지 표시
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        # 분석 버튼
        if st.button("어디 건지 찾아보기"):
            with st.spinner("구글 검색으로 정보를 분석하고 있어요..."):
                try:
                    # 구글 검색 기능이 탑재된 Gemini 모델 호출
                    model = genai.GenerativeModel(
                        model_name='gemini-1.5-flash',
                        tools=[{'google_search_retrieval': {}}] 
                    )
                    
                    prompt = """
                    이 이미지 속 인물이 입은 모든 옷(상의, 하의, 신발 등)의 브랜드와 제품명을 구글 검색을 통해 구체적으로 알려줘. 
                    현재 판매 중인 쇼핑몰 링크와 대략적인 가격 정보가 있다면 함께 리스트 형식으로 정리해줘.
                    """
                    
                    response = model.generate_content([prompt, img])
                    
                    # 결과 출력
                    st.markdown("### 🔍 분석 결과")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")