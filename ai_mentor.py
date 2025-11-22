from typing import Dict, Optional, List
import google.generativeai as genai
from config import Config
import time
from google.generativeai.error import RateLimitError

class AIMentor:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(Config.TEXT_MODEL)
        self.conversation_history = []

    # Safe API call with retry
    def _call_model_with_retry(self, prompt: str) -> str:
        for attempt in range(3):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except RateLimitError:
                wait_time = (attempt + 1) * 5
                print(f"Rate limit hit. Retrying in {wait_time}s...")
                time.sleep(wait_time)
        raise Exception("Rate limit exceeded after retries")

    # Critical Thinking Mode
    def critical_thinking_mode(self, problem_description: str, context: Optional[str] = None) -> Dict:
        prompt = f"You are a Socratic mentor. Problem: {problem_description}"
        try:
            result_text = self._call_model_with_retry(prompt)
            return {'success': True, 'guidance': result_text}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    # Solution Mode
    def solution_mode(self, problem_description: str, template_type: str = 'auto') -> Dict:
        prompt = f"You are a solution-focused mentor. Problem: {problem_description}. Template: {template_type}"
        try:
            result_text = self._call_model_with_retry(prompt)
            return {'success': True, 'template': result_text}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    # Interactive Chat
    def interactive_mentoring(self, user_message: str, mode: str = 'critical_thinking') -> Dict:
        self.conversation_history.append({'role':'user','content':user_message})
        prompt = f"{mode} mentor. Conversation: {self.conversation_history[-4:]}. User: {user_message}"
        try:
            response_text = self._call_model_with_retry(prompt)
            self.conversation_history.append({'role':'mentor','content':response_text})
            return {'success': True, 'mentor_response': response_text}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def reset_conversation(self):
        self.conversation_history = []

# Convenience functions using session state
def get_critical_thinking_guidance(problem: str, context: Optional[str] = None) -> Dict:
    mentor = st.session_state.mentor
    return mentor.critical_thinking_mode(problem, context)

def get_solution_template(problem: str, template_type: str = 'auto') -> Dict:
    mentor = st.session_state.mentor
    return mentor.solution_mode(problem, template_type)