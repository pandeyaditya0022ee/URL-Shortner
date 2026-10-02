def test_create_url_without_auth(client):
    response = client.post(
        "/url/urls",
        json={
            "original_url": "https://www.google.com/search?q=hdhub4u&oq=&gs_lcrp=EgZjaHJvbWUqCQgBECMYJxjqAjISCAAQIxgnGOoCGPAFGJ4GGKIHMgkIARAjGCcY6gIyCQgCECMYJxjqAjIJCAMQIxgnGOoCMgkIBBAjGCcY6gIyCQgFECMYJxjqAjIJCAYQIxgnGOoCMgkIBxAjGCcY6gLSAQsxMTM1NTcyajBqN6gCCLACAfEF6wW_9PGMhKHxBesFv_TxjISh&sourceid=chrome&source=chrome.ob&ie=UTF-8"
        },
    )

    print(response.json())

    assert response.status_code == 401


def test_create_url_success(client):
    login_response = client.post(
        "/auth/login", json={"username": "user6", "password": "password123"}
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/url/urls",
        json={
            "original_url": "https://www.google.com/search?q=hdhub4u&oq=&gs_lcrp=EgZjaHJvbWUqCQgBECMYJxjqAjISCAAQIxgnGOoCGPAFGJ4GGKIHMgkIARAjGCcY6gIyCQgCECMYJxjqAjIJCAMQIxgnGOoCMgkIBBAjGCcY6gIyCQgFECMYJxjqAjIJCAYQIxgnGOoCMgkIBxAjGCcY6gLSAQsxMTM1NTcyajBqN6gCCLACAfEF6wW_9PGMhKHxBesFv_TxjISh&sourceid=chrome&source=chrome.ob&ie=UTF-8"
        },
        headers=headers,
    )

    print(response.json())

    assert response.status_code == 201


def test_get_url_detail(client):
    login_response = client.post(
        "/auth/login", json={"username": "user6", "password": "password123"}
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/url/urls",
        json={
            "original_url": "https://www.google.com/search?q=hdhub4u&oq=&gs_lcrp=EgZjaHJvbWUqCQgBECMYJxjqAjISCAAQIxgnGOoCGPAFGJ4GGKIHMgkIARAjGCcY6gIyCQgCECMYJxjqAjIJCAMQIxgnGOoCMgkIBBAjGCcY6gIyCQgFECMYJxjqAjIJCAYQIxgnGOoCMgkIBxAjGCcY6gLSAQsxMTM1NTcyajBqN6gCCLACAfEF6wW_9PGMhKHxBesFv_TxjISh&sourceid=chrome&source=chrome.ob&ie=UTF-8"
        },
        headers=headers,
    )

    url_id = create_response.json()["id"]

    response = client.get(f"/url/detail/{url_id}", headers=headers)

    data = response.json()

    assert data["id"] == url_id
    assert response.status_code == 200


def test_get_url_detail_not_owner(client):
    login_response = client.post(
        "/auth/login", json={"username": "user6", "password": "password123"}
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/url/urls",
        json={
            "original_url": "https://www.google.com/search?q=hdhub4u&oq=&gs_lcrp=EgZjaHJvbWUqCQgBECMYJxjqAjISCAAQIxgnGOoCGPAFGJ4GGKIHMgkIARAjGCcY6gIyCQgCECMYJxjqAjIJCAMQIxgnGOoCMgkIBBAjGCcY6gIyCQgFECMYJxjqAjIJCAYQIxgnGOoCMgkIBxAjGCcY6gLSAQsxMTM1NTcyajBqN6gCCLACAfEF6wW_9PGMhKHxBesFv_TxjISh&sourceid=chrome&source=chrome.ob&ie=UTF-8"
        },
        headers=headers,
    )

    url_id = create_response.json()["id"]

    login_response = client.post(
        "/auth/login", json={"username": "user5", "password": "password123"}
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(f"/url/detail/{url_id}", headers=headers)

    data = response.json()

    assert response.status_code == 403


def test_deactivate_url_success(client):
    login_response = client.post(
        "/auth/login", json={"username": "user6", "password": "password123"}
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/url/urls",
        json={
            "original_url": "https://www.google.com/search?q=hdhub4u&oq=&gs_lcrp=EgZjaHJvbWUqCQgBECMYJxjqAjISCAAQIxgnGOoCGPAFGJ4GGKIHMgkIARAjGCcY6gIyCQgCECMYJxjqAjIJCAMQIxgnGOoCMgkIBBAjGCcY6gIyCQgFECMYJxjqAjIJCAYQIxgnGOoCMgkIBxAjGCcY6gLSAQsxMTM1NTcyajBqN6gCCLACAfEF6wW_9PGMhKHxBesFv_TxjISh&sourceid=chrome&source=chrome.ob&ie=UTF-8"
        },
        headers=headers,
    )

    url_id = create_response.json()["id"]

    response = client.patch(f"/url/deactivate/{url_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] is False


def test_deactivate_url_without_auth(client):
    login_response = client.post(
        "/auth/login", json={"username": "user6", "password": "password123"}
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/url/urls",
        json={
            "original_url": "https://www.google.com/search?q=hdhub4u&oq=&gs_lcrp=EgZjaHJvbWUqCQgBECMYJxjqAjISCAAQIxgnGOoCGPAFGJ4GGKIHMgkIARAjGCcY6gIyCQgCECMYJxjqAjIJCAMQIxgnGOoCMgkIBBAjGCcY6gIyCQgFECMYJxjqAjIJCAYQIxgnGOoCMgkIBxAjGCcY6gLSAQsxMTM1NTcyajBqN6gCCLACAfEF6wW_9PGMhKHxBesFv_TxjISh&sourceid=chrome&source=chrome.ob&ie=UTF-8"
        },
        headers=headers,
    )

    url_id = create_response.json()["id"]

    login_response = client.post(
        "/auth/login", json={"username": "user5", "password": "password123"}
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    response = client.patch(f"/url/deactivate/{url_id}", headers=headers)
    assert response.status_code == 403
    
    
    
def test_redirect_success(client):
    login_response = client.post(
        "/auth/login", json={"username": "user6", "password": "password123"}
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/url/urls",
        json={
            "original_url": "https://www.google.com/search?q=hdhub4u&oq=&gs_lcrp=EgZjaHJvbWUqCQgBECMYJxjqAjISCAAQIxgnGOoCGPAFGJ4GGKIHMgkIARAjGCcY6gIyCQgCECMYJxjqAjIJCAMQIxgnGOoCMgkIBBAjGCcY6gIyCQgFECMYJxjqAjIJCAYQIxgnGOoCMgkIBxAjGCcY6gLSAQsxMTM1NTcyajBqN6gCCLACAfEF6wW_9PGMhKHxBesFv_TxjISh&sourceid=chrome&source=chrome.ob&ie=UTF-8"
        },
        headers=headers,
    )

    short_code = create_response.json()["short_code"]
    
    response = client.get(
        f"/url/redirect/{short_code}",
        headers=headers,
        follow_redirects=False
    )
    
    assert response.status_code == 307