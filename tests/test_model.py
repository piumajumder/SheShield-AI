import unittest

from model import predict_risk_by_area_name


class PredictRiskByAreaNameTests(unittest.TestCase):
    def test_returns_emergency_help(self):
        score, status, color, details = predict_risk_by_area_name("Park Street")

        self.assertIsNotNone(details)
        self.assertIn("emergency_help", details)
        self.assertTrue(details["emergency_help"]["contacts"])


if __name__ == "__main__":
    unittest.main()
