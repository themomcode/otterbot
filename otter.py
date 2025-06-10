import streamlit as st
st.title("Chat box demo.")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    # For a working AI assistant, you should replace the next line with an LLM call
    ai_answer= "My responses are limited, you have to ask the right question"
    st.session_state.messages.append({"role": "assistant", "content": ai_answer})
    st.chat_message("assistant").write(ai_answer)
