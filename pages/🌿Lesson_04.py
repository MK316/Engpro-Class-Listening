import streamlit as st
from gtts import gTTS
import io
import datetime


# Create a tab bar with three tabs
tab1, tab2 = st.tabs(["🎱 Exercise A", "🎾 Read-aloud"])

with tab1:
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




with tab2:
    st.write("Read aloud - Little Red Riding Hood")
    st.image("https://raw.githubusercontent.com/MK316/Engpro-Class-Listening/main/images/Littleredridinghood.jpg")
    st.markdown("""
    The story revolves around a girl called Little Red Riding Hood, 
    after the red hooded cape or cloak she wears. The girl walks through the woods 
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
    red hooded cape or cloak she wears. The girl walks through the woods to
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
    after the red hooded cape or cloak she wears. The girl walks through the woods 
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


