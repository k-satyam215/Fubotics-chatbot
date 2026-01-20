# Fubotics AI Chat 🔍🤖

**Fubotics AI Chat** is a **premium AI chatbot application** built using **Streamlit**, **Groq LLMs**, and **SQLite** that provides a visually rich chat experience with **persistent conversation memory**.

The system combines a **modern glassmorphism UI**, **neon animations**, and **high-performance LLaMA models** to deliver a fast, elegant, and production-style AI assistant.

---

## 🎯 Objective

The goal of this project is to:
- Build a **production-style AI chat application**
- Demonstrate **LLM integration with persistent memory**
- Store and retrieve chat history reliably using a database
- Design a visually premium, modern UI using Streamlit

---

## 🚀 Key Features

### 🤖 AI Chat Powered by Groq
- Uses **Groq-hosted LLaMA 3.1 (8B Instant)**
- Fast inference with high-quality responses
- Context-aware replies using recent chat history

---

### 💾 Persistent Chat Memory
- Chat history stored in **SQLite**
- Messages automatically saved with timestamps
- Conversation restored on app reload
- Option to clear chat history anytime

---

### 🖥️ Premium UI / UX
- Glassmorphism chat bubbles
- Neon animated headers
- Dark futuristic theme
- Custom chat styling for user and assistant messages

---

### 📊 Live Sidebar Analytics
- Displays total number of messages
- Shows persistence status
- One-click chat history reset

---

### ⚡ Performance & Reliability
- Cached database initialization
- Session-based state handling
- Graceful error handling for API failures

---

## 🧠 How It Works

1. User enters a message in the chat input
2. Message is saved to SQLite
3. Recent conversation history is sent to the Groq LLM
4. LLM generates a response
5. Assistant response is displayed and stored
6. On refresh, chat history is reloaded from the database

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Groq API**
- **LLaMA 3.1**
- **SQLite**
- **Pandas**
- **dotenv**




