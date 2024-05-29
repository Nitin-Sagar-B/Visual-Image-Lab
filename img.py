import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance

st.set_page_config(page_title="Artistic Image Processor", page_icon="🎨", layout="centered")

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

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# Streamlit app
def main():
    st.title("Artistic Image Processor 🎨")
    st.markdown("Upload an image and apply various artistic effects to it!")

    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Convert the file to an opencv image.
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        
        st.write("")
        st.write("Choose an option from the sidebar to process the image:")

        # Sidebar options
        option = st.sidebar.selectbox(
            'Select an option:',
            ('Convert to Greyscale', 'Enhance Image Quality', 'Adjust Brightness', 'Improve Resolution')
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
        
        # Download button for processed image
        st.write("")
        st.write("Download the processed image:")
        processed_pil_image = Image.fromarray(processed_image) if option == 'Convert to Greyscale' else processed_image
        st.download_button(label="Download Image", data=processed_pil_image.tobytes(), file_name="processed_image.png", mime="image/png")

if __name__ == '__main__':
    main()