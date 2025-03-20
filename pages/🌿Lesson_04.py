import streamlit as st
from gtts import gTTS
import io
import datetime

st.markdown("### 🎧 Listening Quiz: Identify [æ] Vowel")
st.caption("Workbook page 35")

# User ID Input
user_id = st.text_input("Enter your name or student ID:", placeholder="홍길동(2025120032)")

# Audio for the quiz
quiz_audio_url = "https://github.com/MK316/Engpro-Class-Listening/raw/main/audio/L04A.wav"
st.audio(quiz_audio_url, format='audio/wav')

st.write("Choose a word that contains [æ] vowel.")

st.write("🐤 Example")
st.write("(You'll hear) 1. add  2. Ed  3. odd")
st.write("Choose '1' for the correct answer")
st.markdown("---")
# Quiz questions and correct answers
quiz_options = {
    "1": "(1) (2) (3)",
    "2": "(1) (2) (3)",
    "3": "(1) (2) (3)",
    "4": "(1) (2) (3)",
    "5": "(1) (2) (3)",
    "6": "(1) (2) (3)",
    "7": "(1) (2) (3)",
    "8": "(1) (2) (3)",
    "9": "(1) (2) (3)",
    "10": "(1) (2) (3)",
  
}
correct_answers = {"1": "1", "2": "3", "3": "1", "4": "2", "5": "3", "6":"1","7":"3","8":"2","9":"1","10":"2"}

# User answers selection
user_answers = {}
for key in quiz_options.keys():
    if f"quiz_{key}" not in st.session_state:
        st.session_state[f"quiz_{key}"] = "1"  # default value
    user_answers[key] = st.radio(f"Question {key}", ["1", "2", "3"], key=f"quiz_{key}")

# Submit button to check answers
if st.button("Submit Quiz"):
    score = sum(1 for q in correct_answers if user_answers[q] == correct_answers[q])
    missing = [q for q in correct_answers if user_answers[q] != correct_answers[q]]

    # Get current date and time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.markdown(f"### 📝 Quiz Results")
    st.write(f"**User ID:** {user_id if user_id else 'Anonymous'}")
    st.write(f"**Date & Time:** {current_time}")
    st.write(f"**Your Score:** {score}/10")
    
    if missing:
        st.write("❌ **Incorrect answers:**", ", ".join(missing))
    else:
        st.success("🎉 Perfect Score! Well done!")
