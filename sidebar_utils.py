import io

import streamlit as st
import PIL.Image
import numpy as np


def plot_original_image(img, additional_information=None):
    st.markdown(
        f"<h4 style='text-align: center; color: black;'>Original</h5>",
        unsafe_allow_html=True,
    )
    st.image(img, use_column_width=True)
    if additional_information:
        st.markdown(additional_information, unsafe_allow_html=True)


def plot_modified_image(img):
    st.markdown(
        f"<h4 style='text-align: center; color: black;'>Augmented image</h5>",
        unsafe_allow_html=True,
    )
    st.image(img, use_column_width=True)


def spacing():
    st.markdown("<br></br>", unsafe_allow_html=True)


def handle_uploaded_image_file(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        img = PIL.Image.open(io.BytesIO(bytes_data))
        return np.array(img), None

    return None, None
