import streamlit as st

# Quiz questions data
QUIZ_DATA = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct": 2
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct": 1
    },
    {
        "question": "What is 7 × 8?",
        "options": ["54", "56", "58", "64"],
        "correct": 1
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
        "correct": 1
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["African Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
        "correct": 1
    },
    {
        "question": "In which year did World War II end?",
        "options": ["1943", "1944", "1945", "1946"],
        "correct": 2
    },
    {
        "question": "What is the chemical symbol for gold?",
        "options": ["Go", "Gd", "Au", "Ag"],
        "correct": 2
    },
    {
        "question": "Which continent is the Sahara Desert located in?",
        "options": ["Asia", "Africa", "Australia", "South America"],
        "correct": 1
    }
]

def initialize_session_state():
    """Initialize session state variables"""
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False

def reset_quiz():
    """Reset all quiz data"""
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = {}
    st.session_state.quiz_completed = False
    st.session_state.show_results = False

def calculate_score():
    """Calculate the final score"""
    score = 0
    for i, answer in st.session_state.answers.items():
        if answer == QUIZ_DATA[i]['correct']:
            score += 1
    return score

def show_question(question_idx):
    """Display current question with radio buttons"""
    question_data = QUIZ_DATA[question_idx]
    
    st.subheader(f"Question {question_idx + 1} of {len(QUIZ_DATA)}")
    st.write(f"**{question_data['question']}**")
    
    # Create radio button options
    selected_option = st.radio(
        "Choose your answer:",
        options=range(len(question_data['options'])),
        format_func=lambda x: question_data['options'][x],
        key=f"question_{question_idx}",
        index=st.session_state.answers.get(question_idx, 0)
    )
    
    return selected_option

def show_results():
    """Display final results with detailed breakdown"""
    st.balloons()
    
    final_score = calculate_score()
    total_questions = len(QUIZ_DATA)
    percentage = (final_score / total_questions) * 100
    
    # Main score display
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🎉 Quiz Completed! 🎉")
        st.markdown(f"## Your Score: {final_score}/{total_questions}")
        st.markdown(f"### Percentage: {percentage:.1f}%")
        
        # Performance message
        if percentage >= 80:
            st.success("🌟 Excellent work!")
        elif percentage >= 60:
            st.info("👍 Good job!")
        else:
            st.warning("📚 Keep studying!")
    
    st.markdown("---")
    
    # Detailed results
    st.subheader("📋 Detailed Results")
    
    for i, question_data in enumerate(QUIZ_DATA):
        user_answer = st.session_state.answers.get(i, 0)
        correct_answer = question_data['correct']
        is_correct = user_answer == correct_answer
        
        with st.expander(f"Question {i+1}: {question_data['question']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Your Answer:**")
                if is_correct:
                    st.success(f"✅ {question_data['options'][user_answer]}")
                else:
                    st.error(f"❌ {question_data['options'][user_answer]}")
            
            with col2:
                st.write("**Correct Answer:**")
                st.info(f"✅ {question_data['options'][correct_answer]}")

def main():
    """Main application function"""
    st.set_page_config(
        page_title="Quiz Game App",
        page_icon="❓",
        layout="centered"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # App header
    st.title("❓ Quiz Game App")
    st.markdown("Test your knowledge with this fun quiz!")
    
    # Progress bar
    if not st.session_state.quiz_completed:
        progress = st.session_state.current_question / len(QUIZ_DATA)
        st.progress(progress)
        st.write(f"Progress: {st.session_state.current_question}/{len(QUIZ_DATA)} questions")
    
    # Main quiz logic
    if st.session_state.show_results:
        show_results()
        
        # Restart button
        if st.button("🔄 Take Quiz Again", type="primary"):
            reset_quiz()
            st.rerun()
            
    elif st.session_state.quiz_completed:
        st.info("Click 'Show Results' to see your final score!")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📊 Show Results", type="primary"):
                st.session_state.show_results = True
                st.rerun()
        
    else:
        # Show current question
        current_q = st.session_state.current_question
        
        if current_q < len(QUIZ_DATA):
            selected_answer = show_question(current_q)
            
            # Store the answer
            st.session_state.answers[current_q] = selected_answer
            
            # Navigation buttons
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if current_q > 0:
                    if st.button("⬅️ Previous"):
                        st.session_state.current_question -= 1
                        st.rerun()
            
            with col3:
                if current_q < len(QUIZ_DATA) - 1:
                    if st.button("Next ➡️", type="primary"):
                        st.session_state.current_question += 1
                        st.rerun()
                else:
                    if st.button("✅ Finish Quiz", type="primary"):
                        st.session_state.quiz_completed = True
                        st.rerun()
    
    # Sidebar with quiz info
    with st.sidebar:
        st.markdown("### 📊 Quiz Information")
        st.write(f"**Total Questions:** {len(QUIZ_DATA)}")
        if st.session_state.answers:
            st.write(f"**Questions Answered:** {len(st.session_state.answers)}")
        
        st.markdown("### 🎯 Instructions")
        st.write("1. Read each question carefully")
        st.write("2. Select your answer using radio buttons")
        st.write("3. Use Next/Previous to navigate")
        st.write("4. Click 'Finish Quiz' when done")
        
        st.markdown("---")
        if st.button("🔄 Restart Quiz", help="This will reset all your progress"):
            reset_quiz()
            st.rerun()

if __name__ == "__main__":
    main()