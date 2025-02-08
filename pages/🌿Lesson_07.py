import streamlit as st
from gtts import gTTS
import io

st.title("🔊 Comparing Pronunciation of Borrowed Words")

# List of borrowed words in Korean and English
borrowed_words = {
    "1. 토이스토리 / Toy Story": ("토이스토리", "Toy Story"),
    "2. 부탄가스 / Butane Gas": ("부탄가스", "Butane Gas"),
    "3. 로그온 / Log On": ("로그온", "Log On"),
    "4. 노트북 / Notebook": ("노트북", "Notebook"),
    "5. 프라이드치킨 / Fried Chicken": ("프라이드치킨", "Fried Chicken")
}

# Function to generate audio for Korean and English separately
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

st.markdown("### 🎧 Listen to the Pronunciations")

# Generate audio buttons for each word pair
for label, (korean, english) in borrowed_words.items():
    st.write(f"**{label}**")
    if st.button(f"Play {label}", key=f"play_{label}"):
        korean_audio, english_audio = generate_audio(korean, english)
        st.audio(korean_audio, format='audio/mp3')
        st.audio(english_audio, format='audio/mp3')
