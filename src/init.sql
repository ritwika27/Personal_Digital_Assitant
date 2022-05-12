-- Table: public.userData

DROP TABLE IF EXISTS public."userData";

CREATE TABLE IF NOT EXISTS public."userData"
(
    event_id numeric,
    preferences character varying COLLATE pg_catalog."default",
    user_location character varying COLLATE pg_catalog."default",
    user_lat numeric,
    user_long numeric,
    event_location character varying COLLATE pg_catalog."default",
    event_lat numeric,
    event_long numeric,
    event_start_time timestamp without time zone,
    event_end_time timestamp without time zone,
    event_title character varying COLLATE pg_catalog."default",
    event_description character varying COLLATE pg_catalog."default",
    event_passed numeric,
    travel_time_estimate numeric
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."userData"
    OWNER to postgres;

