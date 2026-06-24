--Customer Churn Analysis — Table Schema

CREATE TABLE IF NOT EXISTS customers (
    customerid      TEXT PRIMARY KEY,
    gender          TEXT,
    seniorcitizen   INTEGER,
    partner         TEXT,
    dependents      TEXT,
    tenure          INTEGER,
    phoneservice    TEXT,
    multiplelines   TEXT,
    internetservice TEXT,
    onlinesecurity  TEXT,
    onlinebackup    TEXT,
    deviceprotection TEXT,
    techsupport     TEXT,
    streamingtv     TEXT,
    streamingmovies TEXT,
    contract        TEXT,
    paperlessbilling TEXT,
    paymentmethod   TEXT,
    monthlycharges  REAL,
    totalcharges    REAL,
    churn           TEXT
);