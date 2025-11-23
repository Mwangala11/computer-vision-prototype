import streamlit as st
from PIL import Image
import os
from ai_mentor import AIMentor
from integrated_system import AILearningPlatform

# ------------ PAGE CONFIG ------------
st.set_page_config(page_title="AI Learning Platform", layout="wide")

# ------------ UTILS ------------
platform = AILearningPlatform()
mentor = AIMentor()

def save_uploaded_image(uploaded_file):
    temp_path = os.path.join("temp_uploaded_image.jpg")
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return temp_path

def download_text(text: str, filename: str):
    st.download_button(
        label=f"Download {filename}",
        data=text,
        file_name=filename,
        mime="text/plain"
    )

# ------------- STYLES -------------
st.markdown("""
<style>
    .main-title {font-size:36px;font-weight:800;text-align:center;margin-bottom:-10px;color:#003366;}
    .subtitle {text-align:center;font-size:16px;color:#444;margin-bottom:25px;}
    .section-header {font-size:22px;font-weight:700;margin-top:25px;color:#003366;}
</style>
""", unsafe_allow_html=True)

# ------------ HEADER ------------
st.markdown("<div class='main-title'>AI Learning Platform</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Smart Assistance • Problem Analysis • AI Mentorship</div>", unsafe_allow_html=True)
st.write("---")

# ============= SIDEBAR NAVIGATION =============
section = st.sidebar.radio(
    "Navigate",
    [
        "▼ Problem Analysis",
        "▼ AI Mentor"
    ]
)

# =============================================
#          PROBLEM ANALYSIS SECTION
# =============================================
if section == "▼ Problem Analysis":
    st.markdown("<div class='section-header'>Problem Analysis</div>", unsafe_allow_html=True)

    analysis_option = st.selectbox(
        "Choose a method:",
        ["Describe a Problem", "Upload Image"]
    )

    # ---------- DESCRIBE A PROBLEM ----------
    if analysis_option == "Describe a Problem":
        st.subheader("Describe Your Problem")
        problem_text = st.text_area("Enter the problem:", height=150)

        if st.button("Analyze Problem"):
            if problem_text.strip() == "":
                st.warning("Please enter a problem description.")
            else:
                # --- Use text classifier ---
                classification_result = platform.problem_classifier.classify_problem(problem_text)

                if classification_result['success']:
                    category = classification_result['category']
                    confidence = classification_result['confidence']
                    reasoning = classification_result['reasoning']
                    full_response = classification_result['full_response']

                    st.success(f"Classified as: {category}")
                    st.write(f"Confidence: {confidence}")
                    st.write(f"Reasoning: {reasoning}")

                    # Generate mission statement
                    mission = platform.mission_generator.generate_mission_statement(
                        problem_text,
                        context=f"Category: {category}"
                    )

                    st.markdown(f"**Mission Statement:** {mission.get('mission_statement', '')}")
                    st.markdown(f"**Summary:** {platform._create_text_summary(problem_text, classification_result, mission)}")

                    # Download buttons
                    download_text(mission.get('mission_statement', ''), "mission_statement.txt")
                    download_text(platform._create_text_summary(problem_text, classification_result, mission), "problem_summary.txt")
                else:
                    st.error(f"Error: {classification_result.get('error', 'Analysis failed')}")

    # ---------- UPLOAD IMAGE ----------
    elif analysis_option == "Upload Image":
        st.subheader("Upload an Image for Analysis")
        uploaded_img = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])

        if uploaded_img:
            img_path = save_uploaded_image(uploaded_img)
            st.image(uploaded_img, caption="Uploaded Image", use_container_width=True)

            if st.button("Analyze Image"):
                # --- Use full process_image pipeline ---
                analysis_result = platform.process_image(img_path)

                if analysis_result['success']:
                    classification_result = analysis_result['classification']
                    mission = analysis_result['mission_statement']

                    st.success(f"Classified as: {classification_result.get('category', 'Unknown')}")
                    st.write(f"Confidence: {classification_result.get('confidence', 'Unknown')}")
                    st.write(f"Reasoning: {classification_result.get('reasoning', 'N/A')}")

                    st.markdown(f"**Mission Statement:** {mission.get('mission_statement', '')}")
                    st.markdown(f"**Summary:** {analysis_result.get('summary', '')}")

                    # Download buttons
                    download_text(mission.get('mission_statement', ''), "mission_statement.txt")
                    download_text(analysis_result.get('summary', ''), "problem_summary.txt")
                else:
                    st.error(f"Error: {analysis_result.get('error', 'Analysis failed')}")

