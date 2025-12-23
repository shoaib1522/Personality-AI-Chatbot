# 🤖 AI Personality Chatbot

An interactive chatbot web app built with **Streamlit** and **Groq AI** that features personality-based responses with strict domain boundaries.

## ✨ Features

- **🎭 Personality Selection**: Choose from 5 distinct personalities:
  - **Math Teacher**: Only answers math-related questions
  - **Doctor**: Only answers health and medical queries
  - **Travel Guide**: Only provides travel advice and tips
  - **Chef**: Only answers cooking and recipe questions
  - **Tech Support**: Only answers technical troubleshooting

- **🧠 Model Selection**: Choose from current Groq AI free tier models:
  - LLaMA 3.1 8B (Fast - default)
  - LLaMA 3.3 70B (Powerful)
  - Qwen 3 32B (Balanced)

- **💾 Session Memory**: Maintains conversation context throughout the session

- **🛡️ Personality Enforcement**: Chatbot strictly stays within personality boundaries and politely refuses out-of-scope questions

- **⚡ Real-time Streaming**: Responses stream in real-time for better UX

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Groq API Key (get one at https://console.groq.com)

### Installation

1. **Clone or download this repository**

```bash
cd 1
```

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root and add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

The `.env` file is already created with your API key.

### Running Locally

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
1/
├── app.py                 # Main Streamlit application
├── .env                   # Environment variables (API keys)
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── src/
    ├── __init__.py       # Package initialization
    ├── personalities.py  # Personality definitions and system prompts
    └── utils.py          # Utility functions for boundary enforcement
```

## 🎯 How It Works

### 1. Personality System

Each personality has:
- **System Prompt**: Instructions for the AI on how to behave
- **Keywords**: Domain-specific keywords for boundary detection
- **Refuse Message**: Polite message when question is out of scope

### 2. Personality Enforcement

The system prompt is designed to make the AI naturally stay within its domain:
- The AI reads the system prompt with clear instructions on what it can help with
- If a question is out of scope, the AI politely declines and redirects
- No pre-check filtering - the AI handles personality boundaries intelligently

### 3. Session Management

- Conversation history is stored in Streamlit's session state
- Context is maintained throughout the user's session
- Users can clear history with the "Clear Chat History" button

## 🎨 Customization

### Adding a New Personality

Edit `src/personalities.py` and add a new entry to the `PERSONALITIES` dictionary:

```python
"New Personality": {
    "description": "Brief description",
    "system_prompt": """Your detailed system prompt here""",
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "refuse_message": "Polite refusal message"
}
```

### Changing System Prompts

Modify the `system_prompt` in `src/personalities.py` for any personality to customize behavior.

## 📊 Testing

Test the chatbot with questions for each personality:

- **Math Teacher**: "2+2", "What is calculus?", "Solve x² + 5x + 6 = 0"
- **Doctor**: "What are symptoms of flu?", "I have a headache", "Is diabetes treatable?"
- **Travel Guide**: "Where should I visit in Japan?", "Best hotels in Paris", "How to get around London?"
- **Chef**: "How do I make homemade pasta?", "Chocolate cake recipe", "Cooking tips for beginners"
- **Tech Support**: "My computer is slow", "How do I fix WiFi?", "How to install Python?"

Try asking out-of-scope questions to see how each personality handles them gracefully.

## 🚢 Deployment to Streamlit Cloud

1. **Push to GitHub**

```bash
git init
git add .
git commit -m "Initial commit: AI Personality Chatbot"
git remote add origin https://github.com/yourusername/chatbot-repo.git
git push -u origin main
```

2. **Deploy on Streamlit Cloud**

- Go to https://streamlit.io/cloud
- Click "New app"
- Select your GitHub repository
- Choose the branch and file path (`app.py`)
- Deploy

3. **Set Environment Variables**

In Streamlit Cloud dashboard:
- Go to your app settings
- Add secret: `GROQ_API_KEY` = your_groq_api_key

## 📝 Environment Variables

- `GROQ_API_KEY`: Your Groq API key (required)

## 🔒 Security Notes

- Never commit `.env` file to version control (already in `.gitignore`)
- Use Streamlit Cloud secrets for sensitive information in production
- API key is loaded from environment variables for security

## 🐛 Troubleshooting

### "GROQ_API_KEY not found"
- Ensure `.env` file exists in the project root
- Verify your API key is correctly set

### Model not responding
- Check your internet connection
- Verify your Groq API key is valid
- Try switching to a different model
- Check rate limits on https://console.groq.com

### Error: "model has been decommissioned"
- The model has been deprecated by Groq
- Select a different model from the dropdown
- Available models are: LLaMA 3.1 8B, LLaMA 3.3 70B, Qwen 3 32B

## 🤝 Contributing

Feel free to customize personalities, add new ones, or improve the boundary enforcement logic.

## 📄 License

This project is open source and available for educational use.

## 🔗 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Groq API Documentation](https://console.groq.com/docs)
- [Groq Python SDK](https://github.com/groqcloud/groq-python)
- [Available Groq Models](https://console.groq.com/docs/models)

---

**Built with ❤️ using Streamlit and Groq AI**
