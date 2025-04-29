import ollama
import json
import os

PROMPTS_DIR = 'prompts'
MOOD_STYLES_PATH = os.path.join(PROMPTS_DIR, 'mood_styles.json')
BASE_PROMPT_PATH = os.path.join(PROMPTS_DIR, 'base_prompt.txt')

def load_prompt(file_path):
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f'Error: Prompt file not found at {file_path}')
        return ''

def load_mood_styles():
    try:
        with open(MOOD_STYLES_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f'Error: Mood styles file not found at {MOOD_STYLES_PATH}')
        return {}
    except json.JSONDecodeError:
        print(f'Error: Could not decode JSON from {MOOD_STYLES_PATH}')
        return {}

class LorekeeperAgent:
    def __init__(self, model='mistral'):
        self.model = model
        self.base_prompt = load_prompt(BASE_PROMPT_PATH)
        self.mood_styles = load_mood_styles()

    def generate_response(self, user_input, context='', mood='neutral', style='default'):
        # Construct the full prompt including base prompt, context, mood, and user input
        # This is a simplified example; actual prompt engineering would be more complex
        # Using a single string for the prompt to avoid line continuation issues
        full_prompt = f"{self.base_prompt}\n\nContext: {context}\nMood: {mood}\nStyle: {style}\n\nUser Input: {user_input}"

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': self.base_prompt},
                    {'role': 'user', 'content': f"Context: {context}\nMood: {mood}\nStyle: {style}\n\nUser Input: {user_input}"}
                ]
            )
            return response['message']['content']
        except Exception as e:
            print(f'Error interacting with Ollama: {e}')
            return 'Error: Could not generate response from AI.'

# Example usage (for testing)
# if __name__ == '__main__':
#     agent = LorekeeperAgent()
#     response = agent.generate_response("Tell me about the time I learned to ride a bike.", context="Memory about learning bike riding.", mood="joyful", style="epic")
#     print(response)
