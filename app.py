import streamlit as st
import openai
import os
import json
import uuid
from dotenv import load_dotenv
from datetime import datetime

# API 키 불러오기
load_dotenv()
openai.api_key = os.getenv("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")

# 크레딧 & 히스토리 관리용 JSON 경로
USER_DATA_FILE = "user_data.json"
IMAGE_HISTORY_FOLDER = "history"
os.makedirs(IMAGE_HISTORY_FOLDER, exist_ok=True)

# 유저 데이터 초기화 함수
def load_user_data():
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w") as f:
            json.dump({"credits": 5, "history": []}, f)
    with open(USER_DATA_FILE, "r") as f:
        return json.load(f)

def save_user_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# 초기 유저 데이터 불러오기
user_data = load_user_data()

# 앱 제목
st.set_page_config(page_title="🎨 AI 그림 그리기", layout="centered")
st.title("🎨 AI 그림 그리기 (DALL·E 3)")

# 현재 크레딧 표시
st.info(f"💰 현재 크레딧: {user_data['credits']}")

# 프롬프트 입력
prompt = st.text_input("무엇을 그리고 싶나요?", placeholder="예: 무지개를 타는 고양이")

# 광고 보기 버튼 (크레딧 +1)
if st.button("📺 광고 시청하고 크레딧 받기"):
    user_data["credits"] += 1
    save_user_data(user_data)
    st.success("크레딧 +1! 🎉")

# 이미지 생성 버튼
if st.button("이미지 생성하기"):
    if user_data["credits"] < 1:
        st.error("크레딧이 부족합니다. 광고를 시청해 충전해주세요.")
    elif not prompt:
        st.warning("프롬프트를 입력해주세요.")
    else:
        with st.spinner("이미지를 생성 중입니다..."):
            try:
                response = openai.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    n=1,
                    size="1024x1024"
                )
                image_url = response.data[0].url
                st.image(image_url, caption=prompt)

                # 이미지 저장
                filename = f"{uuid.uuid4()}.png"
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user_data["history"].append({
                    "prompt": prompt,
                    "url": image_url,
                    "timestamp": timestamp
                })
                user_data["credits"] -= 1
                save_user_data(user_data)

                st.markdown(f"[🖼️ 이미지 다운로드]({image_url})")

            except Exception as e:
                st.error(f"오류 발생: {str(e)}")

# 히스토리 출력
if st.checkbox("📜 이전에 만든 그림 보기"):
    for item in reversed(user_data["history"][-5:]):  # 최근 5개
        st.markdown(f"🕒 {item['timestamp']} - **{item['prompt']}**")
        st.image(item['url'], width=300)
