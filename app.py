import os
import streamlit as st
from PIL import Image
from ai_mentor import AIMentor, get_critical_thinking_guidance, get_solution_template
from config import Config

# Ensure temp folder exists
TEMP_DIR = os.path.join(os.getcwd(), "temp_uploads")
os.makedirs(TEMP_DIR, exist_ok=True)

def process_image(uploaded_file, domains):
    temp_path = os.path.join(TEMP_DIR, "uploaded_image.jpg")
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Example: process the image (replace with your real logic)
    result = "Classified as: Environment"  # Placeholder
    return result

def display_problem_analysis():
    st.header("Problem Analysis")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"], key="upload_image_1")
    if uploaded_file:
        st.image(Image.open(uploaded_file), width="stretch")
        result = process_image(uploaded_file, domains=Config.CATEGORIES)
        st.success(result)

def display_critical_thinking_mode():
    st.subheader("Critical Thinking Mode")
    problem_input = st.text_area("Describe the problem", key="ct_input_1")
    if st.button("Get Socratic Guidance", key="ct_button_1") and problem_input:
        guidance = get_critical_thinking_guidance(problem_input)
        st.info(guidance)

def display_solution_mode():
    st.subheader("Solution Mode")
    problem_input = st.text_area("Enter problem for solution template", key="sol_input_1")
    if st.button("Generate Template", key="sol_button_1") and problem_input:
        template = get_solution_template(problem_input)
        st.success(template)

def display_interactive_chat():
    st.subheader("Interactive Chat")
    user_message = st.text_input("Send a message", key="chat_input_1")
    if st.button("Send", key="chat_send_1") and user_message:
        response = AIMentor().chat(user_message)
        st.info(response)

def display_mentor_interface():
    st.sidebar.title("AI Mentor Modes")
    mode = st.sidebar.radio("Select Mode", ["Critical Thinking", "Solution", "Chat"], key="mentor_mode_1")

    if mode == "Critical Thinking":
        display_critical_thinking_mode()
    elif mode == "Solution":
        display_solution_mode()
    elif mode == "Chat":
        display_interactive_chat()

def main():
    st.title("Computer Vision & AI Mentor Prototype")
    display_problem_analysis()
    st.markdown("---")
    display_mentor_interface()

if __name__ == "__main__":
    main()