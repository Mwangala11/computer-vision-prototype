import streamlit as st
from PIL import Image
import os
from ai_mentor import AIMentor, get_critical_thinking_guidance, get_solution_template

# Configuration
class Config:
    CATEGORIES = ["Environment", "Education", "Health", "Infrastructure", "Community"]

mentor = AIMentor()

# Helper functions
def save_uploaded_image(uploaded_file):
    temp_path = os.path.join("temp_uploaded_image.jpg")
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return temp_path

def process_image(uploaded_file, domains):
    temp_path = save_uploaded_image(uploaded_file)
    classification = domains[0]  # Dummy classification for now
    mission_statement = f"Recognized challenge in {classification} domain. Structured mission: Improve community well-being through targeted interventions."
    return temp_path, classification, mission_statement

def generate_mission_from_description(description):
    classification = "Environment"
    mission_statement = f"Based on the description: '{description}', the structured mission statement is: Enhance community outcomes by addressing key environmental challenges."
    return classification, mission_statement

# Problem Analysis UI
def display_problem_analysis():
    st.header("Problem Analysis")
    st.write("Recognize and translate community challenges into structured mission statements.")

    option = st.radio("Choose input method:", ("Upload Image", "Describe Problem"))

    if option == "Upload Image":
        uploaded_file = st.file_uploader("Upload an image of the problem", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            image_path, classification, mission_statement = process_image(uploaded_file, domains=Config.CATEGORIES)
            image = Image.open(image_path)
            st.image(image, caption="Uploaded Problem Image", use_column_width=True)
            st.success(f"Classified as: {classification}")
            st.markdown(f"**Mission Statement:** {mission_statement}")
    else:
        description = st.text_area("Describe the problem")
        if description:
            classification, mission_statement = generate_mission_from_description(description)
            st.success(f"Classified as: {classification}")
            st.markdown(f"**Mission Statement:** {mission_statement}")

# AI Mentor Modes UI
def display_critical_thinking_mode():
    st.subheader("Socratic Mode")
    query = st.text_area("Enter your query for Socratic guidance", key="ct_input")
    if st.button("Get Socratic Guidance", key="ct_button_unique"):
        if query:
            response = get_critical_thinking_guidance(query)
            # Display like old app.py style
            st.markdown(f"**Your Query:** {query}")
            st.markdown(f"**Socratic Guidance:** {response}")

def display_solution_mode():
    st.subheader("Solution Mode")
    query = st.text_area("Enter your problem to generate a solution template", key="sol_input")
    if st.button("Generate Template", key="sol_button_unique"):
        if query:
            response = get_solution_template(query)
            # Display like old app.py style
            st.markdown(f"**Your Problem:** {query}")
            st.markdown(f"**Solution Template:** {response}")

def display_interactive_chat():
    st.subheader("Interactive Chat with AI Mentor")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    chat_input = st.text_area("Enter your message", key="chat_input")
    if st.button("Send", key="chat_send_unique"):
        if chat_input:
            # Save user message
            st.session_state.chat_history.append({"user": chat_input, "ai": None})
            # Correct method in AIMentor
            ai_response = mentor.interactive_mentoring(chat_input, mode="chat")  # replace with correct internal call
            st.session_state.chat_history[-1]["ai"] = ai_response.get("mentor_response", ai_response)

    # Display chat history like old app.py
    for chat in st.session_state.chat_history:
        st.markdown(f"**You:** {chat['user']}")
        if chat["ai"]:
            st.markdown(f"**AI Mentor:** {chat['ai']}")
        st.markdown("---")

def display_mentor_interface():
    st.header("AI Mentor")
    mode = st.radio("Select Mentor Mode:", ["Socratic Mode", "Solution Mode", "Interactive Chat"])
    if mode == "Socratic Mode":
        display_critical_thinking_mode()
    elif mode == "Solution Mode":
        display_solution_mode()
    else:
        display_interactive_chat()

# Main
def main():
    st.title("Community Problem Recognition & AI Mentor System")
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to:", ["Problem Analysis", "AI Mentor"])

    if choice == "Problem Analysis":
        display_problem_analysis()
    else:
        display_mentor_interface()

if __name__ == "__main__":
    main()
