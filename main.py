import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from json import loads

load_dotenv()

# Retrieve and configure Google Gemini API credentials
api_token = os.getenv("API_KEY") or os.getenv("GEMINI_API_KEY")

client = None
if api_token:
    client = genai.Client(api_key=api_token)
else:
    print("Warning: Missing GEMINI_API_KEY in environment. Using fallback data generator.")

def generate_quiz(topic, number_of_questions=10, difficulty="Medium"):
    if not client:
        return get_fallback_quiz_data(topic, number_of_questions)

    try:
        level = difficulty.lower()
        if level == "easy":
            difficulty_rules = """
            Difficulty Level: EASY.
            - Ensure questions are direct, beginner-friendly, and target core introductory knowledge.
            - Avoid tricky wording, syntax traps, or complex edge cases.
            """
        elif level == "hard":
            difficulty_rules = """
            Difficulty Level: HARD.
            - Questions should be challenging, requiring intermediate-to-advanced reasoning.
            - Focus on design patterns, optimization, decorators, scoping, or subtle mechanics.
            """
        else:
            difficulty_rules = """
            Difficulty Level: MEDIUM.
            - Questions should target intermediate skills and common practical situations.
            - Include standard classes, standard libraries, dictionary/list operations.
            """

        prompt_text = f"""
        Create a set of exactly {number_of_questions} unique multiple-choice questions about "{topic}".
        
        {difficulty_rules}
        
        Guidelines:
        1. Every question must have exactly 4 options: A, B, C, and D.
        2. Specify exactly one correct option letter ('A', 'B', 'C', or 'D').
        3. Make options mutually exclusive and distinct.
        
        Format the output strictly as a JSON array of objects with these exact keys:
        - "q": The question text.
        - "A": Choice A option.
        - "B": Choice B option.
        - "C": Choice C option.
        - "D": Choice D option.
        - "correct": The letter of the correct choice.
        
        Output raw JSON only. Do not wrap in markdown quotes.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=1.0
            )
        )

        return loads(response.text)

    except Exception as error:
        print(f"Gemini generation failed: {error}. Falling back.")
        try:
            raw_text = response.text
            if "```json" in raw_text:
                json_part = raw_text.split("```json")[1].split("```")[0].strip()
            else:
                json_part = raw_text.strip()
            return loads(json_part)
        except Exception:
            return get_fallback_quiz_data(topic, number_of_questions)

def get_fallback_quiz_data(topic, number_of_questions=5):
    fallback_set = [
        {
            "q": f"What is a primary concept related to {topic}?",
            "A": "The core methodology defining the subject",
            "B": "A secondary alternative application",
            "C": "An obsolete historical approach",
            "D": "A completely unrelated concept",
            "correct": "A"
        },
        {
            "q": f"Which of the following is a key challenge in implementing {topic}?",
            "A": "Lack of interest in the tech community",
            "B": "Scalability and data consistency issues",
            "C": "Excessive hardware requirements",
            "D": "Finding developers who understand it",
            "correct": "B"
        },
        {
            "q": f"How does {topic} benefit modern architectures?",
            "A": "By increasing manual tasks",
            "B": "By reducing system security",
            "C": "By improving efficiency, adaptability, and performance",
            "D": "By requiring more server infrastructure",
            "correct": "C"
        },
        {
            "q": f"Which component is most crucial for {topic}?",
            "A": "The user interface styling",
            "B": "The hosting provider's physical location",
            "C": "The backup storage mechanism",
            "D": "The core logic and data processing layer",
            "correct": "D"
        },
        {
            "q": f"How is {topic} most commonly deployed in production?",
            "A": "As a microservice or modular application component",
            "B": "As a single giant monolithic script",
            "C": "On local desktop computers only",
            "D": "Without any monitoring or error logging",
            "correct": "A"
        }
    ]

    extended_set = []
    while len(extended_set) < number_of_questions:
        extended_set.extend(fallback_set)
    return extended_set[:number_of_questions]