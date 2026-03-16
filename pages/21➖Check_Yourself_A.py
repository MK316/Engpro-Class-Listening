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
        self.set_fill_color(51, 52, 153)
        self.rect(0, 0, 210, 35, 'F')
        self.set_font('Arial', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, 'Exercise A: Listening Discrimination Report', 0, 1, 'C')
        self.ln(5)

def create_pdf(name, score, total, results, start_t, end_t):
    # Calculate Duration
    fmt = "%Y-%m-%d %H:%M:%S"
    start_dt = datetime.strptime(start_t, fmt)
    end_dt = datetime.strptime(end_t, fmt)
    duration = end_dt - start_dt
    
    total_seconds = int(duration.total_seconds())
    mins, secs = divmod(total_seconds, 60)
    duration_str = f"{mins}m {secs}s"

    pdf = PDF()
    pdf.add_page()
    
    # Metadata
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Student Name: {name}", 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, f"Exercise Started (First Play): {start_t} (KST)", 0, 1)
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

# --- 3. Session State for Precise Timing ---
if 'exercise_started' not in st.session_state:
    st.session_state.exercise_started = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# --- 4. Sidebar & Identity ---
st.sidebar.header("📋 Student Identification")
user_name = st.sidebar.text_input("Full Name", placeholder="Enter your name...")

st.title("🎱 Exercise A: Discrimination Task")

# --- 5. Start Trigger Logic ---
if not st.session_state.exercise_started:
    st.info("Click the button below to reveal the audio and start the exercise timer.")
    if st.button("▶️ Start Exercise / Play Audio"):
        st.session_state.exercise_started = True
        st.session_state.start_time = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
        st.rerun()
else:
    # --- 6. Active Exercise UI ---
    st.markdown("#### 🎧 Listening Now")
    audio_url = 'https://raw.githubusercontent.com/MK316/Engpro-Class-Listening/main/audio/L01A.wav'
    st.audio(audio_url, format='audio/wav', autoplay=True) # Autoplay starts when button is clicked

    st.markdown("---")
    
    correct_answers = {1: 1, 2: 3, 3: 2, 4: 3, 5: 1, 6: 1, 7: 2, 8: 1, 9: 2, 10: 1}
    answers = {}
    for i in range(1, 11):
        answers[i] = st.radio(f"Question {i}", ('1', '2', '3'), key=f'ex_a_q{i}', horizontal=True)

    if st.button('Finish & Generate PDF Report'):
        if not user_name.strip():
            st.error("Please enter your name in the sidebar.")
        else:
            end_time = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
            
            score = 0
            report_data = []
            for q, c_ans in correct_answers.items():
                u_ans = int(answers[q])
                is_right = (u_ans == c_ans)
                if is_right: score += 1
                report_data.append((q, u_ans, c_ans, is_right))
                
            pdf_bytes = create_pdf(user_name, score, 10, report_data, st.session_state.start_time, end_time)
            
            st.download_button(
                label="📥 Download Your PDF Report",
                data=pdf_bytes,
                file_name=f"ExerciseA_{user_name}.pdf",
                mime="application/pdf"
            )
