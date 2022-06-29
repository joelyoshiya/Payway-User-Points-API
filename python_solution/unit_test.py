"""
Employee class tests.
"""
import unittest
import datetime

from main import Payer,Transaction,Spend,SpendResponse,BalanceResponse

# TODO create an example input for the create_transaction endpoint


class TestPointSystem(unittest.TestCase):
    """Test class for PointSystem."""

    def test_create_transaction(self):
        # Test for valid transaction
        transaction = Transaction(payer=Payer.dannon, points=100, timestamp=datetime.datetime.now())

if __name__ == "__main__":
    unittest.main()
