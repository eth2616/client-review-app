import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from clients.classify import classify_client

class TestClassifyClient(unittest.TestCase):

    def test_high_risk_enterprise(self):
        client = {
            "name": "Citi",
            "industry": "Retail Banking",
            "hq_location": "New York, NY",
            "annual_revenue": 200,
            "employee_count": 120000,
            "risk_score": 0.9
        }
        result = classify_client(client)
        self.assertEqual(result["risk_tier"], "High Risk")
        self.assertEqual(result["revenue_tier"], "Enterprise")
        self.assertTrue(result["review_required"])

    def test_moderate_risk_enterprise(self):
        client = {
            "name": "MUFG Union Bank",
            "industry": "Global Banking",
            "hq_location": "San Francisco, CA",
            "annual_revenue": 100,
            "employee_count": 10000,
            "risk_score": 0.75
        }
        result = classify_client(client)
        self.assertEqual(result["risk_tier"], "Moderate Risk")
        self.assertEqual(result["revenue_tier"], "Enterprise")
        self.assertFalse(result["review_required"])

    def test_low_risk_small_business(self):
        client = {
            "name": "Ally",
            "industry": "Digital Banking",
            "hq_location": "Detroit, MI",
            "annual_revenue": 8,
            "employee_count": 8800,
            "risk_score": 0.45
        }
        result = classify_client(client)
        self.assertEqual(result["risk_tier"], "Low Risk")
        self.assertEqual(result["revenue_tier"], "Small Business")
        self.assertFalse(result["review_required"])

    def test_edge_case_missing_fields(self):
        client = {
            "name": "Unknown Client"
            # Missing other fields
        }
        result = classify_client(client)
        self.assertEqual(result["risk_tier"], "Low Risk")  # default if score missing
        self.assertEqual(result["revenue_tier"], "Small Business")  # default if revenue missing
        self.assertFalse(result["review_required"])


if __name__ == "__main__":
    unittest.main()
