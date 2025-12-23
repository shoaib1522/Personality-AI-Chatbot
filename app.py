import streamlit as st
import os
from dotenv import load_dotenv
from src.personalities import PERSONALITIES, get_system_prompt

# Load environment variables
load_dotenv()

# Initialize Groq client - with fallback to demo mode
@st.cache_resource
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")

    # For Streamlit Cloud, check st.secrets
    if not api_key:
        try:
            api_key = st.secrets.get("GROQ_API_KEY")
        except:
            pass

    if not api_key or api_key == "your_groq_api_key_here":
        return None

    try:
        from groq import Groq
        return Groq(api_key=api_key)
    except Exception as e:
        st.warning(f"⚠️ Could not initialize Groq: {str(e)}")
        return None

# Initialize session state
def initialize_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_personality" not in st.session_state:
        st.session_state.selected_personality = "Math Teacher"
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "llama-3.1-8b-instant"
    if "api_available" not in st.session_state:
        st.session_state.api_available = False

# Streamlit page configuration
st.set_page_config(
    page_title="AI Personality Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stChatMessage {
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Main app
def main():
    initialize_session()
    client = get_groq_client()

    # Check if API is available
    if client:
        st.session_state.api_available = True
    else:
        st.session_state.api_available = False

    # Sidebar configuration
    with st.sidebar:
        st.title("⚙️ Configuration")

        # Personality selector
        st.subheader("🎭 Select Personality")
        personality_options = list(PERSONALITIES.keys())
        selected_personality = st.radio(
            "Choose a chatbot personality:",
            personality_options,
            index=personality_options.index(st.session_state.selected_personality)
        )
        st.session_state.selected_personality = selected_personality

        # Show personality description
        personality_info = PERSONALITIES[selected_personality]
        st.info(f"**{selected_personality}**\n\n{personality_info['description']}")

        st.divider()

        # API Status
        st.subheader("🔑 API Status")
        if st.session_state.api_available:
            st.success("✅ Groq API Connected")
        else:
            st.warning("⚠️ API Not Available - Demo Mode Active")
            st.caption("Add GROQ_API_KEY to Streamlit Secrets to enable full features")

        # Model selector (only if API available)
        if st.session_state.api_available:
            st.subheader("🧠 AI Model Selection")
            model_options = {
                "LLaMA 3.1 8B (Fast)": "llama-3.1-8b-instant",
                "LLaMA 3.3 70B (Powerful)": "llama-3.3-70b-versatile",
                "Qwen 3 32B": "qwen/qwen3-32b",
            }
            selected_model_label = st.selectbox(
                "Select AI Model:",
                list(model_options.keys()),
                index=0
            )
            st.session_state.selected_model = model_options[selected_model_label]

        st.divider()

        # Clear chat history button
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.divider()

        # Info section
        st.subheader("ℹ️ About")
        st.markdown("""
        This chatbot uses **Groq AI** with personality-based responses.

        Each personality has strict boundaries and will only answer questions
        within its domain of expertise.
        """)

    # Main chat interface
    st.title("🤖 AI Personality Chatbot")

    if st.session_state.api_available:
        st.markdown(f"**Current Personality:** {st.session_state.selected_personality} | **Model:** {st.session_state.selected_model}")
    else:
        st.markdown(f"**Current Personality:** {st.session_state.selected_personality} | **Mode:** Demo (No API)")
        st.info("💡 **Demo Mode:** Add your Groq API key to Streamlit Secrets for full functionality. Go to 'Manage app' → Settings → Secrets")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message..."):
        # Add user message to session
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            if st.session_state.api_available and client:
                try:
                    with st.spinner("🤔 Thinking..."):
                        system_prompt = get_system_prompt(
                            st.session_state.selected_personality,
                            PERSONALITIES
                        )

                        # Prepare messages for API
                        api_messages = [
                            {"role": "system", "content": system_prompt}
                        ]

                        # Add conversation history
                        for msg in st.session_state.messages[:-1]:
                            api_messages.append({
                                "role": msg["role"],
                                "content": msg["content"]
                            })

                        # Stream response from Groq
                        full_response = ""
                        stream = client.chat.completions.create(
                            model=st.session_state.selected_model,
                            messages=api_messages,
                            temperature=0.7,
                            max_tokens=1024,
                            stream=True,
                        )

                        for chunk in stream:
                            if chunk.choices[0].delta.content:
                                full_response += chunk.choices[0].delta.content
                                message_placeholder.markdown(full_response + "▌")

                        message_placeholder.markdown(full_response)

                    # Add assistant response to session
                    st.session_state.messages.append({"role": "assistant", "content": full_response})

                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    message_placeholder.markdown(error_msg)

            else:
                # Demo mode response
                demo_response = f"""I'm a {st.session_state.selected_personality} in demo mode.

Since the Groq API is not configured, I can't provide real AI responses. However, here's what would happen:

1. Your question would be sent to Groq
2. The {st.session_state.selected_personality} system prompt would be applied
3. You'd get a real AI response based on the personality

**To enable real responses:**
1. Go to your Streamlit Cloud app
2. Click "Manage app" (bottom right)
3. Go to Settings → Secrets
4. Add: `GROQ_API_KEY = "your_api_key_here"`
5. Refresh your app

Your question: "{prompt}" would then be answered by the {st.session_state.selected_personality}! 🚀"""

                message_placeholder.markdown(demo_response)
                st.session_state.messages.append({"role": "assistant", "content": demo_response})

if __name__ == "__main__":
    main()
