import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Set page config and custom CSS
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(to bottom right, #1a1a1a, #0a0a0a);
    }
    
    /* Title styling */
    .stTitle {
        color: #ffffff !important;
        font-size: 2.5rem !important;
        text-align: center;
        margin-bottom: 2rem !important;
        text-shadow: 0 0 10px rgba(255,255,255,0.2);
    }
    
    /* Chat message styling */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Chat input styling */
    .stChatInput {
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        padding: 0.75rem !important;
        margin-top: 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatInput:focus {
        border-color: rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #2E3192, #1BFFFF) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Text styling */
    .stMarkdown {
        color: #ffffff !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }
    
    /* Custom container for chat area */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create a container for better layout
chat_container = st.container()

with chat_container:
    # Set page title with emoji
    st.title("💬 AI Chat Assistant")
    
    # Initialize chat history in session state if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Send all previous messages plus current prompt to maintain context
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]} 
                    for m in st.session_state.messages
                ],
                stream=True
            )
            
            # Stream the response with a typing indicator
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Add a clear button with custom styling
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
