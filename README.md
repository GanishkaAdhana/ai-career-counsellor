# AI Career Counselor

AI Career Counselor is an intelligent, AI-powered web application designed to assist users in identifying suitable career paths based on their skills, interests, and resume data. Built using Python and Streamlit, the platform combines interactive UI design with state-of-the-art AI technologies to offer personalized guidance, resume analysis, and insightful career-related suggestions. It is particularly useful for students, recent graduates, or professionals seeking a career transition.

Features of AI Career Counsellor 
1. Home Page - A minimal and clean landing page featuring a centered "Get Started" button that leads users to the main features.
2. Chat with AI - This feature enables users to interact with an AI-powered chatbot for career guidance by adding resumes. It is enhanced with Retrieval-Augmented Generation (RAG) to ensure domain-specific and context-aware answers using custom knowledge files and vector similarity search.
3. Career Test Page - An interactive assessment where users answer a set of questions designed to analyze their interests and strengths. Based on their responses, the system suggests potential career paths that align with their profile.
4. Resume Analysis - Users can upload their resumes in PDF format, which are then parsed to extract relevant skills, experience, and academic data. Based on this information, the system provides tailored career recommendations.

Technologies Used
1. AI Career Counselor leverages a range of modern technologies to deliver a responsive and intelligent user experience:
2. Python 3.11 is used as the core backend language, providing a robust and flexible foundation for application logic, resume processing, and AI integrations.
3. Streamlit is employed to develop an intuitive and interactive web interface. Its simplicity and speed allow for rapid prototyping and deployment of data-driven applications.
4. Ollama serves as the runtime environment for running local large language models, ensuring efficient, offline, and private model inference without relying on external APIs.
5. FAISS (Facebook AI Similarity Search) is integrated for implementing vector-based similarity search, which enables fast and relevant retrieval of career guidance data in the Retrieval-Augmented Generation (RAG) system.
6. gemma:2b, efficient language model, powers the core AI functionality, offering intelligent responses to user queries.

How It Works
1. User Interaction: The user engages with the system either through the chatbot, the career test, or by uploading their resume.
2. Processing & Analysis: The platform processes input data and uses AI-driven algorithms to analyze skills, preferences, and experience.
3. Response Generation: The system retrieves relevant career insights from a structured domain knowledge base using RAG and FAISS, and generates a contextual response using the phi3:mini model.
4. Recommendations Delivered: Personalized career suggestions or test results are presented to the user through the Streamlit interface.


# Install all required Python packages
pip install -r requirements.txt

# Pull the gemma:2b model 
ollama pull gemma:2b

# Run the AI Career Counselor app
streamlit run home_page.py

AI Career Counselor combines the power of modern AI with intuitive design to deliver smart, personalized career guidance.
