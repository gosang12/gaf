import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(
    page_title="AI 그림 생성기 🎨",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# 🔹 사용자 정의 스타일
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
    텍스트로 원하는 그림을 입력하면 AI가 멋진 이미지를 생성해요!  
    OpenAI DALL·E 3 API를 이용한 이미지 생성기입니다.
    """
)

# 🔹 예시 프롬프트 버튼 + 상태 관리
default_prompt = "웃으며 인사하는 귀여운 강아지 캐릭터, 만화 스타일"
if st.button("💡 예시 프롬프트 사용하기"):
    st.session_state["prompt"] = default_prompt

# 🔹 입력창
prompt = st.text_input(
    "🔍 어떤 그림을 원하시나요?",
    value=st.session_state.get("prompt", ""),
    placeholder="예) 고양이가 우주선 타고 날아가는 모습"
)

# 🔹 이미지 크기 선택
size_label = st.selectbox(
    "이미지 크기 선택",
    options=["1024x1024", "1024x1792", "1792x1024"],
    index=0,
    help="크기가 클수록 더 선명하지만 시간이 더 걸릴 수 있어요.",
)

# 🔹 그림 생성 버튼
generate_button = st.button("🎨 그림 생성하기")

# 🔹 이미지 생성 처리
if generate_button:
    if not prompt.strip():
        st.warning("먼저 그림에 대한 설명을 입력해주세요!")
    elif len(prompt.strip()) < 5:
        st.warning("좀 더 자세한 설명을 입력해주세요! 예: '웃으며 인사하는 귀여운 강아지 캐릭터'")
    else:
        with st.spinner("AI가 그림을 그리고 있어요..."):
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size=size_label,
                    quality="standard",
                    n=1,
                )

                image_url = response.data[0].url

                st.image(image_url, caption=f"‘{prompt}’의 AI 그림", use_column_width=True)
                st.markdown(f"[🔗 이미지 직접 보기]({image_url})")

            except Exception as e:
                try:
                    err = e.response.json()["error"]
                    msg = err.get("message") or "에러 메시지가 없습니다."
                except:
                    msg = str(e)
                st.error(f"이미지 생성 중 오류가 발생했습니다:\n\n{msg}")

st.markdown("</div>", unsafe_allow_html=True)

# 🔹 하단 푸터
st.markdown(
    """
    <div class="footer">
        Powered by OpenAI DALL·E API & Streamlit  
        <br>Made with ❤️ by ChatGPT
    </div>
    """,
    unsafe_allow_html=True,
)
