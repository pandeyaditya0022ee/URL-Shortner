
def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "user6",
            "email": "user6@example.com",
            "password": "password123"
        }
    )

    print(response.json())

    assert response.status_code == 201



def test_duplicate_email(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "test3user123",
            "email": "user1@example.com",
            "password": "password123"
        }
    )

    print(response.json())

    assert response.status_code == 409
    
    
    
def test_duplicate_username(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "user1",
            "email": "test3@example.com",
            "password": "password123"
        }
    )

    print(response.json())

    assert response.status_code == 409
    
