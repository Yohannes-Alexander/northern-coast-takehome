from typing import List
import logging

from app.models.schemas import ConversationTurn, LeadScoreResponse
from app.repositories.base import BaseScoringRepository

logger = logging.getLogger(__name__)

class ScoringService:
    def __init__(self, scoring_repository: BaseScoringRepository):
        self.scoring_repository = scoring_repository

    async def score_lead(self, lead_id: str, conversation: List[ConversationTurn]) -> LeadScoreResponse:
        """
        Scores a lead using the repository. If the repository fails, a local business rule-based 
        heuristic fallback is applied to guarantee system availability.
        """
        try:
            llm_result = await self.scoring_repository.score_lead(lead_id, conversation)
            score = llm_result.score
            
            # Deterministic business rules
            if score >= 80:
                tier = "Hot"
                routing = "kam_handoff"
            elif score >= 40:
                tier = "Warm"
                routing = "nurture_pool"
            else:
                tier = "Cold"
                routing = "auto_archive"

            return LeadScoreResponse(
                lead_id=lead_id,
                score=score,
                tier=tier,
                routing=routing,
                reasoning=llm_result.reasoning
            )
        except Exception as e:
            logger.error(f"Error in lead scoring repository: {str(e)}. Triggering local fallback heuristic.", exc_info=True)
            return self._calculate_fallback_score(lead_id, conversation)

    def _calculate_fallback_score(self, lead_id: str, conversation: List[ConversationTurn]) -> LeadScoreResponse:
        """
        Fallback heuristic logic when the LLM service is down.
        Scans for key terms (e.g. FCL, wholesale, distributor, license) to make a best-effort classification.
        """
        full_text = " ".join([turn.text.lower() for turn in conversation])

        # High-intent wholesale keywords
        wholesale_keywords = ["fcl", "container", "distributor", "wholesale", "wholesale supply", "license", "licensed"]
        # Retail or low-intent keywords
        retail_keywords = ["party", "office party", "few cans", "a few", "can i get", "personal"]

        has_wholesale_intent = any(keyword in full_text for keyword in wholesale_keywords)
        has_retail_intent = any(keyword in full_text for keyword in retail_keywords)

        if has_wholesale_intent and not has_retail_intent:
            # Looks like a genuine wholesale lead, route to nurture pool as Warm
            return LeadScoreResponse(
                lead_id=lead_id,
                score=60,
                tier="Warm",
                routing="nurture_pool",
                reasoning="Fallback: Detected B2B wholesale keywords (FCL, license, distributor) in transcript during API outage."
            )
        elif has_retail_intent:
            # Looks like a retail/consumer lead, route to archive
            return LeadScoreResponse(
                lead_id=lead_id,
                score=15,
                tier="Cold",
                routing="auto_archive",
                reasoning="Fallback: Detected consumer/retail intent keywords (party, cans) in transcript during API outage."
            )
        else:
            # Ambiguous/default fallback
            return LeadScoreResponse(
                lead_id=lead_id,
                score=35,
                tier="Cold",
                routing="auto_archive",
                reasoning="Fallback: System offline. Defaulting to Cold classification due to insufficient local indicators."
            )
        
        # Test helper method to force fallback logic
        
