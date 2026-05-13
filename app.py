import streamlit as st
import google.generativeai as genai
from PIL import Image
import streamlit_analytics2 as streamlit_analytics

# 1. API 키 설정 (스트림릿 비밀 금고 연동)
API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)

# 2. 미니멀/클린 무드 CSS 주입
st.set_page_config(page_title="Fashion Lens", layout="centered")
st.markdown("""
    <style>
    /* 폰트: 깔끔한 산세리프 폰트 적용 */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #FAFAFA; }
    .main { background-color: #FAFAFA; }
    
    /* 카드 컨테이너: 그림자 제거, 얇은 테두리 */
    .stImage, .stMarkdown {
        background-color: white;
        padding: 24px;
        border-radius: 8px;
        border: 1px solid #EAEAEA;
        margin-bottom: 16px;
    }
    
    /* 시크한 블랙 버튼 */
    div.stButton > button {
        width: 100%;
        background-color: #111111;
        color: #FFFFFF;
        border-radius: 4px;
        border: none;
        padding: 16px;
        font-weight: 500;
        font-size: 16px;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover { background-color: #333333; color: white; border: none; }
    
    /* 파일 업로더 점선 스타일 */
    .stFileUploader { border: 1px dashed #CCCCCC; background-color: transparent; border-radius: 8px; padding: 20px; }
    
    /* 텍스트 스타일링 */
    h1 { color: #111111; font-weight: 700; font-size: 28px; letter-spacing: -0.5px; text-align: center; }
    p { color: #555555; text-align: center; margin-bottom: 30px; font-size: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. 화면 UI 구성 및 분석 트래커 실행
with streamlit_analytics.track():
    st.markdown("<h1>Fashion Lens</h1>", unsafe_allow_html=True)
    st.markdown("<p>궁금한 아이템의 사진을 올려주세요.</p>", unsafe_allow_html=True)

    # 업로드 섹션
    uploaded_file = st.file_uploader("", type=['jpg', 'png', 'jpeg'])

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        # 분석 버튼
        if st.button("제품 정보 확인하기"):
            with st.spinner("정보를 분석하고 있습니다..."):
                try:
                    model = genai.GenerativeModel(
                        model_name='gemini-3.1-flash-lite',
                        tools=[{'google_search_retrieval': {}}] 
                    )
                    
                    prompt = """
                    이 이미지 속 인물이 입은 모든 옷(상의, 하의, 신발 등)의 브랜드와 제품명을 구글 검색을 통해 구체적으로 알려줘. 
                    현재 판매 중인 쇼핑몰 링크와 대략적인 가격 정보가 있다면 함께 리스트 형식으로 정리해줘.
                    """
                    
                    response = model.generate_content([prompt, img])
                    
                    st.markdown("### 🔍 Analysis Result")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
