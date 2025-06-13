import streamlit as st
import openai
import base64

# API 키를 환경변수 STREAMLIT_OPENAI_API_KEY에서 읽어옴 (Streamlit Cloud에서 설정 가능)
openai.api_key = st.secrets.get("OPENAI_API_KEY") or st.env.get("STREAMLIT_OPENAI_API_KEY")

st.set_page_config(
    page_title="AI 그림 생성기 🎨",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# CSS 꾸미기
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

prompt = st.text_input("🔍 어떤 그림을 원하시나요?", placeholder="예) 아름다운 해변의 노을")

size = st.selectbox(
    "이미지 크기 선택",
    options=["256x256", "512x512", "1024x1024"],
    index=1,
    help="크기가 클수록 더 선명하지만 시간이 조금 더 걸립니다."
)

generate_button = st.button("그림 생성하기 🎨")

if generate_button:
    if not prompt.strip():
        st.warning("먼저 그림에 대한 설명을 입력해주세요!")
    else:
        with st.spinner("AI가 열심히 그림을 그리고 있어요... 잠시만 기다려주세요!"):
            try:
                response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size=size,
                    response_format="b64_json"
                )
                img_data = response['data'][0]['b64_json']
                img_bytes = base64.b64decode(img_data)

                st.image(img_bytes, caption=f"‘{prompt}’ 의 AI 그림", use_column_width=True)

                # 이미지 다운로드 버튼
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
