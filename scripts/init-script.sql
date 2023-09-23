-- Create database and user
CREATE DATABASE blogindex;
CREATE ROLE blogindex WITH PASSWORD 'blogindex';
ALTER ROLE blogindex WITH LOGIN;

-- Create schema
\connect blogindex;
CREATE SCHEMA blogindex;
GRANT ALL PRIVILEGES ON SCHEMA blogindex TO blogindex;
GRANT ALL PRIVILEGES ON SCHEMA blogindex TO postgres;

-- Add search paths
ALTER USER blogindex
SET
  search_path = "$user",
  public,
  blogindex;

ALTER USER postgres
SET
  search_path = "$user",
  public,
  blogindex;
