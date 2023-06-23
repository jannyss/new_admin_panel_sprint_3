from typing import Generator

from models.movie import Movie
from utils.decorators import coroutine
from utils.logger import logger


class Transformer:
    """
    Class for transforming data from Postgres format to dataclass with ElasticSearch format support.
    """

    @staticmethod
    @coroutine
    def transform_movies(next_node: Generator) -> Generator[list[dict], None, None]:
        while movie_dicts := (yield):
            batch = []
            for movie_dict in movie_dicts:
                movie = Movie(**movie_dict)
                logger.info(movie.json())
                batch.append(movie)
            next_node.send(batch)
