"""
Debug test for SAT Score Calculator
"""
import sys
sys.path.append('.')

from app.utils.score_calculator import SATScoreCalculator


# Test the conversion table directly
print("Testing RW Conversion Table:")
print(f"96 correct answers → {SATScoreCalculator.RW_CONVERSION_TABLE.get(96, 'NOT FOUND')}")
print(f"48 correct answers → {SATScoreCalculator.RW_CONVERSION_TABLE.get(48, 'NOT FOUND')}")
print(f"0 correct answers → {SATScoreCalculator.RW_CONVERSION_TABLE.get(0, 'NOT FOUND')}")
print()

print("Testing Math Conversion Table:")
print(f"58 correct answers → {SATScoreCalculator.MATH_CONVERSION_TABLE.get(58, 'NOT FOUND')}")
print(f"29 correct answers → {SATScoreCalculator.MATH_CONVERSION_TABLE.get(29, 'NOT FOUND')}")
print(f"0 correct answers → {SATScoreCalculator.MATH_CONVERSION_TABLE.get(0, 'NOT FOUND')}")
print()

# Test the calculation method
print("Testing calculation methods:")
reading = 54
writing = 44
math = 58

raw_rw = reading + writing
print(f"Reading: {reading}, Writing: {writing}, Raw RW Score: {raw_rw}")

rw_score = SATScoreCalculator.calculate_reading_writing_score(reading, writing)
print(f"RW Scaled Score: {rw_score}")

math_score = SATScoreCalculator.calculate_math_score(math)
print(f"Math Scaled Score: {math_score}")

total = rw_score + math_score
print(f"Total Score: {total}")
