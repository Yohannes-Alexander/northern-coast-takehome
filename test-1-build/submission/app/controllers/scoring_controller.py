from fastapi import APIRouter, Depends, HTTPException, status
import logging

from app.models.schemas import LeadInput, LeadScoreResponse
from app.services.scoring_service import ScoringService
from app.repositories.gemini_repository import GeminiScoringRepository

logger = logging.getLogger(__name__)

router = APIRouter()

def get_scoring_service() -> ScoringService:
    """
    Dependency injection provider for the ScoringService configured with the GeminiScoringRepository.
    """
    repository = GeminiScoringRepository()
    return ScoringService(repository)

@router.post("/score", response_model=LeadScoreResponse, status_code=status.HTTP_200_OK)
@router.post("/api/v1/score", response_model=LeadScoreResponse, status_code=status.HTTP_200_OK)
async def score_lead(
    payload: LeadInput,
    service: ScoringService = Depends(get_scoring_service)
) -> LeadScoreResponse:
    """
    Endpoint that accepts lead conversation transcripts, scores them, and determines the routing action.
    Supports both root `/score` and versioned `/api/v1/score` for convenience.
    """
    try:
        logger.info(f"Received scoring request for Lead ID: {payload.lead_id} via channel {payload.channel}")
        result = await service.score_lead(payload.lead_id, payload.conversation)
        return result
    except Exception as e:
        logger.critical(f"Unhandled exception in scoring endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during lead scoring processing: {str(e)}"
        )
