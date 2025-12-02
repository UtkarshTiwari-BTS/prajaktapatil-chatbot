import streamlit as st
from main import PDFChatbot
 
# ---------------------------------------------------------
# Styled Chat Message Component
# ---------------------------------------------------------
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
 
 
# ---------------------------------------------------------
# Main UI Function
# ---------------------------------------------------------
def render_ui():
 
    st.set_page_config(page_title="Chatbot", layout="wide")
 
    # Header
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
 
    # ---------------------------------------------------------
    # USER INPUTS (SAFE) - NOW PROPERLY INSIDE render_ui()
    # ---------------------------------------------------------
    st.sidebar.header("🔐 Azure OpenAI Settings")
 
    AZURE_OPENAI_ENDPOINT = st.sidebar.text_input(
        "Azure OpenAI Endpoint",
        placeholder="https://your-endpoint.openai.azure.com/"
    )
 
    AZURE_OPENAI_API_KEY = st.sidebar.text_input(
        "Azure OpenAI API Key",
        type="password",
        placeholder="Enter your Azure API Key"
    )
 
    AZURE_OPENAI_API_VERSION = st.sidebar.text_input(
        "Azure OpenAI API Version",
        value="2024-02-15-preview"      # recommended stable version
    )
 
    AZURE_OPENAI_DEPLOYMENT = st.sidebar.text_input(
        "Azure Deployment Name",
        value="gpt-4.1-mini"
    )
 
    # Validate credentials
    if not (AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY):
        st.warning("⚠️ Please enter Azure Endpoint and API Key in the sidebar.")
        return
 
    # ---------------------------------------------------------
    # Load chatbot (only once)
    # ---------------------------------------------------------
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = PDFChatbot("INTRODUCTION TO LOAN AGAINST PROPERTY.pdf")
 
    # Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []
 
    # Display previous messages
    for msg in st.session_state.messages:
        message_box(msg["content"], sender=msg["role"])
 
    # ---------------------------------------------------------
    # User Input Section
    # ---------------------------------------------------------
    user_input = st.chat_input("Ask something from the PDF…")
 
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        message_box(user_input, sender="user")
 
        # Get chatbot response
        answer = st.session_state.chatbot.ask(
            user_input,
            AZURE_OPENAI_API_KEY,
            AZURE_OPENAI_ENDPOINT,
            AZURE_OPENAI_API_VERSION,
            AZURE_OPENAI_DEPLOYMENT
        )
 
        st.session_state.messages.append({"role": "assistant", "content": answer})
        message_box(answer, sender="assistant")
