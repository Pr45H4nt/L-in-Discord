# get_response.py
import google.generativeai as genai
from config import gemini_token, prompt, askl_prompt
import time
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResponseHandler:
    def __init__(self):
        self.configure_api()
        self.last_request_time = 0
        self.min_request_interval = 1  # Minimum seconds between requests

    def configure_api(self):
        """Configure the Gemini API with the token"""
        genai.configure(api_key=gemini_token)
        self.primary_model = "gemini-1.5-pro"
        self.fallback_model = "gemini-pro"

    def rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()

    async def get_response(self, prompt_text: str, model_name: Optional[str] = None) -> str:
        """Get response from the API with error handling and retries"""
        self.rate_limit()
        model_name = model_name or self.primary_model
        
        tries = 3
        while tries > 0:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt_text)
                return response.text
            except ValueError as e:
                logger.warning(f"ValueError occurred: {e}. Tries remaining: {tries-1}")
                tries -= 1
                if tries == 0:
                    # Try fallback model on last attempt
                    try:
                        model = genai.GenerativeModel(self.fallback_model)
                        response = model.generate_content(prompt_text)
                        return response.text
                    except Exception as e:
                        logger.error(f"Final fallback attempt failed: {e}")
                        return "I seem to be... distracted. Try again in a moment."
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return "Something is... not quite right. Let me think about this."
            
            time.sleep(1)  # Brief pause between retries

handler = ResponseHandler()

async def general(history: list) -> str:
    """Handle general conversation responses"""
    conversation = "\n".join(history[-5:])  # Only use last 5 messages for context
    full_prompt = f"{prompt}\nChat History:\n{conversation}\nRespond as L."
    
    logger.info("Generating general response")
    return await handler.get_response(full_prompt)


async def askl(question_with_history: str) -> str:
    """Handle analysis questions"""
    full_prompt = f"{askl_prompt}\n{question_with_history}"
    
    logger.info("Generating analysis response")
    return await handler.get_response(full_prompt)
