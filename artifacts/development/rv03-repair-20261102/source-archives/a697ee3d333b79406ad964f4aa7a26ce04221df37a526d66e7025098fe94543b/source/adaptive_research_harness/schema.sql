PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL);
INSERT OR IGNORE INTO metadata VALUES('schema_version','1');
CREATE TABLE IF NOT EXISTS evidence(
 seq INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT NOT NULL, actor TEXT NOT NULL,
 time_ms INTEGER, body BLOB NOT NULL, sha256 TEXT NOT NULL, command BLOB);
CREATE TABLE IF NOT EXISTS transitions(
 seq INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT NOT NULL, actor TEXT NOT NULL,
 transition_id TEXT NOT NULL, time_ms INTEGER, body BLOB NOT NULL, sha256 TEXT NOT NULL, command BLOB);
CREATE TABLE IF NOT EXISTS applied(
 n INTEGER PRIMARY KEY, transition_seq INTEGER UNIQUE NOT NULL REFERENCES transitions(seq),
 transition_id TEXT UNIQUE NOT NULL, bind_seq INTEGER UNIQUE REFERENCES evidence(seq));
CREATE TABLE IF NOT EXISTS dispositions(
 bind_seq INTEGER PRIMARY KEY REFERENCES evidence(seq),
 transition_seq INTEGER UNIQUE NOT NULL REFERENCES transitions(seq), kind TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS artifacts(sha256 TEXT PRIMARY KEY, bytes BLOB NOT NULL);
CREATE TABLE IF NOT EXISTS requests(
 actor TEXT NOT NULL, request_id TEXT NOT NULL, request_hash TEXT NOT NULL,
 response BLOB NOT NULL, PRIMARY KEY(actor, request_id));
CREATE TABLE IF NOT EXISTS dispatch_claims(
 attempt_seq INTEGER PRIMARY KEY REFERENCES evidence(seq),
 body BLOB NOT NULL, receipt BLOB);
CREATE TABLE IF NOT EXISTS operational_receipts(
 receipt_id TEXT PRIMARY KEY, kind TEXT NOT NULL, body BLOB NOT NULL);
CREATE TABLE IF NOT EXISTS faults(
 target TEXT PRIMARY KEY, body BLOB NOT NULL, consumed INTEGER NOT NULL DEFAULT 0);
CREATE TRIGGER IF NOT EXISTS evidence_no_update BEFORE UPDATE ON evidence
 BEGIN SELECT RAISE(ABORT,'immutable evidence'); END;
CREATE TRIGGER IF NOT EXISTS evidence_no_delete BEFORE DELETE ON evidence
 BEGIN SELECT RAISE(ABORT,'immutable evidence'); END;
CREATE TRIGGER IF NOT EXISTS transition_no_update BEFORE UPDATE ON transitions
 BEGIN SELECT RAISE(ABORT,'immutable transition'); END;
CREATE TRIGGER IF NOT EXISTS transition_no_delete BEFORE DELETE ON transitions
 BEGIN SELECT RAISE(ABORT,'immutable transition'); END;
CREATE TRIGGER IF NOT EXISTS apply_no_update BEFORE UPDATE ON applied
 BEGIN SELECT RAISE(ABORT,'immutable apply'); END;
CREATE TRIGGER IF NOT EXISTS apply_no_delete BEFORE DELETE ON applied
 BEGIN SELECT RAISE(ABORT,'immutable apply'); END;
CREATE TRIGGER IF NOT EXISTS disposition_no_update BEFORE UPDATE ON dispositions
 BEGIN SELECT RAISE(ABORT,'immutable disposition'); END;
CREATE TRIGGER IF NOT EXISTS disposition_no_delete BEFORE DELETE ON dispositions
 BEGIN SELECT RAISE(ABORT,'immutable disposition'); END;
CREATE TRIGGER IF NOT EXISTS artifact_no_update BEFORE UPDATE ON artifacts
 BEGIN SELECT RAISE(ABORT,'immutable artifact'); END;
CREATE TRIGGER IF NOT EXISTS artifact_no_delete BEFORE DELETE ON artifacts
 BEGIN SELECT RAISE(ABORT,'immutable artifact'); END;
