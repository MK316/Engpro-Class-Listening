import streamlit as st

# Create a tab bar with three tabs
tab1, tab2, tab3 = st.tabs(["Exercise A", "Exercise B", "Exercise C"])

with tabs[0]:
  import streamlit as st

# Define the number of questions
num_questions = 10
# This dictionary will hold the user's answers
answers = {}

# Define the correct answers (update these as per your quiz answers)
correct_answers = {
    1: 2, 2: 3, 3: 1, 4: 2, 5: 1,
    6: 3, 7: 2, 8: 1, 9: 3, 10: 2
}

st.title('Listening Quiz')

# Loop through the number of questions to display them
for i in range(1, num_questions + 1):
    # Display the audio file for the question
    audio_file = f'https://github.com/yourusername/yourrepo/blob/main/audio{i}.mp3?raw=true'
    st.audio(audio_file, format='audio/mp3', start_time=0)

    # Let the user select an answer
    answer = st.radio(
        f"Question {i}",
        ('1', '2', '3'),
        key=f'question_{i}'  # This key ensures each question has a unique radio button group
    )
    
    # Save the answer in the dictionary
    answers[i] = answer

# Button to check answers
if st.button('Check Answers'):
    correct_count = 0
    for q in answers:
        if int(answers[q]) == correct_answers[q]:
            correct_count += 1
    # Display the result
    st.write(f'You answered {correct_count} out of {num_questions} correctly!')

with tabs[1]:

with tabs[2]:
