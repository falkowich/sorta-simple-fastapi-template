-- upgrade --
ALTER TABLE "user" ALTER COLUMN "username" TYPE VARCHAR(255) USING "username"::VARCHAR(255);
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "username" TYPE VARCHAR(256) USING "username"::VARCHAR(256);
