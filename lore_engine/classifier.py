import sys
sys.path.append('.') # Allow importing from parent directory

from lore_engine.agent import LorekeeperAgent

class ChapterClassifier:
    def __init__(self, agent: LorekeeperAgent):
        self.agent = agent
        # Define potential chapters
        self.chapters = ["Learning", "Challenges", "Dreams", "Achievements", "Reflections", "Ideas", "Daily Life"]

    def classify(self, text: str) -> str:
        # Craft a prompt for the agent to classify the text
        classification_prompt = f"Analyze the following text and classify it into one of the following chapters: {', '.join(self.chapters)}.\nRespond with ONLY the chapter name and nothing else.\nText: {text}"

        try:
            # Use the agent to get the classification
            response = self.agent.generate_response(classification_prompt, style='concise')
            # Clean up the response and check if it's a valid chapter
            classified_chapter = response.strip().replace('.', '').replace('"', '').replace("'", '')
            if classified_chapter in self.chapters:
                return classified_chapter
            else:
                # If the response isn't a direct match, try to find the closest one or default
                print(f"Warning: Agent returned unexpected classification '{classified_chapter}'. Defaulting to 'Reflections'.")
                return "Reflections" # Default chapter if classification fails
        except Exception as e:
            print(f"Error during classification: {e}")
            return "Reflections" # Default on error

# Example usage (for testing)
# if __name__ == '__main__':
#     agent = LorekeeperAgent()
#     classifier = ChapterClassifier(agent)
#     test_text = "Today I finally understood how recursion works. It was a breakthrough!"
#     chapter = classifier.classify(test_text)
#     print(f"Text: '{test_text}'\nClassified Chapter: {chapter}")

#     test_text_challenge = "I faced a major setback at work, but I'm determined to overcome it."
#     chapter_challenge = classifier.classify(test_text_challenge)
#     print(f"Text: '{test_text_challenge}'\nClassified Chapter: {chapter_challenge}")
