import os
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

movies = [
    {"id": 1, "name": "spider man 3", "length": 139, "genre": "sci-fi"},
    {"id": 2, "name": "undisputed",    "length": 110, "genre": "action"},
]

# -------- HELPER -------- #
def _find_movie(idx):
    return next((m for m in movies if m["id"] == idx), None)

# -------- ROUTES -------- #
@app.get("/movie")
def get_all_movies():
    """Return full list."""
    return jsonify(movies), 200


@app.get("/movie/<int:mid>")
def get_movie(mid):
    movie = _find_movie(mid)
    if movie:
        return jsonify(movie), 200
    return "", 404


@app.post("/movie")
def add_movie():
    movie = request.get_json(force=True) or {}
    movie["id"] = (movies[-1]["id"] + 1) if movies else 1
    movies.append(movie)
    return jsonify(movies), 200


@app.put("/movie/<int:mid>")
def change_movie(mid):
    movie = _find_movie(mid)
    if not movie:
        return "", 404

    new_data = request.get_json(force=True) or {}
    # keep the original id if client didn't send one
    new_data["id"] = mid
    movies[movies.index(movie)] = new_data
    return jsonify(new_data), 200


@app.delete("/movie/<int:mid>")
def delete_movie(mid):
    movie = _find_movie(mid)
    if not movie:
        return "", 404

    movies.remove(movie)
    return "", 204


# Optional: wipe all movies (not used in CI tests)
@app.delete("/movie")
def delete_all_movies():
    movies.clear()
    return "", 204


if __name__ == "__main__":
    # honour $PORT (default 605) for CI
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 605)), debug=True)
