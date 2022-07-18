import streamlit as st
from matplotlib import pyplot as plt
import albumentations as A

from sidebar_utils import handle_uploaded_image_file

st.set_page_config(page_title="Gaussian Blur Demo", page_icon="📈")

st.markdown("# Gaussian Blur Demo")
st.sidebar.header("Image selection")
st.write(
    """This demo shows the effects of `GaussianBlur` transformation and its parameters.
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
blur_limit = st.sidebar.slider('How much blur?', 0, 100, step=2, value=0)
sigmaX_limit = st.sidebar.slider('Sigma X?', 0.0, 100.0, value=5.0)
sigmaY_limit = st.sidebar.slider('Sigma Y?', 0.0, 100.0, value=4.9)
rotate_limit = st.sidebar.slider('Rotation?', -180, 180, value=0)
beta_limit = st.sidebar.slider('β?', 1.01, 2.0, value=1.5)
noise_limit = st.sidebar.slider('Noise?', 0.0, 2.0, value=1.0)


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


@st.cache
def get_transformation(blur_limit, sigmaX_limit: float, sigmaY_limit: float, rotate_limit: int, beta_limit: float,
                       noise_limit: float):
    if blur_limit % 2 == 0:
        blur_limit += 1
    ks = 0 if blur_limit == -1 else blur_limit
    if sigmaX_limit == sigmaY_limit:
        sigmaX_limit += 0.001
    return A.AdvancedBlur(blur_limit=(ks, ks), sigmaX_limit=(0.001, sigmaX_limit), sigmaY_limit=(0.0001, sigmaY_limit),
                          rotate_limit=rotate_limit, beta_limit=(0.01, beta_limit), noise_limit=noise_limit,
                          always_apply=True)


def run():
    global blur_limit, sigmaX_limit, sigmaY_limit, rotate_limit, beta_limit, noise_limit
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
    if blur_limit % 2 == 0:
        blur_limit += 1
    transformation = get_transformation(blur_limit, sigmaX_limit, sigmaY_limit, rotate_limit, beta_limit, noise_limit)
    transformed_img = transformation(image=img)["image"]
    plot_modified_image(transformed_img)


if st.sidebar.button("Apply"):
    run()
