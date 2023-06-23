CREATE SCHEMA IF NOT EXISTS "content";
CREATE TABLE IF NOT EXISTS "content"."film_work" (
    "id" uuid PRIMARY KEY,
    "title" TEXT NOT NULL,
    "description" TEXT,
    "creation_date" DATE,
    "rating" FLOAT,
    "type" TEXT NOT NULL,
    "file_path" TEXT,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL
);

CREATE TABLE IF NOT EXISTS "content"."genre" (
    "id" uuid PRIMARY KEY,
    "name" TEXT NOT NULL UNIQUE,
    "description" TEXT,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL
);

CREATE TABLE IF NOT EXISTS "content"."person" (
    "id" uuid PRIMARY KEY,
    "full_name" TEXT NOT NULL UNIQUE,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL
);

CREATE TABLE IF NOT EXISTS "content"."genre_film_work" (
    "id" uuid PRIMARY KEY,
    "genre_id" uuid NOT NULL,
    "film_work_id" uuid NOT NULL,
    "created_at" timestamp with time zone NOT NULL,
    CONSTRAINT fk_genre_id
    FOREIGN KEY (genre_id)
    REFERENCES content.genre (id)
    ON DELETE CASCADE,
    CONSTRAINT fk_film_work_id_genre
    FOREIGN KEY (film_work_id)
    REFERENCES content.film_work (id)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "content"."person_film_work" (
    "id" uuid PRIMARY KEY,
    "person_id" uuid NOT NULL,
    "film_work_id" uuid NOT NULL,
	"role" TEXT NOT NULL,
    "created_at" timestamp with time zone NOT NULL,
    CONSTRAINT fk_person_id
    FOREIGN KEY (person_id)
    REFERENCES content.person (id)
    ON DELETE CASCADE,
    CONSTRAINT fk_film_work_id_person
    FOREIGN KEY (film_work_id)
    REFERENCES content.film_work (id)
    ON DELETE CASCADE
);

CREATE INDEX "genre_film_work_film_work_id_idx" ON "content"."genre_film_work" ("film_work_id");
CREATE INDEX "genre_film_work_genre_id_idx" ON "content"."genre_film_work" ("genre_id");

CREATE INDEX "person_film_work_film_work_id_idx" ON "content"."person_film_work" ("film_work_id");
CREATE INDEX "person_film_work_person_id_idx" ON "content"."person_film_work" ("person_id");

CREATE UNIQUE INDEX "film_work_genre_idx" ON "content"."genre_film_work" ("film_work_id", "genre_id");

CREATE UNIQUE INDEX "film_work_title_creation_date_idx" ON "content"."film_work" ("title", "creation_date");
CREATE INDEX "film_work_updated_at-idx" ON "content"."film_work" ("updated_at");

CREATE OR REPLACE  FUNCTION update_updated_at_film_work() RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
    BEGIN
        SET TIMEZONE TO 'Europe/Moscow';
        NEW.updated_at = now();
        RETURN NEW;
    END;
$$;

CREATE TRIGGER update_user_task_updated_on
    BEFORE UPDATE
    ON
        content.film_work
    FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_film_work();
