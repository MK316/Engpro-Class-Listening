import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pytz

# --- 1. Timezone Setup (Seoul) ---
KST = pytz.timezone('Asia/Seoul')

# --- 2. PDF Generation Class ---
class PDF(FPDF):
    def header(self):
        self.set_fill_color(51, 102, 153) # Navy Blue
        self.rect(0, 0, 210, 35, 'F')
        self.set_font('Arial', 'B', 18)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, 'Exercise A: Listening Results (KST)', 0, 1, 'C')
        self.ln(5)

def create_pdf(name, score, total, results, start_t, end_t):
    pdf = PDF()
    pdf.add_page()
    
    # Header Info
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"Student Name: {name}", 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, f"Session Started: {start_t}", 0, 1)
    pdf.cell(0, 7, f"Session Ended: {end_t}", 0, 1)
    pdf.cell(0, 7, f"Final Score: {score} / {total}", 0, 1)
    pdf.ln(8)
    
    # Results Table Header
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(30, 10, 'Question', 1, 0, 'C', True)
    pdf.cell(50, 10, 'Your Choice', 1, 0, 'C', True)
    pdf.cell(50, 10, 'Correct Answer', 1, 0, 'C', True)
    pdf.cell(40, 10, 'Result', 1, 1, 'C', True)
    
    # Table Content
    pdf.set_font('Arial', '', 10)
    for q_num, user_ans, correct_ans, is_correct in results:
        pdf.cell(30, 10, f"Q{q_num}", 1, 0, 'C')
        pdf.cell(50, 10, str(user_ans), 1, 0, 'C')
        pdf.cell(50, 10, str(correct_ans), 1, 0, 'C')
        if is_correct:
            pdf.set_text_color(0, 128, 0) # Green
            pdf.cell(40, 10, 'Correct', 1, 1, 'C')
        else:
            pdf.set_text_color(200, 0, 0) # Red
            pdf.cell(40, 10, 'Incorrect', 1, 1, 'C')
        pdf.set_text_color(0, 0, 0)

    return pdf.output(dest='S').encode('latin-1')

# --- 3. Streamlit Page Config & Session State ---
st.set_page_config(page_title="Exercise A", layout="centered")

if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")

# --- 4. Sidebar & Instructions ---
st.sidebar.header("📋 Student ID")
user_name = st.sidebar.text_input("Full Name", placeholder="Type your name...")

st.title("🎱 Exercise A: Discrimination")
st.caption("Workbook page 26")
st.markdown("#### 🎧 Task Instructions")
st.write("Identify the word that sounds different from the others.")

st.info("""
**[Example]** 1. Hear: 1. mitt, 2. meat, 3. meat  
2. Select: **1**
""")

# --- 5. Audio Player (RE-ADDED) ---
# Using the stable 'raw' URL format
audio_url = 'https://raw.githubusercontent.com/MK316/Engpro-Class-Listening/main/audio/L01A.wav'
st.audio(audio_url, format='audio/wav')

st.markdown("---")

# --- 6. Quiz Questions ---
correct_answers = {1: 1, 2: 3, 3: 2, 4: 3, 5: 1, 6: 1, 7: 2, 8: 1, 9: 2, 10: 1}
answers = {}

# Use columns or a container to keep radio buttons neat
for i in range(1, 11):
    answers[i] = st.radio(f"Question {i}", ('1', '2', '3'), key=f'q{i}', horizontal=True)

# --- 7. Submission & PDF Generation ---
if st.button('Finish and Generate PDF Report'):
    if not user_name:
        st.warning("Please enter your name in the sidebar to generate the report.")
    else:
        end_time = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
        
        report_data = []
        score = 0
        for q, c_ans in correct_answers.items():
            u_ans = int(answers[q])
            is_right = (u_ans == c_ans)
            if is_right: score += 1
            report_data.append((q, u_ans, c_ans, is_right))
            
        st.success(f"Score Submitted: {score}/10")
        
        pdf_bytes = create_pdf(
            user_name, 
            score, 
            10, 
            report_data, 
            st.session_state.start_time, 
            end_time
        )
        
        st.download_button(
            label="📥 Download My PDF Report",
            data=pdf_bytes,
            file_name=f"ExerciseA_Report_{user_name}.pdf",
            mime="application/pdf"
        )
