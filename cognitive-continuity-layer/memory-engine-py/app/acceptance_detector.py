class AcceptanceDetector:
    def __init__(self):
        self.accepted_signals = [
            "ok", "accepted", "works", "this works", "thank you", 
            "thanks", "looks good", "perfect", "yes"
        ]
        self.rejected_signals = [
            "no", "wrong", "incorrect", "not this", "not what i meant", 
            "this broke", "don't do this"
        ]
        self.clarification_signals = [
            "i meant", "actually", "not like this", "same as before", 
            "minimal changes"
        ]

    def detect_acceptance(self, message: str) -> str:
        msg_lower = message.lower()
        
        for signal in self.rejected_signals:
            if signal in msg_lower:
                return "rejected"
                
        for signal in self.accepted_signals:
            if signal in msg_lower:
                return "accepted"
                
        for signal in self.clarification_signals:
            if signal in msg_lower:
                return "clarification"
                
        return "neutral"
