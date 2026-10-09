import streamlit as st
import pandas as pd
from utils.data_loader import load_and_validate_csv
from utils.quiz_engine import check_answer, calculate_score

st.set_page_config(
    page_title="MOOC Multi-Subject Quiz Hub", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra-Modern Glassmorphic & Sleek Dark Theme Styling
st.markdown("""
<style>
    /* Global App Background with Radial Gradient */
    .stApp {
        background: radial-gradient(circle at top left, #1e1b4b 0%, #0f172a 55%, #020617 100%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sleek Translucent Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Modern Question Card Container */
    .quiz-card {
        background: rgba(30, 41, 59, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .quiz-card:hover {
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    /* Main Gradient Title */
    .main-title {
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }
    
    .subtitle-text {
        color: #94a3b8;
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 20px;
    }

    /* Radio Options Styling Box */
    div[role="radiogroup"] {
        background: rgba(15, 23, 42, 0.4);
        padding: 12px 16px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 10px;
    }
    
    div[role="radiogroup"] > label {
        padding: 8px 12px;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    div[role="radiogroup"] > label:hover {
        background: rgba(99, 102, 241, 0.12);
    }

    /* Premium Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 22px !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6) !important;
        background: linear-gradient(135deg, #4f46e5 100%, #4338ca 100%) !important;
    }

    /* Gradient Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #6366f1, #a855f7);
        border-radius: 10px;
    }
    
    /* Alert / Success / Error box styling */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# Session States Initialize
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = {}

# CSV Data Load
try:
    df = load_and_validate_csv("data/questions.csv")
except Exception as e:
    st.error(f"⚠️ Error loading question bank: {e}")
    st.info("Ensure 'data/questions.csv' exists with proper columns.")
    st.stop()

# Sidebar Navigation - 1. Subject Selector
st.sidebar.title("🎓 MOOC Navigation")
st.sidebar.markdown("---")
available_subjects = sorted(df['subject'].unique())
selected_subject = st.sidebar.selectbox("📚 Select Subject", available_subjects)

# Filter Data by Subject
subj_df = df[df['subject'] == selected_subject].reset_index(drop=True)

# Sidebar Navigation - 2. Quiz / Week Selector
available_quizzes = sorted(subj_df['quiz_no'].unique())
selected_quiz = st.sidebar.selectbox(
    "🎯 Select Week / Module", 
    available_quizzes, 
    format_func=lambda x: f"Week {x} Module"
)

quiz_df = subj_df[subj_df['quiz_no'] == selected_quiz].reset_index(drop=True)

# Main Title & Header Banner
st.markdown(f'<h1 class="main-title">{selected_subject}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="subtitle-text">📂 Active Module: Week {selected_quiz} &nbsp;|&nbsp; 📝 Total MCQs: {len(quiz_df)}</p>', unsafe_allow_html=True)

# Calculate Scores for Selected Subject
subj_score, subj_attempted, total_subj_questions = calculate_score(
    df, st.session_state.submitted, st.session_state.answers, selected_subject
)

# Progress Section inside a clean layout
col_prog1, col_prog2 = st.columns([3, 1])
with col_prog1:
    st.markdown(f"**Module Completion Progress (Week {selected_quiz})**")
    progress_val = subj_attempted / total_subj_questions if total_subj_questions > 0 else 0
    st.progress(progress_val)
with col_prog2:
    st.markdown(f"<div style='text-align: right; padding-top: 20px; color: #94a3b8; font-weight: 600; font-size: 0.9rem;'>{subj_attempted} / {total_subj_questions} Completed</div>", unsafe_allow_html=True)

st.markdown("---")

# Sidebar Score Metrics Card
st.sidebar.markdown("### 📊 Performance Analytics")
st.sidebar.metric("Subject Score", f"{subj_score} / {subj_attempted}")
if subj_attempted > 0:
    accuracy = int((subj_score / subj_attempted) * 100)
    st.sidebar.metric("Current Accuracy", f"{accuracy}%")
else:
    st.sidebar.metric("Current Accuracy", "0%")

st.sidebar.markdown("---")
st.sidebar.caption("🚀 Built for rigorous MOOC exam prep.")

# Render MCQs Inside Beautiful Cards
for idx, row in quiz_df.iterrows():
    q_key = f"s_{selected_subject}_q{selected_quiz}_qid{row['question_id']}"
    
    # Opening Glassmorphic Card Container
    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    
    st.markdown(f"#### **Q{idx + 1}.** {row['question']}")
    
    options = {
        'A': row['option_a'],
        'B': row['option_b'],
        'C': row['option_c'],
        'D': row['option_d']
    }
    
    valid_options = {k: v for k, v in options.items() if pd.notna(v) and str(v).strip() != ""}
    
    if row['type'] == 'single':
        choice = st.radio(
            "Select your option:",
            options=list(valid_options.keys()),
            format_func=lambda x: f"{x}) {valid_options[x]}",
            key=f"radio_{q_key}",
            index=None,
            label_visibility="collapsed"
        )
        if choice:
            st.session_state.answers[q_key] = [choice]
            
    elif row['type'] == 'multiple':
        st.caption("*(💡 Note: Multiple correct options possible)*")
        selected_checks = []
        for opt_code, opt_val in valid_options.items():
            if st.checkbox(f"{opt_code}) {opt_val}", key=f"chk_{q_key}_{opt_code}"):
                selected_checks.append(opt_code)
        st.session_state.answers[q_key] = selected_checks

    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
    
    col_btn, _ = st.columns([1, 4])
    with col_btn:
        sub_btn = st.button("Check Answer", key=f"btn_{q_key}")
        if sub_btn:
            st.session_state.submitted[q_key] = True

    if st.session_state.submitted.get(q_key, False):
        user_selection = set(st.session_state.answers.get(q_key, []))
        correct_raw = str(row['correct_answer'])
        
        is_correct = check_answer(user_selection, correct_raw)
        
        st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
        if is_correct:
            st.success("✅ **Correct Answer! Excellent job.**")
        else:
            sorted_correct = ", ".join(sorted([x.strip() for x in correct_raw.split(',')]))
            st.error(f"❌ **Incorrect.** The correct option(s): **{sorted_correct}**")
            
        if pd.notna(row['explanation']) and str(row['explanation']).strip() != "":
            st.info(f"💡 **Explanation:** {row['explanation']}")
            
    # Closing Glassmorphic Card Container
    st.markdown('</div>', unsafe_allow_html=True)