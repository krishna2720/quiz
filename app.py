import streamlit as st
import pandas as pd
from utils.data_loader import load_and_validate_csv
from utils.quiz_engine import check_answer, calculate_score

st.set_page_config(
    page_title="GenAI Vision Quiz App", 
    page_icon="👁️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Glassmorphic & Modern Dark CSS Injection
st.markdown("""
<style>
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%);
        color: #F8FAFC;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Question Container Card */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }

    /* Primary Buttons Styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(99, 102, 241, 0.6) !important;
    }

    /* Radio & Checkbox Container Styling */
    div[role="radiogroup"] > label, div[data-testid="stCheckbox"] > label {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 10px 16px;
        margin-bottom: 8px;
        transition: all 0.2s ease;
        width: 100%;
    }

    div[role="radiogroup"] > label:hover, div[data-testid="stCheckbox"] > label:hover {
        background: rgba(99, 102, 241, 0.15);
        border-color: #6366F1;
    }

    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #6366F1, #A855F7);
        border-radius: 10px;
    }

    /* Titles Header */
    .main-title {
        background: linear-gradient(135deg, #818CF8 0%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session States
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = {}

# Load Data
try:
    df = load_and_validate_csv("data/questions.csv")
except Exception as e:
    st.error(f"⚠️ Error loading question bank: {e}")
    st.info("Kripya check karein ki 'data/questions.csv' sahi folder location par hai.")
    st.stop()

# Main App Header
st.markdown('<h1 class="main-title">👁️ Generative AI for Computer Vision</h1>', unsafe_allow_html=True)
st.caption("1 Subject · 10 Quizzes · 100 MCQs (Foundations to VLMs & Diffusion)")

# Sidebar - Quiz Selector (Quiz 1 to Quiz 10)
available_quizzes = sorted(df['quiz_no'].unique())
selected_quiz = st.sidebar.selectbox(
    "🎯 Select Quiz Module", 
    available_quizzes, 
    format_func=lambda x: f"Quiz {x}"
)

quiz_df = df[df['quiz_no'] == selected_quiz].reset_index(drop=True)

# Main Title & Progress Tracking
st.subheader(f"📌 Quiz {selected_quiz} ({len(quiz_df)} Questions)")

overall_score, total_attempted = calculate_score(
    df, st.session_state.submitted, st.session_state.answers
)

st.progress(total_attempted / len(df) if len(df) > 0 else 0)

# Sidebar Score Metrics
st.sidebar.markdown("---")
st.sidebar.metric("📊 Total Score", f"{overall_score} / {total_attempted}")
if total_attempted > 0:
    accuracy = int((overall_score / total_attempted) * 100)
    st.sidebar.metric("⚡ Overall Accuracy", f"{accuracy}%")

# Render Questions
for idx, row in quiz_df.iterrows():
    q_key = f"q{selected_quiz}_qid{row['question_id']}"
    
    st.markdown(f"#### Q{idx + 1}. {row['question']}")
    
    options = {
        'A': row['option_a'],
        'B': row['option_b'],
        'C': row['option_c'],
        'D': row['option_d']
    }
    
    # Render Input Types
    if row['type'] == 'single':
        choice = st.radio(
            "Choose option:",
            options=list(options.keys()),
            format_func=lambda x: f"{x}) {options[x]}",
            key=f"radio_{q_key}",
            index=None
        )
        if choice:
            st.session_state.answers[q_key] = [choice]
            
    elif row['type'] == 'multiple':
        st.caption("*(Multiple correct options possible)*")
        selected_checks = []
        for opt_code, opt_val in options.items():
            if st.checkbox(f"{opt_code}) {opt_val}", key=f"chk_{q_key}_{opt_code}"):
                selected_checks.append(opt_code)
        st.session_state.answers[q_key] = selected_checks

    # Check Answer Action
    col_btn, _ = st.columns([1, 4])
    with col_btn:
        if st.button("Check Answer", key=f"btn_{q_key}"):
            st.session_state.submitted[q_key] = True

    # Feedback Cards
    if st.session_state.submitted.get(q_key, False):
        user_selection = set(st.session_state.answers.get(q_key, []))
        correct_raw = str(row['correct_answer'])
        
        is_correct = check_answer(user_selection, correct_raw)
        
        if is_correct:
            st.success("✅ **Correct Answer!** Great job!")
        else:
            sorted_correct = ", ".join(sorted([x.strip() for x in correct_raw.split(',')]))
            st.error(f"❌ **Incorrect.** Correct Option(s): **{sorted_correct}**")
            
        if pd.notna(row['explanation']) and str(row['explanation']).strip() != "":
            st.info(f"💡 **Explanation:** {row['explanation']}")
            
    st.divider()