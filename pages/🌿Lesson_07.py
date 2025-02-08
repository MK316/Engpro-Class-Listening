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
    korean_tts = gTTS(text=korean, lang='ko')
    english_tts = gTTS(text=english, lang='en')
    
    korean_audio = io.BytesIO()
    english_audio = io.BytesIO()
    
    korean_tts.write_to_fp(korean_audio)
    english_tts.write_to_fp(english_audio)
    
    korean_audio.seek(0)
    english_audio.seek(0)
    
    return korean_audio, english_audio
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
        korean_audio, english_audio = generate_audio(korean, english)
        st.audio(korean_audio.getvalue(), format='audio/mp3')
        st.audio(english_audio.getvalue(), format='audio/mp3')
        audio_data = generate_audio(korean, english)
        st.audio(audio_data.getvalue(), format='audio/mp3')
