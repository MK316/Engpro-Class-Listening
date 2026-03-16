import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pytz
from gtts import gTTS
import os

# --- 1. 시간대 및 페이지 설정 ---
KST = pytz.timezone('Asia/Seoul')
st.set_page_config(page_title="Check Yourself A", page_icon="🎱", layout="centered")

# --- 2. PDF 생성 로직 (수직 헤더 최적화) ---
class PDF(FPDF):
    def header(self):
        self.set_fill_color(51, 102, 153) # Navy Blue
        self.rect(0, 0, 210, 20, 'F') # 세로 높이 20mm로 축소
        self.set_font('Arial', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.set_y(0)
        self.cell(0, 20, 'Check Yourself A: Listening Report', 0, 1, 'C')
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
    pdf.set_top_margin(30) # 헤더 박스와 텍스트 사이 간격 확보
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Student Name: {name}", 0, 1)
    
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, f"Started: {start_t} (KST)", 0, 1)
    pdf.cell(0, 7, f"Submitted: {end_t} (KST)", 0, 1)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 7, f"Total Duration: {duration_str}", 0, 1)
    
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

# --- 4. 메인 화면 구성 (탭) ---
tab1, tab2 = st.tabs(["🎱 Check Yourself A", "🎾 Read-aloud"])

with tab1:
    st.title("Check Yourself A")
    st.caption("Workbook page 31")
    
    if not st.session_state.exercise_started:
        st.subheader("📋 Your name")
        name_input = st.text_input("Please enter your full name to begin:", value=st.session_state.user_name)
        
        st.divider()
        st.markdown("#### 🎧 Task Instructions")
        st.write("Listen to the audio and identify the one word that sounds different from the others.")
        st.info("**Example:** Hear '1. fool, 2. fool, 3. full' -> Choose **3**.")
        
        if st.button("▶️ Start Exercise"):
            if not name_input.strip():
                st.warning("⚠️ Please enter your name first.")
            else:
                st.session_state.user_name = name_input
                st.session_state.exercise_started = True
                st.session_state.start_time = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
                st.rerun()
    else:
        st.write(f"**Student:** {st.session_state.user_name}")
        audio_file = 'https://raw.githubusercontent.com/MK316/Engpro-Class-Listening/main/audio/L03U.wav'
        st.audio(audio_file, format='audio/wav', autoplay=True)

        st.divider()
        correct_answers = {1: 3, 2: 2, 3: 2, 4: 1, 5: 3, 6: 3, 7: 1, 8: 3, 9: 1, 10: 1}
        answers = {}
        
        for i in range(1, 11):
            answers[i] = st.radio(f"Question {i}", ('1', '2', '3'), key=f'cy_a_q{i}', horizontal=True)

        if st.button('Finish & Generate PDF'):
            end_time = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
            report_data = []
            score = 0
            for q, c_ans in correct_answers.items():
                u_ans = int(answers[q])
                is_right = (u_ans == c_ans)
                if is_right: score += 1
                report_data.append((q, u_ans, c_ans, is_right))
                
            pdf_bytes = create_pdf(st.session_state.user_name, score, 10, report_data, st.session_state.start_time, end_time)
            st.success(f"Score: {score}/10")
            st.download_button("📥 Download PDF Report", pdf_bytes, f"CheckA_{st.session_state.user_name}.pdf", "application/pdf")

with tab2:
    st.header("Read-aloud")
    st.image("https://raw.githubusercontent.com/MK316/Engpro-Class-Listening/main/images/Littleredridinghood.jpg")
    
    text = """Little Red Riding Hood. The story revolves around a girl called Little Red Riding Hood, after the
    red hooded cape or cloak she wears. The girl walks through the woods to deliver food to her sickly grandmother..."""
    
    st.markdown(text)
    
    st.subheader("🍎 1. Generate Audio (gTTS)")
    speed = st.radio("Speed:", ('Normal', 'Slow', 'Slower'), horizontal=True)
    if st.button('Generate Audio'):
        tts = gTTS(text, lang='en', slow=(speed != 'Normal'))
        tts.save("audio.mp3")
        st.audio("audio.mp3")

    st.divider()
    st.subheader("🍎 2. Practice with Voices")
    # GitHub Raw 링크로 수정
    audio_urls = {
        'Male': 'https://raw.githubusercontent.com/MK316/Engpro-Class/main/audio/little-red-riding-hood-M.mp3',
        'Female': 'https://raw.githubusercontent.com/MK316/Engpro-Class/main/audio/little-red-riding-hood-F.mp3'
    }
    voice = st.selectbox("Select Voice", options=['Female', 'Male'])
    if st.button("Play Voice"):
        st.audio(audio_urls[voice])
