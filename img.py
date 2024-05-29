import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance
from io import BytesIO

# Set the page configuration
st.set_page_config(page_title="Visual Image Lab", page_icon="🎨", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Shadows+Into+Light&display=swap');

    body {
        font-family: 'Poppins', sans-serif;
        color: white;
    }

    h1 {
        font-family: 'Shadows Into Light', cursive;
        color: #3498db;
        text-align: center;
        margin-bottom: 2rem;
    }

    .stButton>button {
        background-color: #3498db;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 8px;
        transition: background-color 0.3s;
    }

    .stButton>button:hover {
        background-color: #2980b9;
    }

    .stFileUploader label {
        color: #3498db;
        font-size: 18px;
        font-weight: bold;
    }

    .css-1aumxhk {
        background-color: #3498db !important;
        color: white !important;
        border: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to convert image to greyscale
def convert_to_greyscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Function to enhance image quality (simple enhancement)
def enhance_image(image):
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(2.0)  # Adjust enhancement level

# Function to adjust brightness
def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

# Function to improve resolution (using simple resizing)
def improve_resolution(image, scale_factor):
    width, height = image.size
    new_size = (int(width * scale_factor), int(height * scale_factor))
    return image.resize(new_size, Image.ANTIALIAS)

# Function to convert image to HD resolution
def convert_to_hd(image):
    return image.resize((1280, 720), Image.ANTIALIAS)

# Streamlit app
def main():
    st.title("Visual Image Lab 🖌️")
    st.markdown("Upload an image and apply various artistic effects to it!")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Convert the file to a PIL image.
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        
        st.write("")
        st.write("Choose an option from the sidebar to process the image:")

        # Sidebar options
        option = st.sidebar.selectbox(
            'Select an option:',
            ('Convert to Greyscale', 'Enhance Image Quality', 'Adjust Brightness', 'Improve Resolution', 'Convert to HD Resolution',
             'All of the Above (Without Greyscale)', 'All of the Above (With Greyscale)')
        )

        if option == 'Convert to Greyscale':
            processed_image = convert_to_greyscale(np.array(image))
            st.image(processed_image, caption='Processed Image - Greyscale', use_column_width=True, channels="GRAY")

        elif option == 'Enhance Image Quality':
            processed_image = enhance_image(image)
            st.image(processed_image, caption='Processed Image - Enhanced Quality', use_column_width=True)

        elif option == 'Adjust Brightness':
            factor = st.sidebar.slider('Brightness Factor', 0.5, 3.0, 1.0)
            processed_image = adjust_brightness(image, factor)
            st.image(processed_image, caption=f'Processed Image - Brightness: {factor}', use_column_width=True)

        elif option == 'Improve Resolution':
            scale_factor = st.sidebar.slider('Scale Factor', 1.0, 4.0, 2.0)
            processed_image = improve_resolution(image, scale_factor)
            st.image(processed_image, caption=f'Processed Image - Resolution Improved by {scale_factor}x', use_column_width=True)

        elif option == 'Convert to HD Resolution':
            processed_image = convert_to_hd(image)
            st.image(processed_image, caption='Processed Image - HD Resolution', use_column_width=True)

        elif option == 'All of the Above (Without Greyscale)':
            factor = st.sidebar.slider('Brightness Factor', 0.5, 3.0, 1.0)
            scale_factor = st.sidebar.slider('Scale Factor', 1.0, 4.0, 2.0)
            image = enhance_image(image)
            image = adjust_brightness(image, factor)
            image = improve_resolution(image, scale_factor)
            processed_image = convert_to_hd(image)
            st.image(processed_image, caption='Processed Image - All Effects Applied (Without Greyscale)', use_column_width=True)

        elif option == 'All of the Above (With Greyscale)':
            factor = st.sidebar.slider('Brightness Factor', 0.5, 3.0, 1.0)
            scale_factor = st.sidebar.slider('Scale Factor', 1.0, 4.0, 2.0)
            image = enhance_image(image)
            image = adjust_brightness(image, factor)
            image = improve_resolution(image, scale_factor)
            image = convert_to_hd(image)
            processed_image = convert_to_greyscale(np.array(image))
            st.image(processed_image, caption='Processed Image - All Effects Applied (With Greyscale)', use_column_width=True, channels="GRAY")
        
        # Prepare processed image for download
        if option == 'Convert to Greyscale' or option == 'All of the Above (With Greyscale)':
            processed_pil_image = Image.fromarray(processed_image)
        else:
            processed_pil_image = processed_image
        buf = BytesIO()
        processed_pil_image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # Download button for processed image
        st.write("")
        st.write("Download the processed image:")
        st.download_button(label="Download Image", data=byte_im, file_name="processed_image.png", mime="image/png")

if __name__ == '__main__':
    main()
