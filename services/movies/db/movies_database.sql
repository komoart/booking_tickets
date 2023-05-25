CREATE SCHEMA IF NOT EXISTS content;
SET search_path TO content,public;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- # Блок создания таблицы фильмов
CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    certificate TEXT,
    file_path TEXT,
    mpaa_rating TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

comment on column content.film_work.id is 'UUID фильма';
comment on column content.film_work.title is 'Заголовок фильма';
comment on column content.film_work.description is 'Подробное описание фильма';
comment on column content.film_work.creation_date is 'Дата выпуска фильма';
comment on column content.film_work.rating is 'Текущий рейтинг фильма';
comment on column content.film_work.type is 'Классификация фильма';
comment on column content.film_work.certificate is 'Лицензия на прокат фильма';
comment on column content.film_work.file_path is 'Ссылка на файл';
comment on column content.film_work.created is 'Дата и время записи';
comment on column content.film_work.modified is 'Дата и время редактирования записи';

CREATE INDEX ON content.film_work (creation_date, rating);


-- Блок создания таблицы участников фильма
CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

comment on column content.person.id is 'UUID участника';
comment on column content.person.full_name is 'Полное имя участника';
comment on column content.person.created is 'Дата и время записи';
comment on column content.person.modified is 'Дата и время редактирования записи';


-- Блок создания связной таблицы участник-фильм. Делаем перелинковку таблиц.
CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    person_id uuid NOT NULL REFERENCES content.person (id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    role TEXT,
    created timestamp with time zone
);

comment on column content.person_film_work.id is 'UUID привязки участника к фильму';
comment on column content.person_film_work.person_id is 'UUID в таблице content.person';
comment on column content.person_film_work.film_work_id is 'UUID в таблице content.film_work';
comment on column content.person_film_work.role is 'Роль участника в связном фильме';
comment on column content.person_film_work.created is 'Дата и время записи';

CREATE UNIQUE INDEX film_work_person_role_idx ON content.person_film_work (film_work_id, person_id, role);
ALTER TABLE content.person_film_work ADD FOREIGN KEY (person_id) REFERENCES content.person (id);
ALTER TABLE content.person_film_work ADD FOREIGN KEY (film_work_id) REFERENCES content.film_work (id);


-- Блок создания таблицы жанров фильма
CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

comment on column content.genre.id is 'UUID жанра фильма';
comment on column content.genre.name is 'Название жанра фильма';
comment on column content.genre.description is 'Подробное описание жанра фильма';
comment on column content.genre.created is 'Дата и время записи';
comment on column content.genre.modified is 'Дата и время редактирования записи';


-- Блок создания связной таблицы жанр-фильм. Делаем перелинковку таблиц.
CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL REFERENCES content.genre (id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    created timestamp with time zone
);

CREATE UNIQUE INDEX film_work_genre_idx ON content.genre_film_work (film_work_id, genre_id);
ALTER TABLE content.genre_film_work ADD FOREIGN KEY (film_work_id) REFERENCES content.film_work (id);
ALTER TABLE content.genre_film_work ADD FOREIGN KEY (genre_id) REFERENCES content.genre (id);
