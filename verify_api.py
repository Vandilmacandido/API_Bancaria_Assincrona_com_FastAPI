from fastapi.testclient import TestClient
from app.main import app

from fastapi.testclient import TestClient
from app.main import app

def test_api():
    print("--- Starting Verification ---")
    
    with TestClient(app) as client:
        # 1. Register User
        print("\n1. Registering User...")
        response = client.post("/register", json={"username": "testuser", "password": "password123"})
        if response.status_code == 200:
            print("Success:", response.json())
        else:
            print("Failed:", response.text)
            # If user already exists (from previous run), try login
            
        # 2. Login
        print("\n2. Logging in...")
        response = client.post("/token", data={"username": "testuser", "password": "password123"})
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("Success: Got Token")
        else:
            print("Failed to login:", response.text)
            return

        headers = {"Authorization": f"Bearer {token}"}

        # 3. Deposit
        print("\n3. Depositing 100.0...")
        response = client.post("/transactions/deposit", json={"amount": 100.0}, headers=headers)
        print("Status:", response.status_code)
        print("Response:", response.json())

        # 4. Withdraw
        print("\n4. Withdrawing 50.0...")
        response = client.post("/transactions/withdraw", json={"amount": 50.0}, headers=headers)
        print("Status:", response.status_code)
        print("Response:", response.json())

        # 5. Invalid Withdraw
        print("\n5. Attempting to withdraw 1000.0 (Should fail)...")
        response = client.post("/transactions/withdraw", json={"amount": 1000.0}, headers=headers)
        print("Status:", response.status_code)
        print("Response:", response.json())

        # 6. Statement
        print("\n6. Getting Statement...")
        response = client.get("/transactions/statement", headers=headers)
        print("Status:", response.status_code)
        data = response.json()
        print("Balance:", data.get("balance"))
        print("Transactions Count:", len(data.get("transactions", [])))
        print("Latest Transaction:", data.get("transactions", [])[-1] if data.get("transactions") else "None")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    test_api()
