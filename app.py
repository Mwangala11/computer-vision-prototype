import streamlit as st
from PIL import Image
import io
from integrated_system import AILearningPlatform
from ai_mentor import AIMentor, get_critical_thinking_guidance, get_solution_template
from config import Config

# Page configuration
st.set_page_config(
    page_title="Community Issue Analyzer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------
# Custom CSS
# ----------------------
st.markdown("""
<style>
.main-header { font-size: 2.5rem; font-weight: bold; color: #1f77b4; text-align: center; margin-bottom: 1rem; }
.sub-header { font-size: 1.2rem; color: #666; text-align: center; margin-bottom: 2rem; }
.success-box { padding: 1rem; border-radius: 0.5rem; background-color: #d4edda; border: 1px solid #c3e6cb; margin: 1rem 0; }
.info-box { padding: 1rem; border-radius: 0.5rem; background-color: #d1ecf1; border: 1px solid #bee5eb; margin: 1rem 0; }
.warning-box { padding: 1rem; border-radius: 0.5rem; background-color: #fff3cd; border: 1px solid #ffeeba; margin: 1rem 0; }
.stButton>button { width: 100%; background-color: #1f77b4; color: white; font-weight: bold; padding: 0.5rem 1rem; border-radius: 0.5rem; border: none; }
.stButton>button:hover { background-color: #155a8a; }
</style>
""", unsafe_allow_html=True)

# ----------------------
# Session State Setup
# ----------------------
if 'platform' not in st.session_state:
    try:
        st.session_state.platform = AILearningPlatform()
        st.session_state.api_configured = True
    except ValueError as e:
        st.session_state.api_configured = False
        st.session_state.error_message = str(e)

if 'mentor' not in st.session_state:
    try:
        st.session_state.mentor = AIMentor()
        st.session_state.mentor_conversation = []
    except ValueError as e:
        st.session_state.mentor = None
        st.session_state.mentor_error = str(e)

if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

# ----------------------
# Helper Functions
# ----------------------
def display_header():
    st.markdown('<div class="main-header">AI-Powered Learning Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Recognize and translate community challenges into structured learning missions statements</div>', unsafe_allow_html=True)

def process_image(image_file, domains):
    with st.spinner("Analyzing image..."):
        image = Image.open(image_file)
        img_bytes = io.BytesIO()
        image.save(img_bytes, format=image.format or 'PNG')
        temp_path = "/tmp/uploaded_image.jpg"
        with open(temp_path, "wb") as f:
            f.write(img_bytes.getvalue())
        return st.session_state.platform.process_image(temp_path, domains=domains)

def process_text(problem_description):
    with st.spinner("Processing description..."):
        return st.session_state.platform.process_text_description(problem_description)

# ----------------------
# Mentor Convenience Functions
# ----------------------
def get_critical_guidance(problem: str):
    return get_critical_thinking_guidance(problem)

def get_solution(problem: str, template_type='auto'):
    return get_solution_template(problem, template_type)

# ----------------------
# Main Application
# ----------------------
def main():
    display_header()
   
    if not st.session_state.api_configured:
        st.error("Gemini API key not configured! Check `.env` file.")
        return

    main_tab1, main_tab2 = st.tabs(["Problem Analysis", "AI Mentor"])
   
    with main_tab1:
        input_method = st.radio("Choose input method:", ["Upload Image", "Describe Problem"], horizontal=True)
        st.markdown("---")
       
        if input_method == "Upload Image":
            uploaded_file = st.file_uploader("Choose an image...", type=['png','jpg','jpeg','gif','webp'])
            if uploaded_file:
                st.image(Image.open(uploaded_file), caption="Uploaded Image", use_container_width=True)
                if st.button("Analyze Image"):
                    result = process_image(uploaded_file, domains=Config.CATEGORIES)
                    st.session_state.analysis_result = result
        else:
            problem_description = st.text_area("Problem Description:", height=150)
            if problem_description and st.button("Analyze Description"):
                result = process_text(problem_description)
                st.session_state.analysis_result = result

        if st.session_state.analysis_result:
            st.markdown("---")
            st.markdown("## Analysis Results")
            st.write(st.session_state.analysis_result)  # replace with your detailed display_results function if needed

    with main_tab2:
        st.markdown("### AI Mentor")
        mentor_mode = st.radio("Select Mentor Mode:", ["Critical Thinking Mode", "Solution Mode", "Interactive Chat"], horizontal=True)
       
        if mentor_mode == "Critical Thinking Mode":
            problem_input = st.text_area("Describe problem to explore:", height=150)
            if problem_input and st.button("Get Guidance"):
                result = st.session_state.mentor.critical_thinking_mode(problem_input)
                st.write(result)
        elif mentor_mode == "Solution Mode":
            problem_input = st.text_area("Describe problem to solve:", height=120)
            template_type = st.selectbox("Select Template Type:", ["Auto-detect", "SWOT Analysis", "Budget Outline", "Action Plan", "Stakeholder Analysis", "Project Timeline"])
            if problem_input and st.button("Generate Template"):
                result = st.session_state.mentor.solution_mode(problem_input, template_type.lower())
                st.write(result)
        else:  # Interactive Chat
            user_message = st.text_area("Your message:", height=100)
            if user_message and st.button("Send"):
                result = st.session_state.mentor.interactive_mentoring(user_message)
                st.session_state.mentor_conversation.append({'role':'user','content':user_message})
                st.session_state.mentor_conversation.append({'role':'mentor','content':result.get('mentor_response','')})
                for msg in st.session_state.mentor_conversation:
                    st.markdown(f"**{msg['role'].title()}:** {msg['content']}")

if __name__ == "__main__":
    main()