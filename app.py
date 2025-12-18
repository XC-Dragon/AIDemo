import streamlit as st
import google.generativeai as genai
import os

# 1. 页面配置
st.set_page_config(page_title="我的 AI 助手", page_icon="🤖")
st.title("🤖 我的专属 AI 助手")

# 2. 获取 API Key (从云端环境变量中获取，为了安全)
api_key = st.secrets["GOOGLE_API_KEY"]

if not api_key:
    st.error("请设置 API Key！")
    st.stop()

# 3. 配置 Google Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash') # 使用轻量级模型，速度快

# 4. 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 处理用户输入
if prompt := st.chat_input("请输入你的问题..."):
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用 Google AI 并显示回答
    with st.chat_message("assistant"):
        stream = model.generate_content(prompt, stream=True)
        response = st.write_stream(chunk.text for chunk in stream)
    
    st.session_state.messages.append({"role": "model", "content": response})
