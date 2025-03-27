import streamlit as st
import ollama  
import fitz 
# Set page title and icon
st.set_page_config(page_title="Chat with AI", page_icon="💬", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
        .welcome-box {
            background-color: #5c5d5e;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
            color: white;
        }
        .user-message {
            background-color: #2e3036;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            color: white;
        }
        .ai-message {
            background-color: #1b1f2b;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            color: white;
        }
        .stButton>button {
            background-color: white;
            color: black;
            font-weight: bold;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #0e1117;
            color: white;
            border: 2px solid white;
        }
        .chat-input {
            position: fixed;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            width: 60%;
        }
    </style>
    """,
    unsafe_allow_html=True
)
col1, col2 = st.columns([0.8, 0.2])
with col2:
    if st.button("Take Career Test 📖"):
        st.switch_page("pages/career_test_page.py")
# Title
st.title("💬 Chat with Your AI Career Guide")
st.write("Ask any career-related questions, and our AI will guide you!")

# Welcome Box
st.markdown('<div class="welcome-box">🤖 Hello! I am CareerBot. I will analyze your resume and suggest the best job titles & skills. Then, feel free to ask any questions!</div>', unsafe_allow_html=True)

# Initialize session states
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None  
if "messages" not in st.session_state:
    st.session_state.messages = []
if "resume_processed" not in st.session_state:
    st.session_state.resume_processed = False  # Track if AI has already given job suggestions

# Function to extract text from resume
def extract_text_from_resume(uploaded_file):
    """Extracts text from a PDF resume using PyMuPDF."""
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = "\n".join([page.get_text("text") for page in doc])
        return text.strip() if text else "No text found in resume."
    except Exception as e:
        return f"⚠️ Error extracting text: {e}"

# AI Career Suggestions Based on Resume
def suggest_career_from_resume():
    """Generates job title suggestions and career advice based on the resume."""
    if not st.session_state.resume_text:
        return "⚠️ No resume data available."

    system_prompt = f"""
    You are a highly knowledgeable Career Advisor. Based on the resume details below, provide structured career recommendations.
    Analyze the following resume and suggest:
    - **Most suitable job titles from the resume**
    - **Key skills identified on the basis of resume**
    - **Advice for improving job opportunities**
    - **A friendly prompt asking the user for further queries**
    - **Don't add unnecessary stuff**
    
    Resume Content:
    {st.session_state.resume_text}
    
    Keep the response concise and structured
    """
    
    try:
        response = ollama.chat(model="smollm:360m", messages=[{"role": "user", "content": system_prompt}])
        return response["message"]["content"]
    except Exception:
        return "⚠️ Error: AI model is unavailable. Please check the configuration."

# Resume Upload Section (Only visible if no career suggestions given yet)
if not st.session_state.resume_processed:
    uploaded_resume = st.file_uploader("Upload your resume (PDF) *optional", type=["pdf"])
    if uploaded_resume:
        st.session_state.resume_text = extract_text_from_resume(uploaded_resume)
        st.success("✅ Resume uploaded successfully! Processing career suggestions...")
        ai_reply = suggest_career_from_resume()
        st.session_state.messages.append({"role": "ai", "content": ai_reply})
        st.session_state.resume_processed = True  # Mark resume as processed
        st.rerun()  # Refresh the UI after processing

# Display chat history
for message in st.session_state.messages:
    role = "👤" if message["role"] == "user" else "🤖"
    msg_class = "user-message" if message["role"] == "user" else "ai-message"
    st.markdown(f'<div class="{msg_class}">{role} {message["content"]}</div>', unsafe_allow_html=True)

# Chat Form (Always stays at the bottom)
with st.form(key="chat_form", clear_on_submit=True):
    query = st.text_input("Ask your career-related question...", key="user_input", help="Type your message here.", placeholder="Type your message here...")
    submit_button = st.form_submit_button("Send")

# Process user query
if submit_button and query.strip():
    st.session_state.messages.append({"role": "user", "content": query})

    # AI response based on query and resume
    resume_info = f"\n\nUser's Resume Content:\n{st.session_state.resume_text}" if st.session_state.resume_text else ""
    
    ai_prompt = f"""
    You are a highly knowledgeable Career Advisor. Based on the resume details below, provide structured career recommendations.
    Based on these points mainly, answer the question -
    - **Most suitable job titles**
    - **Relevant career options**
    - **Necessary skills to improve**
    - **Any additional recommendations**
    - **Answer the query clearly and concisely**
    - **Keep it in professional and easy tone**
    - **Answer according to the question**
    - **If any question is not career-related, respond like "Please ask me a career related questions. I am best at it!"**
    """
    
    try:
        response = ollama.chat(model="smollm:360m", messages=[{"role": "user", "content": ai_prompt}])
        ai_reply = response["message"]["content"]
    except Exception:
        ai_reply = "⚠️ Error: AI model is unavailable. Please check the configuration."

    st.session_state.messages.append({"role": "ai", "content": ai_reply})
    st.rerun()