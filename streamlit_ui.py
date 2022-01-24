#####-----importing neccessary libraries-----#####

import cv2
import time
import imutils
import requests
import numpy as np
import seaborn as sb
from PIL import Image
import streamlit as st
import matplotlib.pyplot as plt
from skimage.color import rgb2yuv

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

    elif label == 'Low Contrast':
        img_yuv = rgb2yuv(sample)
        Y = img_yuv[:, :, 0]
        fig, ax = plt.subplots()
        sb.heatmap(Y, cbar = False, xticklabels = False, yticklabels = False)
        return fig

    elif label == 'Out of Focus':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        array = cv2.Laplacian(gray, cv2.CV_64F)
        data = Image.fromarray(array)
        return data

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

col1, col2, col3 = st.columns([3,3,1])

with col1:
    st.write("")

with col2:
    st.write("")

with col3:
    st.image(cv2.imread("virtusa_logo.png"), width=250)


st.markdown('<h1 style = "color:#66bfbf; font-size: 75px; text-align:center; font-weight:bold">PreEYE<sup style = "vertical-align: super; font-size: 20px ;">alpha</sup></h1>', unsafe_allow_html=True)
st.markdown('<h2 style = "color:#f76b8a; text-align: center;">Analyse Advert Images', unsafe_allow_html=True)
st.text("")
st.text("")

st.subheader("Paste an image's link here to analyse it")
link = st.text_area("", key = "link")
st.subheader("Insert the Ad text here")
ad_text = st.text_area("", key = "ad_text")
st.text("")
predict = st.button("Analyse Image")
st.text("")
progress_bar = st.progress(0)

col1, col2, col3, col4, col5 = st.columns(5)
visual_appeal_1 = col1.container()
visual_appeal_2 = col2.container()
visual_appeal_3 = col3.container()
visual_appeal_4 = col4.container()
visual_appeal_5 = col5.container()

vcol1, vcol2, vcol3 = st.columns(3)
vision_text = vcol1.container()
vision_compliance = vcol2.container()
vision_relevance = vcol3.container()

#####-----Button function-----#####

if predict:

    if (len(link) or len(ad_text)) <= 0:
        st.error('Please provide the neccessary details to process...')

    else:

        try:
            result = call_preEYE(link)
            image = imutils.url_to_image(link)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            placeholder = cv2.imread("vision_api.jpg")

            message = ""
            for i in result:
                if i=="Collage":
                    if result[i][0]==True:
                        message = message+"The image is a Collage.\n"
                if i=="Low Contrast":
                    if result[i][0]==True:
                        message = message+"The image is of Low Contrast.\n"
                if i=="Out of Focus":
                    if result[i][0]==True:
                        message = message+"The image is Out Of Focus.\n"
                if i=="Color Inverted":
                    if result[i][0]==True:
                        message = message+"The image is Color Inverted.\n"
                if i=="Excessive Blank Space":
                    if result[i][0]==True:
                        message = message+"The image has Excessive Blank Space.\n"

            if len(message)==0:
                message = "PreEYE says the image is good."

            st.subheader("Inference")
            st.text(message)
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
                st.pyplot(processed_image_2)
                st.text('Low Contrast: ' + str(result['Low Contrast'][0]))

            progress_bar.progress(50)

            with visual_appeal_3:
                st.subheader("Out Of Focus / Blurry")
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

            with vision_text:
                st.subheader("Text/Logo")
                st.image(placeholder)
                st.text('Text/Logo: True/False')

            progress_bar.progress(80)

            with vision_compliance:
                st.subheader("Compliance Policy")
                st.image(placeholder)
                st.text('Complies: True/False')

            progress_bar.progress(90)

            with vision_relevance:
                st.subheader("Ad Text-Image Relevance")
                st.image(placeholder)
                st.text('Relevant: True/False')

            progress_bar.progress(100)



        except:
            st.error('Could not load image...')


col1, col2, col3 = st.columns([1,2,1])

with col1:
    st.write("Alpha Development in Progress")

with col2:
    st.write("")

with col3:
    st.write("Developed by TMT-West Solutions Team, Virtusa")
