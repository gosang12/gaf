import streamlit as st
from utils import init_user, load_user, save_user, save_image
import openai
import requests

openai.api_key = "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"  # 여기에 본인의 키 입력

init_user()
user = load_user()

st.title("🎨 AI 그림 생성기")
st.sidebar.markdown("💰 **내 크레딧:** " + str(user["credits"]))

if st.sidebar.button("📺 광고 보기 (크레딧 +1)"):
    user["credits"] += 1
    save_user(user)
    st.sidebar.success("광고 시청 완료! 크레딧 +1 🎉")

prompt = st.text_input("✏️ 그림 프롬프트 입력")

if st.button("그림 생성하기"):
    if user["credits"] <= 0:
        st.error("❌ 크레딧이 부족합니다. 광고를 보거나 충전하세요.")
    elif prompt:
        with st.spinner("AI가 그림을 그리는 중입니다..."):
            response = openai.Image.create(prompt=prompt, n=1, size="512x512")
            img_url = response['data'][0]['url']
            img_path = save_image(img_url, prompt)
            img_data = requests.get(img_url).content
            st.image(img_url, caption=prompt)
            st.download_button("📥 이미지 다운로드", data=img_data, file_name="ai_image.png")
            user["credits"] -= 1
            save_user(user)
    else:
        st.warning("프롬프트를 입력하세요.")

st.markdown("## 🖼 내 그림 히스토리")
for item in reversed(user["history"][-5:]):
    st.image(item["path"], caption=item["prompt"], width=300)
