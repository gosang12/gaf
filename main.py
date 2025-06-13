import streamlit as st
from openai import OpenAI
import base64

# OpenAI 클라이언트 초기화 (Secrets에서 API 키 읽기)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(
    page_title="AI 그림 생성기 🎨",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# 스타일 커스터마이징
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem 3rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton>button {
        background: #4a90e2;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 10px 20px;
        transition: background 0.3s ease;
    }
    .stButton>button:hover {
        background: #357ABD;
        color: #e0e0e0;
    }
    .footer {
        margin-top: 3rem;
        font-size: 0.8rem;
        color: #555;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main">', unsafe_allow_html=True)

st.title("🖼️ AI 그림 생성기")
st.write(
    """
    텍스트로 원하는 그림을 입력하면 AI가 멋진 이미지를 생성해줘요!  
    OpenAI DALL·E API를 이용한 간단하고 빠른 이미지 생성기입니다.
    """
)

prompt = st.text_input("🔍 어떤 그림을 원하시나요?", placeholder="예) 고양이가 우주선 타고 날아가는 모습")

size_label = st.selectbox(
    "이미지 크기 선택",
    options=["1024x1024", "1024x1792", "1792x1024"]
    index=1,
    help="크기가 클수록 더 선명하지만 시간이 더 걸릴 수 있어요.",
)

generate_button = st.button("그림 생성하기 🎨")

if generate_button:
    if not prompt.strip():
        st.warning("먼저 그림에 대한 설명을 입력해주세요!")
    else:
        with st.spinner("AI가 그림을 그리고 있어요..."):
            try:
                response = client.images.generate(
                    model="dall-e-3",  # 최신 모델 사용, 필요시 "dall-e-2"
                    prompt=prompt,
                    size=size_label,
                    quality="standard",
                    n=1,
                    response_format="b64_json"
                )

                img_data = response.data[0].b64_json
                img_bytes = base64.b64decode(img_data)

                st.image(img_bytes, caption=f"‘{prompt}’의 AI 그림", use_column_width=True)

                st.download_button(
                    label="이미지 다운로드",
                    data=img_bytes,
                    file_name="ai_generated_image.png",
                    mime="image/png",
                )

            except Exception as e:
                st.error(f"이미지 생성 중 오류가 발생했습니다: {e}")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="footer">
        Powered by OpenAI DALL·E API & Streamlit  
        <br>Made with ❤️ by ChatGPT
    </div>
    """,
    unsafe_allow_html=True,
)
