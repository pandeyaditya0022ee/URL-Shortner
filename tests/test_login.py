def test_login(client):
    response = client.post(
        "/auth/login",
        json = {
            "username" : "test4user123",
            "password" : "password123"
        }
    )
    print(response.json())

    assert response.status_code == 200
    
    
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
    
