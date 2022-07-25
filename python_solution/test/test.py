"""
Test Driven Development applied to the Payway User Points API (for python implementation)
Testing class for the Payway User Points API
Will test:
- GET /users/{user_id}/points
- PUT /users/{user_id}/spend
- POST /users/{user_id}/transaction
"""
import unittest
import datetime

from main.main import *

from fastapi.testclient import TestClient

client = TestClient(app) # create a test client for the app

class TestPaywaySystem(unittest.TestCase):
    """Test class for PointSystem."""

    # Basic Tests
    def test_read_main(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "wassup big stepper"}

    # Account Creation
    def test_create_account(self):
        # post user info to create account
        # response should be confirmation that the account was created with some info about the account
        pass

    # Validating Transactions
    def test_post_transaction(self):
        # Test for valid transaction
        transaction_1 = Transaction(tid=1,payer=Payer.dannon, points=100, timestamp=datetime.datetime.now())
        pass
    
    # Validating Account State post Transaction POST
    def test_get_balance(self):
        pass

    # Validating correct spending behavior
    def test_spend_points(self):
        pass

if __name__ == "__main__":
   unittest.main()
