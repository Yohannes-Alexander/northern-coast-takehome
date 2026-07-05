import unittest
import os
import sys
from fastapi.testclient import TestClient

# Ensure the app module can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app
from app.models.schemas import LeadScoreResponse
from app.core.config import settings

class TestLeadScorer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        # Check if GEMINI_API_KEY is configured
        cls.api_key_set = bool(settings.GEMINI_API_KEY)
        if not cls.api_key_set:
            print("\nWARNING: GEMINI_API_KEY is not set in environment or .env file.")
            print("Tests will run, but LLM calls will trigger the fallback heuristic.\n")

    def test_hot_lead(self):
        """
        Tests the Hot lead payload.
        UAE distributor, 3 FCL/month, 8 years importing Red Bull.
        """
        payload = {
            "lead_id": "S001",
            "channel": "whatsapp",
            "conversation": [
                {"role": "lead", "text": "UAE distributor, 3 FCL/month Red Bull, 8 years importing energy drinks. Looking for original Austrian product."},
                {"role": "agent", "text": "Volume target on Red Bull specifically?"},
                {"role": "lead", "text": "2-3 FCL/month sustained. ~250 retail accounts across UAE."}
            ]
        }
        response = self.client.post("/score", json=payload)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        print(f"\n[HOT LEAD RESULT] (API Key Set: {self.api_key_set})")
        print(f"Score: {data['score']}")
        print(f"Tier: {data['tier']}")
        print(f"Routing: {data['routing']}")
        print(f"Reasoning: {data['reasoning']}")

        # Validate structure matches schema
        LeadScoreResponse(**data)
        
        # If API key is set, check LLM categorization
        if self.api_key_set:
            self.assertGreaterEqual(data['score'], 80)
            self.assertEqual(data['tier'], "Hot")
            self.assertEqual(data['routing'], "kam_handoff")
        else:
            # Fallback assertion (wholesale keyword triggers Warm fallback)
            self.assertEqual(data['tier'], "Warm")
            self.assertEqual(data['routing'], "nurture_pool")

    def test_cold_lead(self):
        """
        Tests the Cold lead payload.
        Office party, looking for a few cans.
        """
        payload = {
            "lead_id": "S002",
            "channel": "email",
            "conversation": [
                {"role": "lead", "text": "hey can I get a few cans of red bull for my office party"}
            ]
        }
        response = self.client.post("/score", json=payload)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        print(f"\n[COLD LEAD RESULT] (API Key Set: {self.api_key_set})")
        print(f"Score: {data['score']}")
        print(f"Tier: {data['tier']}")
        print(f"Routing: {data['routing']}")
        print(f"Reasoning: {data['reasoning']}")

        LeadScoreResponse(**data)
        
        if self.api_key_set:
            self.assertLess(data['score'], 40)
            self.assertEqual(data['tier'], "Cold")
            self.assertEqual(data['routing'], "auto_archive")
        else:
            # Fallback assertion (retail keyword triggers Cold fallback)
            self.assertEqual(data['tier'], "Cold")
            self.assertEqual(data['routing'], "auto_archive")

    def test_ambiguous_lead(self):
        """
        Tests the Ambiguous lead payload.
        Ghana distributor, Coca-Cola, license in progress, 1 FCL/month.
        """
        payload = {
            "lead_id": "S003",
            "channel": "email",
            "conversation": [
                {"role": "lead", "text": "Ghana-based distributor looking for Coca-Cola products. New entrant, license in process — expected 6 weeks. Initial volume 1 FCL/month."}
            ]
        }
        response = self.client.post("/score", json=payload)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        print(f"\n[AMBIGUOUS LEAD RESULT] (API Key Set: {self.api_key_set})")
        print(f"Score: {data['score']}")
        print(f"Tier: {data['tier']}")
        print(f"Routing: {data['routing']}")
        print(f"Reasoning: {data['reasoning']}")

        LeadScoreResponse(**data)
        
        if self.api_key_set:
            # Should be Warm/Hot because volume is 1 FCL, but license is in process
            self.assertTrue(data['tier'] in ["Warm", "Hot"])
            self.assertTrue(data['routing'] in ["nurture_pool", "kam_handoff"])
        else:
            # Fallback assertion (wholesale keyword triggers Warm fallback)
            self.assertEqual(data['tier'], "Warm")
            self.assertEqual(data['routing'], "nurture_pool")

    def test_fallback_forcing(self):
        """
        Forces the fallback heuristic by mocking a failure or setting an invalid key,
        ensuring the application does not crash.
        """
        original_key = settings.GEMINI_API_KEY
        # Set invalid key to force a call exception
        settings.GEMINI_API_KEY = "invalid_key_to_force_failure"
        
        payload = {
            "lead_id": "S004-FALLBACK",
            "channel": "whatsapp",
            "conversation": [
                {"role": "lead", "text": "Looking for 2 FCL container loads of wholesale Monster Energy per month."}
            ]
        }
        # Run request
        response = self.client.post("/score", json=payload)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        print(f"\n[FORCED FALLBACK RESULT]")
        print(f"Score: {data['score']}")
        print(f"Tier: {data['tier']}")
        print(f"Routing: {data['routing']}")
        print(f"Reasoning: {data['reasoning']}")
        
        self.assertEqual(data['tier'], "Warm")
        self.assertEqual(data['routing'], "nurture_pool")
        self.assertIn("Fallback", data['reasoning'])
        
        # Restore key
        settings.GEMINI_API_KEY = original_key

if __name__ == "__main__":
    unittest.main()
