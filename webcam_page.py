import streamlit as st
import cv2
import numpy as np

st.title("Real-Time Webcam Feed")

# Initialize the webcam
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    st.error("Error: Could not open video device.")
else:
    # Stream the video feed
    stframe = st.empty()
    while True:
        success, frame = video_capture.read()
        if not success:
            st.error("Error: Failed to read frame from video device.")
            break
        else:
            # Convert the frame to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Display the frame
            stframe.image(frame, channels='RGB')
