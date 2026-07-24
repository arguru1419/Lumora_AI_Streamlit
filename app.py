"""
=========================================================
Lumora AI
Enterprise AI Assistant
Streamlit Application
=========================================================
"""

from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

import streamlit as st

import config

from core.orchestrator import AIOrchestrator


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
    max-width:1200px;
}

.chat-title{
    text-align:center;
    margin-bottom:30px;
}

.hero{
    text-align:center;
    margin-top:80px;
}

.hero h1{
    font-size:48px;
    font-weight:700;
}

.hero p{
    color:#888;
    font-size:18px;
}

.chat-card{
    border-radius:14px;
    padding:18px;
    background:#262730;
    margin-bottom:15px;
}

div[data-testid="stSidebar"]{
    background:#111827;
}

</style>
""",
    unsafe_allow_html=True,
)

# =====================================================
# LOAD SERVICES
# =====================================================

@st.cache_resource
def load_orchestrator():
    return AIOrchestrator()


orchestrator = load_orchestrator()

# =====================================================
# SESSION STATE
# =====================================================

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🤖 Lumora AI")

    st.caption("Enterprise AI Assistant")

    st.divider()

    # ------------------------------
    # New Chat
    # ------------------------------

    if st.button(
        "➕ New Chat",
        use_container_width=True,
    ):

        # Save current session
        st.session_state.chat_sessions[
            st.session_state.session_id
        ] = st.session_state.messages.copy()

        # Create new session
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []

        st.rerun()

    # ------------------------------
    # Previous Chats
    # ------------------------------

    if st.session_state.chat_sessions:

        st.subheader("💬 Chats")

        for sid in list(
            st.session_state.chat_sessions.keys()
        )[::-1]:

            title = f"Chat {sid[:6]}"

            if st.button(
                title,
                key=sid,
                use_container_width=True,
            ):

                st.session_state.session_id = sid
                st.session_state.messages = (
                    st.session_state.chat_sessions[sid]
                )

                st.rerun()

    st.divider()

    # ------------------------------
    # Upload Documents
    # ------------------------------

    st.subheader("📄 Upload Documents")

    uploaded_files = st.file_uploader(
        "",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
    )

    if uploaded_files:

        for file in uploaded_files:

            destination = config.UPLOAD_FOLDER / file.name

            # Prevent duplicate indexing
            if file.name not in st.session_state.uploaded_files:

                with open(destination, "wb") as f:
                    f.write(file.getbuffer())

                try:

                    chunks = orchestrator.rag.ingest_document(
                        str(destination)
                    )

                    st.success(
                        f"{file.name} indexed ({chunks} chunks)"
                    )

                    st.session_state.uploaded_files.append(
                        file.name
                    )

                except Exception as e:

                    st.error(str(e))

    if st.session_state.uploaded_files:

        st.markdown("### 📂 Documents")

        for doc in sorted(
            set(st.session_state.uploaded_files)
        ):

            st.write(f"📄 {doc}")

    st.divider()

    # ------------------------------
    # Export Chat
    # ------------------------------

    export = json.dumps(
        st.session_state.messages,
        indent=2,
    )

    st.download_button(
        "⬇ Export Chat",
        export,
        file_name="lumora_chat.json",
        mime="application/json",
        use_container_width=True,
    )

    # ------------------------------
    # Clear Chat
    # ------------------------------

    if st.button(
        "🗑 Clear Current Chat",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.session_state.chat_sessions[
            st.session_state.session_id
        ] = []

        st.rerun()

# =====================================================
# MAIN WINDOW
# =====================================================

st.markdown(
    """
<div class="chat-title">
<h1>🤖 Lumora AI</h1>
<p>Enterprise AI Assistant</p>
</div>
""",
    unsafe_allow_html=True,
)

# =====================================================
# WELCOME SCREEN
# =====================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        """
<div class="hero">

<h1>Welcome 👋</h1>

<p>
Ask questions, upload documents and chat with Lumora AI.
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:

        st.info("📄 Analyze Documents")

        st.info("📝 Summarize PDF")

    with c2:

        st.info("📊 Generate Reports")

        st.info("💡 Ask Anything")


# =====================================================
# CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =====================================================
# CHAT INPUT
# =====================================================

prompt = st.chat_input(
    "Ask Lumora AI..."
)


# =====================================================
# USER MESSAGE
# =====================================================

if prompt:

    # -----------------------------
    # Save User Message
    # -----------------------------

    user_message = {
        "role": "user",
        "content": prompt,
    }

    st.session_state.messages.append(user_message)

    with st.chat_message("user"):

        st.markdown(prompt)

    # -----------------------------
    # Assistant Response
    # -----------------------------

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        final_response = ""

        try:

            with st.spinner("Thinking..."):

                response = orchestrator.chat(
                    st.session_state.session_id,
                    prompt,
                )

            # ----------------------------------
            # Typewriter Animation
            # ----------------------------------

            words = response.split()

            for word in words:

                final_response += word + " "

                response_placeholder.markdown(
                    final_response + "▌"
                )

            response_placeholder.markdown(
                final_response
            )

        except Exception as e:

            final_response = (
                f"Error : {str(e)}"
            )

            response_placeholder.error(
                final_response
            )

    # -----------------------------
    # Save Assistant Message
    # -----------------------------

    assistant_message = {
        "role": "assistant",
        "content": final_response,
    }

    st.session_state.messages.append(
        assistant_message
    )

    # -----------------------------
    # Save Current Session
    # -----------------------------

    st.session_state.chat_sessions[
        st.session_state.session_id
    ] = st.session_state.messages.copy()

    st.rerun()

# =====================================================
# FOOTER
# =====================================================

st.divider()

col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    st.caption("🤖 Lumora AI")

with col2:
    st.caption("Enterprise AI Assistant")

with col3:
    st.caption(f"Model: {config.MODEL_NAME}")