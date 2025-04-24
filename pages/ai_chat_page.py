import streamlit as st
import fitz
import os
from rag_help import init_rag_system, simplified_query_with_rag, process_new_document, get_existing_documents, document_exists

st.set_page_config(page_title="AI Career Guide", page_icon="🚀", layout="wide")

# Custom CSS for improved UI
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .chat-message.user {
        background-color: #e3f2fd;
    }
    .chat-message.bot {
        background-color: #ffffff;
    }
    .chat-message .message-content {
        margin-top: 0.5rem;
    }
    .sidebar .stButton>button {
        width: 100%;
        margin-bottom: 10px;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
    }
    .input-container {
        position: fixed;
        bottom: 0;
        left: 22rem;
        right: 0;
        padding: 1rem;
        background-color: #f5f7f9;
        z-index: 1000;
    }
    .chat-container {
        margin-bottom: 80px;
        padding-left: 22rem;
        padding-right: 2rem;
    }
    [data-testid="stSidebar"] {
        width: 22rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_document" not in st.session_state:
    st.session_state.current_document = None
if "rag_system" not in st.session_state:
    st.session_state.rag_system = None

# Function to extract text from uploaded PDF document
def extract_text_from_pdf(uploaded_file):
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = "\n".join([page.get_text() for page in doc])
        return text.strip() if text else "No text found in document."
    except Exception as e:
        st.error(f"Error extracting text from document: {e}")
        return None

# Function to display chat messages
def display_chat_messages(messages):
    for message in messages:
        with st.container():
            st.markdown(f"""
            <div class="chat-message {message['role']}">
                <div><strong>{'You' if message['role'] == 'user' else 'AI'}:</strong></div>
                <div class="message-content">{message['content']}</div>
            </div>
            """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("📚 Document Manager")

    uploaded_doc = st.file_uploader("Upload a document (PDF)", type=["pdf"])

    existing_docs = get_existing_documents()
    selected_doc = st.selectbox("Select existing document", ["None"] + existing_docs)

    if uploaded_doc:
        if not document_exists(uploaded_doc.name):
            doc_text = extract_text_from_pdf(uploaded_doc)
            if doc_text:
                process_new_document(doc_text, uploaded_doc.name)
                st.success(f"✅ '{uploaded_doc.name}' added!")

        st.session_state.current_document = uploaded_doc.name
        st.session_state.rag_system = init_rag_system(uploaded_doc.name)
        st.rerun()

    if selected_doc != "None" and selected_doc != st.session_state.current_document:
        st.session_state.current_document = selected_doc
        st.session_state.rag_system = init_rag_system(selected_doc)
        st.success(f"✅ Selected: {selected_doc}")
        st.rerun()

    st.markdown("---")
    st.header("📊 Career Resources")
    if st.button("Take Career Assessment"):
        st.switch_page("pages/career_test_page.py")
    if st.button("View Job Market Trends"):
        st.info("Job market trends feature coming soon!")

# Main chat interface
st.title("🚀 AI Career Guide")

if st.session_state.current_document:
    st.subheader(f"📄 Current Document: {st.session_state.current_document}")

# Display chat messages
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    display_chat_messages(st.session_state.messages)
    st.markdown('</div>', unsafe_allow_html=True)

# Input container at the bottom
st.markdown('<div class="input-container">', unsafe_allow_html=True)
user_input = st.chat_input("Ask about careers, skills, or job opportunities...", key="user_input")
st.markdown('</div>', unsafe_allow_html=True)

if user_input:
    if st.session_state.current_document and st.session_state.rag_system:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("AI is thinking..."):
            collection, model = st.session_state.rag_system
            ai_response = simplified_query_with_rag(collection, model, user_input)
            st.session_state.messages.append({"role": "bot", "content": ai_response})

        st.rerun()
    elif not st.session_state.current_document:
        st.warning("Please select or upload a document first.")
