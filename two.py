import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import io

# Configure the Gemini API (use the new gemini-1.5-flash model)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to generate response from Gemini model
def get_gemini_response(input_text=None, image=None):
    try:
        if image:
            # Convert the image to a format that the model can understand
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")  # Save the image in PNG format
            image_bytes.seek(0)  # Move the cursor to the start of the BytesIO object

            if input_text:
                # If input text is provided, use it with the image
                response = model.generate_content(input_text=input_text, image=image_bytes)
            else:
                # If no input text is provided, generate a description of the image
                response = model.generate_content(image=image_bytes)  # Correcting the method call
        elif input_text:
            response = model.generate_content(input_text=input_text)  # Using input_text directly
        else:
            return "Please provide an input or upload an image."
        
        return response.text  # Assuming the API returns a text response
    except Exception as e:
        return f"Error generating content: {str(e)}"

# Streamlit app layout
st.set_page_config(page_title="Gemini Creative Studio", layout="wide", page_icon="🎨")

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #f0f2f6;
            color: #333;
        }
        .section {
            border-radius: 8px;
            padding: 20px;
            background-color: #ffffff;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        h2 {
            color: #4CAF50;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stTextInput, .stFileUploader {
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 10px;
            background-color: #e8f0fe;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🌟 Gemini Creative Studio 🌟")
st.write("Generate creative content with text or images!")

# Section for text generation
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.header("Text Generation")
input_text = st.text_input("Enter your prompt for creative content:", placeholder="Write a poem, story, etc.")
if st.button("Generate Text"):
    if input_text:
        st.write("### Generated Output:")
        with st.spinner("Generating..."):
            response = get_gemini_response(input_text=input_text)
            st.success(response)
    else:
        st.warning("Please provide a prompt to generate content.")
st.markdown("</div>", unsafe_allow_html=True)

# Section for image upload and description
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.header("Image Input")
uploaded_file = st.file_uploader("Upload an image to get a description:", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

if st.button("Describe Image"):
    if image:
        st.write("### Image Description:")
        with st.spinner("Describing the image..."):
            response = get_gemini_response(image=image)
            st.success(response)
    else:
        st.warning("Please upload an image to get a description.")
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.write("💡 Tip: You can use both text and images to generate unique responses!")
st.write("Created with ❤️ by [Ashish]")
