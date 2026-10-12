CREATE TABLE shipping_quotes (
    id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title         VARCHAR(80)  NOT NULL CHECK (length(trim(title)) BETWEEN 1 AND 80),
    weight_g      INTEGER      NOT NULL CHECK (weight_g BETWEEN 1 AND 20000),
    fee           INTEGER      NOT NULL CHECK (fee >= 3000),
    calc_version  VARCHAR(20)  NOT NULL,
    request_key   VARCHAR(36)  NOT NULL UNIQUE,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT now()
);