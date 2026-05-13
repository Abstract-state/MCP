from app.schemas import ConversationEpisode, FrictionMetrics
from app.acceptance_detector import AcceptanceDetector
from app.friction_calculator import FrictionCalculator
from app.signal_extractor import SignalExtractor

class EpisodeAnalyzer:
    def __init__(self):
        self.acceptance_detector = AcceptanceDetector()
        self.friction_calculator = FrictionCalculator()
        self.signal_extractor = SignalExtractor()

    def analyze(self, episode: ConversationEpisode) -> ConversationEpisode:
        # Re-compute metrics based on turns
        turn_count = len(episode.turns)
        clarifications = 0
        corrections = 0
        rejections = 0
        
        last_signal = "neutral"
        
        for turn in episode.turns:
            if turn.role == "user":
                signal = self.acceptance_detector.detect_acceptance(turn.message)
                if signal == "clarification":
                    clarifications += 1
                elif signal == "rejected":
                    rejections += 1
                    corrections += 1  # Often rejections act as corrections
                last_signal = signal
                
                # Assign turn type if not set
                if not turn.turn_type and signal != "neutral":
                    turn.turn_type = signal

        episode.accepted = (last_signal == "accepted")
        episode.acceptance_signal = last_signal if last_signal == "accepted" else None
        
        friction_score = self.friction_calculator.calculate(
            turn_count=turn_count,
            clarification_count=clarifications,
            correction_count=corrections,
            rejection_count=rejections,
            accepted=episode.accepted
        )
        
        episode.metrics = FrictionMetrics(
            turn_count=turn_count,
            clarification_count=clarifications,
            correction_count=corrections,
            rejection_count=rejections,
            friction_score=friction_score
        )
        
        # Extract signals from initial prompt
        extracted = self.signal_extractor.extract_signals(episode.initial_prompt)
        episode.linked_ids = list(set(episode.linked_ids + extracted["linked_ids"]))
        
        if not episode.final_understood_intent and episode.accepted:
            episode.final_understood_intent = f"Understood task '{extracted['task_type']}'" + (f" with phrases {extracted['behavior_phrases']}" if extracted['behavior_phrases'] else "")
            
        return episode
