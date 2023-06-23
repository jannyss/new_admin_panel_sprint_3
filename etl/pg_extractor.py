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
            sql = '''
            SELECT 
            "content"."film_work"."id", 
            "content"."film_work"."rating" as "imdb_rating",
            "content"."film_work"."title", 
            "content"."film_work"."description", 
            "content"."film_work"."type", 
            "content"."film_work"."updated_at", 
            ARRAY_AGG(DISTINCT "content"."genre"."name" ) AS "genre",
            ARRAY_AGG(DISTINCT "content"."person"."full_name" ) 
                FILTER (WHERE "content"."person_film_work"."role" = 'director') AS "director",
            ARRAY_AGG(DISTINCT "content"."person"."full_name" ) 
                FILTER (WHERE "content"."person_film_work"."role" = 'actor') AS "actors_names",
            ARRAY_AGG(DISTINCT "content"."person"."id" ) 
                FILTER (WHERE "content"."person_film_work"."role" = 'actor') AS "actors_ids",
            ARRAY_AGG(DISTINCT "content"."person"."full_name" ) 
                FILTER (WHERE "content"."person_film_work"."role" = 'writer') AS "writers_names",
            ARRAY_AGG(DISTINCT "content"."person"."id" ) 
                FILTER (WHERE "content"."person_film_work"."role" = 'writer') AS "writers_ids"
            FROM "content"."film_work"
            LEFT OUTER JOIN "content"."genre_film_work" 
                ON ("content"."film_work"."id" = "content"."genre_film_work"."film_work_id")
            LEFT OUTER JOIN "content"."genre" 
                ON ("content"."genre_film_work"."genre_id" = "content"."genre"."id")
            LEFT OUTER JOIN "content"."person_film_work" 
                ON ("content"."film_work"."id" = "content"."person_film_work"."film_work_id")
            LEFT OUTER JOIN "content"."person" 
                ON ("content"."person_film_work"."person_id" = "content"."person"."id")
            WHERE "content"."film_work"."updated_at" > %s 
            GROUP BY "content"."film_work"."id"
            ORDER BY "content"."film_work"."updated_at" asc
            '''
            logger.info('Fetching movies updated after %s', last_updated)
            self.cursor.execute(sql, (last_updated,))
            while results := self.cursor.fetchmany(size=self.BATCH_SIZE):
                next_node.send(results)
