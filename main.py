import streamlit as st
import openai
import base64
import os

# 🔐 OpenAI API Key (Streamlit Secrets에서 설정)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 🌐 페이지 설정
st.set_page_config(
    page_title="🎨 AI 그림 생성기",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# 💄 CSS 스타일
st.markdown("""
<style>
html, body {
    background-color: #f5f7fa;
}
.main {
    background: white;
    padding: 2rem 3rem;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', sans-serif;
}
.stButton>button {
    background: linear-gradient(to right, #4facfe, #00f2fe);
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    transition: 0.3s;
}
.stButton>button:hover {
    background: linear-gradient(to right, #43e97b, #38f9d7);
    color: white;
}
.footer {
    margin-top: 3rem;
    font-size: 0.8rem;
    color: #555;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main">', unsafe_allow_html=True)

# 🖌 타이틀
st.title("🎨 AI 그림 생성기")
st.write("원하는 그림을 설명하면 AI가 이미지를 생성해줘요! 🧠🖼️")

# 🔍 입력
prompt = st.text_input("✨ 어떤 그림을 원하시나요?", placeholder="예: 우주를 나는 고양이")

size = st.selectbox(
    "이미지 크기 선택",
    options=["256x256", "512x512", "1024x1024"],
    index=1,
)

if st.button("🧠 그림 생성하기"):
    if not prompt.strip():
        st.warning("먼저 그림 설명을 입력해주세요!")
    else:
        with st.spinner("🖌 AI가 그림을 그리고 있어요..."):
            try:
                response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size=size,
                    response_format="b64_json"
                )
                img_data = response['data'][0]['b64_json']
                img_bytes = base64.b64decode(img_data)
                st.image(img_bytes, caption=f"🖼️ '{prompt}'", use_column_width=True)

                st.download_button(
                    label="📥 이미지 다운로드",
                    data=img_bytes,
                    file_name="ai_image.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"이미지 생성 중 오류 발생: {e}")

st.markdown("</div>", unsafe_allow_html=True)

# 📎 푸터
st.markdown("""
<div class="footer">
    Made with ❤️ using OpenAI DALL·E & Streamlit  
</div>
""", unsafe_allow_html=True)
