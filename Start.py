import streamlit as st
from matplotlib import pyplot as plt
import albumentations as A

from sidebar_utils import handle_uploaded_image_file

plt.rcParams["figure.figsize"] = (10, 7)


def create_pipeline(transformations: list):
    pipeline = []
    for index, transformation in enumerate(transformations):
        if transformation:
            pipeline.append(index_to_transformation(index))

    return pipeline


def spacing():
    st.markdown("<br></br>", unsafe_allow_html=True)


def plot_audio_transformations(original_image, pipeline: A.Compose, additional_information: str = None):
    cols = [1, 2, 1]
    col_1, col_2, col_3 = st.columns(cols)
    with col_2:
        st.markdown(
            f"<h4 style='text-align: center; color: black;'>Original</h5>",
            unsafe_allow_html=True,
        )
        st.image(original_image)
        if additional_information:
            st.markdown(additional_information, unsafe_allow_html=True)

    modified_image = original_image

    for col_index, individual_transformation in enumerate(pipeline.transforms):
        transformation_name = (
            str(type(individual_transformation)).split("'")[1].split(".")[-1]
        )
        modified_image = individual_transformation(image=modified_image)["image"]

        col1, col2, col3 = st.columns(cols)

        with col2:
            st.markdown(
                f"<h4 style='text-align: center; color: black;'>{transformation_name} </h5>",
                unsafe_allow_html=True,
            )
            st.image(modified_image)


def index_to_transformation(index: int):
    if index == 0:
        return A.GaussNoise(p=1.0, var_limit=(0.25, 0.5))
    elif index == 1:
        return A.HorizontalFlip(p=1.0)
    elif index == 2:
        return A.VerticalFlip(p=1.0)
    elif index == 3:
        return A.RandomBrightness(p=1.0, limit=(0.5, 1.5))
    elif index == 4:
        return A.AdvancedBlur(p=1.0, blur_limit=3)
    elif index == 5:
        return A.ChannelShuffle(p=1.0)
    elif index == 6:
        return A.ChannelDropout(p=1.0)
    elif index == 7:
        return A.RandomContrast(p=1.0, limit=(0.5, 1.5))


def action(file_uploader, selected_provided_file, transformations):
    if file_uploader is not None:
        img = handle_uploaded_image_file(file_uploader)
    else:
        if selected_provided_file == "Dog":
            additional_information = 'Image by <a href="https://pixabay.com/users/dm-jones-9527713/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3582038">Marsha Jones</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3582038">Pixabay</a>'
            img = plt.imread("samples/dog.jpg")
        elif selected_provided_file == "Flower":
            img = plt.imread("samples/flower.jpg")
            additional_information = 'Image by <a href="https://pixabay.com/users/engin_akyurt-3656355/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3616249">Engin Akyurt</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3616249">Pixabay</a>'
    pipeline = A.Compose(create_pipeline(transformations))
    plot_audio_transformations(img, pipeline, additional_information)


def main():
    placeholder = st.empty()
    placeholder2 = st.empty()
    placeholder.markdown(
        "# Visualize an image augmentation pipeline\n"
        "### Select the components of the pipeline in the sidebar.\n"
        "Once you have chosen the augmentation techniques, select or upload an image.\n"
        "Then click 'Apply' to start!\n"
    )
    placeholder2.markdown(
        "After clicking start, the individual steps of the pipeline are visualized. The ouput of the previous step is the input to the next step."
    )
    # placeholder.write("Create your audio pipeline by selecting augmentations in the sidebar.")
    st.sidebar.markdown("Choose the transformations here:")
    gaussian_noise = st.sidebar.checkbox("GaussianNoise")

    horizontal_flip = st.sidebar.checkbox("HorizontalFlip")
    vertical_flip = st.sidebar.checkbox("VerticalFlip")
    random_brightness = st.sidebar.checkbox("RandomBrightness")
    advanced_blur = st.sidebar.checkbox("AdvancedBlur")
    channel_shuffle = st.sidebar.checkbox("ChannelShuffle")
    channel_dropout = st.sidebar.checkbox("ChannelDropout")
    random_contrast = st.sidebar.checkbox("RandomContrast")

    st.sidebar.markdown("---")
    st.sidebar.markdown("(Optional) Upload an image file here:")
    file_uploader = st.sidebar.file_uploader(label="", type=[".png", ".jpg", ".jpeg"])
    st.sidebar.markdown("Or select a sample file here:")
    selected_provided_file = st.sidebar.selectbox(
        label="", options=["Flower", "Dog"]
    )

    st.sidebar.markdown("---")
    if st.sidebar.button("Apply"):
        placeholder.empty()
        placeholder2.empty()
        transformations = [
            gaussian_noise,
            horizontal_flip,
            vertical_flip,
            random_brightness,
            advanced_blur,
            channel_shuffle,
            channel_dropout,
            random_contrast,

        ]

        action(
            file_uploader=file_uploader,
            selected_provided_file=selected_provided_file,
            transformations=transformations,
        )


if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Image Augmentation Visualizer")
    main()
