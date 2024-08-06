import json
from difflib import get_close_matches

# Constants
KNOWLEDGE_BASE_FILE = 'knowledge_base.json'

# Load the knowledge base from a JSON file
def load_knowledge_base(file_path: str) -> dict:
    """Loads the knowledge base from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"questions": []}

# Save the updated knowledge base to the JSON file
def save_knowledge_base(file_path: str, data: dict) -> None:
    """Saves the updated knowledge base to the JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Find the closest matching question
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    """Finds the closest matching question."""
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Get the answer for a question from the knowledge base
def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    """Gets the answer for a question from the knowledge base."""
    for q in knowledge_base["questions"]:
        if q["question"].lower() == question.lower():
            return q["answer"]
    return None

# Main function to handle user input and respond
def chatbot() -> None:
    """Main function to handle user input and respond."""
    knowledge_base = load_knowledge_base(KNOWLEDGE_BASE_FILE)

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'quit':
            break

        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            print(f"Bot: {answer}")
        else:
            print("Bot: I don't know the answer. Can you teach me?")
            new_answer = input("Type the answer or'skip' to skip: ")

            if new_answer.lower()!='skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base(KNOWLEDGE_BASE_FILE, knowledge_base)
                print("Bot: Thank you! I've learned something new.")

if __name__ == "__main__":
    chatbot()
