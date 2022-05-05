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
    event_passed numeric
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."userData"
    OWNER to postgres;

INSERT INTO public."userData" (event_id, preferences, user_location, user_lat, user_long, event_location, event_lat, event_long, event_start_time, event_end_time, event_title, event_description, event_passed) VALUES
(1, 'car', 'Democracy blvd', 39.022797, -77.151316, 'College park', 38.991385, -76.937700, '2022-05-11 11:00:00', '2022-05-11 12:00:00', 'Daily Standup', 'work meeting', 0),
(2, 'bus', 'Democracy blvd', 39.022797, -77.151316, 'Paint branch Dr', 38.997691, -76.940289, '2022-05-11 13:00:00', '2022-05-11 13:30:00', 'Weekly Standup', 'work meeting', 0);
