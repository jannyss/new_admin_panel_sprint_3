from datetime import date
from time import sleep

import psycopg
from psycopg import ServerCursor
from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row

from es_loader import ElasticSearchLoader
from es_loader import ElasticSearchWorker
from utils.logger import logger
from pg_extractor import PostgresExtractor
from settings import database_settings, es_settings
from state.json_file_storage import JsonFileStorage
from state.state import State, STATE_KEY
from transformer import Transformer

if __name__ == '__main__':
    state = State(JsonFileStorage())
    logger.info(f'Initial state is {state.state}')

    pg_dsn = make_conninfo(**database_settings.dict())
    es_dsn = es_settings.dict()

    es_worker = ElasticSearchWorker(**es_dsn)
    es_worker.create_index()

    with (
        psycopg.connect(pg_dsn, row_factory=dict_row) as conn, \
            ServerCursor(conn, 'fetcher') as pg_cur,
    ):
        pg_retriever = PostgresExtractor(pg_cur)
        es_loader = ElasticSearchLoader(es_worker)
        transformer = Transformer()

        saver_coro = es_loader.save_movies(state)
        transformer_coro = transformer.transform_movies(next_node=saver_coro)
        fetcher_coro = pg_retriever.fetch_changed_movies(transformer_coro)

        while True:
            last_movies_updated = state.get_state(STATE_KEY)
            logger.info('Starting ETL process for updates ...')

            fetcher_coro.send(state.get_state(STATE_KEY) or str(date(1970, 1, 1)))

            logger.info('ETL process wsa ended. Sleeping for 20 secs ...')
            sleep(20)
