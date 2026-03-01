"""
Test Script for SAT Score Calculator
Tests the score calculation logic directly
"""
import sys
sys.path.append('.')

from app.utils.score_calculator import SATScoreCalculator


def test_perfect_score():
    """Test perfect SAT score (1600)"""
    print("Test 1: Perfect Score")
    print("-" * 50)

    result = SATScoreCalculator.calculate_full_score(
        reading_correct=52,
        writing_correct=44,
        math_correct=58
    )

    print(f"Reading Correct: {result['reading_correct']}/52")
    print(f"Writing Correct: {result['writing_correct']}/44")
    print(f"Math Correct: {result['math_correct']}/58")
    print(f"Reading & Writing Score: {result['reading_writing_score']}/800")
    print(f"Math Score: {result['math_score']}/800")
    print(f"Total Score: {result['total_score']}/1600")
    print(f"Percentile: {result['percentile']}th")

    assert result['total_score'] == 1600, "Perfect score should be 1600"
    assert result['percentile'] == 99, "Perfect score should be 99th percentile"
    print("✅ Test 1 PASSED\n")


def test_average_score():
    """Test average SAT score (~1000)"""
    print("Test 2: Average Score")
    print("-" * 50)

    result = SATScoreCalculator.calculate_full_score(
        reading_correct=28,
        writing_correct=24,
        math_correct=32
    )

    print(f"Reading Correct: {result['reading_correct']}/52")
    print(f"Writing Correct: {result['writing_correct']}/44")
    print(f"Math Correct: {result['math_correct']}/58")
    print(f"Reading & Writing Score: {result['reading_writing_score']}/800")
    print(f"Math Score: {result['math_score']}/800")
    print(f"Total Score: {result['total_score']}/1600")
    print(f"Percentile: {result['percentile']}th")

    assert 900 <= result['total_score'] <= 1100, "Average score should be around 1000"
    print("✅ Test 2 PASSED\n")


def test_target_score():
    """Test target score (1400)"""
    print("Test 3: Target Score (1400)")
    print("-" * 50)

    result = SATScoreCalculator.calculate_full_score(
        reading_correct=48,
        writing_correct=40,
        math_correct=45
    )

    print(f"Reading Correct: {result['reading_correct']}/52")
    print(f"Writing Correct: {result['writing_correct']}/44")
    print(f"Math Correct: {result['math_correct']}/58")
    print(f"Reading & Writing Score: {result['reading_writing_score']}/800")
    print(f"Math Score: {result['math_score']}/800")
    print(f"Total Score: {result['total_score']}/1600")
    print(f"Percentile: {result['percentile']}th")

    assert 1300 <= result['total_score'] <= 1450, "Should be in target range"
    print("✅ Test 3 PASSED\n")


def test_minimum_score():
    """Test minimum SAT score (400)"""
    print("Test 4: Minimum Score")
    print("-" * 50)

    result = SATScoreCalculator.calculate_full_score(
        reading_correct=0,
        writing_correct=0,
        math_correct=0
    )

    print(f"Reading Correct: {result['reading_correct']}/52")
    print(f"Writing Correct: {result['writing_correct']}/44")
    print(f"Math Correct: {result['math_correct']}/58")
    print(f"Reading & Writing Score: {result['reading_writing_score']}/800")
    print(f"Math Score: {result['math_score']}/800")
    print(f"Total Score: {result['total_score']}/1600")
    print(f"Percentile: {result['percentile']}th")

    assert result['total_score'] == 400, "Minimum score should be 400"
    print("✅ Test 4 PASSED\n")


def test_high_score():
    """Test high SAT score (1500)"""
    print("Test 5: High Score (~1500)")
    print("-" * 50)

    result = SATScoreCalculator.calculate_full_score(
        reading_correct=50,
        writing_correct=42,
        math_correct=55
    )

    print(f"Reading Correct: {result['reading_correct']}/52")
    print(f"Writing Correct: {result['writing_correct']}/44")
    print(f"Math Correct: {result['math_correct']}/58")
    print(f"Reading & Writing Score: {result['reading_writing_score']}/800")
    print(f"Math Score: {result['math_score']}/800")
    print(f"Total Score: {result['total_score']}/1600")
    print(f"Percentile: {result['percentile']}th")

    assert 1450 <= result['total_score'] <= 1550, "Should be high score range"
    assert result['percentile'] >= 96, "Should be high percentile"
    print("✅ Test 5 PASSED\n")


if __name__ == "__main__":
    print("=" * 50)
    print("SAT Score Calculator - Unit Tests")
    print("=" * 50)
    print()

    try:
        test_perfect_score()
        test_average_score()
        test_target_score()
        test_minimum_score()
        test_high_score()

        print("=" * 50)
        print("✅ ALL TESTS PASSED!")
        print("=" * 50)
        print("\nScore Calculator is working correctly! ✨")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
