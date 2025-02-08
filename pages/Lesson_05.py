import streamlit as st
from gtts import gTTS
import io

st.markdown("### 🎧 Listening Quiz: Identify [ɔ] Vowel")

# Audio for the quiz
quiz_audio_url = "https://github.com/MK316/Engpro-Class-Listening/raw/main/audio/L05A.wav"
st.audio(quiz_audio_url, format='audio/wav')

st.write("You will hear two sentences. Select the one that contains a word with the vowel [ɔ].")
st.write("Example")
st.write("(a) It's in the hall. (b) It's in the hole.")
st.markdown("---")
# Quiz questions and correct answers
quiz_options = {
    "1": "(a) (b)",
    "2": "(a) (b)",
    "3": "(a) (b)",
    "4": "(a) (b)",
    "5": "(a) (b)"
}
correct_answers = {"1": "a", "2": "b", "3": "a", "4": "b", "5": "a"}

# User answers selection
user_answers = {}
for key in quiz_options.keys():
    user_answers[key] = st.radio(f"Question {key}", ["a", "b"], key=f"quiz_{key}")

# Submit button to check answers
if st.button("Submit Quiz"):
    score = sum(1 for q in correct_answers if user_answers[q] == correct_answers[q])
    missing = [q for q in correct_answers if user_answers[q] != correct_answers[q]]
    
    st.write(f"Your Score: {score}/5")
    if missing:
        st.write("Incorrect answers:", ", ".join(missing))
    else:
        st.success("Perfect Score! Well done!")
