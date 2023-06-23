from typing import Generator

from elasticsearch import Elasticsearch

from etl.es_config import MAPPINGS, SETTINGS
from etl.utils.logger import logger
from models.movie import Movie
from state.state import State, STATE_KEY
from utils.decorators import coroutine


class ElasticSearchWorker:
    def __init__(self, host: str = '127.0.0.1', port: int = 9200, index_name: str = 'movies'):
        self.es = Elasticsearch(f'http://{host}:{port}')
        self.index_name = index_name

    def create_index(self):
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

    def __init__(self, es_worker: ElasticSearchWorker):
        self.worker = es_worker

    @coroutine
    def save_movies(self, state: State) -> Generator[list[Movie], None, None]:
        while movies := (yield):
            logger.info(f'Received for saving {len(movies)} movies')
            for movie in movies:
                self.worker.es.index(index=self.worker.index_name, id=str(movie.id), document=movie.to_es_doc())
            state.set_state(STATE_KEY, str(movies[-1].updated_at))
