import streamlit as st
from gtts import gTTS
import io
import datetime

st.title("🎧 Listening Quiz: Identify [ɔ] Vowel")

# Audio for the quiz
quiz_audio_url = "https://github.com/MK316/Engpro-Class/raw/main/audio/listening_quiz.mp3"
st.audio(quiz_audio_url, format='audio/mp3')

st.write("You will hear two sentences. Select the one that contains a word with the vowel [ɔ].")

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

    # Get current date and time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Placeholder for user ID (Replace with authentication-based ID if available)
    user_id = "User123"  # If authentication is available, replace with actual user identifier

    st.markdown(f"### 📝 Quiz Results")
    st.write(f"**User ID:** {user_id}")
    st.write(f"**Date & Time:** {current_time}")
    st.write(f"**Your Score:** {score}/5")
    
    if missing:
        st.write("❌ **Incorrect answers:**", ", ".join(missing))
    else:
        st.success("🎉 Perfect Score! Well done!")
