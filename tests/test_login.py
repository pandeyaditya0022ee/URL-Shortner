def test_login(client):
    # Create user first
    register_response = client.post(
        "/auth/register",
        json={
            "username": "user6",
            "email": "user6@example.com",
            "password": "password123"
        }
    )

    assert register_response.status_code == 201

    # Login
    response = client.post(
        "/auth/login",
        json={
            "username": "user6",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    
def test_wrong_password(client):
    response = client.post(
        "/auth/login",
        json = {
            "username" : "test4user123",
            "password" : "password"
        }
    )
    print(response.json())

    assert response.status_code == 401
    
    
    
def test_invalid_user(client):
    response = client.post(
        "/auth/login",
        json = {
            "username" : "xyzuser123",
            "password" : "password"
        }
    )
    print(response.json())

    assert response.status_code == 401
    
