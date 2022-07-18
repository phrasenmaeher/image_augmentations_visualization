import streamlit as st
from matplotlib import pyplot as plt
import albumentations as A

from sidebar_utils import handle_uploaded_image_file

st.set_page_config(page_title="Gaussian Blur Demo", page_icon="📈")

st.markdown("# Gaussian Noise Demo")
st.sidebar.header("Image selection")
st.write(
    """This demo shows the effects of `GaussianNoise` transformation and its parameters.
    Enjoy!"""
)

st.sidebar.markdown("(Optional) Upload an image file here:")
file_uploader = st.sidebar.file_uploader(label="", type=[".png", ".jpg", ".jpeg"])
st.sidebar.markdown("Or select a sample file here:")
selected_provided_file = st.sidebar.selectbox(
    label="", options=["Flower", "Dog"]
)
st.sidebar.markdown("---")
st.sidebar.header("Parameters")
var_limit_lower = st.sidebar.slider('Variance (lower bound)?', 0.0, 100.0, value=0.0)
var_limit_upper = st.sidebar.slider('Variance (upper bound)?', 0.0, 100.0, value=50.0)
mean = st.sidebar.slider('Mean?', 0.0, 100.0, value=30.0)
per_channel = st.sidebar.checkbox(label="Apply per channel?", value=False)


@st.cache
def get_transformation(var_limit_lower: float, var_limit_upper: float, mean: float, per_channel: bool):
    return A.GaussNoise(var_limit=(var_limit_lower, var_limit_upper), mean=mean, per_channel=per_channel,
                        always_apply=True)


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


def run():
    global var_limit_lower, var_limit_upper, mean, per_channel
    additional_information = None
    if file_uploader is not None:
        img, additional_information = handle_uploaded_image_file(file_uploader)
    else:
        if selected_provided_file == "Dog":
            additional_information = 'Image by <a href="https://pixabay.com/users/dm-jones-9527713/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3582038">Marsha Jones</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3582038">Pixabay</a>'
            img = plt.imread("samples/dog.jpg")
        elif selected_provided_file == "Flower":
            img = plt.imread("samples/flower.jpg")
            additional_information = 'Image by <a href="https://pixabay.com/users/engin_akyurt-3656355/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3616249">Engin Akyurt</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3616249">Pixabay</a>'
    plot_original_image(img, additional_information)
    transformation = get_transformation(var_limit_lower, var_limit_upper, mean, per_channel)
    transformed_img = transformation(image=img)["image"]
    plot_modified_image(transformed_img)


if st.sidebar.button("Apply"):
    run()
