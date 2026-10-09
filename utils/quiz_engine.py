import pandas as pd

def check_answer(user_selection: set, correct_str: str) -> bool:
    """Exact set match verification for Single & Multiple Select MCQs."""
    correct_set = {x.strip().upper() for x in str(correct_str).split(',')}
    return user_selection == correct_set

def calculate_score(df: pd.DataFrame, submitted_dict: dict, answers_dict: dict):
    """Overall score aur total attempted count calculate karta hai."""
    total_score = 0
    total_attempted = len(submitted_dict)
    
    for q_key in submitted_dict:
        # Key format: "q{quiz_no}_qid{question_id}"
        parts = q_key.split('_')
        q_num = int(parts[0].replace('q', ''))
        qid_num = int(parts[1].replace('qid', ''))
        
        match = df[(df['quiz_no'] == q_num) & (df['question_id'] == qid_num)]
        if not match.empty:
            correct_raw = match.iloc[0]['correct_answer']
            user_ans = set(answers_dict.get(q_key, []))
            if check_answer(user_ans, correct_raw):
                total_score += 1
                
    return total_score, total_attempted