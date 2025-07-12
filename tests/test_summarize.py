import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import patch, MagicMock
from ai.openai_summary import summarize_client

class TestSummarizeClient(unittest.TestCase):

    @patch("ai.openai_summary.openai_client.chat.completions.create")
    def test_summary_format(self, mock_create):
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Test Bank is a Retail Banking client with a 0.92 risk score."))
        ]
        mock_create.return_value = mock_response

        dummy_client = {
            "name": "Test Bank",
            "industry": "Retail Banking",
            "hq_location": "Nowhere, ZZ",
            "annual_revenue": 12.5,
            "employee_count": 5000,
            "risk_score": 0.92,
            "watchlist": True,
            "regulatory_issues": "Pending investigation from FDIC"
        }

        result = summarize_client(dummy_client)

        self.assertIn("Test Bank", result)
        self.assertIn("retail banking", result.lower())
        self.assertIn("0.92", result)
        self.assertNotIn("❌", result)

if __name__ == "__main__":
    unittest.main()
