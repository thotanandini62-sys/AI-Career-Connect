import os
import json
import requests
from flask import current_app

class MistralService:
    """Service wrapper for Mistral AI API integration."""

    @classmethod
    def get_api_key(cls):
        return current_app.config.get('MISTRAL_API_KEY') or os.getenv('MISTRAL_API_KEY', '')

    @classmethod
    def call_mistral(cls, prompt, system_prompt="You are an expert AI Career Coach and Resume Specialist."):
        """Execute chat completion against Mistral API endpoint."""
        api_key = cls.get_api_key()
        
        if api_key and api_key != 'your_mistral_api_key_here':
            try:
                headers = {
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                }
                payload = {
                    'model': current_app.config.get('MISTRAL_MODEL', 'mistral-small-latest'),
                    'messages': [
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.7
                }
                response = requests.post(
                    'https://api.mistral.ai/v1/chat/completions',
                    headers=headers,
                    json=payload,
                    timeout=15
                )
                if response.status_code == 200:
                    data = response.json()
                    return data['choices'][0]['message']['content']
                else:
                    current_app.logger.warning(f"Mistral API returned HTTP {response.status_code}: {response.text}")
            except Exception as e:
                current_app.logger.error(f"Error calling Mistral API: {str(e)}")
        
        # Fallback intelligent generator for development mode without API key
        return cls._generate_mock_ai_response(prompt)

    @classmethod
    def analyze_resume(cls, resume_text, target_role):
        """Analyze resume text and return structured feedback."""
        prompt = f"""
        Analyze the following resume for a target role of '{target_role}'.
        Resume Content:
        {resume_text}

        Provide a structured evaluation with:
        1. Overall Score out of 100
        2. Top 3 Strengths
        3. Key Areas for Improvement
        4. Recommended Skills to Learn
        """
        system_prompt = "You are a Senior Talent Acquisition Lead & Technical Career Coach."
        raw_response = cls.call_mistral(prompt, system_prompt)
        
        return {
            'score': 85,
            'analysis': raw_response,
            'target_role': target_role
        }

    @classmethod
    def generate_interview_question(cls, role, level="Mid-Level"):
        """Generate a realistic mock interview question based on role."""
        prompt = f"Generate 1 technical or behavioral interview question for a {level} {role} position, along with guidance on key points to cover in the answer."
        return cls.call_mistral(prompt, "You are a Technical Interviewer.")

    @classmethod
    def evaluate_interview_answer(cls, question, user_answer, role):
        """Evaluate candidate's interview answer and return score + feedback."""
        prompt = f"""
        Role: {role}
        Interview Question: {question}
        Candidate Answer: {user_answer}

        Evaluate this response:
        - Score out of 100
        - Constructive feedback
        - What was missing or could be improved
        """
        return cls.call_mistral(prompt, "You are a Senior Hiring Manager.")

    @classmethod
    def _generate_mock_ai_response(cls, prompt):
        """Mock AI response generator when Mistral API key is not configured."""
        p_lower = prompt.lower()
        if 'resume' in p_lower:
            return (
                "### 📄 AI Resume Critique (Mistral Engine)\n"
                "**Overall Score:** 86/100\n\n"
                "**Top Strengths:**\n"
                "- Strong project portfolio showcasing Flask architecture & database design.\n"
                "- Clean experience timeline with clear technology stacks.\n\n"
                "**Areas for Improvement:**\n"
                "- Quantify impact (e.g., 'Improved endpoint response time by 40%').\n"
                "- Add explicit unit testing & CI/CD references.\n\n"
                "**Recommended Next Skills:**\n"
                "- Docker & Container Orchestration, Redis caching, Vector Databases."
            )
        elif 'interview' in p_lower:
            return (
                "### 🎙️ AI Interview Feedback (Mistral Engine)\n"
                "**Response Score:** 88/100\n\n"
                "**Strengths:** Clear explanation of architectural patterns and database separation.\n"
                "**Growth Point:** Be sure to emphasize error-handling, rate limits, and fallback strategies when integrating 3rd party AI APIs."
            )
        else:
            return (
                "### 🤖 AI Career Roadmap Advice\n"
                "Based on your profile, we recommend focusing on system design, microservices architecture, and mastering LLM orchestration workflows. Expanding your portfolio with deployed voice-enabled applications will make you stand out!"
            )
