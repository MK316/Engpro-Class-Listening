import streamlit as st
from fpdf import FPDF
from datetime import datetime
import base64

# --- PDF Generation Function ---
class PDF(FPDF):
    def header(self):
        self.set_fill_color(200, 220, 255)
        self.rect(0, 0, 210, 40, 'F')
        self.set_font('Arial', 'B', 16)
        self.set_text_color(33, 37, 41)
        self.cell(0, 20, 'Exercise A: Listening Report', 0, 1, 'C')
        self.ln(5)

def create_pdf(name, score, total, results, timestamp):
    pdf = PDF()
    pdf.add_page()
    
    # User Info Section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Name: {name}", 0, 1)
    pdf.cell(0, 10, f"Date/Time: {timestamp}", 0, 1)
    pdf.cell(0, 10, f"Final Score: {score} / {total}", 0, 1)
    pdf.ln(10)
    
    # Results Table Header
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(30, 10, 'Question', 1, 0, 'C', True)
    pdf.cell(40, 10, 'Your Answer', 1, 0, 'C', True)
    pdf.cell(40, 10, 'Correct Answer', 1, 0, 'C', True)
    pdf.cell(30, 10, 'Result', 1, 1, 'C', True)
    
    # Results Table Rows
    pdf.set_font('Arial', '', 10)
    for q_num, user_ans, correct_ans, is_correct in results:
        pdf.cell(30, 10, f"Q{q_num}", 1, 0, 'C')
        pdf.cell(40, 10, str(user_ans), 1, 0, 'C')
        pdf.cell(40, 10, str(correct_ans), 1, 0, 'C')
        
        if is_correct:
            pdf.set_text_color(0, 128, 0)
            pdf.cell(30, 10, 'Correct', 1, 1, 'C')
        else:
            pdf.set_text_color(255, 0, 0)
            pdf.cell(30, 10, 'Incorrect', 1, 1, 'C')
        pdf.set_text_color(0, 0, 0)

    return pdf.output(dest='S').encode('latin-1')

# --- Streamlit UI ---
st.set_page_config(page_title="Exercise A Report", page_icon="🎱")

# Sidebar for User Info
st.sidebar.header("User Information")
user_name = st.sidebar.text_input("Enter your full name:", placeholder="John Doe")

st.caption("Workbook page 26")
st.markdown("#### 🎧 Task Instructions")
st.write("Identify the word that sounds different from the other two.")

st.info("""
**[Example]** You hear: 1. mitt, 2. meat, 3. meat  
Correct Answer: **1 (mitt)**
""")

# Quiz Data
num_questions = 10
correct_answers = {
    1: 1, 2: 3, 3: 2, 4: 3, 5: 1,
    6: 1, 7: 2, 8: 1, 9: 2, 10: 1
}

audio_url = 'https://raw.githubusercontent.com/MK316/Engpro-Class-Listening/main/audio/L01A.wav'
st.audio(audio_url, format='audio/wav')

st.markdown("---")

answers = {}
for i in range(1, num_questions + 1):
    answers[i] = st.radio(f"Question {i}", ('1', '2', '3'), key=f'q_{i}', horizontal=True)

if st.button('Submit and Generate Report'):
    if not user_name:
        st.error("Please enter your name in the sidebar (left side >>) before submitting.")
    else:
        correct_count = 0
        report_data = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for q in range(1, num_questions + 1):
            u_ans = int(answers[q])
            c_ans = correct_answers[q]
            is_right = u_ans == c_ans
            if is_right:
                correct_count += 1
            report_data.append((q, u_ans, c_ans, is_right))
        
        st.success(f"Done! Your score: {correct_count}/{num_questions}")
        
        # PDF Generation
        pdf_bytes = create_pdf(user_name, correct_count, num_questions, report_data, timestamp)
        
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_bytes,
            file_name=f"Report_{user_name}_{datetime.now().strftime('%m%d')}.pdf",
            mime="application/pdf"
        )
