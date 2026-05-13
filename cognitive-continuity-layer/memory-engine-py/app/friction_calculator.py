class FrictionCalculator:
    def calculate(self, turn_count: int, clarification_count: int, correction_count: int, rejection_count: int, accepted: bool) -> float:
        """
        Formula:
        friction_score = (clarification_count * 2) + (correction_count * 3) + (rejection_count * 4) + (turn_count * 0.5) - acceptance_bonus
        """
        base_friction = (clarification_count * 2) + (correction_count * 3) + (rejection_count * 4) + (turn_count * 0.5)
        acceptance_bonus = 2.0 if accepted else 0.0
        return max(0.0, base_friction - acceptance_bonus)
