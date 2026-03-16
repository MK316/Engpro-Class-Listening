import streamlit as st
from gtts import gTTS
import io

st.markdown("#### 🔊 Comparing Pronunciation of Borrowed Words")
st.caption("Workbook page 48")

# List of borrowed words in Korean and English
borrowed_words = {
    "1. 토이스토리 / Toy Story": ("토이스토리", "Toy Story"),
    "2. 부탄가스 / Butane Gas": ("부탄가스", "Butane Gas"),
    "3. 로그온 / Log On": ("로그온", "Log On"),
    "4. 노트북 / Notebook": ("노트북", "Notebook"),
    "5. 프라이드치킨 / Fried Chicken": ("프라이드치킨", "Fried Chicken")
}

# Function to generate audio for Korean and English separately
def generate_audio(text, language):
    tts = gTTS(text=text, lang=language)
    audio_data = io.BytesIO()
    tts.write_to_fp(audio_data)
    audio_data.seek(0)
    return audio_data

# Generate audio buttons for each word pair
for label, (korean, english) in borrowed_words.items():
    st.write(f"**{label}**")
    if st.button(f"Play {label}", key=f"play_{label}"):
        korean_audio = generate_audio(korean, 'ko')
        english_audio = generate_audio(english, 'en')
        st.audio(korean_audio, format='audio/mp3')
        st.audio(english_audio, format='audio/mp3')
st.markdown("---")
st.markdown("### 🎤 Generate Audio for Any Text")

# User input box for text
user_text = st.text_input("Enter text:")

# Button to generate audio for user-input text
if st.button("Generate Audio"):
    if user_text:
        audio_output = generate_audio(user_text, "en")
        st.audio(audio_output, format='audio/mp3')
    else:
        st.warning("Please enter text before generating audio.")
