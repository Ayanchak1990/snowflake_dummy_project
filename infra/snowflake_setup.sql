USE ROLE ACCOUNTADMIN;

-- CREATE DATABASE FOR CONVEX-INSURANCE PROJECT

CREATE DATABASE CONVEX_INSURANCE COMMENT = 'This database is for convex test account';

--CREATE WAREHOUSE TO BE USED FOR LATER BY DATA SCIENTISTS TO FETCH THE RESULT:

CREATE WAREHOUSE CONVEX_INSURANCE WITH WAREHOUSE_SIZE = 'XSMALL' 
WAREHOUSE_TYPE = 'STANDARD' AUTO_SUSPEND = 300 AUTO_RESUME = TRUE 
COMMENT = 'This warehouse is for convex-insurance test';

-- USE DATABASE FOR NEXT TASKS TO CONTONUE

USE DATABASE CONVEX_INSURANCE;

-- CREATE SCHEMA FOR STAGING AREA OBJECTS

CREATE SCHEMA IF NOT EXISTS CONVEX_STAGE;

-- CREATE DATA VAULT 2.0 FOR FUTURERISTIC AGILE DESIGN OF THE DATA MODEL

CREATE SCHEMA IF NOT EXISTS CONVEX_VAULT;

-- CREATE SCHEMA FOR INFORMATION VAULT (KIMBALL MODELLING - START SCHEMA)

CREATE SCHEMA IF NOT EXISTS CONVEX_WAREHOUSE;

-- CREATE SCHEMA FOR DATA MART (TO BE USED BY DATA SCIENTISTS )

CREATE SCHEMA IF NOT EXISTS CONVEX_DATAMART;


-- USE PRIMARY SCHEMA FOR LOADING THE DATA FROM S3 TO SNOWFLAKE

USE SCHEMA CONVEX_INSURANCE.CONVEX_VAULT;
