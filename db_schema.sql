CREATE TABLE weather_data (
  id         INTEGER PRIMARY KEY NOT NULL,
  created_at TEXT                NOT NULL,
  "temp"     FLOAT,
  pressure   INTEGER,
  temp_min   FLOAT,
  temp_max   FLOAT,
  humidity   INTEGER,
  wind_speed FLOAT,
  wind_gust  FLOAT,
  wind_deg   INTEGER,
  clouds     INTEGER,
  rain       INTEGER,
  snow       INTEGER,
  weather_id INTEGER
);
CREATE TABLE IF NOT EXISTS "pvdata" (
  id            INTEGER PRIMARY KEY NOT NULL,
  created_at    DATETIME            NOT NULL,
  dc_1_u        INTEGER,
  dc_1_i        REAL,
  ac_1_u        INTEGER,
  ac_1_p        INTEGER,
  dc_2_u        INTEGER,
  dc_2_i        REAL,
  ac_2_u        INTEGER,
  ac_2_p        INTEGER,
  dc_3_u        INTEGER,
  dc_3_i        REAL,
  ac_3_u        INTEGER,
  ac_3_p        INTEGER,
  current_power INTEGER,
  daily_energy  REAL,
  total_energy  INTEGER
);
CREATE TABLE IF NOT EXISTS "electricity_data" (
  id           INTEGER PRIMARY KEY NOT NULL,
  created_at   DATETIME            NOT NULL,
  meter_180    REAL,
  meter_280    REAL,
  active_power REAL
);
