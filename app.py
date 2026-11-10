import streamlit as st

from sentiment import analyze_text

st.set_page_config(page_title="Sentiment Analysis Lab", page_icon=":brain:")
st.title(":brain: English Sentiment Analysis")
st.write("Explore positive, negative, or neutral polarity with TextBlob's built-in analyzer. No model is trained by this app.")

text_input = st.text_area("Input Text (English only):", height=150)

if st.button("Analyze"):
    if text_input.strip():
        try:
            score, label = analyze_text(text_input)
        except Exception:
            # Do not display submitted text or internal exception details.
            st.error("Analysis is unavailable. Please try again or check the local installation.")
        else:
            st.divider()
            st.subheader("Analysis Results:")

            if label == "Positive":
                st.success(f":blush: Positive (Score: {score:.2f})")
                st.balloons()
            elif label == "Negative":
                st.error(f":rage: Negative (Score: {score:.2f})")
            else:
                st.info(f":neutral_face: Neutral (Score: {score:.2f})")
    else:
        st.warning("Please type a message before pressing the button!")
