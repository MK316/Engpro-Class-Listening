import streamlit as st
from gtts import gTTS
import io

# Create a new page for the lesson
st.title("📘 Lesson: Stress Shift in Noun-Verb Pairs")

# Introduction
st.markdown("""
### Understanding Noun-Verb Stress Shift
Some English words change their stress pattern depending on whether they are a **noun** or a **verb**.
""", unsafe_allow_html=True)

# Visual representation of stress patterns
st.markdown("""
<style>
    .stress { font-size: 24px; font-weight: bold; color: #E74C3C; }
    .word { font-size: 22px; font-weight: bold; }
</style>

- **<span class="word">Noun</span>:** The stress is on the **first syllable**  
  → <span class="stress">'REcord</span>  
- **<span class="word">Verb</span>:** The stress is on the **second syllable**  
  → <span class="stress">re'CORD</span>  
""", unsafe_allow_html=True)

# Word pairs for demonstration
word_pairs = {
    "record": ("Keep a **record** of your expenses.", "Please **record** your presentation."),
    "address": ("Let me know your **address**.", "The president **addressed** the matter."),
    "envelope": ("Can I borrow an **envelope**?", "Can you **envelop** the box?"),
    "invalid": ("The **invalid** is in the hospital.", "The rule is **invalid** in this situation."),
    "desert": ("The city has a huge **desert**.", "The boy was **deserted** on the street.")
}

# Function to generate audio
def generate_audio(noun_text, verb_text):
    plain_text = f"{noun_text}\n{verb_text}"  # Remove Markdown formatting for audio
    tts = gTTS(text=plain_text, lang='en')
    audio_data = io.BytesIO()
    tts.write_to_fp(audio_data)
    audio_data.seek(0)
    return audio_data

# User selection for audio playback
st.markdown("### 🎧 Listen to Examples")
selected_word = st.selectbox("Choose a word to hear its noun and verb pronunciation:", list(word_pairs.keys()))

if selected_word:
    noun_sentence, verb_sentence = word_pairs[selected_word]

    # Display text in bold (Markdown)
    st.write(f"**💛 Noun Usage:** {noun_sentence}")
    st.write(f"**💙 Verb Usage:** {verb_sentence}")

    # Generate and play audio using plain text
    audio_data = generate_audio(noun_sentence.replace("**", ""), verb_sentence.replace("**", ""))
    st.audio(audio_data.getvalue(), format='audio/mp3')

st.markdown("---")
st.markdown("**Practice different word pairs to understand the pronunciation changes!** 🎤")
