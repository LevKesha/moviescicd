import requests
import environ


def get_movies(url):
    res = requests.get(url)
    if 200 <= res.status_code < 400:
        return res.data
    else:
        raise Exception('no movies found')


def add_new_movie(url, movie: dict):
    res = requests.post(url, json={})


def check_movie_addtion(url):
    movie = {}
    add_new_movie(url, movie=)
    movies = get_movies(url)
    for k, v in movies.items():
        if k == 'name':
            v == 'adam project'


if __name__ == '__main__':
    url = environ.get.URL or 'localhost:80/movie'