-- DB Initialization

-- ============================================================

\c postgres
DROP DATABASE IF EXISTS queues;

CREATE database queues;
\c queues

\i create.SQL

-- ============================================================

\copy Queue(q_id, name, queuedescr, course, location) FROM 'queue.csv' csv header
\copy QueueUser(u_id, q_id, name, andrewid) FROM 'queueuser.csv' csv header

-- ============================================================