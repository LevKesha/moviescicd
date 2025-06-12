#!/usr/bin/env python3
import os
import sys
import requests
from dotenv import load_dotenv

# Load .env if present, then fallback defaults
load_dotenv()
API_URL = os.getenv("URL", "http://localhost:1993/movie")

def get_movies():
    r = requests.get(API_URL)
    r.raise_for_status()
    return r.json()

def add_movie(payload):
    r = requests.post(API_URL, json=payload)
    if r.status_code != 201:
        raise Exception(f"POST failed ({r.status_code}): {r.text}")
    return r.json()

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
    print(f"→ GET empty list @ {API_URL}")
    movies = get_movies()
    assert movies == [], f"Expected empty list, got {movies}"

    print("→ POST new movie")
    new = {"name": "CI Movie", "genre": "test", "length": 123}
    created = add_movie(new)
    mid = created["id"]
    assert created["name"] == new["name"]

    print(f"→ GET /{mid}")
    fetched = get_movie_by_id(mid)
    assert fetched and fetched["id"] == mid

    print(f"→ PUT /{mid}")
    updated = update_movie(mid, {"name": "CI Movie X"})
    assert updated["name"] == "CI Movie X"

    print(f"→ DELETE /{mid}")
    delete_movie(mid)

    print(f"→ GET deleted /{mid} (should 404)")
    assert get_movie_by_id(mid) is None

    print("All tests passed.")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print("Test failure:", e, file=sys.stderr)
        sys.exit(1)
