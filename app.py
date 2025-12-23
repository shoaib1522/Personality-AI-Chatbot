import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from src.personalities import PERSONALITIES, get_system_prompt

# Load environment variables
load_dotenv()

# Initialize Groq client
@st.cache_resource
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("❌ GROQ_API_KEY not found in .env file")
        st.stop()
    return Groq(api_key=api_key)

# Initialize session state
def initialize_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_personality" not in st.session_state:
        st.session_state.selected_personality = "Math Teacher"
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "llama-3.1-8b-instant"

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

        # Model selector
        st.subheader("🧠 AI Model Selection")
        model_options = {
            "LLaMA 3.1 8B (Fast)": "llama-3.1-8b-instant",
            "LLaMA 3.3 70B (Powerful)": "llama-3.3-70b-versatile",
            "Qwen 3 32B": "qwen/qwen3-32b",
        }

        # Find current model in options
        current_model_label = None
        for label, model_id in model_options.items():
            if model_id == st.session_state.selected_model:
                current_model_label = label
                break

        if current_model_label is None:
            current_model_label = list(model_options.keys())[0]
            st.session_state.selected_model = model_options[current_model_label]

        selected_model_label = st.selectbox(
            "Select AI Model:",
            list(model_options.keys()),
            index=list(model_options.keys()).index(current_model_label)
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
    st.markdown(f"**Current Personality:** {st.session_state.selected_personality} | **Model:** {st.session_state.selected_model}")

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

        # Make API call to Groq
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                system_prompt = get_system_prompt(
                    st.session_state.selected_personality,
                    PERSONALITIES
                )

                # Build conversation history for context
                conversation_history = []

                # Add previous messages (keep last 10 for context)
                for msg in st.session_state.messages[:-1]:  # Exclude the latest user message
                    conversation_history.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

                # Add current user message
                conversation_history.append({
                    "role": "user",
                    "content": prompt
                })

                # Prepare messages for API with system prompt
                api_messages = [{"role": "system", "content": system_prompt}] + conversation_history

                # Stream response from Groq
                with st.spinner("🤔 Thinking..."):
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
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()
