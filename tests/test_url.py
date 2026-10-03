def test_create_url_without_auth(client):
    response = client.post(
        "/url/urls",
        json={
            "original_url": "https://www.google.com/search?q=hdhub4u&oq=&gs_lcrp=EgZjaHJvbWUqCQgBECMYJxjqAjISCAAQIxgnGOoCGPAFGJ4GGKIHMgkIARAjGCcY6gIyCQgCECMYJxjqAjIJCAMQIxgnGOoCMgkIBBAjGCcY6gIyCQgFECMYJxjqAjIJCAYQIxgnGOoCMgkIBxAjGCcY6gLSAQsxMTM1NTcyajBqN6gCCLACAfEF6wW_9PGMhKHxBesFv_TxjISh&sourceid=chrome&source=chrome.ob&ie=UTF-8"
        },
    )

    print(response.json())

    assert response.status_code == 401


def test_create_url_success(client, headers):

    response = client.post(
        "/url/urls",
        json={
            "original_url": "https://www.google.com/search?q=hdhub4u&oq=&gs_lcrp=EgZjaHJvbWUqCQgBECMYJxjqAjISCAAQIxgnGOoCGPAFGJ4GGKIHMgkIARAjGCcY6gIyCQgCECMYJxjqAjIJCAMQIxgnGOoCMgkIBBAjGCcY6gIyCQgFECMYJxjqAjIJCAYQIxgnGOoCMgkIBxAjGCcY6gLSAQsxMTM1NTcyajBqN6gCCLACAfEF6wW_9PGMhKHxBesFv_TxjISh&sourceid=chrome&source=chrome.ob&ie=UTF-8"
        },
        headers=headers,
    )

    print(response.json())

    assert response.status_code == 201


def test_get_url_detail(client, headers):

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


