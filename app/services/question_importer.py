"""Question import service for bulk question upload via CSV/JSON."""
import csv
import json
from typing import List, Dict, Optional, Tuple
from io import StringIO
from sqlalchemy.orm import Session
from datetime import datetime
from app.models import Question, SectionEnum, DifficultyEnum, CorrectAnswerEnum


class QuestionImportError(Exception):
    """Custom exception for question import errors."""
    pass


class QuestionImporter:
    """Service for importing questions from CSV or JSON files."""

    # Required fields for question import
    REQUIRED_FIELDS = [
        'section', 'question_text', 'choice_a', 'choice_b',
        'choice_c', 'choice_d', 'correct_answer', 'difficulty'
    ]

    # Optional fields
    OPTIONAL_FIELDS = [
        'category', 'subcategory', 'topic', 'subtopic',
        'explanation', 'is_bluebook', 'passage_text', 'source_attribution'
    ]

    # Valid enum values
    VALID_SECTIONS = ['math', 'english']
    VALID_DIFFICULTIES = ['easy', 'medium', 'hard']
    VALID_ANSWERS = ['A', 'B', 'C', 'D']

    # English category mappings
    ENGLISH_CATEGORIES = {
        'craft_and_structure': ['cross_text_connections', 'text_structure_and_purpose', 'words_in_context'],
        'expression_of_ideas': ['rhetorical_synthesis', 'transitions'],
        'information_and_ideas': ['central_ideas_and_details', 'command_of_evidence', 'inferences'],
        'standard_english_conventions': ['boundaries', 'form_structure_and_sense']
    }

    @staticmethod
    def import_from_csv(csv_content: str, db: Session) -> Tuple[int, List[Dict]]:
        """
        Import questions from CSV content.

        Args:
            csv_content: CSV file content as string
            db: Database session

        Returns:
            Tuple of (success_count, error_list)
        """
        errors = []
        success_count = 0

        try:
            csv_file = StringIO(csv_content)
            reader = csv.DictReader(csv_file)

            if not reader.fieldnames:
                raise QuestionImportError("CSV file is empty or invalid")

            # Validate headers
            missing_fields = set(QuestionImporter.REQUIRED_FIELDS) - set(reader.fieldnames)
            if missing_fields:
                raise QuestionImportError(f"Missing required fields: {', '.join(missing_fields)}")

            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                try:
                    question = QuestionImporter._parse_question_row(row, row_num)
                    db.add(question)
                    success_count += 1
                except Exception as e:
                    errors.append({
                        'row': row_num,
                        'error': str(e),
                        'data': row
                    })

            if success_count > 0:
                db.commit()

        except QuestionImportError as e:
            raise e
        except Exception as e:
            raise QuestionImportError(f"CSV parsing error: {str(e)}")

        return success_count, errors

    @staticmethod
    def import_from_json(json_content: str, db: Session) -> Tuple[int, List[Dict]]:
        """
        Import questions from JSON content.

        Args:
            json_content: JSON file content as string
            db: Database session

        Returns:
            Tuple of (success_count, error_list)
        """
        errors = []
        success_count = 0

        try:
            data = json.loads(json_content)

            if not isinstance(data, list):
                raise QuestionImportError("JSON must be an array of question objects")

            for idx, item in enumerate(data, start=1):
                try:
                    question = QuestionImporter._parse_question_dict(item, idx)
                    db.add(question)
                    success_count += 1
                except Exception as e:
                    errors.append({
                        'index': idx,
                        'error': str(e),
                        'data': item
                    })

            if success_count > 0:
                db.commit()

        except json.JSONDecodeError as e:
            raise QuestionImportError(f"Invalid JSON format: {str(e)}")
        except QuestionImportError as e:
            raise e
        except Exception as e:
            raise QuestionImportError(f"JSON parsing error: {str(e)}")

        return success_count, errors

    @staticmethod
    def _parse_question_row(row: Dict, row_num: int) -> Question:
        """Parse a CSV row into a Question object."""
        try:
            # Validate required fields
            for field in QuestionImporter.REQUIRED_FIELDS:
                if not row.get(field) or not row[field].strip():
                    raise ValueError(f"Missing or empty required field: {field}")

            # Validate section
            section = row['section'].strip().lower()
            if section not in QuestionImporter.VALID_SECTIONS:
                raise ValueError(f"Invalid section: {section}. Must be one of {QuestionImporter.VALID_SECTIONS}")

            # Validate difficulty
            difficulty = row['difficulty'].strip().lower()
            if difficulty not in QuestionImporter.VALID_DIFFICULTIES:
                raise ValueError(f"Invalid difficulty: {difficulty}. Must be one of {QuestionImporter.VALID_DIFFICULTIES}")

            # Validate correct answer
            correct_answer = row['correct_answer'].strip().upper()
            if correct_answer not in QuestionImporter.VALID_ANSWERS:
                raise ValueError(f"Invalid correct answer: {correct_answer}. Must be one of {QuestionImporter.VALID_ANSWERS}")

            # Build choices array
            choices = [
                row['choice_a'].strip(),
                row['choice_b'].strip(),
                row['choice_c'].strip(),
                row['choice_d'].strip()
            ]

            # Validate category/subcategory for English
            category = row.get('category', '').strip() or None
            subcategory = row.get('subcategory', '').strip() or None

            if section == 'english' and category:
                QuestionImporter._validate_english_hierarchy(category, subcategory)

            # Parse is_bluebook
            is_bluebook = QuestionImporter._parse_bool(row.get('is_bluebook', 'false'))

            # Create question object
            question = Question(
                section=SectionEnum(section),
                topic=row.get('topic', '').strip() or None,
                subtopic=row.get('subtopic', '').strip() or None,
                category=category,
                subcategory=subcategory,
                difficulty=DifficultyEnum(difficulty),
                question_text=row['question_text'].strip(),
                choices=choices,
                correct_answer=CorrectAnswerEnum(correct_answer),
                explanation=row.get('explanation', '').strip() or None,
                is_bluebook=is_bluebook,
                passage_text=row.get('passage_text', '').strip() or None,
                source_attribution=row.get('source_attribution', '').strip() or None,
                created_at=datetime.utcnow()
            )

            return question

        except Exception as e:
            raise ValueError(f"Row {row_num}: {str(e)}")

    @staticmethod
    def _parse_question_dict(data: Dict, index: int) -> Question:
        """Parse a JSON dictionary into a Question object."""
        try:
            # Validate required fields
            for field in QuestionImporter.REQUIRED_FIELDS:
                if field not in data or not str(data[field]).strip():
                    # Handle choice fields specially
                    if field.startswith('choice_'):
                        if 'choices' not in data or not isinstance(data['choices'], list) or len(data['choices']) != 4:
                            raise ValueError(f"Missing or invalid 'choices' array (must have 4 items)")
                    else:
                        raise ValueError(f"Missing or empty required field: {field}")

            # Get section
            section = str(data['section']).strip().lower()
            if section not in QuestionImporter.VALID_SECTIONS:
                raise ValueError(f"Invalid section: {section}")

            # Get difficulty
            difficulty = str(data['difficulty']).strip().lower()
            if difficulty not in QuestionImporter.VALID_DIFFICULTIES:
                raise ValueError(f"Invalid difficulty: {difficulty}")

            # Get correct answer
            correct_answer = str(data['correct_answer']).strip().upper()
            if correct_answer not in QuestionImporter.VALID_ANSWERS:
                raise ValueError(f"Invalid correct answer: {correct_answer}")

            # Get choices (support both array and separate fields)
            if 'choices' in data and isinstance(data['choices'], list):
                if len(data['choices']) != 4:
                    raise ValueError("Choices array must have exactly 4 items")
                choices = [str(c).strip() for c in data['choices']]
            else:
                choices = [
                    str(data['choice_a']).strip(),
                    str(data['choice_b']).strip(),
                    str(data['choice_c']).strip(),
                    str(data['choice_d']).strip()
                ]

            # Get category/subcategory
            category = data.get('category', '').strip() or None
            subcategory = data.get('subcategory', '').strip() or None

            if section == 'english' and category:
                QuestionImporter._validate_english_hierarchy(category, subcategory)

            # Parse is_bluebook
            is_bluebook = QuestionImporter._parse_bool(data.get('is_bluebook', False))

            # Create question
            question = Question(
                section=SectionEnum(section),
                topic=data.get('topic', '').strip() or None,
                subtopic=data.get('subtopic', '').strip() or None,
                category=category,
                subcategory=subcategory,
                difficulty=DifficultyEnum(difficulty),
                question_text=str(data['question_text']).strip(),
                choices=choices,
                correct_answer=CorrectAnswerEnum(correct_answer),
                explanation=data.get('explanation', '').strip() or None,
                is_bluebook=is_bluebook,
                passage_text=data.get('passage_text', '').strip() or None,
                source_attribution=data.get('source_attribution', '').strip() or None,
                created_at=datetime.utcnow()
            )

            return question

        except Exception as e:
            raise ValueError(f"Item {index}: {str(e)}")

    @staticmethod
    def _validate_english_hierarchy(category: str, subcategory: Optional[str]):
        """Validate that category and subcategory match SAT English hierarchy."""
        if not category:
            return

        category_lower = category.lower().replace(' ', '_')

        if category_lower not in QuestionImporter.ENGLISH_CATEGORIES:
            raise ValueError(f"Invalid English category: {category}")

        if subcategory:
            subcategory_lower = subcategory.lower().replace(' ', '_')
            valid_subcategories = QuestionImporter.ENGLISH_CATEGORIES[category_lower]

            if subcategory_lower not in valid_subcategories:
                raise ValueError(
                    f"Invalid subcategory '{subcategory}' for category '{category}'. "
                    f"Valid options: {', '.join(valid_subcategories)}"
                )

    @staticmethod
    def _parse_bool(value) -> bool:
        """Parse various boolean representations."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in ['true', '1', 'yes', 'y']
        if isinstance(value, int):
            return value == 1
        return False

    @staticmethod
    def get_csv_template() -> str:
        """Generate a CSV template for question import."""
        headers = QuestionImporter.REQUIRED_FIELDS + QuestionImporter.OPTIONAL_FIELDS

        example_row = {
            'section': 'english',
            'question_text': 'Which of the following best describes the author\'s main argument?',
            'choice_a': 'Option A',
            'choice_b': 'Option B',
            'choice_c': 'Option C',
            'choice_d': 'Option D',
            'correct_answer': 'A',
            'difficulty': 'medium',
            'category': 'information_and_ideas',
            'subcategory': 'central_ideas_and_details',
            'topic': 'Reading Comprehension',
            'subtopic': 'Main Idea',
            'explanation': 'The correct answer is A because...',
            'is_bluebook': 'true',
            'passage_text': 'The passage text goes here...',
            'source_attribution': 'Author Name, Work Title'
        }

        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        writer.writerow(example_row)

        return output.getvalue()

    @staticmethod
    def get_json_template() -> str:
        """Generate a JSON template for question import."""
        template = [
            {
                'section': 'english',
                'question_text': 'Which of the following best describes the author\'s main argument?',
                'choices': ['Option A', 'Option B', 'Option C', 'Option D'],
                'correct_answer': 'A',
                'difficulty': 'medium',
                'category': 'information_and_ideas',
                'subcategory': 'central_ideas_and_details',
                'topic': 'Reading Comprehension',
                'subtopic': 'Main Idea',
                'explanation': 'The correct answer is A because...',
                'is_bluebook': True,
                'passage_text': 'The passage text goes here...',
                'source_attribution': 'Author Name, Work Title'
            },
            {
                'section': 'math',
                'question_text': 'What is 2 + 2?',
                'choices': ['3', '4', '5', '6'],
                'correct_answer': 'B',
                'difficulty': 'easy',
                'category': 'algebra',
                'explanation': 'Basic addition',
                'is_bluebook': False
            }
        ]


        return json.dumps(template, indent=2)
