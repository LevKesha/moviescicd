#!/usr/bin/env python3
import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()
API_URL = os.getenv("URL", "http://localhost:605/movie")

def get_movies():
    r = requests.get(API_URL)
    r.raise_for_status()
    return r.json()

def add_movie(payload):
    r = requests.post(API_URL, json=payload)
    # Our API returns the full movie list with a 200 status on POST
    if r.status_code != 200:
        raise Exception(f"POST failed ({r.status_code}): {r.text}")
    movies = r.json()
    # The newly added movie should be the last element
    new = movies[-1]
    if new.get("name") != payload.get("name"):
        raise Exception(
            f"Last movie name mismatch: expected {payload['name']}, got {new.get('name')}"
        )
    return new

def get_movie_by_id(mid):
    url = f"{API_URL}/{mid}"
    r = requests.get(url)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()

def update_movie(mid, payload):
    url = f"{API_URL}/{mid}"
    r = requests.put(url, json=payload)
    if r.status_code != 200:
        raise Exception(f"PUT failed ({r.status_code}): {r.text}")
    return r.json()

def delete_movie(mid):
    url = f"{API_URL}/{mid}"
    r = requests.delete(url)
    if r.status_code != 204:
        raise Exception(f"DELETE failed ({r.status_code}): {r.text}")

def main():
    print(f"→ GET movie list @ {API_URL}")
    movies = get_movies()
    assert isinstance(movies, list), f"Expected list, got {type(movies)}"

    print("→ POST new movie")
    new_payload = {"name": "CI Movie", "genre": "test", "length": 123}
    created = add_movie(new_payload)
    mid = created.get("id")
    assert created.get("name") == new_payload["name"], "POSTed movie name mismatch"

    print(f"→ GET /movie/{mid}")
    fetched = get_movie_by_id(mid)
    assert fetched and fetched.get("id") == mid, "GET by ID failed"

    print(f"→ PUT /movie/{mid}")
    updated = update_movie(mid, {"name": "CI Movie Updated"})
    assert updated.get("name") == "CI Movie Updated", "PUT did not update name"

    print(f"→ DELETE /movie/{mid}")
    delete_movie(mid)

    print(f"→ GET deleted /movie/{mid} (should 404)")
    assert get_movie_by_id(mid) is None, "Deleted movie still found"

    print("✔ All tests passed.")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print("Test failure:", e, file=sys.stderr)
        sys.exit(1)