def test_get_url_detail_not_owner(client, headers):
    

    create_response = client.post(
        "/url/urls",
        json={
            "original_url": "https://www.google.com/search?q=hdhub4u&oq=&gs_lcrp=EgZjaHJvbWUqCQgBECMYJxjqAjISCAAQIxgnGOoCGPAFGJ4GGKIHMgkIARAjGCcY6gIyCQgCECMYJxjqAjIJCAMQIxgnGOoCMgkIBBAjGCcY6gIyCQgFECMYJxjqAjIJCAYQIxgnGOoCMgkIBxAjGCcY6gLSAQsxMTM1NTcyajBqN6gCCLACAfEF6wW_9PGMhKHxBesFv_TxjISh&sourceid=chrome&source=chrome.ob&ie=UTF-8"
        },
        headers=headers,
    )

    url_id = create_response.json()["id"]
     # Create user first
    register_response = client.post(
        "/auth/register",
        json={
            "username": "user5",
            "email": "user5@example.com",
            "password": "password123"
        }
    )

    assert register_response.status_code == 201
    login_response = client.post(
        "/auth/login", json={"username": "user5", "password": "password123"}
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(f"/url/detail/{url_id}", headers=headers)

    data = response.json()

    assert response.status_code == 403


def test_deactivate_url_success(client, headers):

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


def test_deactivate_url_without_auth(client, headers):

    create_response = client.post(
        "/url/urls",
        json={
            "original_url": "https://www.google.com/search?q=hdhub4u&oq=&gs_lcrp=EgZjaHJvbWUqCQgBECMYJxjqAjISCAAQIxgnGOoCGPAFGJ4GGKIHMgkIARAjGCcY6gIyCQgCECMYJxjqAjIJCAMQIxgnGOoCMgkIBBAjGCcY6gIyCQgFECMYJxjqAjIJCAYQIxgnGOoCMgkIBxAjGCcY6gLSAQsxMTM1NTcyajBqN6gCCLACAfEF6wW_9PGMhKHxBesFv_TxjISh&sourceid=chrome&source=chrome.ob&ie=UTF-8"
        },
        headers=headers,
    )

    url_id = create_response.json()["id"]
    
    register_response = client.post(
        "/auth/register",
        json={
            "username": "user5",
            "email": "user5@example.com",
            "password": "password123"
        }
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login", json={"username": "user5", "password": "password123"}
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    response = client.patch(f"/url/deactivate/{url_id}", headers=headers)
    assert response.status_code == 403


def test_redirect_success(client, headers):

    create_response = client.post(
        "/url/urls",
        json={
            "original_url": "https://www.google.com/search?q=hdhub4u&oq=&gs_lcrp=EgZjaHJvbWUqCQgBECMYJxjqAjISCAAQIxgnGOoCGPAFGJ4GGKIHMgkIARAjGCcY6gIyCQgCECMYJxjqAjIJCAMQIxgnGOoCMgkIBBAjGCcY6gIyCQgFECMYJxjqAjIJCAYQIxgnGOoCMgkIBxAjGCcY6gLSAQsxMTM1NTcyajBqN6gCCLACAfEF6wW_9PGMhKHxBesFv_TxjISh&sourceid=chrome&source=chrome.ob&ie=UTF-8"
        },
        headers=headers,
    )

    short_code = create_response.json()["short_code"]

    response = client.get(
        f"/url/redirect/{short_code}", headers=headers, follow_redirects=False
    )

    assert response.status_code == 307


def test_inactive_redirect(client, headers):

    create_response = client.post(
        "/url/urls",
        json={
            "original_url": "https://www.google.com/search?q=hdhub4u&oq=&gs_lcrp=EgZjaHJvbWUqCQgBECMYJxjqAjISCAAQIxgnGOoCGPAFGJ4GGKIHMgkIARAjGCcY6gIyCQgCECMYJxjqAjIJCAMQIxgnGOoCMgkIBBAjGCcY6gIyCQgFECMYJxjqAjIJCAYQIxgnGOoCMgkIBxAjGCcY6gLSAQsxMTM1NTcyajBqN6gCCLACAfEF6wW_9PGMhKHxBesFv_TxjISh&sourceid=chrome&source=chrome.ob&ie=UTF-8"
        },
        headers=headers,
    )

    url_id = create_response.json()["id"]

    response = client.patch(f"/url/deactivate/{url_id}", headers=headers)

    short_code = create_response.json()["short_code"]

    response = client.get(
        f"/url/redirect/{short_code}", headers=headers, follow_redirects=False
    )

    assert response.status_code == 410


def test_expired_redirect(client, headers):

    create_response = client.post(
        "/url/urls",
        json={
            "original_url": "https://www.google.com/search?q=hdhub4u&oq=&gs_lcrp=EgZjaHJvbWUqCQgBECMYJxjqAjISCAAQIxgnGOoCGPAFGJ4GGKIHMgkIARAjGCcY6gIyCQgCECMYJxjqAjIJCAMQIxgnGOoCMgkIBBAjGCcY6gIyCQgFECMYJxjqAjIJCAYQIxgnGOoCMgkIBxAjGCcY6gLSAQsxMTM1NTcyajBqN6gCCLACAfEF6wW_9PGMhKHxBesFv_TxjISh&sourceid=chrome&source=chrome.ob&ie=UTF-8",
            "expires_at": "2026-10-01T00:00:00",
        },
        headers=headers,
    )

    short_code = create_response.json()["short_code"]

    response = client.get(
        f"/url/redirect/{short_code}", headers=headers, follow_redirects=False
    )

    assert response.status_code == 410


def test_not_exist_redirect(client, headers):

    short_code = "x4e5s4"

    response = client.get(
        f"/url/redirect/{short_code}", headers=headers, follow_redirects=False
    )

    assert response.status_code == 404



from src.utils.redis_client import redis_client
def clear_rate_limits():
    for key in redis_client.scan_iter(match="rate_limit:*"):
        redis_client.delete(key)

def test_redirect_records_click(client, headers):
    clear_rate_limits()

    create_response = client.post(
        "/url/urls",
        json={
            "original_url": "https://example.com"
        },
        headers=headers,
    )

    assert create_response.status_code == 201

    data = create_response.json()

    url_id = data["id"]
    short_code = data["short_code"]

    redis_client.delete(f"url:{short_code}")

    response = client.get(
        f"/url/redirect/{short_code}",
        headers=headers,
        follow_redirects=False,
    )

    assert response.status_code == 307

    analytics_response = client.get(
        f"/url/analytics/{url_id}",
        headers=headers,
    )

    assert analytics_response.status_code == 200
    assert analytics_response.json()["total_clicks"] == 1

    clear_rate_limits()


def test_get_my_urls(client, headers):
    

    # Create first URL
    response1 = client.post(
        "/url/urls", json={"original_url": "https://example.com/one"}, headers=headers
    )

    assert response1.status_code == 201

    # Create second URL
    response2 = client.post(
        "/url/urls", json={"original_url": "https://example.com/two"}, headers=headers
    )

    assert response2.status_code == 201

    # Get user's URLs
    response = client.get("/url/my-urls", headers=headers)

    print(response.json())

    assert response.status_code == 200

    data = response.json()

    # Check that URLs are returned
    assert len(data) >= 2


def test_my_urls_pagination(client, headers):

    # Create 5 URLs
    for i in range(5):
        response = client.post(
            "/url/urls",
            json={"original_url": f"https://example.com/{i}"},
            headers=headers,
        )

        assert response.status_code == 201

    # Page 1
    response = client.get("/url/my-urls?page=1&limit=2", headers=headers)

    assert response.status_code == 200

    data = response.json()
    print("PAGE 1:", data)

    # If your API directly returns a list
    assert len(data) == 2

    # Page 2
    response = client.get("/url/my-urls?page=2&limit=2", headers=headers)

    assert response.status_code == 200

    data = response.json()
    print("PAGE 2:", data)

    assert len(data) == 2

    # Page 3
    response = client.get("/url/my-urls?page=3&limit=2", headers=headers)

    assert response.status_code == 200

    data = response.json()
    print("PAGE 3:", data)

    assert len(data) <= 2


def test_my_urls_only_returns_current_user_urls(client, headers):
    

    # Create first URL
    response1 = client.post(
        "/url/urls", json={"original_url": "https://example.com/one"}, headers=headers
    )

    assert response1.status_code == 201

    # Create second URL
    response2 = client.post(
        "/url/urls", json={"original_url": "https://example.com/two"}, headers=headers
    )
    
    register_response = client.post(
        "/auth/register",
        json={
            "username": "user5",
            "email": "user5@example.com",
            "password": "password123"
        }
    )

    assert register_response.status_code == 201
    
    login_response = client.post(
        "/auth/login", json={"username": "user5", "password": "password123"}
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    assert response2.status_code == 201

    # Get user's URLs
    response = client.get("/url/my-urls", headers=headers)

    print(response.json())

    assert response.status_code == 200
  
    
def test_my_urls_invalid_page(client, headers):
    response = client.get(
        "/url/my-urls?page=0&limit=10",
        headers=headers,
    )

    assert response.status_code in [400, 422]
   
 
def test_analytics_url_not_found(client, headers):
    response = client.get(
        "/url/analytics/999999",
        headers=headers,
    )

    assert response.status_code == 404
 
def test_analytics_not_owner(client, headers):
    # Create URL as user6
    response = client.post(
        "/url/urls",
        json={
            "original_url": "https://example.com"
        },
        headers=headers,
    )

    assert response.status_code == 201

    url_id = response.json()["id"]

    # Create another user
    client.post(
        "/auth/register",
        json={
            "username": "anotheruser",
            "email": "another@example.com",
            "password": "password123",
        },
    )

    login_response = client.post(
        "/auth/login",
        json={
            "username": "anotheruser",
            "password": "password123",
        },
    )

    assert login_response.status_code == 200

    another_headers = {
        "Authorization": f"Bearer {login_response.json()['access_token']}"
    }

    response = client.get(
        f"/url/analytics/{url_id}",
        headers=another_headers,
    )

    assert response.status_code == 401
    
    
def test_my_urls_invalid_limit(client, headers):
    response = client.get(
        "/url/my-urls?page=1&limit=0",
        headers=headers,
    )

    assert response.status_code in [400, 422]