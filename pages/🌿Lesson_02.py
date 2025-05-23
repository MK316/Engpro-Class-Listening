import streamlit as st
from gtts import gTTS
import os

# Create a tab bar with three tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎱 Exercise A", "🎱 Exercise B", "🎱 Exercise C", "🎾 Read-aloud"])

with tab1:
    st.caption("Workbook page 26")
    st.info("<Example> Choose ONE that is different from the others. (you will hear) 1. mitt  2. meat 3. meat, and choose  1. mitt as the correct answer")
    
    # Define the number of questions
    num_questions = 10
    # This dictionary will hold the user's answers
    answers = {}
    
    # Define the correct answers (update these as per your quiz answers)
    correct_answers = {
        1: 1, 2: 3, 3: 2, 4: 3, 5: 1,
        6: 1, 7: 2, 8: 1, 9: 2, 10: 1
    }

    # Provide a single audio file that contains all questions
    audio_file1 = 'https://github.com/MK316/Engpro-Class-Listening/blob/main/audio/L01A.wav?raw=true'
    st.audio(audio_file1, format='audio/wav', start_time=0)
    
    # Display instructions


    st.markdown("#### Q: Listen to the audio and answer the questions below. Each number corresponds to the sequence of words spoken in the audio.")
    st.markdown("---")
    
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
        incorrect_feedback = []
        for q in answers:
            if int(answers[q]) == correct_answers[q]:
                correct_count += 1
            else:
                incorrect_feedback.append(f"Question {q}: Your answer was {answers[q]}, but the correct answer is {correct_answers[q]}.")
        # Display the result
        st.write(f'You answered {correct_count} out of {num_questions} correctly!')
        
        if incorrect_feedback:
            st.subheader("Review the incorrect answers:")
            for feedback in incorrect_feedback:
                st.text(feedback)

with tab2:
    # Define the pairs of words as shown in the image
    word_pairs = {
        1: ("field", "filled"),
        2: ("bean", "bin"),
        3: ("neat", "knit"),
        4: ("deal", "dill"),
        5: ("beat", "bit"),
        6: ("team", "Tim"),
        7: ("sleep", "slip"),
        8: ("green", "grin"),
        9: ("heel", "hill"),
        10: ("week", "wick")
    }

    st.info("<Example> Choose the ONE you hear: mitt / meat (circle mitt)")
    
    # Provide a single audio file that contains all questions
    audio_file2 = 'https://github.com/MK316/Engpro-Class-Listening/blob/main/audio/L01B.wav?raw=true'
    st.audio(audio_file2, format='audio/wav', start_time=0)

    # Display instructions
    st.markdown("#### Q: You’ll hear one word. Listen and circle the word that you hear.")
    st.markdown("---")
    # This dictionary will hold the user's answers
    answers = {}
    # Define the correct answers (update these as per your quiz answers)
    correct_answers = {
        1: "field", 2: "bean", 3: "knit", 4: "dill", 5: "bit",
        6: "team", 7: "slip", 8: "green", 9: "hill", 10: "wick"
    }

    # Loop through the number of questions to display them
    for i in word_pairs:
        # Let the user select an answer
        answer = st.radio(
            f"Question {i}: {word_pairs[i][0]} / {word_pairs[i][1]}",
            word_pairs[i],
            key=f'tab2_question_{i}'  # Unique key by prefixing with 'tab2_'
        )
        
        # Save the answer in the dictionary
        answers[i] = answer
    
    # Button to check answers
    if st.button('Check Answers', key='tab2_check_answers'):  # Ensure unique key for the button as well
        correct_count = 0
        incorrect_feedback = []
        for q in answers:
            if answers[q] == correct_answers[q]:
                correct_count += 1
            else:
                incorrect_feedback.append(f"Question {q}: Your answer was {answers[q]}, but the correct answer is {correct_answers[q]}.")

        # Display the result
        st.write(f'You answered {correct_count} out of {len(word_pairs)} correctly!')
        
        if incorrect_feedback:
            st.subheader("Review the incorrect answers:")
            for feedback in incorrect_feedback:
                st.text(feedback)