# =============================================
#                 AI MENTOR SECTION
# =============================================
elif section == "▼ AI Mentor":
    st.markdown("<div class='section-header'>AI Mentor</div>", unsafe_allow_html=True)

    mentor_option = st.selectbox(
        "Choose Mentor Mode:",
        ["Socratic Mode", "Solution Mode", "Interactive Chat"]
    )

    # ---------- SOCRATIC MODE ----------
    if mentor_option == "Socratic Mode":
        st.subheader("Socratic Mode")
        st.write("Receive guiding questions to help you think deeper.")
        user_query = st.text_area("Ask a question:")

        if st.button("Generate Socratic Response"):
            if user_query.strip() == "":
                st.warning("Please type something.")
            else:
                response = mentor.critical_thinking_mode(user_query)
                if response['success']:
                    st.markdown("**GUIDING QUESTIONS:**")
                    for q in response['guiding_questions']:
                        st.write(f"- {q}")

                    st.markdown("**REFLECTION PROMPTS:**")
                    for r in response['reflection_prompts']:
                        st.write(f"- {r}")

                    st.markdown("**CHALLENGE POINTS:**")
                    for c in response['challenge_points']:
                        st.write(f"- {c}")

                    st.markdown("**NEXT STEPS:**")
                    for n in response['next_steps']:
                        st.write(f"- {n}")

                    full_response = response.get('full_response', '')
                    download_text(full_response, "socratic_response.txt")
                else:
                    st.error(f"Error: {response.get('error', 'Failed to generate response')}")

    # ---------- SOLUTION MODE ----------
    elif mentor_option == "Solution Mode":
        st.subheader("Solution Mode")
        st.write("Get direct, actionable answers.")
        user_query = st.text_area("Ask your question:")

        if st.button("Generate Solution"):
            if user_query.strip() == "":
                st.warning("Please type something.")
            else:
                response = mentor.solution_mode(user_query)
                if response['success']:
                    template = response.get('template', {})
                    if template:
                        st.markdown("**Solution Template:**")
                        for section_name, lines in template.items():
                            st.markdown(f"**{section_name}:**")
                            for line in lines:
                                st.write(f"- {line}")

                    guide = response.get('implementation_guide', '')
                    if guide:
                        st.markdown("**Implementation Guide:**")
                        st.write(guide)

                    tips = response.get('tips', [])
                    if tips:
                        st.markdown("**Tips:**")
                        for tip in tips:
                            st.write(f"- {tip}")

                    full_response = response.get('full_response', '')
                    download_text(full_response, "solution_response.txt")
                else:
                    st.error(f"Error: {response.get('error', 'Failed to generate response')}")

    # ---------- INTERACTIVE CHAT ----------
    elif mentor_option == "Interactive Chat":
        st.subheader("Interactive Chat")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for user_msg, ai_msg in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(user_msg)
            with st.chat_message("assistant"):
                st.write(ai_msg)

        user_input = st.chat_input("Type your message...")

        if user_input:
            with st.chat_message("user"):
                st.write(user_input)

            ai_reply = mentor.interactive_mentoring(user_input).get('mentor_response', '')

            with st.chat_message("assistant"):
                st.write(ai_reply)

            st.session_state.chat_history.append((user_input, ai_reply))

        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.experimental_rerun()