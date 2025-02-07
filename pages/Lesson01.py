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


  # Provide a single audio file that contains all questions
  audio_file = 'https://github.com/MK316/Engpro-Class-Listening/blob/main/audio/L01A.wav?raw=true'
  st.audio(audio_file, format='audio/wav', start_time=0)
  
  # Display instructions
  st.write("Listen to the audio and answer the questions below. Each question corresponds to a segment in the audio.")
  
  # Loop through the number of questions to display them
  for i in range(1, num_questions + 1):
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
    st.write("test")
with tabs[2]:
    st.write("test")
