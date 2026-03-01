"""
Digital SAT Score Calculator (Bluebook-Based Estimation Model)

⚠️ **CRITICAL DISCLAIMER:**
This is an ESTIMATION MODEL based on heuristics and observed patterns.
These are NOT official College Board scores and may vary significantly from actual results.

The College Board does not publish their exact scoring algorithms.
This calculator uses a transparent, logical model for practice guidance only.

Digital SAT Structure:
- Reading & Writing: 27q Module 1 + 27q Module 2 (adaptive) = 54 total
- Math: 22q Module 1 + 22q Module 2 (adaptive) = 44 total
- Each section scored 200-800 (total 400-1600)
- Module 2 difficulty based on Module 1 performance

Author: EduNexus Team
Version: 2.0 (Digital SAT / Bluebook)
Last Updated: January 2026
"""
from typing import Dict, Literal


class DigitalSATScoreCalculator:
    """
    Digital SAT Score Calculator using transparent heuristic model.
    
    IMPORTANT: These are ESTIMATES, not official scores.
    """
    
    # Digital SAT constants
    RW_MODULE1_TOTAL = 27
    RW_MODULE2_TOTAL = 27
    RW_TOTAL = 54
    
    MATH_MODULE1_TOTAL = 22
    MATH_MODULE2_TOTAL = 22
    MATH_TOTAL = 44
    
    # Score ranges
    MIN_SECTION_SCORE = 200
    MAX_SECTION_SCORE = 800
    SECTION_SCORE_RANGE = MAX_SECTION_SCORE - MIN_SECTION_SCORE  # 600 points
    
    @classmethod
    def calculate_score(
        cls,
        rw_module1_correct: int,
        rw_module2_correct: int,
        rw_module2_difficulty: Literal['easy', 'medium', 'hard'],
        math_module1_correct: int,
        math_module2_correct: int,
        math_module2_difficulty: Literal['easy', 'medium', 'hard']
    ) -> Dict:
        """
        Calculate estimated Digital SAT scores.
        
        Returns:
            Dict containing:
            - rw_module1_correct, rw_module2_correct, rw_module2_difficulty
            - math_module1_correct, math_module2_correct, math_module2_difficulty
            - reading_writing_score (200-800)
            - math_score (200-800)
            - total_score (400-1600)
            - percentile (1-99)
            - is_estimated (always True)
            - confidence ('low'/'medium'/'high')
            - disclaimer (warning text)
        """
        # Validate inputs
        cls._validate_inputs(
            rw_module1_correct, rw_module2_correct, rw_module2_difficulty,
            math_module1_correct, math_module2_correct, math_module2_difficulty
        )
        
        # Calculate section scores
        rw_score = cls._calculate_section_score(
            module1_correct=rw_module1_correct,
            module2_correct=rw_module2_correct,
            module2_difficulty=rw_module2_difficulty,
            module1_total=cls.RW_MODULE1_TOTAL,
            module2_total=cls.RW_MODULE2_TOTAL
        )
        
        math_score = cls._calculate_section_score(
            module1_correct=math_module1_correct,
            module2_correct=math_module2_correct,
            module2_difficulty=math_module2_difficulty,
            module1_total=cls.MATH_MODULE1_TOTAL,
            module2_total=cls.MATH_MODULE2_TOTAL
        )
        
        total_score = rw_score + math_score
        
        # Calculate percentile (approximate based on score)
        percentile = cls._estimate_percentile(total_score)
        
        # Determine confidence level
        confidence = cls._determine_confidence(
            rw_module2_difficulty, math_module2_difficulty,
            rw_module1_correct, math_module1_correct
        )
        
        return {
            # Module inputs
            'rw_module1_correct': rw_module1_correct,
            'rw_module2_correct': rw_module2_correct,
            'rw_module2_difficulty': rw_module2_difficulty,
            'math_module1_correct': math_module1_correct,
            'math_module2_correct': math_module2_correct,
            'math_module2_difficulty': math_module2_difficulty,
            # Calculated scores
            'reading_writing_score': rw_score,
            'math_score': math_score,
            'total_score': total_score,
            'percentile': percentile,
            # Estimation metadata
            'is_estimated': True,
            'confidence': confidence,
            'disclaimer': (
                "This is an ESTIMATED score based on a heuristic model. "
                "Actual Digital SAT scores may vary significantly. "
                "Use for practice guidance only."
            )
        }
    
    @classmethod
    def _validate_inputs(
        cls,
        rw_m1: int, rw_m2: int, rw_diff: str,
        math_m1: int, math_m2: int, math_diff: str
    ):
        """Validate all input parameters."""
        # Check R&W module scores
        if not (0 <= rw_m1 <= cls.RW_MODULE1_TOTAL):
            raise ValueError(f"R&W Module 1 must be 0-{cls.RW_MODULE1_TOTAL}, got {rw_m1}")
        if not (0 <= rw_m2 <= cls.RW_MODULE2_TOTAL):
            raise ValueError(f"R&W Module 2 must be 0-{cls.RW_MODULE2_TOTAL}, got {rw_m2}")
        
        # Check Math module scores
        if not (0 <= math_m1 <= cls.MATH_MODULE1_TOTAL):
            raise ValueError(f"Math Module 1 must be 0-{cls.MATH_MODULE1_TOTAL}, got {math_m1}")
        if not (0 <= math_m2 <= cls.MATH_MODULE2_TOTAL):
            raise ValueError(f"Math Module 2 must be 0-{cls.MATH_MODULE2_TOTAL}, got {math_m2}")
        
        # Check difficulty levels
        valid_difficulties = ['easy', 'medium', 'hard']
        if rw_diff not in valid_difficulties:
            raise ValueError(f"R&W difficulty must be one of {valid_difficulties}, got {rw_diff}")
        if math_diff not in valid_difficulties:
            raise ValueError(f"Math difficulty must be one of {valid_difficulties}, got {math_diff}")
    
    @classmethod
    def _calculate_section_score(
        cls,
        module1_correct: int,
        module2_correct: int,
        module2_difficulty: str,
        module1_total: int,
        module2_total: int
    ) -> int:
        """
        Calculate section score (200-800) using adaptive difficulty model.
        
        Algorithm:
        1. Calculate raw percentage correct across both modules
        2. Apply difficulty multiplier to Module 2 performance
        3. Normalize to base percentage (0.0 to 1.0)
        4. Apply non-linear curve to match SAT score distribution
        5. Scale to 200-800 range
        """
        # Total questions and correct answers
        total_questions = module1_total + module2_total
        
        # Module 1 performance (standard weight)
        module1_pct = module1_correct / module1_total
        
        # Module 2 performance with difficulty multiplier
        difficulty_multipliers = {
            'easy': 0.85,    # Lower weight - easier questions
            'medium': 1.0,   # Standard weight
            'hard': 1.15     # Higher weight - harder questions
        }
        
        multiplier = difficulty_multipliers[module2_difficulty]
        module2_weighted_correct = module2_correct * multiplier
        module2_weighted_total = module2_total * multiplier
        
        # Combined weighted performance
        weighted_correct = module1_correct + module2_weighted_correct
        weighted_total = module1_total + module2_weighted_total
        weighted_pct = weighted_correct / weighted_total
        
        # Clamp to 0.0-1.0 range
        weighted_pct = max(0.0, min(1.0, weighted_pct))
        
        # Apply non-linear scoring curve to match SAT distribution
        # SAT scores cluster around middle, with diminishing returns at extremes
        curved_pct = cls._apply_scoring_curve(weighted_pct)
        
        # Scale to 200-800 range
        section_score = cls.MIN_SECTION_SCORE + int(curved_pct * cls.SECTION_SCORE_RANGE)
        
        # Ensure within bounds
        section_score = max(cls.MIN_SECTION_SCORE, min(cls.MAX_SECTION_SCORE, section_score))
        
        return section_score
    
    @classmethod
    def _apply_scoring_curve(cls, pct: float) -> float:
        """
        Apply non-linear curve to percentage to match SAT score distribution.
        
        SAT scoring characteristics:
        - Below 50%: Steeper penalty (harder to recover)
        - 50-80%: Linear region
        - Above 80%: Compressed (harder to get perfect score)
        """
        if pct < 0.5:
            # Below 50%: Quadratic penalty
            return 0.3 + (pct * 0.8)
        elif pct < 0.8:
            # 50-80%: Near-linear region
            return 0.7 + ((pct - 0.5) * 0.6)
        else:
            # Above 80%: Compressed high end
            return 0.88 + ((pct - 0.8) * 0.6)
    
    @classmethod
    def _estimate_percentile(cls, total_score: int) -> int:
        """
        Estimate percentile based on total score.
        
        Based on approximate College Board percentile data:
        - 1200: ~74th percentile
        - 1300: ~87th percentile
        - 1400: ~94th percentile
        - 1500: ~99th percentile
        - 1600: 99th percentile (perfect)
        """
        percentile_map = [
            (400, 1), (500, 2), (600, 5), (700, 10),
            (800, 20), (900, 30), (1000, 40), (1100, 55),
            (1200, 74), (1300, 87), (1400, 94), (1500, 99), (1600, 99)
        ]
        
        # Linear interpolation between known points
        for i in range(len(percentile_map) - 1):
            score_low, pct_low = percentile_map[i]
            score_high, pct_high = percentile_map[i + 1]
            
            if score_low <= total_score <= score_high:
                # Interpolate
                score_range = score_high - score_low
                pct_range = pct_high - pct_low
                score_offset = total_score - score_low
                pct = pct_low + int((score_offset / score_range) * pct_range)
                return max(1, min(99, pct))
        
        # Handle edge cases
        if total_score < 400:
            return 1
        else:
            return 99
    
    @classmethod
    def _determine_confidence(
        cls,
        rw_diff: str,
        math_diff: str,
        rw_m1_correct: int,
        math_m1_correct: int
    ) -> Literal['low', 'medium', 'high']:
        """
        Determine confidence level based on difficulty alignment with Module 1 performance.
        
        High confidence: Difficulty matches performance
        Medium confidence: Slight mismatch
        Low confidence: Significant mismatch
        """
        # Calculate Module 1 performance percentages
        rw_m1_pct = rw_m1_correct / cls.RW_MODULE1_TOTAL
        math_m1_pct = math_m1_correct / cls.MATH_MODULE1_TOTAL
        
        # Expected difficulty thresholds
        def expected_difficulty(pct: float) -> str:
            if pct < 0.5:
                return 'easy'
            elif pct < 0.75:
                return 'medium'
            else:
                return 'hard'
        
        rw_expected = expected_difficulty(rw_m1_pct)
        math_expected = expected_difficulty(math_m1_pct)
        
        # Count mismatches
        mismatches = 0
        if rw_diff != rw_expected:
            mismatches += 1
        if math_diff != math_expected:
            mismatches += 1
        
        # Determine confidence
        if mismatches == 0:
            return 'high'
        elif mismatches == 1:
            return 'medium'
        else:
            return 'low'
