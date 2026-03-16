import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pytz
import io

# --- 1. 시간대 및 페이지 설정 ---
KST = pytz.timezone('Asia/Seoul')
st.set_page_config(page_title="Check Yourself B", page_icon="🎱", layout="centered")

# --- 2. PDF 생성 로직 (Vertical Header Fix 반영) ---
class PDF(FPDF):
    def header(self):
        self.set_fill_color(51, 102, 153) # Navy Blue
        self.rect(0, 0, 210, 20, 'F') # 가로 전체, 세로 20mm
        self.set_font('Arial', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.set_y(0)
        self.cell(0, 20, 'Exercise B: Word Identification Report', 0, 1, 'C')
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
    
    # 학생 정보
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
    
    # 결과 테이블 헤더
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(30, 10, 'Question', 1, 0, 'C', True)
    pdf.cell(50, 10, 'Your Choice', 1, 0, 'C', True)
    pdf.cell(50, 10, 'Correct Answer', 1, 0, 'C', True)
    pdf.cell(40, 10, 'Result', 1, 1, 'C', True)
    
    # 결과 테이블 내용
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

# --- 3. 공통 안내 문구 함수 ---
def display_instructions():
    st.markdown("#### 🎧 Task Instructions")
    st.write("You will hear one word from each pair. Listen carefully and circle the word that you hear.")
    st.info("""
    **[Practice Example]**
    - Pair: *mitt / meat*
    - If you hear 'mitt', choose: **mitt**
    """)

# --- 4. 세션 상태 관리 ---
if 'exercise_started' not in st.session_state:
    st.session_state.exercise_started = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# 테스트용 리셋 버튼 (사이드바)
if st.sidebar.button("🔄 Reset Exercise"):
    st.session_state.exercise_started = False
    st.session_state.start_time = None
    st.session_state.user_name = ""
    st.rerun()

st.markdown("### 🎱 Check Yourself B: Word Identification")

# --- 5. 앱 로직 흐름 ---
if not st.session_state.exercise_started:
    # 단계 1: 이름 입력 및 시작 전 안내
    st.subheader("📋 Your name")
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
    # 단계 2: 오디오 재생 및 문제 풀이
    st.write(f"**Student:** {st.session_state.user_name}")
    display_instructions()
    
    st.divider()
    st.markdown("#### 🔊 Now Playing")
    # GitHub Raw URL 사용
    audio_url = 'https://raw.githubusercontent.com/MK316/Engpro-Class-Listening/main/audio/L01B.wav'
    st.audio(audio_url, format='audio/wav', autoplay=True)

    st.divider()
    
    # 문제 데이터
    word_pairs = {
        1: ("field", "filled"), 2: ("bean", "bin"), 3: ("neat", "knit"),
        4: ("deal", "dill"), 5: ("beat", "bit"), 6: ("team", "Tim"),
        7: ("sleep", "slip"), 8: ("green", "grin"), 9: ("heel", "hill"), 10: ("week", "wick")
    }
    correct_answers = {
        1: "field", 2: "bean", 3: "knit", 4: "dill", 5: "bit",
        6: "team", 7: "slip", 8: "green", 9: "hill", 10: "wick"
    }
    
    answers = {}
    for i in word_pairs:
        answers[i] = st.radio(
            f"Question {i}: Select the word you hear",
            word_pairs[i],
            key=f'ex_b_q{i}',
            horizontal=True
        )

    st.divider()

    if st.button('Finish & Generate PDF Report'):
        end_time = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
        
        # 결과 계산
        score = 0
        report_data = []
        for i in word_pairs:
            u_ans = answers[i]
            c_ans = correct_answers[i]
            is_right = (u_ans == c_ans)
            if is_right: score += 1
            report_data.append((i, u_ans, c_ans, is_right))
            
        st.success(f"Exercise Finished! Your Score: {score}/{len(word_pairs)}")
        
        # PDF 생성 및 다운로드 버튼
        pdf_bytes = create_pdf(st.session_state.user_name, score, len(word_pairs), report_data, st.session_state.start_time, end_time)
        
        st.download_button(
            label="📥 Download My PDF Report",
            data=pdf_bytes,
            file_name=f"ExerciseB_{st.session_state.user_name}.pdf",
            mime="application/pdf"
        )
