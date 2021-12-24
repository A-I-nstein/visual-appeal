#####-----importing neccessary libraries-----#####

import cv2
import time
import imutils
import requests
import streamlit as st

#####-----Backend Elements-----#####

def call_preEYE(link):

    params = {"link": link}
    result = requests.post('https://analyse-visual-appeal.herokuapp.com/vis-ap/', params = params)

    return result.json()

def draw_on_image(link, result, label):

    image = imutils.url_to_image(link)
    sample = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if label == 'Collage':
        for i in result[label][1]:
            x1, y1, x2, y2 = i[0], i[1], i[2], i[3]
            cv2.line(sample, (x1,y1), (x2,y2), (255, 0, 0), 5)

    else:
        cnts = result[label][1]
        for c in cnts:
            x, y, w, h = c[0], c[1], c[2], c[3]
            cv2.rectangle(sample, (x, y), (x + w, y + h), (255, 0, 0), 5)

    return sample

#####-----UI Elements-----#####

st.set_page_config(layout="wide")

hide_streamlit_style = """
                   <style>
                   #MainMenu {visibility: hidden;}
                   footer {visibility: hidden;}
                   </style>
                   """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown('<h1 style = "color:#66bfbf; font-size: 75px; text-align:center; font-weight:bold">PreEYE</h1>', unsafe_allow_html=True)
st.markdown('<h2 style = "color:#f76b8a; text-align: center;">Analysing Visual Appeals', unsafe_allow_html=True)
st.markdown('<h3 style = "color:#66bfbf; text-align: center;">Developed by TMT-West Solutions Team', unsafe_allow_html=True)
st.text("")
st.text("")
st.subheader("Paste an image's link here to analyse it's visual appeal")
link = st.text_area("")
st.text("")

predict = st.button("Check Visual Appeal")

progress_bar = st.progress(0)

col1, col2, col3, col4, col5 = st.columns(5)

visual_appeal_1 = col1.container()
visual_appeal_2 = col2.container()
visual_appeal_3 = col3.container()
visual_appeal_4 = col4.container()
visual_appeal_5 = col5.container()

#####-----Button function-----#####

if predict:

    if len(link) <= 0:
        st.error('Please provide a link to process...')

    else:

        try:
            result = call_preEYE(link)
            image = imutils.url_to_image(link)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            st.subheader("Original Image")
            st.image(image)

            progress_bar.progress(30)

            with visual_appeal_1:
                st.subheader("Collage")
                processed_image_1 = draw_on_image(link, result, 'Collage')
                st.image(processed_image_1)
                st.text('Collage: ' + str(result['Collage'][0]))

            progress_bar.progress(40)

            with visual_appeal_2:
                st.subheader("Low Contrast")
                processed_image_2 = draw_on_image(link, result, 'Low Contrast')
                st.image(processed_image_2)
                st.text('Low Contrast: ' + str(result['Low Contrast'][0]))

            progress_bar.progress(50)

            with visual_appeal_3:
                st.subheader("Out Of Focus")
                processed_image_3 = draw_on_image(link, result, 'Out of Focus')
                st.image(processed_image_3)
                st.text('Out of Focus: ' + str(result['Out of Focus'][0]))

            progress_bar.progress(60)

            with visual_appeal_4:
                st.subheader("Color Inverted")
                processed_image_4 = draw_on_image(link, result, 'Color Inverted')
                st.image(processed_image_4)
                st.text('Color Inverted: ' + str(result['Color Inverted'][0]))

            progress_bar.progress(70)

            with visual_appeal_5:
                st.subheader("Excessive Blank Space")
                processed_image_5 = draw_on_image(link, result, 'Excessive Blank Space')
                st.image(processed_image_5)
                st.text('Excessive Blank Space: ' + str(result['Excessive Blank Space'][0]))

            progress_bar.progress(100)

        except:
            st.error('Could not load image...')
