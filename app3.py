import streamlit as st
import io
import nltk
import string
import emoji
from nltk.corpus import stopwords

nltk.download('stopwords')

def clean_text(text, keep_emojis, keep_stopwords, keep_punctuation, language):
    if not keep_emojis:
        text = emoji.replace_emoji(text, replace='')  # Remove emojis

    arabic_punctuation = '؟،؛«»'
    if not keep_punctuation:
        if language == 'arabic':
            text = text.translate(str.maketrans('', '', arabic_punctuation + string.punctuation))
        else:
            text = text.translate(str.maketrans('', '', string.punctuation))

    if not keep_stopwords:
        stop_words = set(stopwords.words(language))
        text = ' '.join([word for word in text.split() if word.lower() not in stop_words])

    return text

def detect_stopwords(text, stopwords_list):
    stopwords_in_text = [word for word in text.split() if word.lower() in stopwords_list]
    return stopwords_in_text

def detect_punctuation(text):
    punctuation_in_text = [char for char in text if char in string.punctuation]
    return punctuation_in_text

def detect_emojis(text):
    emojis_in_text = [char for char in text if char in emoji.EMOJI_DATA]
    return emojis_in_text

st.set_page_config(page_title='Text Cleaner App', layout='wide')

st.markdown("""
    <style>
        .centered-text {
            text-align: center;
            font-size: 18px;
            font-weight: bold;
        }
        .cleaned-text {
            text-align: center;
            font-family: 'Courier New', monospace;
            font-size: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.header('Text Cleaning Options')

language_map = {'EN': 'english', 'FR': 'french', 'AR': 'arabic'}
language_choice = st.sidebar.selectbox('Choose Language', ['EN', 'FR', 'AR'])
language = language_map[language_choice]

keep_emojis = st.sidebar.radio("Keep the emojis?", ('Yes', 'No')) == 'Yes'
keep_stopwords = st.sidebar.radio("Keep the stopwords?", ('Yes', 'No')) == 'Yes'
keep_punctuation = st.sidebar.radio("Keep the punctuations?", ('Yes', 'No')) == 'Yes'

st.markdown('<h2 class="centered-text">Input Text</h2>', unsafe_allow_html=True)
text = st.text_area("Write your text here:", height=200)

if 'clean_text_button_clicked' not in st.session_state:
    st.session_state.clean_text_button_clicked = False

if not st.session_state.clean_text_button_clicked:
    clean_button_clicked = st.button("Clean Text", key="clean_text_button", help="Click to clean the input text")

    if clean_button_clicked:
        st.session_state.clean_text_button_clicked = True

if st.session_state.clean_text_button_clicked and text:
    stop_words = set(stopwords.words(language))
    stopwords_in_text = detect_stopwords(text, stop_words)
    punctuation_in_text = detect_punctuation(text)
    emojis_in_text = detect_emojis(text)

    if keep_stopwords and stopwords_in_text:
        st.warning(f"Stop words detected: {', '.join(stopwords_in_text)}")
    if keep_punctuation and punctuation_in_text:
        st.warning(f"Punctuation marks detected: {', '.join(punctuation_in_text)}")
    if keep_emojis and emojis_in_text:
        st.warning(f"Emojis detected: {', '.join(emojis_in_text)}")

    cleaned_text = clean_text(text, keep_emojis, keep_stopwords, keep_punctuation, language)

    st.markdown('<h2 class="centered-text">Cleaned Text</h2>', unsafe_allow_html=True)
    st.markdown(f'<div class="cleaned-text">{cleaned_text}</div>', unsafe_allow_html=True)

    cleaned_text_buffer = io.BytesIO(cleaned_text.encode('utf-8'))
    st.download_button(
        label="⬇️ Download the cleaned text",
        data=cleaned_text_buffer,
        file_name="cleaned_text.txt",
        mime="text/plain"
    )
elif not text and st.session_state.clean_text_button_clicked:
    st.write("Please enter text to clean.")
