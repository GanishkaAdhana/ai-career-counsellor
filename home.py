import streamlit as st

# Set page config
st.set_page_config(page_title="AI Career Counsellor", page_icon="🎓", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        /* Center content */
        .center-container {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
        }

        /* Style the Get Started button */
        .stButton>button {
            background-color: white;
            color: black;
            border-radius: 10px;
            padding: 10px 20px;
            border: 2px solid white;
            font-size: 18px;
        }
        
        /* Hover effect */
        .stButton>button:hover {
            background-color: #0e1117; /* Dark background */
            color: white;
            border: 2px solid white;
        }

        /* Positioning Career Test button */
        .career-test-container {
            display: flex;
            justify-content: flex-end;
            padding: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Career Test button in the top-right
col1, col2 = st.columns([0.8, 0.2])
with col2:
    if st.button("Take Career Test"):
        st.switch_page("pages/career_test_page.py")

# Centered content
st.markdown('<div class="center-container">', unsafe_allow_html=True)
st.title("AI Career Counsellor")
st.write("Find the right career path with AI-driven guidance.")

if st.button("Get Started"):
    st.switch_page("pages/ai_chat_page.py")

st.markdown('</div>', unsafe_allow_html=True)