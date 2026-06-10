"""
app.py — Streamlit chat interface for the AI Study Buddy.
Run with: streamlit run app.py
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from chatbot import get_response, build_starter_message

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="centered",
)

st.markdown("""
<style>
    .mode-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .explain  { background:#dbeafe; color:#1d4ed8; }
    .quiz     { background:#fef9c3; color:#854d0e; }
    .summarise{ background:#dcfce7; color:#166534; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("📚 AI Study Buddy")
st.markdown("Your personal AI tutor — explain concepts, test your knowledge, or summarise your notes.")
st.divider()

# ── Mode selector ─────────────────────────────────────────────────────────────
mode = st.radio(
    "Choose a study mode:",
    ["Explain It", "Quiz Me", "Summarise"],
    horizontal=True,
)

badge_class = {"Explain It": "explain", "Quiz Me": "quiz", "Summarise": "summarise"}[mode]
mode_icons  = {"Explain It": "💡", "Quiz Me": "🧠", "Summarise": "📝"}

st.markdown(
    f'<span class="mode-badge {badge_class}">{mode_icons[mode]} {mode}</span>',
    unsafe_allow_html=True,
)

# ── Session state ─────────────────────────────────────────────────────────────
# Reset history when mode changes
if "current_mode" not in st.session_state or st.session_state.current_mode != mode:
    st.session_state.current_mode = mode
    st.session_state.messages = []          # conversation history for API
    st.session_state.display_messages = [   # messages shown in UI
        {"role": "assistant", "content": build_starter_message(mode)}
    ]

# ── Render chat history ───────────────────────────────────────────────────────
for msg in st.session_state.display_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
placeholder_hints = {
    "Explain It": "e.g. Explain machine learning in simple terms...",
    "Quiz Me":    "e.g. Quiz me on the American Civil War...",
    "Summarise":  "e.g. Paste your notes here or type a topic...",
}

user_input = st.chat_input(placeholder_hints[mode])

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.display_messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get and show AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = get_response(st.session_state.messages, mode)
        st.markdown(reply)

    st.session_state.display_messages.append({"role": "assistant", "content": reply})
    st.session_state.messages.append({"role": "assistant", "content": reply})

# ── Sidebar controls ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.display_messages = [
            {"role": "assistant", "content": build_starter_message(mode)}
        ]
        st.rerun()

    st.divider()
    st.markdown("### 📖 Mode Guide")
    st.markdown("""
**💡 Explain It**
Ask about any concept and get a clear, simple explanation with examples.

**🧠 Quiz Me**
Give a topic and get multiple-choice questions to test yourself.

**📝 Summarise**
Paste notes or describe a topic for a structured summary with key takeaways.
    """)

    st.divider()
    st.caption("Powered by OpenAI GPT-3.5 Turbo")
