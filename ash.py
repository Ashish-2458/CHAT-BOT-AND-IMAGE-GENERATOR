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
    if input_text and image:
        # Convert the image to bytes
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes = image_bytes.getvalue()

        # Combine input text and image
        response = model.generate_content(input_text)
    elif input_text:
        response = model.generate_content(input_text)
    elif image:
        # Convert image to bytes
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes = image_bytes.getvalue()
        
        response = model.generate_content(image_bytes)
    else:
        return "No input provided."
    
    return response.text

# Enhanced Streamlit UI
st.set_page_config(page_title="Gemini Creative Studio", layout="wide", page_icon="🎨")

# Custom CSS for UI styling
st.markdown("""
    <style>
        body {
            background-color: #f0f2f6;
            color: #333;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stTextInput, .stFileUploader {
            background-color: #e8f0fe;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #ccc;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for user navigation
with st.sidebar:
    st.title("Gemini Creative Studio 🎨")
    st.write("Generate creative content based on text and image inputs.")
    st.markdown("**Navigation:**")
    st.write("- Upload an image and/or type a prompt.")
    st.write("- Get a creative response based on your inputs!")
    st.markdown("---")

# Main content
st.title("🌟 Welcome to Gemini Creative Studio 🌟")
st.subheader("Let's create something amazing!")

# Input section
st.write("### Step 1: Provide an input")
input_text = st.text_input("Enter a prompt or description for creative content:", placeholder="Write a poem, describe a sunset, etc.")

uploaded_file = st.file_uploader("Upload an image to inspire the response:", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Response section
if st.button("Generate Response"):
    if input_text or image:
        st.write("### Response from Gemini:")
        with st.spinner("Generating..."):
            try:
                response = get_gemini_response(input_text=input_text, image=image)
                st.success("Here is your creative output:")
                st.write(response)
            except Exception as e:
                st.error(f"Error generating content: {e}")
    else:
        st.warning("Please provide text or upload an image to proceed.")

# Feedback Section
st.markdown("### How was the result?")
feedback = st.radio("Rate the response", ("Good 😊", "Bad 😔"))

if feedback == "Good 😊":
    st.balloons()
    st.success("Thank you for the positive feedback! 🎉")
elif feedback == "Bad 😔":
    st.error("Sorry to hear that. We'll keep improving! 🙌")

# Footer
st.markdown("---")
st.write("💡 Tip: You can combine text and image to generate unique responses!")
st.write("Made with ❤️ by [Your Name]")

