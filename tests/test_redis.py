import json
from datetime import datetime, timedelta

from src.utils.redis_client import redis_client


def test_cache_miss_populates_redis(client, headers):
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
    key = f"url:{short_code}"

    # Make sure cache doesn't already exist
    redis_client.delete(key)

    # First request -> Redis MISS -> Database -> Redis
    response = client.get(
        f"/url/redirect/{short_code}",
        follow_redirects=False,
    )

    assert response.status_code == 307

    # Redis should now contain the URL
    cached = redis_client.get(key)

    assert cached is not None

    cached_data = json.loads(cached)

    assert cached_data["original_url"] == "https://example.com"


def test_cache_hit_returns_cached_url(client, headers):
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
    key = f"url:{short_code}"

    redis_client.delete(key)

    # First request populates cache
    response1 = client.get(
        f"/url/redirect/{short_code}",
        headers=headers,
        follow_redirects=False,
    )

    assert response1.status_code == 307

    # Second request should use cache
    response2 = client.get(
        f"/url/redirect/{short_code}",
        headers=headers,
        follow_redirects=False,
    )

    assert response2.status_code == 307
    assert response2.headers["location"] == "https://example.com"

    # Cache should still exist
    assert redis_client.get(key) is not None


def test_cache_has_ttl(client, headers):
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
    key = f"url:{short_code}"

    redis_client.delete(key)

    # Populate cache
    response = client.get(
        f"/url/redirect/{short_code}",
        headers=headers,
        follow_redirects=False,
    )

    assert response.status_code == 307

    # Check TTL
    ttl = redis_client.ttl(key)

    assert ttl > 0
    assert ttl <= 300
    
def test_inactive_url_not_served_from_cache(client, headers):
    response = client.post(
        "/url/urls",
        json={
            "original_url": "https://example.com"
        },
        headers=headers,
    )

    assert response.status_code == 201

    data = response.json()
    
    url_id = data["id"]

    short_code = data["short_code"]

    # Deactivate URL
    response = client.patch(
        f"/url/deactivate/{url_id}",
        headers=headers,
    )

    assert response.status_code == 200

    # Redirect should not work
    response = client.get(
        f"/url/redirect/{short_code}",
        headers=headers,
        follow_redirects=False,
    )

    assert response.status_code == 410
    



def test_expired_url_from_cache(client, headers):
    response = client.post(
        "/url/urls",
        json={
            "original_url": "https://example.com",
            "expires_at": (datetime.now() - timedelta(minutes=5)).isoformat(),
        },
        headers=headers,
    )

    assert response.status_code == 201

    data = response.json()
    short_code = data["short_code"]

    key = f"url:{short_code}"

    # Manually put expired URL into Redis
    cached_data = {
        "id": data["id"],
        "original_url": "https://example.com",
        "is_active": True,
        "expires_at": (
            datetime.now() - timedelta(minutes=5)
        ).isoformat(),
    }

    redis_client.set(
        key,
        json.dumps(cached_data),
        ex=300,
    )

    response = client.get(
        f"/url/redirect/{short_code}",
        headers=headers,
        follow_redirects=False,
    )

    assert response.status_code == 410

    redis_client.delete(key)