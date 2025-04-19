import unittest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


class TestUserAPI(unittest.TestCase):

    def test_create_user_success(self):
        response = client.post(
            "/users", json={"name": "Test User", "email": "testuser@example.com"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_id", response.json())

    def test_create_user_invalid_email(self):
        response = client.post(
            "/users", json={"name": "Invalid Email User", "email": "invalid-email"}
        )
        self.assertEqual(response.status_code, 422)

    def test_create_user_empty_name(self):
        response = client.post(
            "/users", json={"name": "", "email": "emptyname@example.com"}
        )
        self.assertEqual(response.status_code, 422)

    def test_create_user_duplicate_email(self):
        # First insert
        client.post("/users", json={"name": "Dup", "email": "dup@example.com"})

        # Insert again with same email
        response = client.post(
            "/users", json={"name": "Dup2", "email": "dup@example.com"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email already exists", response.text)

    def test_get_all_users(self):
        response = client.get("/users")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_single_user_not_found(self):
        response = client.get("/users/99999")  # Assuming this ID doesn’t exist
        self.assertEqual(response.status_code, 404)

    def test_update_user_not_found(self):
        response = client.put(
            "/users/99999", json={"name": "New Name", "email": "newemail@example.com"}
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_user_not_found(self):
        response = client.delete("/users/99999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
