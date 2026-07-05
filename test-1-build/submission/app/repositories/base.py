from abc import ABC, abstractmethod
from typing import List
from app.models.schemas import ConversationTurn, LLMScoringResponse

class BaseScoringRepository(ABC):
    @abstractmethod
    async def score_lead(self, lead_id: str, conversation: List[ConversationTurn]) -> LLMScoringResponse:
        """
        Analyze a lead's conversation transcript and return a scored routing decision.
        """
        pass
