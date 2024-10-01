import streamlit as st
import os
import google.generativeai as genai
from PIL import Image



def get_response(input_text=None, image=None):
    if input_text and image:
        # If both input_text and image are present, combine them
        response = model.generate_content(input_text)  # Assuming the API handles text + image internally
    elif input_text:
        response = model.generate_content(input_text)
    elif image:
        response = model.generate_content(image)
    else:
        return "No input provided."
    
    return response.text

# Initialize the Streamlit app
st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini Application")

# Text input prompt
input_text = st.text_input("Input Prompt:", key="input")

# Image upload option
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Button to submit input
submit = st.button("Tell me about the image")

# Process the response if the button is clicked
if submit:
    if input_text or image:  # Ensure there is input or an image
        response = get_gemini_response(input_text=input_text, image=image)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.warning("Please provide an input prompt or upload an image.")
