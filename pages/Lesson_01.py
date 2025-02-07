import streamlit as st
from gtts import gTTS
import os

st.markdown("### Preview and practice English vowels.")
st.write("Get familiarized with the vowel symbols")

st.markdown("""
[i]: 1. She sees three green trees near the deep sea.  
[ɪ]: 2. It's pretty chilly in the city this winter.  
[e]: 3. Let's get some fresh bread and celebrate.  
[æ]: 4. Jack grabbed a snack and sat on the back deck.  
[ɑ]: 5. Mark parked his car in the dark barn.  
[ʊ]: 6. Good cooks look for full wood bookshelves.  
[u]: 7. Sue uses a blue spoon to scoop soup.  
[ʌ]: 8. A bunch of us must discuss the subject.  
[ɔ]: 9. All the small laws are for all.  
[ə]: 10. A week ago, the gentleman opened another sofa shop.  
[eɪ]: 11. They made their way to the lake today.  
[aɪ]: 12. I like riding my bike by the lively riverside.  
[aʊ]: 13. How now brown cow.  
[ɔɪ]: 14. The noisy boys enjoyed the royal oysters.  
[oʊ]: 15. Go home alone and phone Joan.  
[ɝ]: 16. The nurse works first on Thursday.  
[ɚ]: 17. Anna's umbrella covers her brother in the summer weather.  
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
