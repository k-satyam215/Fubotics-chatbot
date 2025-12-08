import streamlit as st
import sqlite3
import pandas as pd
from groq import Groq
from datetime import datetime
from dotenv import load_dotenv
import os

st.set_page_config(
    page_title="Fubotics AI Chat",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🔥 Premium Glassmorphism + Neon CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);}
    .stApp {background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);}
    
    /* Glassmorphism Chat Bubbles */
    .chat-user {background: rgba(59, 130, 246, 0.2) !important; 
                backdrop-filter: blur(20px) !important; border: 1px solid rgba(59, 130, 246, 0.3) !important;
                border-radius: 20px !important; box-shadow: 0 8px 32px rgba(59, 130, 246, 0.1) !important;}
    
    .chat-assistant {background: rgba(16, 185, 129, 0.2) !important; 
                     backdrop-filter: blur(20px) !important; border: 1px solid rgba(16, 185, 129, 0.3) !important;
                     border-radius: 20px !important; box-shadow: 0 8px 32px rgba(16, 185, 129, 0.1) !important;}
    
    /* Neon Header */
    .neon-header {font-family: 'Inter', sans-serif; font-size: 3rem; font-weight: 800;
                  background: linear-gradient(45deg, #00f5ff, #ff00ff, #00ff88); 
                  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                  background-clip: text; animation: neonGlow 2s ease-in-out infinite alternate;}
    
    @keyframes neonGlow {from {text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #00f5ff;}
                         to {text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #ff00ff;}}
    
    /* Glass Input */
    .glass-input {background: rgba(255,255,255,0.1) !important; backdrop-filter: blur(20px) !important;
                  border: 1px solid rgba(255,255,255,0.2) !important; border-radius: 25px !important;
                  color: white !important; box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;}

    /* Sidebar Glass */
    .sidebar .stMetric {background: rgba(255,255,255,0.05) !important; backdrop-filter: blur(20px) !important;
                        border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 16px !important;}

    /* 🔵 Assistant ke text ke andar blue highlight box */
    .assistant-highlight {
        background: #1d4ed8;
        color: #ffffff;
        padding: 14px 18px;
        border-radius: 10px;
        font-weight: 500;
        line-height: 1.5;
        border: 1px solid #2563eb;
    }
    </style>
""", unsafe_allow_html=True)

# Load .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("GROQ_API_KEY missing!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# Database functions
@st.cache_resource
def init_db():
    conn = sqlite3.connect('chat_history.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS messages 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

init_db()

def load_history():
    conn = sqlite3.connect('chat_history.db')
    df = pd.read_sql_query("SELECT role, content FROM messages ORDER BY id", conn)
    conn.close()
    return df.to_dict('records') if not df.empty else []

def save_message(role, content):
    conn = sqlite3.connect('chat_history.db')
    conn.execute("INSERT INTO messages (role, content, timestamp) VALUES (?, ?, ?)",
                 (role, content, datetime.now().isoformat()))
    conn.commit()
    conn.close()

# clear history function
def clear_history():
    conn = sqlite3.connect('chat_history.db')
    conn.execute("DELETE FROM messages")
    conn.commit()
    conn.close()
    st.session_state.messages = []

# Header
st.markdown('<h1 class="neon-header">🔍 Fubotics AI Chat</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #a1a1aa; font-size: 1.2rem; text-align: center;">Premium AI Assistant with Persistent Memory</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Live Stats")
    conn = sqlite3.connect('chat_history.db')
    count = conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    st.metric("💬 Total Messages", count)
    st.success("✅ SQLite Persistence")

    # ✅ Clear history button
    if st.button("🗑 Clear Chat History"):
        clear_history()
        st.success("History cleared! Enter you new message.")

# Chat Area
col1, col2 = st.columns([1, 3.5])
with col1:
    st.markdown("### 🚀 Premium Features")
    st.markdown("- ✨ Glassmorphism UI")
    st.markdown("- 🌌 Neon Animations")
    st.markdown("- ⚡ Groq Llama3")
    st.markdown("- 💾 Auto-save History")

with col2:
    if "messages" not in st.session_state:
        st.session_state.messages = load_history()

    chat_container = st.container(height=600)
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(
                msg["role"],
                avatar="👤" if msg["role"] == "user" else "🤖"
            ):
                if msg["role"] == "assistant":
                    st.markdown(
                        f"""
<div class="assistant-highlight">
    {msg['content']}
</div>
""",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
<div style="
    max-width: 900px;
    line-height: 1.5;
    font-size: 0.95rem;
">
    {msg['content']}
</div>
""",
                        unsafe_allow_html=True,
                    )

# Input
st.markdown('<div class="glass-input">', unsafe_allow_html=True)
prompt = st.chat_input("🔍 Ask anything...", key="premium_input")
st.markdown('</div>', unsafe_allow_html=True)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message("user", prompt)
    with st.chat_message("user", avatar="👤"):
        st.markdown(
            f"""
<div style="
    max-width: 900px;
    line-height: 1.5;
    font-size: 0.95rem;
">
    {prompt}
</div>
""",
            unsafe_allow_html=True,
        )

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🧠 Groq AI Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": m["role"], "content": m["content"]}
                              for m in st.session_state.messages[-10:]],
                    temperature=0.7,
                    max_tokens=1000
                ).choices[0].message.content

                st.markdown(
                    f"""
<div class="assistant-highlight">
    {response}
</div>
""",
                    unsafe_allow_html=True,
                )
                save_message("assistant", response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

            except Exception as e:
                st.error(f"❌ {str(e)[:100]}")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 20px; background: rgba(255,255,255,0.05); 
                backdrop-filter: blur(20px); border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);'>
        <p style='color: #a1a1aa; font-size: 16px; margin: 0;'>✨ Fubotics AI Chatbot | Satyam Kumar</p>
    </div>
""", unsafe_allow_html=True)
