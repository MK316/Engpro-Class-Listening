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
        self.rect(0, 0, 210, 20, 'F') 
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
    pdf.set_top_margin(30)
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
    st.write("Listen to the three words. Select the **one** word that is different.")
    st.info("""
    **[Practice Example]**
    - Hear: *1. mitt, 2. meat, 3. meat*
    - Correct: **1**
    """)

# --- 4. Session State Management ---
if 'exercise_started' not in st.session_state:
    st.session_state.exercise_started = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# Simple reset in sidebar for testing
if st.sidebar.button("🔄 Reset Exercise"):
    st.session_state.exercise_started = False
    st.session_state.start_time = None
    st.session_state.user_name = ""
    st.rerun()

st.title("🎱 Exercise A")

# --- 5. App Logic Flow ---
if not st.session_state.exercise_started:
    # --- PHASE 1: IDENTIFICATION & START ---
    st.subheader("📋 Student Identification")
    name_input = st.text_input("Please enter your full name to begin:", value=st.session_state.user_name)
    
    st.divider()
    display_instructions()
    
    if st.button("▶️ Start Exercise"):
        if not name_input.strip():
            st.warning("⚠️ Please enter your name before starting.")
        else:
            st.session_state.user_name = name_input
            st.session_state.exercise_started = True
            st.session_state.start_time = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
            st.rerun()
else:
    # --- PHASE 2: AUDIO & QUESTIONS ---
    # Show name at the top so they know they are logged in
    st.write(f"**Student:** {st.session_state.user_name}")
    display_instructions()
    
    audio_url = 'https://raw.githubusercontent.com/MK316/Engpro-Class-Listening/main/audio/L01A.wav'
    st.audio(audio_url, format='audio/wav', autoplay=True)

    st.divider()
    
    correct_answers = {1: 1, 2: 3, 3: 2, 4: 3, 5: 1, 6: 1, 7: 2, 8: 1, 9: 2, 10: 1}
    answers = {}
    
    for i in range(1, 11):
        answers[i] = st.radio(f"Question {i}", ('1', '2', '3'), key=f'ex_a_q{i}', horizontal=True)

    if st.button('Finish & Generate PDF'):
        end_time = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
        score = sum(1 for q, c in correct_answers.items() if int(answers[q]) == c)
        
        report_data = []
        for q, c_ans in correct_answers.items():
            report_data.append((q, int(answers[q]), c_ans, int(answers[q]) == c_ans))
            
        st.success(f"Final Score: {score}/10")
        
        pdf_bytes = create_pdf(st.session_state.user_name, score, 10, report_data, st.session_state.start_time, end_time)
        
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_bytes,
            file_name=f"ExerciseA_{st.session_state.user_name}.pdf",
            mime="application/pdf"
        )
