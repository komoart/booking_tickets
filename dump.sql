--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: eventstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.eventstatus AS ENUM (
    'Created',
    'Alive',
    'Closed',
    'Done'
);


ALTER TYPE public.eventstatus OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: announcements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.announcements (
    id uuid NOT NULL,
    status public.eventstatus,
    title character varying(256),
    description character varying(4096),
    movie_id uuid,
    author_id uuid,
    sub_only boolean DEFAULT true,
    is_free boolean DEFAULT true,
    tickets_count integer,
    event_time timestamp with time zone NOT NULL,
    event_location character varying(4096),
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone,
    duration integer
);


ALTER TABLE public.announcements OWNER TO postgres;

--
-- Name: booking; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.booking (
    id uuid NOT NULL,
    announcement_id uuid NOT NULL,
    movie_id uuid,
    author_id uuid,
    guest_id uuid,
    author_status boolean,
    guest_status boolean DEFAULT true,
    event_time timestamp with time zone NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone
);


ALTER TABLE public.booking OWNER TO postgres;

--
-- Data for Name: announcements; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.announcements (id, status, title, description, movie_id, author_id, sub_only, is_free, tickets_count, event_time, event_location, created, modified, duration) FROM stdin;
2a580a71-4ba6-4626-b88e-381d3cf6e1da	Created	Fake Title	Fake description	23536729-1e1f-4639-a9cf-0883634143aa	f55291b9-c09d-405b-b025-36f26c887905	f	t	2	2023-05-26 11:19:13.732697+00	Fake location	2023-05-26 11:19:13.822707+00	2023-05-26 11:19:13.822714+00	0
52b1c581-5ab9-48c1-9df6-52f29bc71872	Created	Fake Title	Fake description	23536729-1e1f-4639-a9cf-0883634143aa	f55291b9-c09d-405b-b025-36f26c887905	f	t	2	2023-05-26 11:20:39.945723+00	Fake location	2023-05-26 11:20:39.983887+00	2023-05-26 11:20:39.983895+00	0
3b694076-c2a2-4aac-b7e1-b496a3f9724b	Created	Fake Title	Fake description	23536729-1e1f-4639-a9cf-0883634143ab	f55291b9-c09d-405b-b025-36f26c887905	f	t	2	2023-05-26 12:45:22.842896+00	Fake location	2023-05-26 12:45:22.889921+00	2023-05-26 12:45:22.889933+00	0
\.


--
-- Data for Name: booking; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.booking (id, announcement_id, movie_id, author_id, guest_id, author_status, guest_status, event_time, created, modified) FROM stdin;
862cc5f8-d445-48b0-bcec-2219a97093c8	52b1c581-5ab9-48c1-9df6-52f29bc71872	23536729-1e1f-4639-a9cf-0883634143aa	f55291b9-c09d-405b-b025-36f26c887905	39e60237-83ea-4c65-9bc9-f6b47d109738	\N	t	2023-05-26 11:20:39.945723+00	2023-05-26 12:53:20.996222+00	2023-05-26 12:53:20.996237+00
\.


--
-- Name: announcements _author_event_time; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.announcements
    ADD CONSTRAINT _author_event_time UNIQUE (author_id, event_time);


--
-- Name: booking _bk_guest_event_time; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.booking
    ADD CONSTRAINT _bk_guest_event_time UNIQUE (guest_id, event_time);


--
-- Name: announcements announcements_event_time_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.announcements
    ADD CONSTRAINT announcements_event_time_key UNIQUE (event_time);


--
-- Name: announcements announcements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.announcements
    ADD CONSTRAINT announcements_pkey PRIMARY KEY (id);


--
-- Name: booking booking_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.booking
    ADD CONSTRAINT booking_pkey PRIMARY KEY (id);


--
-- Name: ix_announcements_author_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_announcements_author_id ON public.announcements USING btree (author_id);


--
-- Name: ix_announcements_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_announcements_id ON public.announcements USING btree (id);


--
-- Name: ix_announcements_movie_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_announcements_movie_id ON public.announcements USING btree (movie_id);


--
-- Name: ix_booking_author_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_booking_author_id ON public.booking USING btree (author_id);


--
-- Name: ix_booking_guest_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_booking_guest_id ON public.booking USING btree (guest_id);


--
-- Name: ix_booking_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_booking_id ON public.booking USING btree (id);


--
-- Name: ix_booking_movie_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_booking_movie_id ON public.booking USING btree (movie_id);


--
-- Name: booking booking_announcement_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.booking
    ADD CONSTRAINT booking_announcement_id_fkey FOREIGN KEY (announcement_id) REFERENCES public.announcements(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

