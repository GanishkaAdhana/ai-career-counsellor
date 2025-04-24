AI Career Counselor

AI Career Counselor is an intelligent, AI-powered web application designed to assist users in identifying suitable career paths based on their skills, interests, and resume data. Built using Python and Streamlit, the platform combines interactive UI design with state-of-the-art AI technologies to offer personalized guidance, resume analysis, and insightful career-related suggestions. It is particularly useful for students, recent graduates, or professionals seeking a career transition.

Features of AI Career Counsellor 

Home Page - A minimal and clean landing page featuring a centered "Get Started" button that leads users to the main features.

Chat with AI - This feature enables users to interact with an AI-powered chatbot for career guidance by adding resumes. It is enhanced with Retrieval-Augmented Generation (RAG) to ensure domain-specific and context-aware answers using custom knowledge files and vector similarity search.

Career Test Page - An interactive assessment where users answer a set of questions designed to analyze their interests and strengths. Based on their responses, the system suggests potential career paths that align with their profile.

Resume Analysis - Users can upload their resumes in PDF format, which are then parsed to extract relevant skills, experience, and academic data. Based on this information, the system provides tailored career recommendations.

Technologies Used

AI Career Counselor leverages a range of modern technologies to deliver a responsive and intelligent user experience:

Python 3.11 is used as the core backend language, providing a robust and flexible foundation for application logic, resume processing, and AI integrations.

Streamlit is employed to develop an intuitive and interactive web interface. Its simplicity and speed allow for rapid prototyping and deployment of data-driven applications.

Ollama serves as the runtime environment for running local large language models, ensuring efficient, offline, and private model inference without relying on external APIs.

FAISS (Facebook AI Similarity Search) is integrated for implementing vector-based similarity search, which enables fast and relevant retrieval of career guidance data in the Retrieval-Augmented Generation (RAG) system.

phi3:mini, a lightweight and efficient language model, powers the core AI functionality, offering intelligent responses to user queries with minimal resource consumption.

How It Works

User Interaction: The user engages with the system either through the chatbot, the career test, or by uploading their resume.

Processing & Analysis: The platform processes input data and uses AI-driven algorithms to analyze skills, preferences, and experience.

Response Generation: The system retrieves relevant career insights from a structured domain knowledge base using RAG and FAISS, and generates a contextual response using the phi3:mini model.

Recommendations Delivered: Personalized career suggestions or test results are presented to the user through the Streamlit interface.

Powering intelligent career guidance with Python and AI
