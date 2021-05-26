USE aebc;


CREATE TABLE client
(
    id             BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(50)        NOT NULL,
    rfc            VARCHAR(13) UNIQUE NOT NULL,
    password       VARCHAR(20)        NOT NULL,
    monthly_income BIGINT             NOT NULL,
    has_credit     BOOLEAN            NOT NULL,
    address        VARCHAR(50)        NOT NULL,
    city           VARCHAR(50)        NOT NULL,
    state          VARCHAR(50)        NOT NULL,
    neighborhood   VARCHAR(50)        NOT NULL,
    is_active      BOOLEAN            NOT NULL DEFAULT true,
    curp           VARCHAR(50) UNIQUE NOT NULL
);


CREATE TRIGGER `valid_client_income`
    BEFORE INSERT
    ON `client`
    FOR EACH ROW
BEGIN
    IF new.monthly_income < 1 OR new.monthly_income IS NULL THEN
        SET new.monthly_income = 1;
    END IF;
END;


CREATE TABLE credit_card
(
    id         BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    min_credit INT         NOT NULL,
    max_credit INT         NOT NULL,
    tier       INT         NOT NULL DEFAULT 0,
    image      VARCHAR(50) NOT NULL,
    name       VARCHAR(50) NOT NULL
);


CREATE TRIGGER `valid_credit_bounds`
    BEFORE INSERT
    ON `credit_card`
    FOR EACH ROW IF new.min_credit <= 1000 OR new.max_credit IS NULL THEN
    SET new.min_credit = 1001;
ELSEIF new.min_credit >= 1000000 THEN
    SET new.min_credit = 999998;
ELSEIF new.max_credit >= 1000000 THEN
    SET new.max_credit = 999999;
ELSEIF new.max_credit <= 1000 OR new.max_credit IS NULL THEN
    SET new.max_credit = 1002;
END IF;


CREATE TABLE preapproval_request
(
    invoice        BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    creation_date  TIMESTAMP                DEFAULT NOW(),
    was_accepted   BOOLEAN                  DEFAULT NULL,
    is_active      BOOLEAN         NOT NULL DEFAULT TRUE,
    id_credit_card BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (id_credit_card) REFERENCES credit_card (id)
);


CREATE TABLE benefit
(
    id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(300) NOT NULL,
    valid_until DATETIME NOT NULL
);


CREATE TABLE admin_token
(
    id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    token         VARCHAR(30) NOT NULL,
    creation_date TIMESTAMP DEFAULT NOW(),
    is_active     BOOLEAN   DEFAULT true
);


CREATE TABLE credit_card_benefit
(
    id             BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_credit_card BIGINT UNSIGNED,
    id_benefit     BIGINT UNSIGNED,
    FOREIGN KEY (id_credit_card) REFERENCES credit_card (id),
    FOREIGN KEY (id_benefit) REFERENCES benefit (id)
);


CREATE TABLE client_request
(
    id                     BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_client              BIGINT UNSIGNED,
    id_preapproval_request BIGINT UNSIGNED,
    FOREIGN KEY (id_client) REFERENCES client (id),
    FOREIGN KEY (id_preapproval_request) REFERENCES preapproval_request (invoice)
);
