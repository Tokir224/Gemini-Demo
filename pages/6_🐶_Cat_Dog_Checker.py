import requests
import streamlit as st
import keras
import tensorflow as tf

from PIL import Image
from io import BytesIO

load_model = keras.models.load_model("dog_cat.h5")

image_size = (180, 180)


def predict(image):
    image = image.resize(image_size)
    img_array = keras.utils.img_to_array(image)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis

    predictions = load_model.predict(img_array)
    score = float(predictions[0])

    # Create a list of tuples with labels and percentages
    results = [("Cat", 100 * (1 - score)), ("Dog", 100 * score)]

    # Sort the list in descending order based on percentages
    results.sort(key=lambda x: x[1], reverse=True)

    # Create a dictionary from the sorted list
    result_dict = {label: f"{percentage:.2f}%" for label, percentage in results}

    for label, percentage in result_dict.items():
        return f"**{label}:** {percentage}"


def validate_image_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            return image
        else:
            return None
    except Exception as e:
        return None


def main():
    st.title("Dog VS Cat Classifier")

    image_url = st.text_input("Enter Image URL:")
    clicked = st.button("Predict")
    uploaded_file = None

    # Validate the image URL
    if image_url:
        uploaded_file = validate_image_url(image_url)
        if uploaded_file is not None:
            # Display the image from the URL
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        else:
            st.warning("Invalid image URL. Please enter a valid URL.")

    if clicked and uploaded_file:
        result = predict(uploaded_file)
        st.success(result)


if __name__ == "__main__":
    main()