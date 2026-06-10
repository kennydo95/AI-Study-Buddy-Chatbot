# 📚 AI Study Buddy Chatbot

An AI-powered study assistant built with OpenAI GPT and Streamlit. Supports three modes — explain concepts, generate quizzes, and summarise notes — with full multi-turn conversation memory.

## 📁 Project Structure
```
study-buddy-chatbot/
├── src/
│   └── chatbot.py       ← OpenAI API calls + mode prompts + history
├── app.py               ← Streamlit chat UI
├── .env.example         ← API key template
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your API key
```bash
cp .env.example .env
# Open .env and paste your OpenAI API key
# Get one free at: https://platform.openai.com/api-keys
```

### 3. Run the app
```bash
streamlit run app.py
```
Open http://localhost:8501 in your browser.

## 🧠 How It Works

| Component | Detail |
|-----------|--------|
| **Model** | OpenAI GPT-3.5 Turbo (swap to GPT-4o for better answers) |
| **Prompt Engineering** | Each mode has a custom system prompt that shapes the AI's behaviour |
| **Memory** | Full conversation history is sent with every API call |
| **UI** | Streamlit `st.chat_message` for a native chat experience |

## 🎮 Study Modes

| Mode | What it does |
|------|-------------|
| 💡 **Explain It** | Explains any concept with analogies and examples |
| 🧠 **Quiz Me** | Generates multiple-choice questions and tracks your score |
| 📝 **Summarise** | Turns notes or topics into structured summaries with key takeaways |

## 💡 Ideas to Extend This
- Add a **Flashcard Generator** mode that exports to Anki format
- Let users upload a PDF textbook and chat with it (use PyMuPDF + embeddings)
- Add a **voice input** option using `streamlit-webrtc` + Whisper API
- Save chat history to a local JSON file so users can review past sessions
- Deploy for free on **Streamlit Community Cloud**
