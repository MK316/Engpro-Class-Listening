import streamlit as st
from gtts import gTTS
import io

st.title("🔊 Comparing Pronunciation of Borrowed Words")

# List of borrowed words in Korean and English
borrowed_words = {
    "토이스토리 / Toy Story": ("토이스토리", "Toy Story"),
    "부탄가스 / Butane Gas": ("부탄가스", "Butane Gas"),
    "로그온 / Log On": ("로그온", "Log On"),
    "노트북 / Notebook": ("노트북", "Notebook"),
    "프라이드치킨 / Fried Chicken": ("프라이드치킨", "Fried Chicken")
}

# Function to generate audio for Korean and English together
def generate_audio(korean, english):
    text = f"{korean}. {english}."
    tts = gTTS(text=text, lang='ko')  # Use Korean language setting
    audio_data = io.BytesIO()
    tts.write_to_fp(audio_data)
    audio_data.seek(0)
    return audio_data

st.markdown("### 🎧 Listen to the Pronunciations")

# Generate audio buttons for each word pair
for label, (korean, english) in borrowed_words.items():
    st.write(f"**{label}**")
    if st.button(f"Play {label}"):
        audio_data = generate_audio(korean, english)
        st.audio(audio_data.getvalue(), format='audio/mp3')
