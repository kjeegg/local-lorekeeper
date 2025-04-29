import sys
sys.path.append('.') # Allow importing from parent directory

from lore_engine.agent import LorekeeperAgent, load_mood_styles

class MoodShaper:
    def __init__(self, agent: LorekeeperAgent):
        self.agent = agent
        self.mood_styles = load_mood_styles()

    def shape_text(self, text: str, mood: str = 'neutral', style: str = 'default') -> str:
        # Get the specific style instruction from the loaded styles
        style_instruction = self.mood_styles.get(style, self.mood_styles.get('default', ''))

        if not style_instruction:
             # If style not found and no default, just return original text
             print(f"Warning: Style '{style}' not found and no default style defined. Returning original text.")
             return text

        # Craft a prompt for the agent to reshape the text
        # Include the original text and the desired mood/style instruction
        shaping_prompt = f"Rewrite the following text to adopt a {mood} tone and {style} style.\nStyle Instruction: {style_instruction}\n\nOriginal Text:\n{text}"

        try:
            # Use the agent to reshape the text
            reshaped_text = self.agent.generate_response(shaping_prompt, mood=mood, style=style)
            return reshaped_text
        except Exception as e:
            print(f"Error during mood shaping: {e}")
            return "Error: Could not reshape text."

# Example usage (for testing)
# if __name__ == '__main__':
#     agent = LorekeeperAgent()
#     shaper = MoodShaper(agent)
#     original_text = "I had a difficult day at work."
#     # Example: Reshape to epic and melancholic
#     # epic_melancholic_text = shaper.shape_text(original_text, mood='melancholic', style='epic')
#     # print("\n--- Epic Melancholic ---\n", epic_melancholic_text)

#     # Example: Reshape to poetic and joyful
#     # poetic_joyful_text = shaper.shape_text("I saw a beautiful sunset.", mood='joyful', style='poetic')
#     # print("\n--- Poetic Joyful ---\n", poetic_joyful_text)
