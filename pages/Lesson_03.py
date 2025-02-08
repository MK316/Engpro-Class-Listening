import streamlit as st
from gtts import gTTS
import os

# Create a tab bar with three tabs
tab1, tab2 = st.tabs(["🎱 Exercise A", "🎾 Read-aloud"])

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
    audio_file = 'https://github.com/MK316/Engpro-Class-Listening/blob/main/audio/L03A.wav?raw=true'
    st.audio(audio_file, format='audio/wav', start_time=0)
    
    # Display instructions
    st.write("Listen to the audio and answer the questions below. Each question corresponds to a segment in the audio.")

    st.markdown("""
    ---
    <Example>  
    
    Q: Choose ONE that is different from the others.
    
    (you will hear) 
    
    1. fool  2. fool 3. full  

    (you answer)

    1. full
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
    st.write("Read aloud - Little Red Riding Hood")
    st.markdown("""
    Little Red Riding Hood. The story revolves around a girl called Little Red Riding Hood, 
    after the red hooded cape/cloak she wears. The girl walks through the woods 
    to deliver food to her sickly grandmother (wine and cake depending on the translation). 
    In the Grimms' version at least, she had the order from her mother to stay strictly on the path.
    A mean wolf wants to eat the girl and the food in the basket. He secretly stalks her 
    behind trees, bushes, shrubs, and patches of little and tall grass. 
    He approaches Little Red Riding Hood and she naïvely tells him where she is going. 
    He suggests that the girl pick some flowers; which she does. In the meantime; 
    he goes to the grandmother's house and gains entry by pretending to be the girl. 
    He swallows the grandmother whole (in some stories, he locks her in the closet) 
    and waits for the girl, disguised as the grandma. 
    """)
  
    st.markdown("#### 🍎 1. Generate Audio with Different Speeds")
    st.write("Select the speed and generate the audio for the provided text.")

    # Text to be converted to speech
    text = """Little Red Riding Hood. The story revolves around a girl called Little Red Riding Hood, after the
    red hooded cape/cloak she wears. The girl walks through the woods to
    deliver food to her sickly grandmother (wine and cake depending on the
    translation). In the Grimms' version at least, she had the order from her
    mother to stay strictly on the path.
    A mean wolf wants to eat the girl and the food in the basket. He secretly stalks
    her behind trees, bushes, shrubs, and patches of little and tall grass. He approaches
    Little Red Riding Hood and she naïvely tells him where she is going. He suggests that
    the girl pick some flowers; which she does. In the meantime; he goes to the
    grandmother's house and gains entry by pretending to be the girl. He swallows the
    grandmother whole (in some stories, he locks her in the closet) and waits for the girl,
    disguised as the grandma."""

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
    
    st.write("Read aloud - Little Red Riding Hood. ")
    st.markdown("""
    Little Red Riding Hood. The story revolves around a girl called Little Red Riding Hood, 
    after the red hooded cape/cloak she wears. The girl walks through the woods 
    to deliver food to her sickly grandmother (wine and cake depending on the translation). 
    In the Grimms' version at least, she had the order from her mother to stay strictly on the path.
    A mean wolf wants to eat the girl and the food in the basket. He secretly stalks her 
    behind trees, bushes, shrubs, and patches of little and tall grass. 
    He approaches Little Red Riding Hood and she naïvely tells him where she is going. 
    He suggests that the girl pick some flowers; which she does. In the meantime; 
    he goes to the grandmother's house and gains entry by pretending to be the girl. 
    He swallows the grandmother whole (in some stories, he locks her in the closet) 
    and waits for the girl, disguised as the grandma. 

    """)
