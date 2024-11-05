CREATE TABLE "users" (
    "number"                        INTEGER,
    "name"                          TEXT DEFAULT NULL,
    "uploaded_audios"               INTEGER DEFAULT 0,
    "gpt_requests"                  INTEGER DEFAULT 0,
    "last_summary_text"             TEXT DEFAULT NULL,
    "last_transcription_text"       TEXT DEFAULT NULL,
    "state"                         TEXT DEFAULT NULL,
    "is_admin"                      BOOLEAN DEFAULT FALSE,
    "subscription_status"           TEXT DEFAULT "free",
    "created_at"                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at"                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("number")
);

