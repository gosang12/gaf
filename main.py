import streamlit as st
from openai import OpenAI
import base64

# OpenAI 클라이언트 초기화 (Secrets에 API 키 저장 필요)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 페이지 설정
st.set_page_config(
    page_title="AI 그림 생성기 🎨",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# 💄 스타일
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #111 0%, #222 100%);
    padding: 2rem 3rem;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: white;
}
.stButton>button {
    background: #f06292;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    padding: 10px 20px;
}
.stButton>button:hover {
    background: #ec407a;
}
.footer {
    margin-top: 3rem;
    font-size: 0.8rem;
    color: #bbb;
    text-align: center;
}
textarea::after {
    content: none !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main">', unsafe_allow_html=True)

# 타이틀
st.title("🖼️ AI 그림 생성기")
st.write("텍스트로 원하는 그림을 입력하면 AI가 멋진 이미지를 만들어줘요!")

# 프롬프트 입력
default_prompt = "웃으며 인사하는 귀여운 강아지 캐릭터, 만화 스타일"
prompt = st.text_input("🔍 어떤 그림을 원하시나요?", placeholder="예) 고양이가 우주선 타고 날아가는 모습")

if st.button("💡 예시 프롬프트 사용하기"):
    prompt = default_prompt
    st.experimental_rerun()

# 사이즈 선택
size_label = st.selectbox(
    "이미지 크기 선택",
    options=["1024x1024", "1024x1792", "1792x1024"],
    index=0,
    help="크기가 클수록 더 선명하지만 시간이 더 걸릴 수 있어요.",
)

# 생성 버튼
generate_button = st.button("🎨 그림 생성하기")

# 생성 로직
if generate_button:
    if not prompt.strip():
        st.warning("먼저 그림에 대한 설명을 입력해주세요!")
    else:
        with st.spinner("AI가 그림을 그리고 있어요..."):
            try:
                response = client.images.generate(
                    model="dall-e-3",
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
                try:
                    error_message = e.response.json()['error'].get('message', '알 수 없는 오류입니다.')
                except:
                    error_message = str(e)
                st.error(f"이미지 생성 중 오류가 발생했습니다:\n\n{error_message}")

# 푸터
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    Powered by OpenAI DALL·E API & Streamlit<br>
    Made with ❤️ by ChatGPT
</div>
""", unsafe_allow_html=True)
