import streamlit as st
from PIL import Image
import io
import tempfile
from typing import Optional

from integrated_system import AILearningPlatform
from ai_mentor import AIMentor
from config import Config

# Page configuration
st.set_page_config(
    page_title="Community Issue Analyzer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
# Initialize session state
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
    except ValueError:
        st.session_state.mentor = None

if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

if 'mentor_conversation' not in st.session_state:
    st.session_state.mentor_conversation = []

# ----------------- Image Processing -----------------
def process_image(image_file, domains):
    """Process uploaded image (Windows-compatible)"""
    with st.spinner("Analyzing image..."):
        image = Image.open(image_file)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=image.format or 'PNG')
        img_byte_arr = img_byte_arr.getvalue()
       
        # Temporary file (works on Windows/Linux/Mac)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(img_byte_arr)
            temp_path = tmp.name
       
        # Process with platform
        result = st.session_state.platform.process_image(temp_path, domains=domains)
        return result

# ----------------- Text Processing -----------------
def process_text(problem_description):
    """Process text description"""
    with st.spinner("Processing description..."):
        result = st.session_state.platform.process_text_description(problem_description)
        return result

# ----------------- Display Results -----------------
def display_results(result):
    """Display analysis results"""
    if not result.get('success'):
        st.error(f"Error: {result.get('error', 'Unknown error occurred')}")
        return
   
    st.success("Analysis Complete!")
   
    tab1, tab2, tab3 = st.tabs(["Detection", "Classification", "Mission Statement"])

    with tab1:
        st.markdown("### Vision Analysis" if 'vision_analysis' in result else "### Problem Description")
        if 'vision_analysis' in result:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown(result['vision_analysis'])
            st.markdown('</div>', unsafe_allow_html=True)
        elif 'original_description' in result:
            st.info(f"**Original Description:** {result['original_description']}")

    with tab2:
        st.markdown("### Problem Classification")
        classification = result.get('classification', {})
        col1, col2 = st.columns(2)
        with col1:
            category = classification.get('category', 'Unknown')
            emoji_map = {'Environment':'', 'Health':'', 'Education':''}
            st.metric("Category", f"{emoji_map.get(category,'❓')} {category}")
        with col2:
            confidence = classification.get('confidence', 'Unknown')
            st.metric("Confidence", confidence)
        if classification.get('reasoning'):
            st.markdown("**Reasoning:**")
            st.info(classification['reasoning'])

    with tab3:
        st.markdown("### Mission Statement")
        mission = result.get('mission_statement', {})
        if mission.get('mission_statement'):
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown(f"**{mission['mission_statement']}**")
            st.markdown('</div>', unsafe_allow_html=True)
        if mission.get('problem_definition'):
            st.markdown("#### Problem Definition")
            st.write(mission['problem_definition'])
        if mission.get('goal'):
            st.markdown("#### Goal")
            st.write(mission['goal'])
        if mission.get('expected_impact'):
            st.markdown("#### Expected Impact")
            st.write(mission['expected_impact'])
        if mission.get('action_steps'):
            st.markdown("#### Action Steps")
            for i, step in enumerate(mission['action_steps'], 1):
                st.markdown(f"{i}. {step}")
   
    # Download results
    st.markdown("---")
    col1, col2 = st.columns([3,1])
    with col2:
        download_content = f"""
# Community Issue Analysis Report

## Classification
- **Category**: {result.get('classification', {}).get('category','N/A')}
- **Confidence**: {result.get('classification', {}).get('confidence','N/A')}

## Mission Statement
{result.get('mission_statement', {}).get('mission_statement','N/A')}

## Problem Definition
{result.get('mission_statement', {}).get('problem_definition','N/A')}

## Goal
{result.get('mission_statement', {}).get('goal','N/A')}

## Expected Impact
{result.get('mission_statement', {}).get('expected_impact','N/A')}

## Action Steps
"""
        for i, step in enumerate(result.get('mission_statement', {}).get('action_steps', []), 1):
            download_content += f"{i}. {step}\n"
       
        st.download_button(
            label="Download Report",
            data=download_content,
            file_name="community_issue_report.txt",
            mime="text/plain"
        )

# ----------------- AI Mentor -----------------
def display_mentor_interface():
    st.markdown("### AI Mentor & Guidance System")
    st.markdown("Get personalized guidance through critical thinking or solution templates")
    mentor_mode = st.radio(
        "Select Mentor Mode:",
        ["Critical Thinking Mode", "Solution Mode", "Interactive Chat"],
        horizontal=True
    )
    st.markdown("---")
    if mentor_mode == "Critical Thinking Mode":
        display_critical_thinking_mode()
    elif mentor_mode == "Solution Mode":
        display_solution_mode()
    else:
        display_interactive_chat()

# Critical Thinking Mode
def display_critical_thinking_mode():
    st.markdown("#### Critical Thinking Mode")
    st.info("Explore your problem through Socratic questioning. The mentor will guide you with thought-provoking questions.")
    problem_input = st.text_area("Describe the problem or topic:", height=150, key="ct_problem")
    if st.button("Get Socratic Guidance", key="ct_button") and problem_input:
        with st.spinner("Generating guidance..."):
            result = st.session_state.mentor.critical_thinking_mode(problem_input, None)
            if result.get('success'):
                st.success("Guidance Generated!")
                if result.get('guiding_questions'):
                    st.markdown("##### Guiding Questions")
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    for i, q in enumerate(result['guiding_questions'],1):
                        st.markdown(f"**{i}.** {q}")
                    st.markdown('</div>', unsafe_allow_html=True)
                if result.get('reflection_prompts'):
                    st.markdown("##### Reflection Prompts")
                    for r in result['reflection_prompts']:
                        st.info(r)
                if result.get('challenge_points'):
                    st.markdown("##### Challenge Points")
                    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                    for c in result['challenge_points']:
                        st.markdown(f"- {c}")
                    st.markdown('</div>', unsafe_allow_html=True)
                if result.get('next_steps'):
                    st.markdown("##### Suggested Next Steps")
                    for step in result['next_steps']:
                        st.markdown(f"- {step}")
            else:
                st.error(f"Error: {result.get('error')}")
    elif st.button("Get Socratic Guidance", key="ct_button"):
        st.warning("Please describe a problem first.")

