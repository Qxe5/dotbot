CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    minors INTEGER NOT NULL CHECK(minors BETWEEN 0 AND 3),
    majors INTEGER NOT NULL CHECK(majors BETWEEN 0 AND 3),
    tally INTEGER NOT NULL CHECK(tally BETWEEN 0 AND 3),
    mute INTEGER NOT NULL,
    timestamp INTEGER NOT NULL
);

CREATE TABLE reasons(
    id INTEGER PRIMARY KEY,
    userid INTEGER NOT NULL,
    punishment TEXT NOT NULL,
    reason TEXT NOT NULL,
    issuer INTEGER NOT NULL,
    FOREIGN KEY(userid) REFERENCES users(id)
);
