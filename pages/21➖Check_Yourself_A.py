import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pytz
import io

# --- 1. Timezone Configuration ---
KST = pytz.timezone('Asia/Seoul')
st.set_page_config(page_title="Listening Exercise A", page_icon="🎱")

# --- 2. PDF Generation Logic ---
class PDF(FPDF):
    def header(self):
        self.set_fill_color(51, 102, 153) 
        self.rect(0, 0, 210, 20, 'F') # Shorter vertical height

        self.set_font('Arial', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.set_y(0)
        self.cell(0, 20, 'Exercise A: Listening Discrimination Report', 0, 1, 'C')
        self.ln(5)

def create_pdf(name, score, total, results, start_t, end_t):
    fmt = "%Y-%m-%d %H:%M:%S"
    start_dt = datetime.strptime(start_t, fmt)
    end_dt = datetime.strptime(end_t, fmt)
    duration = end_dt - start_dt
    
    total_seconds = int(duration.total_seconds())
    mins, secs = divmod(total_seconds, 60)
    duration_str = f"{mins}m {secs}s"

    pdf = PDF()
    pdf.set_top_margin(30) # Space for metadata below the blue box
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Student Name: {name}", 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, f"Exercise Started: {start_t} (KST)", 0, 1)
    pdf.cell(0, 7, f"Exercise Submitted: {end_t} (KST)", 0, 1)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 7, f"Actual Duration: {duration_str}", 0, 1)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Final Score: {score} / {total}", 0, 1)
    pdf.ln(5)
    
    # Table Results
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(30, 10, 'Question', 1, 0, 'C', True)
    pdf.cell(50, 10, 'Your Choice', 1, 0, 'C', True)
    pdf.cell(50, 10, 'Correct Answer', 1, 0, 'C', True)
    pdf.cell(40, 10, 'Result', 1, 1, 'C', True)
    
    pdf.set_font('Arial', '', 10)
    for q_num, user_ans, correct_ans, is_correct in results:
        pdf.cell(30, 10, f"Q{q_num}", 1, 0, 'C')
        pdf.cell(50, 10, str(user_ans), 1, 0, 'C')
        pdf.cell(50, 10, str(correct_ans), 1, 0, 'C')
        if is_correct:
            pdf.set_text_color(0, 128, 0)
            pdf.cell(40, 10, 'Correct', 1, 1, 'C')
        else:
            pdf.set_text_color(200, 0, 0)
            pdf.cell(40, 10, 'Incorrect', 1, 1, 'C')
        pdf.set_text_color(0, 0, 0)

    return pdf.output(dest='S').encode('latin-1')

# --- 3. Shared Instruction Component ---
def display_instructions():
    st.markdown("#### 🎧 Task Instructions")
    st.write("Listen to the three words provided in the audio. Select the **one** word that is different from the others.")
    st.info("""
    **[Practice Example]**
    - You will hear: *1. mitt, 2. meat, 3. meat*
    - The correct choice is: **1** (mitt)
    """)

# --- 4. Session State ---
if 'exercise_started' not in st.session_state:
    st.session_state.exercise_started = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# --- 5. UI Layout ---
st.sidebar.header("📋 Student Identification")
user_name = st.sidebar.text_input("Full Name", placeholder="Enter your name...")

st.title("🎱 Exercise A: Discrimination Task")
st.caption("Workbook page 26")

# --- 6. Conditional Logic (Pre-Start vs. Active) ---
if not st.session_state.exercise_started:
    # PRE-START PHASE: Display instructions as scaffolding
    display_instructions()
    st.warning("Make sure your volume is up. The timer starts and the audio plays as soon as you click the button below.")
    
    if st.button("▶️ Start Exercise"):
        st.session_state.exercise_started = True
        st.session_state.start_time = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
        st.rerun()

else:
    # ACTIVE EXERCISE PHASE
    # Display instructions again because the audio includes the example
    display_instructions()
    
    st.markdown("---")
    st.markdown("#### 🔊 Now Playing")
    audio_url = 'https://raw.githubusercontent.com/MK316/Engpro-Class-Listening/main/audio/L01A.wav'
    st.audio(audio_url, format='audio/wav', autoplay=True)

    st.markdown("---")
    
    # Quiz Data
    correct_answers = {1: 1, 2: 3, 3: 2, 4: 3, 5: 1, 6: 1, 7: 2, 8: 1, 9: 2, 10: 1}
    answers = {}
    
    # Grid-like layout for questions
    for i in range(1, 11):
        answers[i] = st.radio(f"Question {i}", ('1', '2', '3'), key=f'ex_a_q{i}', horizontal=True)

    st.markdown("---")

    if st.button('Finish & Generate PDF Report'):
        if not user_name.strip():
            st.error("⚠️ Please enter your name in the sidebar.")
        else:
            end_time = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
            
            score = 0
            report_data = []
            for q, c_ans in correct_answers.items():
                u_ans = int(answers[q])
                is_right = (u_ans == c_ans)
                if is_right: score += 1
                report_data.append((q, u_ans, c_ans, is_right))
                
            st.success(f"Score Submitted: {score}/10")
            
            pdf_bytes = create_pdf(user_name, score, 10, report_data, st.session_state.start_time, end_time)
            
            st.download_button(
                label="📥 Download My PDF Report",
                data=pdf_bytes,
                file_name=f"ExerciseA_{user_name}.pdf",
                mime="application/pdf"
            )