with tab3:
    st.info("<Example> (You'll hear) 'You need a new wheel'. Choose 'wheel' as the correct answer.")

    

    # Define the sentences with choice pairs as shown in the image
    sentence_pairs = {
        1: ("They cleaned the _______.", ["ship", "sheep"]),
        2: ("Will he _______?", ["leave", "live"]),
        3: ("The boy was _______.", ["beaten", "bitten"]),
        4: ("His clothes are _______.", ["neat", "knit"]),
        5: ("She has plump _______.", ["cheeks", "chicks"]),
        6: ("I like low _______.", ["heels", "hills"]),
        7: ("The children will _______.", ["sleep", "slip"]),
        8: ("I heard every _______.", ["beat", "bit"]),
        9: ("They stored the _______.", ["beans", "bins"]),
        10: ("Everyone talks about the _______.", ["heat", "hit"])
        }

    # Provide a single audio file that contains all questions
    audio_file3 = 'https://github.com/MK316/Engpro-Class-Listening/blob/main/audio/L01C.wav?raw=true'
    st.audio(audio_file3, format='audio/wav', start_time=0)

    # Display instructions
    st.markdown("#### Q: Listen and circle the word that is used to complete each sentence.")
    st.markdown("---")
    # This dictionary will hold the user's answers
    answers = {}
    # Define the correct answers (update these as per your quiz answers)
    correct_answers = {
        1: "ship", 2: "leave", 3: "bitten", 4: "neat", 5: "cheeks",
        6: "heels", 7: "slip", 8: "beat", 9: "beans", 10: "heat"
    }

    # Loop through the number of questions to display them
    for i in sentence_pairs:
        # Let the user select an answer
        answer = st.radio(
            f"Question {i}: {sentence_pairs[i][0]}",
            sentence_pairs[i][1],
            key=f'tab3_question_{i}'  # Unique key by prefixing with 'tab3_'
        )
        
        # Save the answer in the dictionary
        answers[i] = answer
    
    # Button to check answers
    if st.button('Check Answers', key='tab3_check_answers'):  # Ensure unique key for the button as well
        correct_count = 0
        incorrect_feedback = []
        for q in answers:
            if answers[q] == correct_answers[q]:
                correct_count += 1
            else:
                incorrect_feedback.append(f"Question {q}: Your answer was {answers[q]}, but the correct answer is {correct_answers[q]}.")

        # Display the result
        st.write(f'You answered {correct_count} out of {len(sentence_pairs)} correctly!')
        
        if incorrect_feedback:
            st.subheader("Review the incorrect answers:")
            for feedback in incorrect_feedback:
                st.text(feedback)
with tab4:
    st.write("Read aloud - The Beatles")
    st.markdown("""
    The Beatles were an English rock band that formed in Liverpool, in 1960.  
    With John Lennon, Paul McCartney, George Harrison and Ringo Starr,  
    they became widely regarded as the greatest and most influential act of the rock era.   
    Rooted in skiffle, beat and 1950s rock and roll,  
    the Beatles later experimented with several genres, ranging from pop ballads and Indian music  
    to psychedelic and hard rock, often incorporating classical elements in innovative ways.  
    In the early 1960s, their enormous popularity first emerged as 'Beatlemania',  
    but as their songwriting grew in sophistication they came to be perceived  
    as an embodiment of the ideals shared by the era's sociocultural revolutions.  
    
    _From wikipedia.org_
    """)
    st.markdown("#### 🍎 1. Generate Audio with Different Speeds")
    st.write("Select the speed and generate the audio for the provided text.")

    # Text to be converted to speech
    text = """The Beatles were an English rock band that formed in Liverpool in 1960.
              With John Lennon, Paul McCartney, George Harrison and Ringo Starr,
              they became widely regarded as the greatest and most influential act of
              the rock era. Rooted in skiffle, beat and 1950s rock and roll, the Beatles
              later experimented with several genres, ranging from pop ballads and Indian music to
              psychedelic and hard rock, often incorporating classical elements in innovative ways.
              In the early 1960s, their enormous popularity first emerged as "Beatlemania", but as
              their songwriting grew in sophistication they came to be perceived as an embodiment
              of the ideals shared by the era's sociocultural revolutions."""

    speed = st.radio("Choose the speech speed:", ('Normal', 'Slow', 'Slower'), key='speech_speed')

    if st.button('Generate Audio'):
        tts = gTTS(text, lang='en', slow=(speed != 'Normal'))
        audio_file = '/tmp/audio.mp3'
        tts.save(audio_file)
        audio_bytes = open(audio_file, "rb").read()
        st.audio(audio_bytes, format='audio/mp3')

    st.write("---")
    st.markdown("#### 🍎 2. Shadowing: Practice with different voices")

    # Audio files
    audio_urls = {
        'Male': 'https://github.com/MK316/Engpro-Class-Listening/blob/main/audio/Read-Beatles-M.mp3?raw=true',
        'Female': 'https://github.com/MK316/Engpro-Class-Listening/blob/main/audio/Read-Beatles-F.mp3?raw=true',
        'MK316': 'https://github.com/MK316/Engpro-Class-Listening/blob/main/audio/Read-Beatles-Elliot.mp3?raw=true'
    }

    selected_voice = st.selectbox("Select Voice", options=['Male', 'Female', 'MK316'], key='selected_voice')
    st.caption("You can change the speech by clicking the three vertical dots in the audio panel.")
    if st.button("Show Selected Audio"):
        selected_audio_url = audio_urls[selected_voice]

        # Display audio without adjusted speed (default playback)
        st.markdown(f"""
        <audio controls>
            <source src="{selected_audio_url}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """, unsafe_allow_html=True)
    st.markdown("---")
    
    st.write("Read aloud - The Beatles")
    st.markdown("""
    The Beatles were an English rock band that formed in Liverpool, in 1960. With John Lennon, Paul McCartney, George Harrison and Ringo Starr,  
    they became widely regarded as the greatest and most influential act of the rock era. Rooted in skiffle, beat and 1950s rock and roll, the Beatles later experimented with several genres, ranging from pop ballads and Indian music  
    to psychedelic and hard rock, often incorporating classical elements in innovative ways. In the early 1960s, their enormous popularity first emerged as 'Beatlemania',  
    but as their songwriting grew in sophistication they came to be perceived as an embodiment of the ideals shared by the era's sociocultural revolutions.  
    
    _From wikipedia.org_
    """)
