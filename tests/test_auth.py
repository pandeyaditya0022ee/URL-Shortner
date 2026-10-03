
def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "user7",
            "email": "user7@example.com",
            "password": "password123"
        }
    )

    print(response.json())

    assert response.status_code == 201



def test_duplicate_email(client):
    # First user
    client.post(
        "/auth/register",
        json={
            "username": "user1",
            "email": "user1@example.com",
            "password": "password123"
        }
    )

    # Duplicate email
    response = client.post(
        "/auth/register",
        json={
            "username": "test3user123",
            "email": "user1@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 409
    
    
    
def test_duplicate_username(client):
    # First user
    client.post(
        "/auth/register",
        json={
            "username": "user1",
            "email": "user1@example.com",
            "password": "password123"
        }
    )

    # Duplicate username
    response = client.post(
        "/auth/register",
        json={
            "username": "user1",
            "email": "test3@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 409
    
