import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_chatbot():
    """Initialize the chatbot and OpenAI client"""
    # Initialize session state variables if not already present
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    if "resumes" not in st.session_state:
        st.session_state.resumes = {}
    if "job_description" not in st.session_state:
        st.session_state.job_description = ""
    if "results" not in st.session_state:
        st.session_state.results = {}
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "openai_client" not in st.session_state:
        st.session_state.openai_client = None

    # Get API key - try both environment variables and secrets
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except:
            api_key = None
    
    # Status logging
    if api_key:
        print("OpenAI API key found")  # Console logging only
    else:
        st.warning("OpenAI API key not found. The chatbot will run in limited mode.")

    # Initialize OpenAI client
    if api_key:
        try:
            openai.api_key = api_key
            st.session_state.openai_client = openai
            st.session_state.chatbot_enabled = True
            print("OpenAI client initialized successfully")  # Console logging
        except Exception as e:
            print(f"Error initializing OpenAI client: {str(e)}")  # Console logging
            st.error("Could not initialize the AI service. The chatbot will run in limited mode.")
            st.session_state.openai_client = None
            st.session_state.chatbot_enabled = False
    else:
        st.session_state.openai_client = None
        st.session_state.chatbot_enabled = False

def get_app_context():
    """Generate context about the current state of the application for the AI assistant"""
    context = []
    
    # Page context
    context.append(f"Current page: {st.session_state.page}")
    
    # Resume context
    resume_count = len(st.session_state.resumes)
    context.append(f"Number of uploaded resumes: {resume_count}")
    
    if resume_count > 0:
        resume_names = ", ".join(list(st.session_state.resumes.keys()))
        context.append(f"Uploaded resume names: {resume_names}")
    
    # Job description context
    has_job = bool(st.session_state.job_description)
    context.append(f"Job description provided: {has_job}")
    
    # Results context
    has_results = len(st.session_state.results) > 0
    context.append(f"Results available: {has_results}")
    
    if has_results:
        try:
            top_candidate = max(st.session_state.results.items(), key=lambda x: x[1]["score"])[0]
            top_score = st.session_state.results[top_candidate]["score"] * 100
            context.append(f"Top candidate is {top_candidate} with a score of {top_score:.1f}%")
        except (ValueError, KeyError):
            pass
    
    return " ".join(context)

def render_chatbot():
    st.title("AI Assistant")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input for new message
    user_message = st.chat_input("Ask about resume screening, job matching, or how to use the app")
    
    if user_message:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_message})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_message)
        
        # Handle bot response
        with st.chat_message("assistant"):
            if st.session_state.chatbot_enabled and st.session_state.openai_client:
                try:
                    # Get context based on current app state
                    context = get_app_context()
                    
                    # Prepare messages for OpenAI
                    messages = [
                        {"role": "system", "content": f"""You are a helpful AI assistant for a resume screening application. 
                        You can help users understand how to use the app, explain how resume matching works, provide tips for creating good resumes and job descriptions, and interpret results.
                        
                        Current application context: {context}
                        
                        Keep your answers clear, helpful, and concise. Focus on being practical and solution-oriented.
                        """}
                    ]
                    
                    # Add chat history
                    for message in st.session_state.chat_history:
                        messages.append({"role": message["role"], "content": message["content"]})
                    
                    # Get response from OpenAI
                    response = st.session_state.openai_client.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        max_tokens=500,
                        temperature=0.7
                    )
                    
                    # Extract and display the response
                    assistant_response = response.choices[0].message.content
                    st.markdown(assistant_response)
                    
                    # Store the response
                    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    response = """I'm having trouble connecting to the AI service right now. Here are some general tips:
                    
                    - Upload PDF resumes for best results
                    - Provide detailed job descriptions
                    - Check your OpenAI API key if this error persists
                    - You can still use all the resume matching features without the chatbot
                    
                    How else can I help you with resume screening?"""
                    st.write(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
            else:
                response = """
                I'm the AI HR Assistant. I can help you:
                - Upload and process resumes
                - Understand how the matching system works
                - Interpret your results
                - Provide resume and job description tips
                
                Note: For full AI functionality, please add your OpenAI API key to the .env file or Streamlit secrets.
                """
                st.write(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Rerun to update the UI
        st.rerun()

# Remove the direct function calls at the module level
# initialize_chatbot()
# render_chatbot()
