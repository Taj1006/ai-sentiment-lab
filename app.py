import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="My AI Lab", page_icon=":brain:")

st.title(":brain: AI for Sentiment Analysis (CD TEST v1)")
st.write("Enter an English message in the box below, and AI will determine whether it's Positive or Negative.")

text_input = st.text_area("Input Text (English only):", height=150)

if st.button("Analyze"):
    if text_input:
        blob = TextBlob(text_input)
        score = blob.sentiment.polarity

        st.divider()
        st.subheader("Analysis Results:")

        if score > 0:
            st.success(f":blush: Positive (Score: {score:.2f})")
            st.balloons()
        elif score < 0:
            st.error(f":rage: Negative (Score: {score:.2f})")
        else:
            st.info(f":neutral_face: Neutral (Score: {score:.2f})")
    else:
        st.warning("Please type a message before pressing the button!")