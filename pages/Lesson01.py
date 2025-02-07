import streamlit as st

# Create a tab bar with three tabs
tab1, tab2, tab3 = st.tabs(["Exercise A", "Exercise B", "Exercise C"])

with tab1:

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

    st.markdown("""
    ---
    <Example>  

    (you will hear) 
    
    1. mitt  2. meat 3. meat  
    """)
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

    # Provide a single audio file that contains all questions
    audio_file = 'https://github.com/MK316/Engpro-Class-Listening/blob/main/audio/L01A.wav?raw=true'
    st.audio(audio_file, format='audio/wav', start_time=0)

    # Display instructions
    st.write("You’ll hear one word. Listen and circle the word that you hear.")
    
    # This dictionary will hold the user's answers
    answers = {}
    # Define the correct answers (update these as per your quiz answers)
    correct_answers = {
        1: "filled", 2: "bin", 3: "knit", 4: "dill", 5: "bit",
        6: "Tim", 7: "slip", 8: "grin", 9: "hill", 10: "wick"
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
    # Define the sentences with choice pairs as shown in the image
    sentence_pairs = {
        1: ("They cleaned the", ["ship", "sheep"]),
        2: ("Will he", ["leave", "live"]),
        3: ("The boy was", ["beaten", "bitten"]),
        4: ("His clothes are", ["neat", "knit"]),
        5: ("She has plump", ["cheeks", "chicks"]),
        6: ("I like low", ["heels", "hills"]),
        7: ("The children will", ["sleep", "slip"]),
        8: ("I heard every", ["beat", "bit"]),
        9: ("They stored the", ["beans", "bins"]),
        10: ("Everyone talks about the", ["heat", "hit"])
    }

    # Provide a single audio file that contains all questions
    audio_file = 'https://github.com/MK316/Engpro-Class-Listening/blob/main/audio/L01A.wav?raw=true'
    st.audio(audio_file, format='audio/wav', start_time=0)

    # Display instructions
    st.write("Listen and circle the word that is used to complete each sentence.")

    # This dictionary will hold the user's answers
    answers = {}
    # Define the correct answers (update these as per your quiz answers)
    correct_answers = {
        1: "ship", 2: "leave", 3: "bitten", 4: "neat", 5: "cheeks",
        6: "hills", 7: "sleep", 8: "bit", 9: "bins", 10: "heat"
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
