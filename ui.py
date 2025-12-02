import streamlit as st
from main import PDFChatbot

# Read credentials from Streamlit sidebar safely (no keys stored in repo)
AZURE_OPENAI_ENDPOINT = st.sidebar.text_input("Azure Endpoint")
AZURE_OPENAI_API_KEY = st.sidebar.text_input("Azure API Key", type="password")
AZURE_OPENAI_API_VERSION = st.sidebar.text_input("API Version", value="2025-01-01-preview")
AZURE_OPENAI_DEPLOYMENT = st.sidebar.text_input("Deployment Name", value="gpt-4.1-mini")



# Styled Chat Message
def message_box(text, sender="assistant"):
    text = text.replace("\n", "<br>")  
    if sender == "assistant":
        st.markdown(
            f"""
            <div style="background-color:#F0F2F6; padding:15px; border-radius:12px; margin:10px 0; max-width:80%; font-size:16px;">
                🤖 <b>Bot:</b><br>{text}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f"""
            <div style="background-color:#DCF8C6;
                        padding:15px;
                        border-radius:12px;
                        margin:10px 0;
                        max-width:80%;
                        margin-left:auto;
                        font-size:16px;">
                🙋‍♂️ <b>You:</b><br>{text}
            </div>
            """,
            unsafe_allow_html=True
        )


def render_ui():

    st.set_page_config(page_title="Chatbot", layout="wide")

    st.markdown(
        """
        <div style="
            background-color:#1E88E5;
            padding:20px;
            border-radius:10px;
            margin-bottom:20px;
            text-align:center;">
            <h3 style="color:white; margin:0;">UGRO Chatbot</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )



    # Load chatbot once
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = PDFChatbot("INTRODUCTION TO LOAN AGAINST PROPERTY.pdf")

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past messages with styled bubbles
    for msg in st.session_state.messages:
        message_box(msg["content"], sender=msg["role"])

    # User input
    user_input = st.chat_input("Ask something from the PDF…")

    if user_input:
        # Save + display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        message_box(user_input, sender="user")

        # Bot answer
        answer = st.session_state.chatbot.ask(
            user_input,
            AZURE_OPENAI_API_KEY,
            AZURE_OPENAI_ENDPOINT,
            AZURE_OPENAI_API_VERSION,
            AZURE_OPENAI_DEPLOYMENT
        )

        st.session_state.messages.append({"role": "assistant", "content": answer})
        message_box(answer, sender="assistant")
