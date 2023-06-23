from typing import Generator

import backoff
from elasticsearch import Elasticsearch

from es_config import MAPPINGS, SETTINGS
from utils.logger import logger
from models.movie import Movie
from state.state import State, STATE_KEY
from utils.decorators import coroutine


class ElasticSearchWorker:
    """Class for work with ElasticSearch."""
    def __init__(self, host: str, port: int, index_name: str = 'movies'):
        self.es = Elasticsearch(f'http://{host}:{port}')
        self.index_name = index_name

    @backoff.on_exception(backoff.expo, Exception)
    def create_index(self):
        """Creates index."""
        if self.es.indices.exists(index=self.index_name):
            logger.info(f'Index {self.index_name} is already exists')
            return
        self.es.indices.create(
            index=self.index_name,
            mappings=MAPPINGS,
            settings=SETTINGS,
        )
        logger.info(f'Index {self.index_name} was created')


class ElasticSearchLoader:
    """Class for loading data to ElasticSearch."""

    def __init__(self, es_worker: ElasticSearchWorker):
        self.worker = es_worker

    @coroutine
    @backoff.on_exception(backoff.expo, Exception)
    def save_movies(self, state: State) -> Generator[list[Movie], None, None]:
        """Saves movies to ElasticSearch. Updates state."""
        while movies := (yield):
            logger.info(f'Received for saving {len(movies)} movies')
            for movie in movies:
                self.worker.es.index(
                    index=self.worker.index_name,
                    id=str(movie.id),
                    document=movie.to_es_doc(),
                )
                logger.info(f'Movie data for id={movie.id} were loaded')
            state.set_state(STATE_KEY, str(movies[-1].updated_at))
