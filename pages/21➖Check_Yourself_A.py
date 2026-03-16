import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pytz

# --- Timezone Setup ---
KST = pytz.timezone('Asia/Seoul')

class PDF(FPDF):
    def header(self):
        self.set_fill_color(51, 102, 153)
        self.rect(0, 0, 210, 35, 'F')
        self.set_font('Arial', 'B', 18)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, 'Exercise A: Listening Results (KST)', 0, 1, 'C')
        self.ln(5)

def create_pdf(name, score, total, results, start_t, end_t):
    pdf = PDF()
    pdf.add_page()
    
    # User and Time Information
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"Student Name: {name}", 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, f"Session Started: {start_t}", 0, 1)
    pdf.cell(0, 7, f"Session Ended: {end_t}", 0, 1)
    pdf.cell(0, 7, f"Final Score: {score} / {total}", 0, 1)
    pdf.ln(8)
    
    # Table Results... (Same as previous table code)
    pdf.set_fill_color(220, 220, 220)
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

# --- Main App ---
if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")

st.sidebar.header("📋 Student ID")
user_name = st.sidebar.text_input("Full Name")

st.title("🎱 Exercise A: Discrimination")

# (Audio and Quiz Logic here...)
correct_answers = {1: 1, 2: 3, 3: 2, 4: 3, 5: 1, 6: 1, 7: 2, 8: 1, 9: 2, 10: 1}
answers = {}
for i in range(1, 11):
    answers[i] = st.radio(f"Question {i}", ('1', '2', '3'), key=f'q{i}', horizontal=True)

if st.button('Finish and Generate PDF'):
    if not user_name:
        st.warning("Please enter your name.")
    else:
        # Generate final timestamp in Seoul time
        end_time = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate results...
        report_data = []
        score = 0
        for q, c_ans in correct_answers.items():
            u_ans = int(answers[q])
            is_right = (u_ans == c_ans)
            if is_right: score += 1
            report_data.append((q, u_ans, c_ans, is_right))
            
        pdf_bytes = create_pdf(user_name, score, 10, report_data, st.session_state.start_time, end_time)
        
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_bytes,
            file_name=f"Report_ExerciseA_{user_name}.pdf",
            mime="application/pdf"
        )
