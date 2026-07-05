from typing import List, Literal
from pydantic import BaseModel, Field

class ConversationTurn(BaseModel):
    role: Literal["lead", "agent"]
    text: str

class LeadInput(BaseModel):
    lead_id: str
    channel: str
    conversation: List[ConversationTurn]

class LeadScoreResponse(BaseModel):
    lead_id: str
    score: int = Field(..., ge=0, le=100, description="Lead score from 0 to 100 based on B2B beverage distribution criteria.")
    tier: Literal["Hot", "Warm", "Cold"] = Field(..., description="Lead classification: Hot (score >= 80), Warm (score 40-79), or Cold (score < 40).")
    routing: Literal["kam_handoff", "nurture_pool", "auto_archive"] = Field(..., description="Action to route: kam_handoff for Hot, nurture_pool for Warm, auto_archive for Cold.")
    reasoning: str = Field(..., description="A 1-2 sentence concise explanation justifying the score, tier, and routing based on the client's import license, volume commitment, and product fit.")

class LLMScoringResponse(BaseModel):
    score: int = Field(..., ge=0, le=100, description="Lead score from 0 to 100 based on B2B beverage distribution criteria.")
    reasoning: str = Field(..., description="A 1-2 sentence concise explanation justifying the score based on the client's import license, volume commitment, and product fit.")

