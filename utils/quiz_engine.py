import pandas as pd

def check_answer(user_selection, correct_raw):
    """
    Validates the user's selected answers against the correct answer(s) from CSV.
    Supports single choices ('A') and multiple comma-separated choices ('A, C').
    """
    # Clean and split correct answers into a set of uppercase strings
    correct_set = set([ans.strip().upper() for ans in correct_raw.split(',') if ans.strip()])
    
    # Ensure user selection is a set of uppercase strings
    user_set = set([str(ans).strip().upper() for ans in user_selection if str(ans).strip()])
    
    return user_set == correct_set

def calculate_score(df, submitted, answers, selected_subject=None):
    """
    Calculates the score, attempted count, and total questions.
    If selected_subject is provided, filters the calculations for that specific subject only.
    """
    # Filter dataframe by subject if specified
    if selected_subject:
        filtered_df = df[df['subject'] == selected_subject].reset_index(drop=True)
    else:
        filtered_df = df.reset_index(drop=True)

    total_questions = len(filtered_df)
    score = 0
    attempted = 0

    for idx, row in filtered_df.iterrows():
        # Construct the unique question key matching app.py naming convention
        q_key = f"s_{row['subject']}_q{row['quiz_no']}_qid{row['question_id']}"
        
        # Check if the question has been submitted/answered by the user
        if submitted.get(q_key, False):
            attempted += 1
            user_selection = answers.get(q_key, [])
            correct_raw = str(row['correct_answer'])
            
            # Validate if the user's selection matches the correct answer
            if check_answer(user_selection, correct_raw):
                score += 1

    return score, attempted, total_questions