import pandas as pd
import streamlit as st

@st.cache_data
def load_and_validate_csv(file_path: str = "data/questions.csv") -> pd.DataFrame:
    """CSV file load aur column structure validate karti hai."""
    # engine='python' aur on_bad_lines='skip' / quotechar='"' handle bad rows gracefully
    df = pd.read_csv(file_path, quotechar='"', skipinitialspace=True)
    
    required_columns = [
        'quiz_no', 'question_id', 'type', 'question', 
        'option_a', 'option_b', 'option_c', 'option_d', 
        'correct_answer', 'explanation'
    ]
    
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"CSV file mein ye columns missing hain: {', '.join(missing_cols)}")
        
    # Standardize types & strings
    df['quiz_no'] = df['quiz_no'].astype(int)
    df['question_id'] = df['question_id'].astype(int)
    df['type'] = df['type'].astype(str).str.strip().str.lower()
    
    return df