# Solution Mode
def display_solution_mode():
    st.markdown("#### Solution Mode")
    st.info("Get practical frameworks and templates to structure your approach.")
    problem_input = st.text_area("Describe the problem:", height=120, key="sol_problem")
    template_type = st.selectbox("Select Template Type:", ["Auto-detect","SWOT Analysis","Budget Outline","Action Plan","Stakeholder Analysis","Project Timeline"])
    if st.button("Generate Template", key="sol_button") and problem_input:
        with st.spinner("Creating solution template..."):
            template_map = {
                "Auto-detect": "auto",
                "SWOT Analysis": "swot",
                "Budget Outline": "budget",
                "Action Plan": "action_plan",
                "Stakeholder Analysis": "stakeholder",
                "Project Timeline": "timeline"
            }
            result = st.session_state.mentor.solution_mode(problem_input, template_map[template_type], None)
            if result.get('success'):
                st.success(f"Template Generated: {result.get('template_type','').replace('_',' ').title()}")
                template_data = result.get('template',{})
                if template_data:
                    st.markdown("##### Template")
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    for section, items in template_data.items():
                        st.markdown(f"**{section}**")
                        if isinstance(items,list):
                            for item in items:
                                st.markdown(f"- {item}")
                        else:
                            st.markdown(items)
                        st.markdown("")
                    st.markdown('</div>', unsafe_allow_html=True)
                if result.get('implementation_guide'):
                    st.markdown("##### Implementation Guide")
                    st.info(result['implementation_guide'])
                if result.get('tips'):
                    st.markdown("##### Practical Tips")
                    for tip in result['tips']:
                        st.markdown(f"- {tip}")
            else:
                st.error(f"Error: {result.get('error')}")
    elif st.button("Generate Template", key="sol_button"):
        st.warning("Please describe a problem first.")

# Interactive Chat
def display_interactive_chat():
    st.markdown("#### Interactive Mentor Chat")
    st.info("Have a conversation with the AI mentor. Choose your preferred guidance style.")
    chat_mode = st.radio("Guidance Style:", ["Critical Thinking","Solution-Focused"], horizontal=True, key="chat_mode_radio")
    if st.session_state.mentor_conversation:
        st.markdown("##### Conversation")
        for msg in st.session_state.mentor_conversation:
            role = "You" if msg['role']=='user' else "Mentor"
            st.markdown(f"**{role}:** {msg['content']}")
            st.markdown("---")
    user_message = st.text_area("Your message:", height=100, key="chat_input")
    col1, col2 = st.columns([1,4])
    with col1:
        if st.button("Send", key="chat_send") and user_message:
            mode = "critical_thinking" if chat_mode=="Critical Thinking" else "solution"
            with st.spinner("Mentor is thinking..."):
                result = st.session_state.mentor.interactive_mentoring(user_message, mode)
                if result.get('success'):
                    st.session_state.mentor_conversation.append({'role':'user','content':user_message})
                    st.session_state.mentor_conversation.append({'role':'mentor','content':result['mentor_response']})
                    st.experimental_rerun()
                else:
                    st.error(f"Error: {result.get('error')}")
        elif st.button("Send", key="chat_send"):
            st.warning("Please enter a message.")
    with col2:
        if st.button("Clear Conversation", key="chat_clear"):
            st.session_state.mentor_conversation = []
            if st.session_state.mentor:
                st.session_state.mentor.reset_conversation()
            st.experimental_rerun()

# ----------------- Main -----------------
def main():
    display_header = lambda : st.markdown('<div class="main-header">AI-Powered Learning Platform</div><div class="sub-header">Recognize and translate community challenges into structured learning missions statements</div>', unsafe_allow_html=True)
    display_header()
   
    if not st.session_state.api_configured:
        st.error("Gemini API key not configured!")
        st.markdown("Please set your GEMINI_API_KEY in `.env` and restart the app.")
        return

    st.markdown("---")
    main_tab1, main_tab2 = st.tabs(["Problem Analysis", "AI Mentor"])

    with main_tab1:
        input_method = st.radio("Choose input method:", ["Upload Image", "Describe Problem"], horizontal=True)
        st.markdown("---")

        if input_method=="Upload Image":
            st.markdown("### Upload Community Issue Image")
            uploaded_file = st.file_uploader("Choose an image...", type=['png','jpg','jpeg','gif','webp'])
            if uploaded_file:
                st.image(Image.open(uploaded_file), caption="Uploaded Image", use_container_width=True)
            if uploaded_file and st.button("Analyze Image", key="analyze_image"):
                domains = st.session_state.get('selected_domains', Config.CATEGORIES)
                st.session_state.analysis_result = process_image(uploaded_file, domains)
        else:
            problem_description = st.text_area("Problem Description:", height=150)
            if problem_description and st.button("Analyze Description", key="analyze_text"):
                st.session_state.analysis_result = process_text(problem_description)

        if st.session_state.analysis_result:
            st.markdown("---")
            st.markdown("## Analysis Results")
            display_results(st.session_state.analysis_result)

    with main_tab2:
        display_mentor_interface()

if __name__=="__main__":
    main()