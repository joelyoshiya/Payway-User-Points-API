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
        assert response.json() == {"message": "server up and running"}

    # Account Creation
    def test_create_account(self):
        response = client.post(
            "/users/", 
            json={"firstName": "John", "lastName": "Doe", "email": "john.doe@gmail.com", "userName" : "jdoe"},
        )
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "userName": "jdoe",
            "message": "account created"
        }

    def test_create_duplicate_username(self):
        response = client.post(
            "/users/", 
            json={"firstName": "bad", "lastName": "request", "email": "bad.request@gmail.com", "userName" : "jdoe"},
        )
        assert response.status_code == 400
        assert response.json() == {
            "detail": "username is taken"
        }
    
    def test_create_duplicate_email(self):
        response = client.post(
            "/users/", 
            json={"firstName": "same", "lastName": "mail", "email": "john.doe@gmail.com", "userName" : "sameEmail"},
        )
        assert response.status_code == 400
        assert response.json() == {
            "detail": "account already created with this email"
        }

    # Testing User Account getter
    def test_create_duplicate_account(self):
        response = client.get(
            "/users/jdoe",
        )
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "userName": "jdoe",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@gmail.com"
        }

    def test_get_inexistent_account(self):
        response = client.get(
            "/users/bad_user",
        )
        assert response.status_code == 404
        assert response.json() == {
            "detail": "user not found"
        }

    # Validating Transactions
    def test_create_transaction(self):
        # Test for valid transaction
        transaction_1 = Transaction(tid=1,payer="DANNON", points=1000, timestamp="2020-11-02T14:00:00Z")
        # TODO TypeError: Object of type datetime is not JSON serializable
        response = client.post( 
            "/users/jdoe/transactions/",
            json=transaction_1.dict(),
        )
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "payer": "dannon",
            "points": 100,
            "timestamp": "2020-11-02T14:00:00Z"
        }

    def test_create_transaction_bad_payer(self):
        transaction_2 = Transaction(tid=2,payer="bad_payer", points=100, timestamp="2020-11-02T14:00:00Z")
        response = client.post(
            "/users/jdoe/transactions/",
            json=transaction_2.dict(),
        )
        assert response.status_code == 400
        assert response.json() == {
            "detail": "payer not found"
        }

    def test_create_transaction_bad_points(self):
        transaction_3 = Transaction(tid=3,payer="DANNON", points="bad", timestamp="2020-11-02T14:00:00Z")
        response = client.post(
            "/users/jdoe/transactions/",
            json=transaction_3.dict(),
        )
        assert response.status_code == 400
        assert response.json() == {
            "detail": "invalid points"
        }

    def test_create_transaction_points_exceed_max(self):
        transaction_4 = Transaction(tid=4,payer="DANNON", points=1000000000, timestamp="2020-11-02T14:00:00Z")
        response = client.post(
            "/users/jdoe/transactions/",
            json=transaction_4.dict(),
        )
        assert response.status_code == 400
        assert response.json() == {
            "detail": "points exceed max for a single transaction"
        }
    
    def test_create_transaction_points_exceed_min(self):
        transaction_4 = Transaction(tid=4,payer="DANNON", points=-1000000000, timestamp="2020-11-02T14:00:00Z")
        response = client.post(
            "/users/jdoe/transactions/",
            json=transaction_4.dict(),
        )
        assert response.status_code == 400
        assert response.json() == {
            "detail": "points exceed minimum for a single transaction"
        }

    def test_create_transaction_bad_date(self):
        transaction_5 = Transaction(tid=5,payer="DANNON", points=-1000000000, timestamp="malformed date")
        response = client.post(
            "/users/jdoe/transactions/",
            json=transaction_5.dict(),
        )
        assert response.status_code == 400
        assert response.json() == {
            "detail": "malformed date"
        }


    # Now post rest of valid transactions to account
    def test_post_rest_transactions(self):
        transaction_2 = Transaction(tid=2,payer="UNILEVER", points=200, timestamp="2020-10-31T11:00:00Z")
        transaction_3 = Transaction(tid=3,payer="DANNON", points=-200, timestamp="2020-10-31T15:00:00Z")
        transaction_4 = Transaction(tid=4,payer="MILLER COORS", points=10000, timestamp="2020-11-01T14:00:00Z")
        transaction_5 = Transaction(tid=5,payer="DANNON", points=300, timestamp="2020-10-31T10:00:00Z")
        # now post rest of valid transactions
        transactions = [transaction_2, transaction_3, transaction_4, transaction_5]
        for transaction in transactions:
            response = client.post(
                "/users/jdoe/transactions/",
                json=transaction.dict(),
            )
            assert response.status_code == 200
            # validate full transaction payload
            assert response.json() == {
                "id": transaction.tid,
                "payer": transaction.payer,
                "points": transaction.points,
                "timestamp": transaction.timestamp
            }

    # Validating Account State before and after spending
    def test_get_balance_pre_spend(self):
        response = client.get(
            "/users/jdoe/points/"
        )
        assert response.status_code == 200
        assert response.json() == {
        "DANNON": 1100,
        "UNILEVER": 200,
        "MILLER COORS": 10000
        }

    # Validating correct spending behavior
    def test_spend_points(self):
        # TODO figure out if should be PUT or POST
        response = client.put(
            "/users/jdoe/spend/",
            json={"points": 5000}
        )
        assert response.status_code == 200
        assert response.json() == {
            { "payer": "DANNON", "points": -100 },
            { "payer": "UNILEVER", "points": -200 },
            { "payer": "MILLER COORS", "points": -4700 }
        }
    
    def test_spend_points_exceed_balance(self):
        response = client.put(
            "/users/jdoe/spend/",
            json={"points": 100000000}
        )
        assert response.status_code == 400
        assert response.json() == {
            "detail": "spending exceeds account balance"
        }
    
    def test_spend_points_below_minimum(self):
        response = client.put(
            "/users/jdoe/spend/",
            json={"points": 1}
        )
        assert response.status_code == 400
        assert response.json() == {
            "detail": "spending below minimum spending amount"
        }

    def test_get_balance_post_spend(self):
        response = client.get(
            "/users/jdoe/points/"
        )
        assert response.status_code == 200
        assert response.json() == {
            "DANNON": 1000,
            "UNILEVER": 0,
            "MILLER COORS": 5300
        }

if __name__ == "__main__":
   unittest.main()
