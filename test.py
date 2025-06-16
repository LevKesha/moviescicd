#!/usr/bin/env python3
import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()
API_URL = os.getenv("URL", "http://localhost:605/movie")


# ---------- helper ---------- #
def _json_or_raise(resp: requests.Response):
    """
    Return resp.json() iff the response is successful **and**
    declares a JSON content-type. Otherwise raise with a clear message.
    """
    if resp.status_code >= 400:
        raise Exception(
            f"{resp.request.method} {resp.url} → {resp.status_code}:\n{resp.text}"
        )

    ctype = resp.headers.get("Content-Type", "")
    if "application/json" not in ctype.lower():
        snippet = resp.text[:300].replace("\n", " ")
        raise Exception(
            f"Expected JSON but got '{ctype}'. Body (truncated): {snippet}"
        )

    return resp.json()


# ---------- API wrappers ---------- #
def get_movies():
    r = requests.get(API_URL)
    return _json_or_raise(r)


def add_movie(payload):
    r = requests.post(API_URL, json=payload)
    movies = _json_or_raise(r)          # also checks 2xx
    new = movies[-1]                    # last element should be the new movie
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
    return _json_or_raise(r)


def update_movie(mid, payload):
    url = f"{API_URL}/{mid}"
    r = requests.put(url, json=payload)
    return _json_or_raise(r)


def delete_movie(mid):
    url = f"{API_URL}/{mid}"
    r = requests.delete(url)
    if r.status_code != 204:
        raise Exception(
            f"DELETE failed ({r.status_code}): {r.text}"
        )


# ---------- test flow ---------- #
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
