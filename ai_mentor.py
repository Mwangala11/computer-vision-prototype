from typing import Dict, Optional, List
import time
import google.generativeai as genai
from config import Config


class AIMentor:
    """AI Mentor providing Socratic guidance, solution templates, and interactive chat"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        self.conversation_history = []

    # --------------------------
    # Critical Thinking Mode
    # --------------------------
    def critical_thinking_mode(self, problem_description: str, context: Optional[str] = None) -> Dict:
        prompt = self._create_critical_thinking_prompt(problem_description, context)
        try:
            result_text = self._generate_with_retry(prompt)
            parsed = self._parse_socratic_response(result_text)
            return {
                'success': True,
                'mode': 'Critical Thinking',
                'problem': problem_description,
                'guiding_questions': parsed.get('questions', []),
                'reflection_prompts': parsed.get('reflections', []),
                'challenge_points': parsed.get('challenges', []),
                'next_steps': parsed.get('next_steps', []),
                'full_response': result_text
            }
        except Exception as e:
            return {'success': False, 'error': str(e), 'mode': 'Critical Thinking'}

    # --------------------------
    # Solution Mode
    # --------------------------
    def solution_mode(self, problem_description: str, template_type: str = 'auto', category: Optional[str] = None) -> Dict:
        if template_type == 'auto':
            template_type = self._determine_template_type(problem_description, category)

        prompt = self._create_solution_template_prompt(problem_description, template_type, category)
        try:
            result_text = self._generate_with_retry(prompt)
            parsed = self._parse_template_response(result_text, template_type)
            return {
                'success': True,
                'mode': 'Solution',
                'template_type': template_type,
                'problem': problem_description,
                'template': parsed.get('template', {}),
                'implementation_guide': parsed.get('guide', ''),
                'tips': parsed.get('tips', []),
                'full_response': result_text
            }
        except Exception as e:
            return {'success': False, 'error': str(e), 'mode': 'Solution'}

    # --------------------------
    # Interactive Chat Mode
    # --------------------------
    def interactive_mentoring(self, user_message: str, mode: str = 'critical_thinking') -> Dict:
        # Append user message to conversation
        self.conversation_history.append({'role': 'user', 'content': user_message})

        # Prepare prompt with context from last 6 exchanges
        prompt = self._create_interactive_prompt(user_message, mode)
        try:
            response_text = self._generate_with_retry(prompt)
            # Append AI response to conversation
            self.conversation_history.append({'role': 'mentor', 'content': response_text})
            return {
                'success': True,
                'mode': mode,
                'user_message': user_message,
                'mentor_response': response_text,
                'conversation_length': len(self.conversation_history)
            }
        except Exception as e:
            return {'success': False, 'error': str(e), 'mode': mode}

    # --------------------------
    # Reset conversation
    # --------------------------
    def reset_conversation(self):
        self.conversation_history = []

    # --------------------------
    # Gemini API call with retries
    # --------------------------
    def _generate_with_retry(self, prompt: str, max_retries: int = 3, wait_seconds: int = 2) -> str:
        retries = 0
        while retries < max_retries:
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                if "429" in str(e):  # Rate limit
                    retries += 1
                    time.sleep(wait_seconds * retries)
                else:
                    raise e
        raise Exception("Exceeded retry limit due to API rate limits (429)")

    # --------------------------
    # Prompt creation helpers
    # --------------------------
    def _create_critical_thinking_prompt(self, problem_description: str, context: Optional[str] = None) -> str:
        prompt = f"You are a Socratic mentor guiding learners with questions, not answers.\nProblem: {problem_description}\n"
        if context:
            prompt += f"Context: {context}\n"
        prompt += "\nGenerate:\nGUIDING QUESTIONS:\nREFLECTION PROMPTS:\nCHALLENGE POINTS:\nNEXT STEPS:\n"
        return prompt

    def _create_solution_template_prompt(self, problem_description: str, template_type: str, category: Optional[str] = None) -> str:
        instruction = f"Create a {template_type.upper()} template for the following problem:\n{problem_description}"
        if category:
            instruction += f"\nCategory: {category}"
        return instruction

    def _create_interactive_prompt(self, user_message: str, mode: str) -> str:
        history_context = ""
        for entry in self.conversation_history[-6:]:
            role = entry['role'].title()
            history_context += f"{role}: {entry['content']}\n"
        if mode == 'critical_thinking':
            system_role = "You are a Socratic mentor. Continue guiding through questions and reflections."
        else:
            system_role = "You are a solution-focused mentor. Provide practical advice, frameworks, and next steps."
        prompt = f"{system_role}\nConversation history:\n{history_context}\nUser: {user_message}\nMentor response:"
        return prompt

    # --------------------------
    # Helper methods for templates
    # --------------------------
    def _determine_template_type(self, problem_description: str, category: Optional[str] = None) -> str:
        desc_lower = problem_description.lower()
        if any(word in desc_lower for word in ['budget', 'cost', 'funding', 'finance']):
            return 'budget'
        elif any(word in desc_lower for word in ['stakeholder', 'community', 'people']):
            return 'stakeholder'
        elif any(word in desc_lower for word in ['timeline', 'schedule', 'deadline']):
            return 'timeline'
        elif any(word in desc_lower for word in ['strength', 'weakness', 'opportunity', 'threat']):
            return 'swot'
        else:
            return 'action_plan'

    # --------------------------
    # Parsing methods
    # --------------------------
    def _parse_socratic_response(self, response: str) -> Dict:
        sections = {
            'questions': 'GUIDING QUESTIONS:',
            'reflections': 'REFLECTION PROMPTS:',
            'challenges': 'CHALLENGE POINTS:',
            'next_steps': 'NEXT STEPS:'
        }
        parsed = {}
        for key, header in sections.items():
            if header in response:
                content = response.split(header)[1].split('\n\n')[0]
                parsed[key] = [line.strip('-•* ') for line in content.split('\n') if line.strip()]
            else:
                parsed[key] = []
        return parsed

    def _parse_template_response(self, response: str, template_type: str) -> Dict:
        return {'template': {'raw': response}, 'guide': '', 'tips': []}


# --------------------------
# Convenience functions
# --------------------------
def get_critical_thinking_guidance(problem: str, context: Optional[str] = None) -> Dict:
    mentor = AIMentor()
    return mentor.critical_thinking_mode(problem, context)


def get_solution_template(problem: str, template_type: str = 'auto', category: Optional[str] = None) -> Dict:
    mentor = AIMentor()
    return mentor.solution_mode(problem, template_type, category)
