import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pytz
import io

# --- 1. 시간대 및 페이지 설정 ---
KST = pytz.timezone('Asia/Seoul')
st.set_page_config(page_title="Check Yourself: [æ] Vowel", page_icon="🎱", layout="centered")

# --- 2. PDF 생성 로직 (수직 높이 최적화) ---
class PDF(FPDF):
    def header(self):
        self.set_fill_color(51, 102, 153) # Navy Blue
        self.rect(0, 0, 210, 20, 'F') # 수직 높이 20mm
        self.set_font('Arial', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.set_y(0)
        self.cell(0, 20, 'Lesson 4 Check Yourself: [ae] Vowel Discrimination', 0, 1, 'C')
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
    
    # 학생 정보 섹션
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Student ID/Name: {name}", 0, 1)
    
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, f"Exercise Started: {start_t} (KST)", 0, 1)
    pdf.cell(0, 7, f"Exercise Submitted: {end_t} (KST)", 0, 1)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 7, f"Actual Duration: {duration_str}", 0, 1)
    
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Final Score: {score} / {total}", 0, 1)
    pdf.ln(5)
    
    # 결과 테이블
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

# --- 3. 세션 상태 관리 ---
if 'exercise_started' not in st.session_state:
    st.session_state.exercise_started = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# 리셋 기능 (사이드바)
if st.sidebar.button("🔄 Reset Exercise"):
    st.session_state.exercise_started = False
    st.session_state.start_time = None
    st.session_state.user_name = ""
    st.rerun()

# --- 4. 메인 UI 구성 ---
tab1, tab2 = st.tabs(["🎱 Check Yourself", "🎾 Read-aloud"])

with tab1:
    st.markdown("### 🎧 Listening Quiz: Identify [æ] Vowel")
    st.caption("Workbook page 34")

    if not st.session_state.exercise_started:
        # --- PHASE 1: IDENTIFICATION ---
        st.subheader("📋 Student Identification")
        name_input = st.text_input("Enter your name or student ID:", placeholder="e.g., Hong Gil-dong (20251234)", value=st.session_state.user_name)
        
        st.divider()
        st.write("#### Task Instructions")
        st.write("Listen to the sequence of three words. Choose the **one** word that contains the **[æ]** vowel.")
        
        st.info("""
        **🐤 Example**
        - You hear: *1. add, 2. Ed, 3. odd*
        - You choose: **1**
        """)
        
        if st.button("▶️ Start Exercise"):
            if not name_input.strip():
                st.warning("⚠️ Please enter your ID/Name to begin.")
            else:
                st.session_state.user_name = name_input
                st.session_state.exercise_started = True
                st.session_state.start_time = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
                st.rerun()
    else:
        # --- PHASE 2: ACTIVE QUIZ ---
        st.write(f"**Student:** {st.session_state.user_name}")
        
        # Audio Player with Autoplay
        audio_url = "https://raw.githubusercontent.com/MK316/Engpro-Class-Listening/main/audio/L04A.wav"
        st.audio(audio_url, format='audio/wav', autoplay=True)
        
        st.divider()
        
        correct_answers = {"1": "1", "2": "3", "3": "1", "4": "2", "5": "3", "6":"1","7":"3","8":"2","9":"1","10":"2"}
        user_answers = {}

        # Questions Grid
        for i in range(1, 11):
            key = str(i)
            user_answers[key] = st.radio(f"Question {i}", ["1", "2", "3"], key=f"quiz_ae_{i}", horizontal=True)

        st.divider()

        if st.button("Finish & Generate PDF Report"):
            end_time = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
            
            # 점수 계산 및 리포트 데이터 생성
            score = 0
            report_data = []
            for i in range(1, 11):
                key = str(i)
                u_ans = user_answers[key]
                c_ans = correct_answers[key]
                is_right = (u_ans == c_ans)
                if is_right: score += 1
                report_data.append((i, u_ans, c_ans, is_right))
            
            st.success(f"Final Score: {score}/10")
            
            # PDF 생성
            pdf_bytes = create_pdf(st.session_state.user_name, score, 10, report_data, st.session_state.start_time, end_time)
            
            st.download_button(
                label="📥 Download My PDF Report",
                data=pdf_bytes,
                file_name=f"Check_ae_Vowel_{st.session_state.user_name}.pdf",
                mime="application/pdf"
            )

with tab2:
    st.caption("No reading for now")
    st.write("Content will be updated soon.")
