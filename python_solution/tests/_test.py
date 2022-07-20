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

import main
from main import main
from main.main import *

# TODO create an example input for the create_transaction endpoint


class TestPaywaySystem(unittest.TestCase):
    """Test class for PointSystem."""

    def test_create_account(self):
        pass

    def test_create_transaction(self):
        # Test for valid transaction
        transaction_1 = Transaction(payer=Payer.dannon, points=100, timestamp=datetime.datetime.now())

if __name__ == "__main__":
   unittest.main()
