# app.py
# Main Streamlit application for the Conversational LLM Web App (Deployment Ready & Fixed)

import streamlit as st
import time
from test_inference import get_response

# --- Page Configuration ---
st.set_page_config(
    page_title="LLM Playground",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- Title and Description ---
st.title("🤖 LLM Playground")
st.markdown("""
Welcome to the LLM Playground! Chat with a Large Language Model and see what it can do.
Select a model from the sidebar, type your message, and get a response.
""")

# --- Sidebar for Configuration ---
with st.sidebar:
    st.header("Configuration")
    
    # Hugging Face Token Management for Deployment
    # The app will try to get the token from st.secrets
    try:
        st.session_state['HUGGINGFACEHUB_API_TOKEN'] = st.secrets['HUGGINGFACEHUB_API_TOKEN']
        st.success("Hugging Face API token loaded successfully!")
    except KeyError:
        st.session_state['HUGGINGFACEHUB_API_TOKEN'] = None
        st.error("Hugging Face API token not found! Please add it to your Streamlit secrets.")
        st.info("For local testing, create a .streamlit/secrets.toml file. For deployment, add it in the app's settings.")

    # Model Selection
    st.subheader("Model Selection")
    # The selectbox widget with a key automatically updates st.session_state
    st.selectbox(
        "Choose a model",
        ["mistralai/Mistral-7B-Instruct-v0.2", "mistralai/Mistral-7B-Instruct-v0.1"],
        key="selected_model"
    )
    st.markdown("You can switch models anytime during the chat.")

    # --- Session State Management ---
    st.subheader("Chat Controls")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.success("Chat history cleared!")

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat Messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input ---
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        if not st.session_state.get('HUGGINGFACEHUB_API_TOKEN'):
            st.error("Cannot generate response. Please configure your Hugging Face API token in the sidebar.")
            full_response = "API token not configured."
        else:
            with st.spinner("Thinking..."):
                try:
                    # We now safely access the selected model from session_state
                    full_response = get_response(
                        st.session_state.selected_model,
                        st.session_state.messages,
                        st.session_state['HUGGINGFACEHUB_API_TOKEN']
                    )
                    
                    # Simulate stream of response with milliseconds delay
                    response_text = ""
                    for chunk in full_response.split():
                        response_text += chunk + " "
                        time.sleep(0.05)
                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(response_text + "▌")
                    message_placeholder.markdown(response_text)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    full_response = "Sorry, I couldn't process your request."

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- Export Chat History ---
with st.sidebar:
    st.subheader("Export Conversation")
    chat_history_str = "\n".join(
        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages]
    )
    if chat_history_str:
        st.download_button(
            label="Download Chat History",
            data=chat_history_str,
            file_name="chat_history.txt",
            mime="text/plain",
        )
    else:
        st.info("Chat history is empty.")
