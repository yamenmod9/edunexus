"""
Seed sample SAT questions for testing the Question Bank feature.
"""
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.question import Question, SectionEnum, DifficultyEnum, CorrectAnswerEnum


SAMPLE_QUESTIONS = [
    # English - Craft and Structure - Words in Context
    {
        "section": SectionEnum.ENGLISH,
        "category": "craft_and_structure",
        "subcategory": "words_in_context",
        "difficulty": DifficultyEnum.EASY,
        "question_text": "In context, which word best replaces 'ubiquitous' in the following sentence: The smartphone has become ubiquitous in modern society.",
        "choices": ["rare", "expensive", "everywhere", "outdated"],
        "correct_answer": CorrectAnswerEnum.C,
        "explanation": "'Ubiquitous' means present everywhere at once. Therefore, 'everywhere' is the best replacement.",
        "is_bluebook": True,
        "topic": "Reading",
        "subtopic": "Vocabulary"
    },
    {
        "section": SectionEnum.ENGLISH,
        "category": "craft_and_structure",
        "subcategory": "words_in_context",
        "difficulty": DifficultyEnum.MEDIUM,
        "question_text": "As used in line 12, 'tempered' most nearly means:",
        "choices": ["angered", "moderated", "heated", "destroyed"],
        "correct_answer": CorrectAnswerEnum.B,
        "explanation": "In this context, 'tempered' means to moderate or make less extreme.",
        "is_bluebook": False,
        "topic": "Reading",
        "subtopic": "Vocabulary"
    },

    # English - Craft and Structure - Text Structure and Purpose
    {
        "section": SectionEnum.ENGLISH,
        "category": "craft_and_structure",
        "subcategory": "text_structure_and_purpose",
        "difficulty": DifficultyEnum.MEDIUM,
        "question_text": "The primary purpose of the second paragraph is to:",
        "choices": [
            "provide historical context",
            "introduce a counterargument",
            "present statistical evidence",
            "describe a personal anecdote"
        ],
        "correct_answer": CorrectAnswerEnum.A,
        "explanation": "The paragraph discusses the historical background necessary to understand the main argument.",
        "is_bluebook": True,
        "topic": "Reading",
        "subtopic": "Structure"
    },

    # English - Information and Ideas - Central Ideas and Details
    {
        "section": SectionEnum.ENGLISH,
        "category": "information_and_ideas",
        "subcategory": "central_ideas_and_details",
        "difficulty": DifficultyEnum.EASY,
        "question_text": "According to the passage, photosynthesis primarily occurs in which part of the plant?",
        "choices": ["roots", "stems", "leaves", "flowers"],
        "correct_answer": CorrectAnswerEnum.C,
        "explanation": "The passage explicitly states that photosynthesis mainly occurs in the leaves where chlorophyll is concentrated.",
        "is_bluebook": False,
        "passage_text": "Photosynthesis is the process by which plants convert light energy into chemical energy. This process primarily takes place in the leaves, where chlorophyll captures sunlight.",
        "topic": "Reading",
        "subtopic": "Main Ideas"
    },
    {
        "section": SectionEnum.ENGLISH,
        "category": "information_and_ideas",
        "subcategory": "command_of_evidence",
        "difficulty": DifficultyEnum.HARD,
        "question_text": "Which choice provides the best evidence for the answer to the previous question?",
        "choices": [
            "Lines 1-3 ('Photosynthesis...energy')",
            "Lines 4-6 ('This process...chlorophyll')",
            "Lines 8-10 ('The roots...nutrients')",
            "Lines 12-14 ('Scientists believe...efficiency')"
        ],
        "correct_answer": CorrectAnswerEnum.B,
        "explanation": "Lines 4-6 directly state where photosynthesis occurs, providing the strongest evidence.",
        "is_bluebook": True,
        "topic": "Reading",
        "subtopic": "Evidence"
    },

    # English - Standard English Conventions - Boundaries
    {
        "section": SectionEnum.ENGLISH,
        "category": "standard_english_conventions",
        "subcategory": "boundaries",
        "difficulty": DifficultyEnum.EASY,
        "question_text": "Which choice correctly punctuates the following sentence?\nThe students studied for hours they were determined to succeed.",
        "choices": [
            "hours they",
            "hours, they",
            "hours; they",
            "hours: they"
        ],
        "correct_answer": CorrectAnswerEnum.C,
        "explanation": "A semicolon correctly joins two independent clauses without a coordinating conjunction.",
        "is_bluebook": False,
        "topic": "Writing",
        "subtopic": "Punctuation"
    },
    {
        "section": SectionEnum.ENGLISH,
        "category": "standard_english_conventions",
        "subcategory": "form_structure_and_sense",
        "difficulty": DifficultyEnum.MEDIUM,
        "question_text": "The committee members ____ to meet every Tuesday.",
        "choices": ["decides", "decide", "deciding", "to decide"],
        "correct_answer": CorrectAnswerEnum.B,
        "explanation": "'Committee members' is plural, requiring the plural verb form 'decide'.",
        "is_bluebook": True,
        "topic": "Writing",
        "subtopic": "Grammar"
    },

    # English - Expression of Ideas - Transitions
    {
        "section": SectionEnum.ENGLISH,
        "category": "expression_of_ideas",
        "subcategory": "transitions",
        "difficulty": DifficultyEnum.MEDIUM,
        "question_text": "Which transition word best connects these two sentences?\nThe experiment was carefully planned. ____ the results were unexpected.",
        "choices": ["Therefore,", "However,", "Similarly,", "Consequently,"],
        "correct_answer": CorrectAnswerEnum.B,
        "explanation": "'However' correctly indicates a contrast between careful planning and unexpected results.",
        "is_bluebook": True,
        "topic": "Writing",
        "subtopic": "Transitions"
    },
    {
        "section": SectionEnum.ENGLISH,
        "category": "expression_of_ideas",
        "subcategory": "rhetorical_synthesis",
        "difficulty": DifficultyEnum.HARD,
        "question_text": "The writer wants to add a sentence that emphasizes the significance of the discovery. Which choice best accomplishes this goal?",
        "choices": [
            "Many scientists worked on this project.",
            "The discovery was made in 2020.",
            "This finding could revolutionize our understanding of climate change.",
            "The research was funded by a grant."
        ],
        "correct_answer": CorrectAnswerEnum.C,
        "explanation": "This choice directly emphasizes the significance by explaining the potential impact.",
        "is_bluebook": False,
        "topic": "Writing",
        "subtopic": "Rhetoric"
    },

    # Math - Algebra
    {
        "section": SectionEnum.MATH,
        "category": "algebra",
        "subcategory": "linear_equations",
        "difficulty": DifficultyEnum.EASY,
        "question_text": "If 2x + 5 = 13, what is the value of x?",
        "choices": ["2", "3", "4", "5"],
        "correct_answer": CorrectAnswerEnum.C,
        "explanation": "Solving: 2x + 5 = 13, subtract 5: 2x = 8, divide by 2: x = 4",
        "is_bluebook": True,
        "topic": "Algebra",
        "subtopic": "Linear Equations"
    },
    {
        "section": SectionEnum.MATH,
        "category": "algebra",
        "subcategory": "linear_equations",
        "difficulty": DifficultyEnum.MEDIUM,
        "question_text": "If 3(x - 2) = 2(x + 1), what is x?",
        "choices": ["4", "6", "8", "10"],
        "correct_answer": CorrectAnswerEnum.C,
        "explanation": "Expand: 3x - 6 = 2x + 2, subtract 2x: x - 6 = 2, add 6: x = 8",
        "is_bluebook": False,
        "topic": "Algebra",
        "subtopic": "Linear Equations"
    },
]


def seed_questions(db: Session):
    """Seed sample questions into the database."""
    print("🌱 Seeding sample questions...")

    # Check if questions already exist
    existing_count = db.query(Question).count()
    if existing_count > 0:
        print(f"⚠️  Database already has {existing_count} questions. Skipping seed.")
        return

    # Add all sample questions
    questions_added = 0
    for q_data in SAMPLE_QUESTIONS:
        question = Question(**q_data)
        db.add(question)
        questions_added += 1

    db.commit()
    print(f"✅ Successfully seeded {questions_added} sample questions!")

    # Print summary
    english_count = db.query(Question).filter(Question.section == SectionEnum.ENGLISH).count()
    math_count = db.query(Question).filter(Question.section == SectionEnum.MATH).count()
    print(f"   - English: {english_count} questions")
    print(f"   - Math: {math_count} questions")


if __name__ == "__main__":
    # Run seed when script is executed directly
    db = next(get_db())
    try:
        seed_questions(db)
    finally:
        db.close()
