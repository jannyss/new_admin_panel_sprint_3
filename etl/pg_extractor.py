from datetime import datetime
from typing import Generator

import psycopg

from utils.decorators import coroutine
from utils.logger import logger


class PostgresExtractor:
    BATCH_SIZE = 100

    def __init__(self, cursor: psycopg.cursor.Cursor):
        self.cursor = cursor

    @coroutine
    def fetch_changed_movies(self, next_node: Generator) -> Generator[datetime, None, None]:
        while last_updated := (yield):
            logger.info(f'Fetching movies changed after ' f'{last_updated}')
            sql = 'SELECT * FROM movies WHERE updated_at > %s order by updated_at asc'
            logger.info('Fetching movies updated after %s', last_updated)
            self.cursor.execute(sql, (last_updated,))
            while results := self.cursor.fetchmany(size=self.BATCH_SIZE):
                next_node.send(results)
