from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image


# Load environment variables
load_dotenv()

# Set up Google Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Streamlit app
st.set_page_config(page_title="MindCare AI Chatbot", layout="centered")

# Function to get responses from Gemini API
def get_gemini_response(question, image=None):
    model = genai.GenerativeModel('gemini-pro' if image else 'gemini-pro')
    if image:
        response = model.generate_content([question, image])
    else:
        response = model.generate_content(question)
    return response.text

# Chat bubble style
def display_message(role, message):
    if role == "User":
        st.markdown(f"""
        <div style='text-align: right; background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin: 10px; max-width: 70%; margin-left: auto;'>
            <b>You:</b> {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='text-align: left; background-color: #F1F0F0; padding: 10px; border-radius: 10px; margin: 10px; max-width: 70%;'>
            <b>Chatbot:</b> {message}
        </div>
        """, unsafe_allow_html=True)

# Chat Interface Initialization
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

# Create a placeholder for chat messages
chat_placeholder = st.empty()

# Function to display the conversation in a scrollable chat format
def display_conversation():
    with chat_placeholder.container():
        st.subheader("MindCare Chatbot")
        for role, text in st.session_state['conversation']:
            display_message(role, f"{text}")

# Display the conversation first
display_conversation()

# Add vertical space to push input to the bottom
st.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)

# User input for text and image (if applicable)
input_text = st.text_input("Type your message", key="input", placeholder="Ask a question...", label_visibility="collapsed")
uploaded_file = st.file_uploader("Upload an image (optional):", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

# Display uploaded image (if applicable)
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Submit button for asking questions
if st.button("Send") and input_text:
    # Get Gemini's response
    response = get_gemini_response(input_text, image)

    # Append user query and bot response to conversation with timestamps
    st.session_state['conversation'].append(("User", input_text))
    st.session_state['conversation'].append(("Bot", response))
    
    # Refresh the conversation display
    display_conversation()

# Keep the focus on input field after sending a message
st.write(f"<script>document.getElementById('input').focus();</script>", unsafe_allow_html=True)
