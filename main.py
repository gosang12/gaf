import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import base64

# 제목 및 스타일
st.set_page_config(page_title="🎨 AI 그림 생성기", layout="centered")
st.markdown(
    """
    <style>
    .main {
        background-color: #f4f4f4;
    }
    .title {
        font-size: 40px;
        text-align: center;
        color: #4A4A4A;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 20px;
        text-align: center;
        color: #777;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True
)

# 타이틀
st.markdown('<div class="title">🖌️ AI 그림 생성기</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">텍스트를 입력하면 AI가 그림을 그려드려요!</div>', unsafe_allow_html=True)

# 사용자 입력
prompt = st.text_input("✏️ 그리고 싶은 내용을 입력하세요:", placeholder="예: 고양이가 우주를 여행하는 모습")

# 버튼
if st.button("그림 생성하기 🎨") and prompt:
    with st.spinner("AI가 열심히 그림을 그리고 있어요..."):
        # 예시: DALL·E API로 이미지 생성 (아래는 임의 URL 사용)
        image_url = "https://source.unsplash.com/600x400/?art,painting"  # 테스트용 이미지

        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        st.image(image, caption="🧠 AI가 그린 그림", use_column_width=True)

        # 다운로드 버튼
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        b64 = base64.b64encode(buffered.getvalue()).decode()
        href = f'<a href="data:file/png;base64,{b64}" download="ai_art.png">📥 그림 다운로드</a>'
        st.markdown(href, unsafe_allow_html=True)
else:
    st.info("먼저 그리고 싶은 내용을 입력해주세요 😊")
