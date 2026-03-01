"""
Seed script to populate the database with sample SAT questions.
This creates realistic SAT-style questions for development and testing.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db import SessionLocal
from app.models import Question, SectionEnum, DifficultyEnum, CorrectAnswerEnum


def create_sample_questions():
    """Create sample SAT questions across all sections."""

    questions = [
        # MATH - Algebra (Easy)
        {
            "section": SectionEnum.MATH,
            "topic": "Algebra",
            "subtopic": "Linear Equations",
            "difficulty": DifficultyEnum.EASY,
            "question_text": "If 3x + 5 = 20, what is the value of x?",
            "choices": ["3", "5", "7", "15"],
            "correct_answer": CorrectAnswerEnum.B,
            "explanation": "Solve for x: 3x + 5 = 20, so 3x = 15, and x = 5."
        },
        {
            "section": SectionEnum.MATH,
            "topic": "Algebra",
            "subtopic": "Linear Equations",
            "difficulty": DifficultyEnum.EASY,
            "question_text": "What is the value of y in the equation 2y - 8 = 14?",
            "choices": ["6", "11", "22", "3"],
            "correct_answer": CorrectAnswerEnum.B,
            "explanation": "2y = 22, so y = 11."
        },
        {
            "section": SectionEnum.MATH,
            "topic": "Algebra",
            "subtopic": "Expressions",
            "difficulty": DifficultyEnum.EASY,
            "question_text": "Simplify: 4(x + 3) - 2x",
            "choices": ["2x + 12", "2x + 3", "6x + 12", "2x + 7"],
            "correct_answer": CorrectAnswerEnum.A,
            "explanation": "4x + 12 - 2x = 2x + 12"
        },

        # MATH - Algebra (Medium)
        {
            "section": SectionEnum.MATH,
            "topic": "Algebra",
            "subtopic": "Quadratic Equations",
            "difficulty": DifficultyEnum.MEDIUM,
            "question_text": "If x² - 5x + 6 = 0, what are the possible values of x?",
            "choices": ["1 and 6", "2 and 3", "-2 and -3", "5 and 1"],
            "correct_answer": CorrectAnswerEnum.B,
            "explanation": "Factor: (x - 2)(x - 3) = 0, so x = 2 or x = 3."
        },
        {
            "section": SectionEnum.MATH,
            "topic": "Algebra",
            "subtopic": "Systems of Equations",
            "difficulty": DifficultyEnum.MEDIUM,
            "question_text": "If x + y = 10 and x - y = 4, what is the value of x?",
            "choices": ["3", "7", "6", "14"],
            "correct_answer": CorrectAnswerEnum.B,
            "explanation": "Add equations: 2x = 14, so x = 7."
        },

        # MATH - Geometry (Easy)
        {
            "section": SectionEnum.MATH,
            "topic": "Geometry",
            "subtopic": "Area and Perimeter",
            "difficulty": DifficultyEnum.EASY,
            "question_text": "What is the area of a rectangle with length 8 and width 5?",
            "choices": ["13", "26", "40", "80"],
            "correct_answer": CorrectAnswerEnum.C,
            "explanation": "Area = length × width = 8 × 5 = 40"
        },
        {
            "section": SectionEnum.MATH,
            "topic": "Geometry",
            "subtopic": "Angles",
            "difficulty": DifficultyEnum.EASY,
            "question_text": "If two angles are supplementary and one measures 110°, what is the measure of the other angle?",
            "choices": ["70°", "80°", "90°", "250°"],
            "correct_answer": CorrectAnswerEnum.A,
            "explanation": "Supplementary angles add to 180°. 180° - 110° = 70°"
        },

        # MATH - Geometry (Medium)
        {
            "section": SectionEnum.MATH,
            "topic": "Geometry",
            "subtopic": "Circles",
            "difficulty": DifficultyEnum.MEDIUM,
            "question_text": "What is the circumference of a circle with radius 7? (Use π ≈ 3.14)",
            "choices": ["21.98", "43.96", "153.86", "14"],
            "correct_answer": CorrectAnswerEnum.B,
            "explanation": "Circumference = 2πr = 2 × 3.14 × 7 = 43.96"
        },
        {
            "section": SectionEnum.MATH,
            "topic": "Geometry",
            "subtopic": "Triangles",
            "difficulty": DifficultyEnum.MEDIUM,
            "question_text": "In a right triangle, if one leg is 3 and the other leg is 4, what is the length of the hypotenuse?",
            "choices": ["5", "7", "12", "25"],
            "correct_answer": CorrectAnswerEnum.A,
            "explanation": "Use Pythagorean theorem: 3² + 4² = c², so c = 5"
        },

        # MATH - Statistics (Easy)
        {
            "section": SectionEnum.MATH,
            "topic": "Statistics",
            "subtopic": "Mean",
            "difficulty": DifficultyEnum.EASY,
            "question_text": "What is the mean of 5, 10, 15, and 20?",
            "choices": ["10", "12.5", "15", "50"],
            "correct_answer": CorrectAnswerEnum.B,
            "explanation": "Mean = (5 + 10 + 15 + 20) / 4 = 50 / 4 = 12.5"
        },

        # MATH - Statistics (Medium)
        {
            "section": SectionEnum.MATH,
            "topic": "Statistics",
            "subtopic": "Probability",
            "difficulty": DifficultyEnum.MEDIUM,
            "question_text": "A bag contains 3 red balls and 7 blue balls. What is the probability of drawing a red ball?",
            "choices": ["0.3", "0.7", "3", "7"],
            "correct_answer": CorrectAnswerEnum.A,
            "explanation": "Probability = 3/10 = 0.3"
        },

        # MATH - Hard Questions
        {
            "section": SectionEnum.MATH,
            "topic": "Algebra",
            "subtopic": "Functions",
            "difficulty": DifficultyEnum.HARD,
            "question_text": "If f(x) = 2x² - 3x + 1, what is f(3)?",
            "choices": ["10", "11", "12", "13"],
            "correct_answer": CorrectAnswerEnum.A,
            "explanation": "f(3) = 2(3²) - 3(3) + 1 = 18 - 9 + 1 = 10"
        },
        {
            "section": SectionEnum.MATH,
            "topic": "Geometry",
            "subtopic": "Volume",
            "difficulty": DifficultyEnum.HARD,
            "question_text": "What is the volume of a cylinder with radius 3 and height 10? (Use π ≈ 3.14)",
            "choices": ["94.2", "188.4", "282.6", "942"],
            "correct_answer": CorrectAnswerEnum.C,
            "explanation": "Volume = πr²h = 3.14 × 9 × 10 = 282.6"
        },

        # READING - Comprehension (Easy)
        {
            "section": SectionEnum.READING,
            "topic": "Reading Comprehension",
            "subtopic": "Main Idea",
            "difficulty": DifficultyEnum.EASY,
            "question_text": "The passage primarily discusses the importance of regular exercise for maintaining health. What is the main idea?",
            "choices": [
                "Exercise is expensive",
                "Regular exercise promotes health",
                "Health is not important",
                "Exercise is difficult"
            ],
            "correct_answer": CorrectAnswerEnum.B,
            "explanation": "The passage's main focus is on exercise promoting health."
        },
        {
            "section": SectionEnum.READING,
            "topic": "Reading Comprehension",
            "subtopic": "Details",
            "difficulty": DifficultyEnum.EASY,
            "question_text": "According to the passage, renewable energy sources include solar, wind, and hydroelectric power. Which is NOT mentioned?",
            "choices": ["Solar", "Nuclear", "Wind", "Hydroelectric"],
            "correct_answer": CorrectAnswerEnum.B,
            "explanation": "Nuclear is not mentioned in the list of renewable sources."
        },

        # READING - Comprehension (Medium)
        {
            "section": SectionEnum.READING,
            "topic": "Reading Comprehension",
            "subtopic": "Inference",
            "difficulty": DifficultyEnum.MEDIUM,
            "question_text": "The author describes the character as 'reluctant yet determined.' What can we infer about the character?",
            "choices": [
                "They are lazy",
                "They face challenges but persist",
                "They give up easily",
                "They are always confident"
            ],
            "correct_answer": CorrectAnswerEnum.B,
            "explanation": "Reluctant yet determined suggests facing challenges but continuing."
        },
        {
            "section": SectionEnum.READING,
            "topic": "Reading Comprehension",
            "subtopic": "Author's Purpose",
            "difficulty": DifficultyEnum.MEDIUM,
            "question_text": "The passage uses statistics and expert opinions to support its argument. What is the author's purpose?",
            "choices": [
                "To entertain",
                "To persuade with evidence",
                "To confuse",
                "To describe emotions"
            ],
            "correct_answer": CorrectAnswerEnum.B,
            "explanation": "Using statistics and expert opinions indicates persuasive intent."
        },

        # READING - Vocabulary (Easy)
        {
            "section": SectionEnum.READING,
            "topic": "Vocabulary",
            "subtopic": "Context Clues",
            "difficulty": DifficultyEnum.EASY,
            "question_text": "In the sentence 'The benevolent donor gave generously to charity,' what does 'benevolent' mean?",
            "choices": ["Cruel", "Kind", "Wealthy", "Famous"],
            "correct_answer": CorrectAnswerEnum.B,
            "explanation": "Context of generous giving suggests kindness."
        },
        {
            "section": SectionEnum.READING,
            "topic": "Vocabulary",
            "subtopic": "Word Meaning",
            "difficulty": DifficultyEnum.EASY,
            "question_text": "'Meticulous' most nearly means:",
            "choices": ["Careless", "Careful and precise", "Fast", "Lazy"],
            "correct_answer": CorrectAnswerEnum.B,
            "explanation": "Meticulous means showing great attention to detail."
        },

        # READING - Medium to Hard
        {
            "section": SectionEnum.READING,
            "topic": "Reading Comprehension",
            "subtopic": "Tone",
            "difficulty": DifficultyEnum.MEDIUM,
            "question_text": "The author's tone in describing the historical event is somber and reflective. This suggests:",
            "choices": [
                "Celebration",
                "Serious contemplation",
                "Humor",
                "Indifference"
            ],
            "correct_answer": CorrectAnswerEnum.B,
            "explanation": "Somber and reflective indicate serious, thoughtful tone."
        },
        {
            "section": SectionEnum.READING,
            "topic": "Reading Comprehension",
            "subtopic": "Structure",
            "difficulty": DifficultyEnum.HARD,
            "question_text": "The passage moves from general statements to specific examples. This structure serves to:",
            "choices": [
                "Confuse the reader",
                "Support the thesis with concrete evidence",
                "Contradict the main point",
                "Change the topic"
            ],
            "correct_answer": CorrectAnswerEnum.B,
            "explanation": "Moving from general to specific provides supporting evidence."
        },

        # WRITING - Grammar (Easy)
        {
            "section": SectionEnum.WRITING,
            "topic": "Grammar",
            "subtopic": "Subject-Verb Agreement",
            "difficulty": DifficultyEnum.EASY,
            "question_text": "Which sentence is correct?",
            "choices": [
                "The dogs runs in the park",
                "The dogs run in the park",
                "The dog run in the park",
                "The dogs running in the park"
            ],
            "correct_answer": CorrectAnswerEnum.B,
            "explanation": "Plural subject 'dogs' requires plural verb 'run'."
        },
        {
            "section": SectionEnum.WRITING,
            "topic": "Grammar",
            "subtopic": "Pronoun Usage",
            "difficulty": DifficultyEnum.EASY,
            "question_text": "Choose the correct sentence:",
            "choices": [
                "Me and John went to the store",
                "John and me went to the store",
                "John and I went to the store",
                "I and John went to the store"
            ],
            "correct_answer": CorrectAnswerEnum.C,
            "explanation": "'John and I' is correct as the subject of the sentence."
        },

        # WRITING - Grammar (Medium)
        {
            "section": SectionEnum.WRITING,
            "topic": "Grammar",
            "subtopic": "Verb Tense",
            "difficulty": DifficultyEnum.MEDIUM,
            "question_text": "Which sentence maintains consistent verb tense?",
            "choices": [
                "She walked to school and sees her friend",
                "She walks to school and saw her friend",
                "She walked to school and saw her friend",
                "She walking to school and saw her friend"
            ],
            "correct_answer": CorrectAnswerEnum.C,
            "explanation": "Both verbs are in past tense: walked and saw."
        },
        {
            "section": SectionEnum.WRITING,
            "topic": "Grammar",
            "subtopic": "Modifiers",
            "difficulty": DifficultyEnum.MEDIUM,
            "question_text": "Which sentence has correct modifier placement?",
            "choices": [
                "Running quickly, the bus was missed by Tom",
                "Tom missed the bus running quickly",
                "Running quickly, Tom missed the bus",
                "The bus was missed running quickly by Tom"
            ],
            "correct_answer": CorrectAnswerEnum.C,
            "explanation": "The modifier 'running quickly' correctly modifies Tom."
        },

        # WRITING - Punctuation (Easy)
        {
            "section": SectionEnum.WRITING,
            "topic": "Punctuation",
            "subtopic": "Commas",
            "difficulty": DifficultyEnum.EASY,
            "question_text": "Which sentence uses commas correctly?",
            "choices": [
                "I bought apples oranges and bananas",
                "I bought, apples, oranges, and bananas",
                "I bought apples, oranges, and bananas",
                "I bought apples oranges, and bananas"
            ],
            "correct_answer": CorrectAnswerEnum.C,
            "explanation": "Items in a list should be separated by commas."
        },

        # WRITING - Rhetoric (Medium)
        {
            "section": SectionEnum.WRITING,
            "topic": "Rhetoric",
            "subtopic": "Sentence Combining",
            "difficulty": DifficultyEnum.MEDIUM,
            "question_text": "Which option best combines: 'The storm was fierce. It lasted all night.'?",
            "choices": [
                "The storm was fierce it lasted all night",
                "The storm was fierce, and it lasted all night",
                "The storm was fierce it lasting all night",
                "Being fierce the storm lasted all night"
            ],
            "correct_answer": CorrectAnswerEnum.B,
            "explanation": "Comma and coordinating conjunction properly join the clauses."
        },
        {
            "section": SectionEnum.WRITING,
            "topic": "Rhetoric",
            "subtopic": "Transitions",
            "difficulty": DifficultyEnum.MEDIUM,
            "question_text": "Choose the best transition: 'The experiment failed. ____, we learned valuable lessons.'",
            "choices": ["Therefore", "However", "Similarly", "Meanwhile"],
            "correct_answer": CorrectAnswerEnum.B,
            "explanation": "'However' shows contrast between failure and learning."
        },

        # WRITING - Hard
        {
            "section": SectionEnum.WRITING,
            "topic": "Grammar",
            "subtopic": "Parallel Structure",
            "difficulty": DifficultyEnum.HARD,
            "question_text": "Which sentence demonstrates correct parallel structure?",
            "choices": [
                "She likes reading, to write, and painting",
                "She likes reading, writing, and to paint",
                "She likes reading, writing, and painting",
                "She likes to read, writing, and painting"
            ],
            "correct_answer": CorrectAnswerEnum.C,
            "explanation": "All items in the list are gerunds: reading, writing, painting."
        },
        {
            "section": SectionEnum.WRITING,
            "topic": "Rhetoric",
            "subtopic": "Style",
            "difficulty": DifficultyEnum.HARD,
            "question_text": "Which revision best improves conciseness? Original: 'Due to the fact that it was raining, we stayed inside.'",
            "choices": [
                "Because it was raining, we stayed inside",
                "Due to rain, we stayed inside",
                "It was raining so we stayed inside",
                "We stayed inside it was raining"
            ],
            "correct_answer": CorrectAnswerEnum.A,
            "explanation": "'Because' is more concise than 'due to the fact that'."
        },
    ]

    return questions


def seed_database():
    """Seed the database with sample questions."""
    db = SessionLocal()

    try:
        # Check if questions already exist
        existing_count = db.query(Question).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} questions.")
            response = input("Do you want to add more sample questions? (y/n): ")
            if response.lower() != 'y':
                print("Seeding cancelled.")
                return

        # Create questions
        questions = create_sample_questions()
        for q_data in questions:
            question = Question(**q_data)
            db.add(question)

        db.commit()
        print(f"\n✅ Successfully seeded {len(questions)} sample questions!")

        # Print summary
        math_count = sum(1 for q in questions if q["section"] == SectionEnum.MATH)
        reading_count = sum(1 for q in questions if q["section"] == SectionEnum.READING)
        writing_count = sum(1 for q in questions if q["section"] == SectionEnum.WRITING)

        print(f"\nBreakdown:")
        print(f"  Math: {math_count} questions")
        print(f"  Reading: {reading_count} questions")
        print(f"  Writing: {writing_count} questions")

        easy_count = sum(1 for q in questions if q["difficulty"] == DifficultyEnum.EASY)
        medium_count = sum(1 for q in questions if q["difficulty"] == DifficultyEnum.MEDIUM)
        hard_count = sum(1 for q in questions if q["difficulty"] == DifficultyEnum.HARD)

        print(f"\nDifficulty:")
        print(f"  Easy: {easy_count} questions")
        print(f"  Medium: {medium_count} questions")
        print(f"  Hard: {hard_count} questions")

    except Exception as e:
        print(f"❌ Error seeding database: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Starting database seed...")
    seed_database()
