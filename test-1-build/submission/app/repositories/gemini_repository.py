from typing import List
from google import genai
from google.genai import types

from app.repositories.base import BaseScoringRepository
from app.models.schemas import ConversationTurn, LLMScoringResponse
from app.core.config import settings

class GeminiScoringRepository(BaseScoringRepository):
    def __init__(self):
        import os
        try:
            # If API key is empty and not present in environment, we set client to None 
            # instead of raising ValueError during class instantiation.
            api_key = settings.GEMINI_API_KEY or None
            if not api_key and not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
                self.client = None
            else:
                self.client = genai.Client(api_key=api_key)
        except Exception:
            self.client = None

    async def score_lead(self, lead_id: str, conversation: List[ConversationTurn]) -> LLMScoringResponse:
        if not self.client:
            raise RuntimeError("Gemini API key is not configured. Please set GEMINI_API_KEY in your .env file.")

        # Format the conversation transcript for the prompt
        formatted_dialogue = ""
        for turn in conversation:
            role_label = "Lead" if turn.role == "lead" else "Agent"
            formatted_dialogue += f"{role_label}: {turn.text}\n"

        system_instruction = (
            "You are an expert B2B Lead Scoring Agent for Northern Coast Beverages, a global wholesale distributor "
            "of premium beverage brands (e.g., Coca-Cola, Monster, Red Bull). Your goal is to evaluate inbound leads "
            "based on their chat/email transcript and assign a score (0-100) and reasoning.\n\n"
            "Here is the scoring rubric:\n"
            "1. Volume Commitment (up to 30 points):\n"
            "   - 30 pts: High volume, ordering container-loads (>= 1 FCL/month, FCL = Full Container Load).\n"
            "   - 15 pts: Medium volume or unclear but clearly commercial wholesaling.\n"
            "   - 0 pts: Office party, single personal use, or very low volume (e.g., a few cans/cases).\n"
            "2. Import License (up to 30 points):\n"
            "   - 30 pts: Active import license mentioned or established importer history.\n"
            "   - 15 pts: License in process/underway.\n"
            "   - 0 pts: No license, individual, or refuses to provide license details.\n"
            "3. Product Fit (up to 20 points):\n"
            "   - 20 pts: Seeking brands we distribute (beverages: Red Bull, Monster, Coca-Cola, etc.).\n"
            "   - 0 pts: Requesting products outside beverages.\n"
            "4. Business Presence / Credibility (up to 20 points):\n"
            "   - 20 pts: Clear B2B distributor presence (distribution channels, retail accounts, years in business).\n"
            "   - 10 pts: New business or startup with some B2B structure.\n"
            "   - 0 pts: Individual consumer, spam, or office party request.\n\n"
            "Your output MUST be a JSON object matching the requested schema. The reasoning MUST be a concise 1-2 sentence "
            "rationale explaining why the specific score was assigned based on the criteria."
        )

        user_content = f"Evaluate the following lead conversation transcript:\n\nLead ID: {lead_id}\n\nTranscript:\n{formatted_dialogue}"

        try:
            # Call Gemini using structured JSON output
            response = await self.client.aio.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_content,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=LLMScoringResponse,
                    temperature=0.0,
                )
            )

            if not response.text:
                raise ValueError("Received empty response from Gemini API.")

            # Parse and return it
            return LLMScoringResponse.model_validate_json(response.text)

        except Exception as e:
            # Re-raise to be handled by the service or middleware
            raise RuntimeError(f"Gemini API execution error: {str(e)}")
