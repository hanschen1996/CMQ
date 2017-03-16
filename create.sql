CREATE TABLE dbo.Queue
    (q_id int PRIMARY KEY NOT NULL,
    name text NOT NULL,
    queuedescr text NOT NULL,
    course VARCHAR(5) NULL,
    location text NOT NULL);

CREATE TABLE dbo.QueueUSER
    (u_id int PRIMARY KEY NOT NULL,
    q_id int NULL,
    name text NOT NULL,
    andrewid text NOT NULL,
)

