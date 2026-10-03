from src.utils.redis_client import redis_client


def clear_rate_limits():
    for key in redis_client.scan_iter(match="rate_limit:*"):
        redis_client.delete(key)


def test_rate_limit_allows_first_10_requests(client, headers):
    clear_rate_limits()

    # Create URL
    response = client.post(
        "/url/urls",
        json={
            "original_url": "https://example.com"
        },
        headers=headers,
    )

    assert response.status_code == 201

    short_code = response.json()["short_code"]

    # First 10 requests should be allowed
    for _ in range(10):
        response = client.get(
            f"/url/redirect/{short_code}",
            follow_redirects=False,
        )

        assert response.status_code == 307

    clear_rate_limits()


def test_rate_limit_blocks_11th_request(client, headers):
    clear_rate_limits()

    # Create URL
    response = client.post(
        "/url/urls",
        json={
            "original_url": "https://example.com"
        },
        headers=headers,
    )

    assert response.status_code == 201

    short_code = response.json()["short_code"]

    # First 10 requests
    for _ in range(10):
        response = client.get(
            f"/url/redirect/{short_code}",
            follow_redirects=False,
        )

        assert response.status_code == 307

    # 11th request
    response = client.get(
        f"/url/redirect/{short_code}",
        follow_redirects=False,
    )

    assert response.status_code == 429
    assert response.json()["detail"] == "Too many requests"

    clear_rate_limits()


def test_rate_limit_key_has_ttl(client, headers):
    clear_rate_limits()

    response = client.post(
        "/url/urls",
        json={
            "original_url": "https://example.com"
        },
        headers=headers,
    )

    assert response.status_code == 201

    short_code = response.json()["short_code"]

    # First request creates rate-limit key
    response = client.get(
        f"/url/redirect/{short_code}",
        follow_redirects=False,
    )

    assert response.status_code == 307

    # Find rate-limit key
    keys = list(redis_client.scan_iter(match="rate_limit:*"))

    assert len(keys) >= 1

    # Check TTL
    ttl = redis_client.ttl(keys[0])

    assert ttl > 0
    assert ttl <= 60

    clear_rate_limits()