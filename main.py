try:
    import streamlit as st
    import openai
    import requests
except ImportError:
    import os
    os.system("pip install streamlit openai requests")
    import streamlit as st
    import openai
    import requests

# ▶ OpenAI API 키 (여기에 본인의 키를 붙여넣으세요)
openai.api_key = "sk-여기-당신의-API키를-붙여넣으세요"

# ▶ Streamlit 페이지 설정
st.set_page_config(page_title="AI 그림 생성기", page_icon="🎨")
st.title("🎨 AI 그림 생성기")
st.write("텍스트로 설명하면 AI가 그림을 그려드려요!")

# ▶ 사용자 입력
prompt = st.text_input("무엇을 그릴까요? 예: '우주에서 기타 치는 고양이'")

# ▶ 버튼 누르면 그림 생성
if st.button("그림 그리기"):
    if not prompt:
        st.warning("먼저 그림 설명을 입력해주세요!")
    else:
        with st.spinner("그림 그리는 중... 잠시만 기다려주세요!"):
            try:
                response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size="512x512"
                )
                image_url = response["data"][0]["url"]
                st.image(image_url, caption="🖼️ 생성된 그림", use_column_width=True)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
