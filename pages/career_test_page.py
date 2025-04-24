import streamlit as st
import ollama

st.markdown(
    """
    <style>
    .stButton>button {
            background-color: white;
            color: black;
            border-radius: 10px;
            padding: 10px 20px;
            border: 2px solid white;
            font-size: 18px;
        }
        
        .stButton>button:hover {
            background-color: #0e1117; /* Dark background */
            color: white;
            border: 2px solid white;
        }
        </style>
    """, unsafe_allow_html=True
)
col1, col2 = st.columns([0.8, 0.2])
with col2:
    if st.button("Chat with AI 🤖"):
        st.switch_page("pages/ai_chat_page.py")

def get_career_suggestion(answers):
    prompt = f"""
    Analyze the following responses from a career interest test and suggest the 3 best-suited careers for the user. 
    Answers: {answers}
    Provide only the job titles in a bullet-point format.
    """
    response = ollama.chat(model='phi3:mini', messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def career_test_page():
    st.title("Career Test 📖")
    st.write("Answer the following questions to find out which career suits you best.")

    questions = [
        "Do you enjoy working with numbers and data?",
        "Are you interested in solving complex problems?",
        "Do you like creative work such as designing or writing?",
        "Are you comfortable working in a team environment?",
        "Do you prefer working with technology and programming?",
        "Would you enjoy a career that involves public speaking?",
        "Do you like helping others and giving advice?",
        "Are you interested in business and entrepreneurship?",
        "Do you prefer working indoors or outdoors?",
        "Are you comfortable handling pressure and deadlines?",
        "Do you enjoy learning about human behavior and psychology?",
        "Would you like to work in healthcare and medicine?",
        "Do you prefer hands-on work over theoretical work?",
        "Are you interested in law and justice?",
        "Do you enjoy conducting research and analysis?",
        "Would you like to work with children and education?",
        "Are you passionate about environmental sustainability?",
        "Do you enjoy planning and organizing events?",
        "Would you like a job that involves traveling frequently?",
        "Do you prefer a structured job role or a flexible one?"
    ]

    answers = []
    for i, question in enumerate(questions):
        response = st.radio(f"{i+1}. {question}", ["Yes", "No", "Maybe"], index=2)
        answers.append(response)

    if st.button("Get Career Suggestion"):
        with st.spinner("Analyzing your responses..."):
            career_suggestion = get_career_suggestion(answers)
            st.subheader("Your Suggested Careers:")
            st.write(career_suggestion)

career_test_page()
