import pytest
from app.acceptance_detector import AcceptanceDetector
from app.friction_calculator import FrictionCalculator
from app.signal_extractor import SignalExtractor
from app.hybrid_ranker import HybridRanker
from app.prompt_refinement_engine import PromptRefinementEngine
from app.behavioral_retriever import BehavioralRetriever
from unittest.mock import MagicMock

def test_acceptance_detector():
    detector = AcceptanceDetector()
    assert detector.detect_acceptance("Yes, that looks perfect") == "accepted"
    assert detector.detect_acceptance("No, this is wrong") == "rejected"
    assert detector.detect_acceptance("Actually I meant minimal changes") == "clarification"
    assert detector.detect_acceptance("Just asking a question") == "neutral"

def test_friction_calculator():
    calc = FrictionCalculator()
    # High friction but accepted
    score = calc.calculate(turn_count=5, clarification_count=2, correction_count=1, rejection_count=0, accepted=True)
    # base = (2*2) + (1*3) + 0 + (5*0.5) = 4 + 3 + 2.5 = 9.5
    # accepted bonus = -2.0 -> 7.5
    assert score == 7.5
    
    # Low friction accepted
    score2 = calc.calculate(turn_count=1, clarification_count=0, correction_count=0, rejection_count=0, accepted=True)
    # base = 0.5, bonus = -2.0 -> max(0, -1.5) = 0.0
    assert score2 == 0.0

def test_signal_extractor():
    extractor = SignalExtractor()
    res = extractor.extract_signals("Fix this DAX query same as before for PROJ-123")
    assert "same as before" in res["behavior_phrases"]
    assert "PROJ-123" in res["linked_ids"]
    assert res["task_type"] == "fix"

def test_hybrid_ranker():
    ranker = HybridRanker()
    candidates = [
        {"id": "1", "document": "DAX query format", "distance": 0.1, "collection": "conversation_episodes", "metadata": {"accepted": True}},
        {"id": "2", "document": "Different topic", "distance": 0.9, "collection": "cognitive_memories", "metadata": {"accepted": False}}
    ]
    ranked = ranker.rank(candidates, "DAX query")
    assert ranked[0]["id"] == "1"
    assert ranked[0]["final_score"] > ranked[1]["final_score"]

def test_prompt_refinement_engine():
    mock_retriever = MagicMock(spec=BehavioralRetriever)
    mock_retriever.retrieve.return_value = [
        {"document": "Always use variables in DAX."}
    ]
    engine = PromptRefinementEngine(mock_retriever)
    preview = engine.generate_preview("Fix DAX measure same as before", "user_1", "ws_1", [])
    
    assert "same as before" in str(preview["interpreted_meaning"])
    assert "Always use variables in DAX." in str(preview["retrieved_context"])
    assert "Context Applied" in preview["refined_prompt"]
