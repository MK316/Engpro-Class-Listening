
import streamlit as st
from gtts import gTTS
import io
import datetime


# Create a tab bar with three tabs
tab1, tab2 = st.tabs(["🎱 Exercise A", "🎾 Read-aloud"])

with tab1:
    st.markdown("### 🎧 Animal names")


with tab2:
    st.write("Read aloud - US Constitution")
    # st.image("https://raw.githubusercontent.com/MK316/Engpro-Class-Listening/main/images/constitution.jpg")
    st.markdown("""
    The Constitution of the United States is the supreme law of the United States of America. The Constitution, originally comprising seven articles, delineates the national frame of government. Its first three articles entrench the doctrine of the separation of powers, whereby the federal government is divided into three branches: the legislative, consisting of the bicameral Congress; the executive, consisting of the President; and the judicial, consisting of the Supreme Court and other federal courts. Articles Four, Five and Six entrench concepts of federalism, describing the rights and responsibilities of state governments and of the states in relationship to the federal government. Article Seven establishes the procedure subsequently used by the thirteen States to ratify it.
    """)
  
    st.markdown("#### 🍎 1. Generate Audio with Different Speeds")
    st.write("Select the speed and generate the audio for the provided text.")

    # Text to be converted to speech
    text = """The Constitution of the United States is the supreme law of the United States of America. The Constitution, originally comprising seven articles, delineates the national frame of government. Its first three articles entrench the doctrine of the separation of powers, whereby the federal government is divided into three branches: the legislative, consisting of the bicameral Congress; the executive, consisting of the President; and the judicial, consisting of the Supreme Court and other federal courts. Articles Four, Five and Six entrench concepts of federalism, describing the rights and responsibilities of state governments and of the states in relationship to the federal government. Article Seven establishes the procedure subsequently used by the thirteen States to ratify it."""

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
        'Male': 'https://github.com/MK316/Engpro-Class/raw/main/audio/constitution-M.mp3',
        'Female': 'https://github.com/MK316/Engpro-Class/raw/main/audio/constitution-F.mp3',
    }

    selected_voice = st.selectbox("Select Voice", options=['Male', 'Female'], key='selected_voice')
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
    
    st.write("Read aloud - US Constitution ")
    st.markdown("""
    The Constitution of the United States is the supreme law of the United States of America.  
    The Constitution, originally comprising seven articles, delineates the national frame of government.  
    Its first three articles entrench the doctrine of the separation of powers, whereby the federal government  
    is divided into three branches: the legislative, consisting of the bicameral Congress; the executive,  
    consisting of the President; and the judicial, consisting of the Supreme Court and other federal courts.  
    Articles Four, Five and Six entrench concepts of federalism, describing the rights and responsibilities  
    of state governments and of the states in relationship to the federal government. Article Seven establishes  
    the procedure subsequently used by the thirteen States to ratify it.  
    """)
