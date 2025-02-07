import streamlit as st
from gtts import gTTS
import os

st.markdown("### Preview and practice English vowels.")
st.write("Get familiarized with the vowel symbols")

# Use HTML with inline CSS for font color on target vowel words
st.markdown("""
1. [i]: She <span style="color:blue">sees</span> three <span style="color:red">green</span> trees near the deep <span style="color:green">sea</span>.  

2. [ɪ]: It's <span style="color:red">pretty</span> <span style="color:blue">chilly</span> in the <span style="color:green">city</span> this winter.  

3. [e]: Let's <span style="color:blue">get</span> some <span style="color:red">fresh</span> <span style="color:green">bread</span> and celebrate.  

4. [æ]: Jack <span style="color:red">grabbed</span> a <span style="color:blue">snack</span> and sat on the <span style="color:green">back</span> deck.  

5. [ɑ]: <span style="color:blue">Mark</span> <span style="color:red">parked</span> his car in the dark <span style="color:green">barn</span>.  

6. [ʊ]: <span style="color:red">Good</span> cooks <span style="color:blue">look</span> for full <span style="color:green">wood</span> bookshelves.  

7. [u]: <span style="color:blue">Sue</span> uses a <span style="color:red">blue</span> spoon to scoop <span style="color:green">soup</span>.  

8. [ʌ]: A <span style="color:red">bunch</span> of us <span style="color:blue">must</span> discuss the <span style="color:green">subject</span>.  

9. [ɔ]: <span style="color:red">All</span> the small <span style="color:blue">laws</span> are for <span style="color:green">all</span>.  

10. [ə]: A <span style="color:blue">week</span> ago, the gentleman opened another <span style="color:red">sofa</span> shop.  

11. [eɪ]: They <span style="color:blue">made</span> their <span style="color:red">way</span> to the <span style="color:green">lake</span> today.  

12. [aɪ]: I <span style="color:red">like</span> <span style="color:blue">riding</span> my <span style="color:green">bike</span> by the lively riverside.  

13. [aʊ]: <span style="color:red">How</span> now brown <span style="color:blue">cow</span>.  

14. [ɔɪ]: The <span style="color:red">noisy</span> boys enjoyed the royal <span style="color:blue">oysters</span>.  

15. [oʊ]: <span style="color:red">Go</span> home <span style="color:blue">alone</span> and <span style="color:green">phone</span> Joan.  

16. [ɝ]: The <span style="color:red">nurse</span> works <span style="color:blue">first</span> on Thursday.  

17. [ɚ]: Anna's <span style="color:red">umbrella</span> covers her <span style="color:blue">brother</span> in the summer <span style="color:green">weather</span>.  
""", unsafe_allow_html=True)


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
