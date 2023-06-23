import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class Movie(BaseModel):
    """Dataclass for movie."""
    id: uuid.UUID
    title: str
    genre: list[str]
    imdb_rating: Optional[str]
    updated_at: datetime
    description: Optional[str]
    director: Optional[list[str]]
    actors_names: Optional[list[str]]
    actors_ids: Optional[list[uuid.UUID]]
    writers_names: Optional[list[str]]
    writers_ids: Optional[list[uuid.UUID]]

    def to_es_doc(self) -> dict[str, Any]:
        """Converts for ElasticSearch doc format."""
        doc = {
            'id': self.id,
            'imdb_rating': self.imdb_rating,
            'genre': self.genre,
            'title': self.title,
            'description': self.description,
            'director': self.director if self.director else [],
            'actors_names': self.actors_names if self.actors_names else [],
            'writers_names': self.writers_names if self.writers_names else [],
        }
        if self.actors_ids and self.actors_names:
            doc.update({'actors': [
                {
                    'id': actor_id,
                    'name': actor_name,
                } for actor_id, actor_name in zip(self.actors_ids, self.actors_names)
            ]})
        else:
            doc.update({'actors': []})
        if self.writers_ids and self.writers_names:
            doc.update({'writers':  [
                {
                    'id': writer_id,
                    'name': writer_name,
                } for writer_id, writer_name in zip(self.writers_ids, self.writers_names)
            ]})
        else:
            doc.update({'writers': []})
        return doc
