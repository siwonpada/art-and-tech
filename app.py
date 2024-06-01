import streamlit as st
from llm.image_model import make_image
from llm.model import llm_chain

MAX_ATTEMPT = 3

st.set_page_config(
    page_title="chatting with the AI!",
    page_icon="🤖",
    initial_sidebar_state="collapsed"
)

if "emotion" not in st.session_state:
    st.session_state.emotion = "happy"

col1, col2 = st.columns(2)
with col1:
    st.header("Chatting")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "context" not in st.session_state:
        st.session_state.context = ""

    chattings = st.container(height=500)
    for message in st.session_state.messages:
        chattings.chat_message(message["role"]).write(message["content"])

    if prompt := st.chat_input("Say someting"):
        chattings.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        for i in range(MAX_ATTEMPT):
            try:
                print(prompt)
                print(st.session_state.context)
                response = llm_chain.invoke({
                    "user_input": prompt,
                    "context": st.session_state.context
                })
                if response['result']:
                    break
            except:
                print(response)
                print("error occured")
                continue
        print(response)
        chattings.chat_message("assistant").write(response['result'])
        st.session_state.messages.append(
            {"role": "assistant", "content": response['result']})
        context = f"user:{prompt}\nassistant: {response['result']}\n"
        st.session_state.context += context
        st.session_state.emotion = response["emotion"]


with col2:
    st.header("AI")
    url = make_image(st.session_state.emotion)
    st.image(url)
