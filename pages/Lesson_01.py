import streamlit as st
from gtts import gTTS
import os

st.markdown("### Preview and practice English vowels.")
st.write("Get familiarized with the vowel symbols")

st.markdown("""
1. [i]: She sees three green trees near the deep sea.  

2. [ɪ]: It's pretty chilly in the city this winter.  

3. [e]: Let's get some fresh bread and celebrate.  
4. [æ]: Jack grabbed a snack and sat on the back deck.  
5. [ɑ]: Mark parked his car in the dark barn.  
6. [ʊ]: Good cooks look for full wood bookshelves.  
7. [u]: Sue uses a blue spoon to scoop soup.  
8. [ʌ]: A bunch of us must discuss the subject.  
9. [ɔ]: All the small laws are for all.  
10. [ə]: A week ago, the gentleman opened another sofa shop.  
11. [eɪ]: They made their way to the lake today.  
12. [aɪ]: I like riding my bike by the lively riverside.  
13. [aʊ]: How now brown cow.  
14. [ɔɪ]: The noisy boys enjoyed the royal oysters.  
15. [oʊ]: Go home alone and phone Joan.  
16. [ɝ]: The nurse works first on Thursday.  
17. [ɚ]: Anna's umbrella covers her brother in the summer weather.  
""")


# Define sentences
sentences = {
    "[i]": "Number one. She sees three green trees near the deep sea.",
    "[ɪ]": "Number two. It's pretty chilly in the city this winter.",
    "[e]": "Number three. Let's get some fresh bread and celebrate.",
    "[æ]": "Number four. Jack grabbed a snack and sat on the back deck.",
    "[ɑ]": "Number five. Mark parked his car in the dark barn.",
    "[ʊ]": "Number six. Good cooks look for full wood bookshelves.",
    "[u]": "Number seven. Sue uses a blue spoon to scoop soup.",
    "[ʌ]": "Number eight. A bunch of us must discuss the subject.",
    "[ɔ]": "Number nine. All the small laws are for all.",
    "[ə]": "Number ten. A week ago, the gentleman opened another sofa shop.",
    "[eɪ]": "Number eleven. They made their way to the lake today.",
    "[aɪ]": "Number twelve. I like riding my bike by the lively riverside.",
    "[aʊ]": "Number thirteen. How now brown cow.",
    "[ɔɪ]": "Number fourteen. The noisy boys enjoyed the royal oysters.",
    "[oʊ]": "Number fifteen. Go home alone and phone Joan.",
    "[ɝ]": "Number sixteen. The nurse works first on Thursday.",
    "[ɚ]": "Number seventeen. Anna's umbrella covers her brother in the summer weather.",
}

# Speeds to generate (normal, slow, slower)
speeds = {
    "Normal": False,  # Default speed
    "Slow": True,     # Slower than normal
    "Slower": True    # Uses gTTS's built-in 'slow' mode (same as Slow, but we differentiate in filenames)
}

# Directory to save audio files
output_dir = "generated_audio"
os.makedirs(output_dir, exist_ok=True)

# Generate audio for each sentence in different speeds
for vowel, sentence in sentences.items():
    for speed_name, slow_mode in speeds.items():
        tts = gTTS(text=sentence, lang='en', slow=slow_mode)
        filename = f"{output_dir}/{vowel.strip('[]')}_{speed_name}.mp3"
        tts.save(filename)
        print(f"Generated: {filename}")
