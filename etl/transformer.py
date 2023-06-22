from typing import Generator

from etl.utils.decorators import coroutine
from models.movie import Movie
from utils.logger import logger


class Transformer:

    @staticmethod
    @coroutine
    def transform_movies(next_node: Generator) -> Generator[list[dict], None, None]:
        while movie_dicts := (yield):
            batch = []
            for movie_dict in movie_dicts:
                movie = Movie(**movie_dict)
                movie.title = movie.title.upper()
                logger.info(movie.json())
                batch.append(movie)
            next_node.send(batch)
