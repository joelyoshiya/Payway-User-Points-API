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
        transaction_1 = Transaction(tid=1,payer=Payer.dannon, points=100, timestamp=datetime.datetime.now())
        pass

    def test_create_transaction_bad_payer(self):
        pass

    def test_create_transaction_bad_points(self):
        pass

    def test_create_transaction_bad_date(self):
        pass

    
    # Validating Account State post Transaction POST
    def test_get_balance(self):
        pass

    # Validating correct spending behavior
    def test_spend_points(self):
        pass

    def test_spend_points_bad_request(self):
        pass

if __name__ == "__main__":
   unittest.main()
