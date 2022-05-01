--
-- PostgreSQL database dump
--

-- Dumped from database version 14.0
-- Dumped by pg_dump version 14.0

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: userData; Type: TABLE; Schema: public; Owner: farnazzamiri
--

CREATE TABLE public."userData" (
    event_id numeric,
    preferences character varying,
    user_location character varying,
    user_lat numeric,
    user_long numeric,
    event_location character varying,
    event_lat numeric,
    event_long numeric,
    event_start_time time without time zone,
    event_end_time time without time zone,
    event_date date,
    event_description character varying
);


ALTER TABLE public."userData" OWNER TO postgres;

--
-- Data for Name: userData; Type: TABLE DATA; Schema: public; Owner: farnazzamiri
--

COPY public."userData" (user_id, preferences, user_location, user_lat, user_long, event_location, event_lat, event_long, event_start_time, event_end_time, event_date, event_description) FROM stdin;
1	car	Democracy blvd	39.022797	-77.151316	College park	38.991385	-76.937700	11:00:00	12:00:00	2022-06-11	work meeting
2	bus	Democracy blvd	39.022797	-77.151316	Paint branch Dr	38.997691	-76.940289	13:00:00	13:30:00	2022-06-11	work meeting
\.


--
-- PostgreSQL database dump complete
--

