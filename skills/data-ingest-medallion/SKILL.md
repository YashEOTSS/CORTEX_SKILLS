---
name: data-ingest-medallion
description: "Automate end-to-end data ingestion into Snowflake following medallion architecture (Raw → Staging). Handles file staging, schema inference, table creation, data loading, and staging view generation. Use when: ingesting a file, loading data into Snowflake, staging a CSV, new dataset to process, medallion ingest, load CSV into raw table, ingest and transform data. Triggers: ingest this file, load data, new dataset, stage and process, medallion ingest, ingest CSV, load into snowflake, put file in snowflake, upload and process data."
---

# Data Ingest — Medallion Architecture

Automates the repetitive process of ingesting local files into Snowflake following a medallion architecture pattern: Stage → Raw → Staging.

## When to Use

- User wants to upload a local file (CSV, Parquet, JSON) to Snowflake
- User wants to create tables from staged files
- User mentions "ingest", "load data", "medallion", or "stage and process"
- User has a file and wants it queryable in Snowflake with proper structure

## Workflow

### Step 1: Gather Inputs

**Goal:** Collect the minimum information needed to proceed.

**Ask the user:**

1. **File path** — Local path to the file to ingest (e.g., `C:\Users\...\data.csv`)
2. **Database** — Which database to load into (e.g., `SYNTHEA_DB`)
3. **Dataset name** — A short name for this dataset (e.g., `claims_transactions`). Used for table/view naming.
4. **File format** — Default CSV. Ask only if unclear. Supported: CSV, PARQUET, JSON.
5. **Stage name** — If the user has a preferred stage. Otherwise default to `<DATABASE>.<SCHEMA>.RAW_DATA_STAGE`.

**Defaults:**
- Format: CSV with `SKIP_HEADER=1`, `FIELD_OPTIONALLY_ENCLOSED_BY='"'`
- Schemas: `RAW` for raw tables, `STAGING` for cleaned views
- Metadata columns: `_LOADED_AT`, `_SOURCE_FILE`

### Step 2: Ensure Schemas Exist

**Goal:** Create RAW and STAGING schemas if they don't already exist.

**Execute:**

```sql
CREATE SCHEMA IF NOT EXISTS <DATABASE>.RAW;
CREATE SCHEMA IF NOT EXISTS <DATABASE>.STAGING;
```

**If error:** Check that the user's role has CREATE SCHEMA privileges. Report the error and suggest switching roles.

### Step 3: Ensure Stage Exists

**Goal:** Create an internal stage if one doesn't already exist.

**Execute:**

```sql
CREATE STAGE IF NOT EXISTS <DATABASE>.RAW.<STAGE_NAME>
  DIRECTORY = (ENABLE = TRUE)
  COMMENT = 'Raw data ingestion stage';
```

### Step 4: Upload File to Stage

**Goal:** PUT the local file into the Snowflake stage.

**Execute:**

```sql
PUT 'file://<LOCAL_FILE_PATH>' @<DATABASE>.RAW.<STAGE_NAME>/<DATASET_NAME>/ AUTO_COMPRESS=TRUE;
```

**Important:** On Windows, convert backslashes to forward slashes in the file path. Wrap path in single quotes.

**Verify:** Run `LIST @<DATABASE>.RAW.<STAGE_NAME>/<DATASET_NAME>/` to confirm the file landed.

**If error "file not found":** Verify the path exists. Common issue: OneDrive paths with spaces need quoting.

### Step 5: Infer Schema

**Goal:** Detect column names and types from the staged file without manual specification.

**Execute:**

```sql
SELECT *
FROM TABLE(
  INFER_SCHEMA(
    LOCATION => '@<DATABASE>.RAW.<STAGE_NAME>/<DATASET_NAME>/',
    FILE_FORMAT => '<FORMAT_NAME_OR_INLINE>'
  )
);
```

For CSV without a pre-existing file format object, use inline:

```sql
SELECT *
FROM TABLE(
  INFER_SCHEMA(
    LOCATION => '@<DATABASE>.RAW.<STAGE_NAME>/<DATASET_NAME>/',
    FILE_FORMAT => 'TYPE=CSV, PARSE_HEADER=TRUE'
  )
);
```

**Output:** List of column names, types, and nullable flags. Present these to the user for review.

**If INFER_SCHEMA fails:** Fall back to reading a sample with `SELECT $1, $2, ... FROM @<stage> LIMIT 5` and ask the user to provide column names.

### Step 6: Create Raw Table

**Goal:** Create the raw-layer table using inferred schema plus metadata columns.

**Execute:**

```sql
CREATE OR REPLACE TABLE <DATABASE>.RAW.<DATASET_NAME> (
  <inferred columns from Step 5>,
  _LOADED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
  _SOURCE_FILE VARCHAR DEFAULT METADATA$FILENAME
);
```

**Naming convention:** Table name = uppercase dataset name. Schema = RAW.

### Step 7: Load Data (COPY INTO)

**Goal:** Load the staged file into the raw table.

**Execute:**

```sql
COPY INTO <DATABASE>.RAW.<DATASET_NAME>
FROM @<DATABASE>.RAW.<STAGE_NAME>/<DATASET_NAME>/
FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '"' ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE)
ON_ERROR = 'CONTINUE'
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
```

For Parquet:
```sql
COPY INTO <DATABASE>.RAW.<DATASET_NAME>
FROM @<DATABASE>.RAW.<STAGE_NAME>/<DATASET_NAME>/
FILE_FORMAT = (TYPE = 'PARQUET')
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
```

**After loading:** Report row count:
```sql
SELECT COUNT(*) AS rows_loaded FROM <DATABASE>.RAW.<DATASET_NAME>;
```

**If errors:** Check `VALIDATE(<table>, JOB_ID => '_last')` for rejected rows.

### Step 8: Create Staging View

**Goal:** Create a cleaned view in the STAGING schema with standardized column names and types.

**Transformations applied:**
- Column names → UPPER_SNAKE_CASE
- Trim whitespace from VARCHAR columns
- Cast date/timestamp strings to proper types where detected
- Remove exact duplicate rows (if applicable)

**Execute:**

```sql
CREATE OR REPLACE VIEW <DATABASE>.STAGING.STG_<DATASET_NAME> AS
SELECT
  <cleaned and cast columns>,
  _LOADED_AT,
  _SOURCE_FILE
FROM <DATABASE>.RAW.<DATASET_NAME>;
```

### Step 9: Validate and Report

**Goal:** Confirm the pipeline succeeded end-to-end.

**Execute:**
```sql
SELECT COUNT(*) AS raw_count FROM <DATABASE>.RAW.<DATASET_NAME>;
SELECT COUNT(*) AS stg_count FROM <DATABASE>.STAGING.STG_<DATASET_NAME>;
SELECT * FROM <DATABASE>.STAGING.STG_<DATASET_NAME> LIMIT 5;
```

**Present to user:**
- Row counts (raw vs staging — should match unless dedup applied)
- Sample of 5 rows from the staging view
- Summary of what was created

## Stopping Points

- After Step 1: Confirm inputs before proceeding
- After Step 5: Show inferred schema for user review before creating tables
- After Step 9: Present final summary

## Output

Upon completion, the user has:
1. File staged at `@<DB>.RAW.<STAGE>/<DATASET>/`
2. Raw table at `<DB>.RAW.<DATASET_NAME>` with all source data + metadata
3. Staging view at `<DB>.STAGING.STG_<DATASET_NAME>` with cleaned data
4. Validation confirming row counts match

## Troubleshooting

**Error: "Database does not exist or not authorized"**
- Verify the database name. Run `SHOW DATABASES` to list available ones.
- Check current role has access: `SELECT CURRENT_ROLE()`

**Error: PUT command fails with "file not found"**
- Verify the local file path exists
- On Windows, use forward slashes: `C:/Users/...`
- Paths with spaces need single quotes around the full `file://` URI

**Error: INFER_SCHEMA returns no results**
- File may be empty or malformed
- Try `SELECT $1 FROM @<stage>/<file> LIMIT 1` to check if data is readable
- For headerless CSVs, you'll need to provide column names manually

**Error: COPY INTO loads 0 rows**
- Check file format matches actual file structure
- Verify `SKIP_HEADER` is correct (use 0 if no header)
- Run `VALIDATE` to see rejection reasons

## Notes

- This skill creates Raw + Staging layers only. The Analytics layer requires business logic and should be built manually or via a separate skill.
- The skill uses `ON_ERROR = 'CONTINUE'` to avoid blocking on bad rows. Always check for rejected records after loading.
- For repeated ingestion of the same file structure, consider creating a named FILE FORMAT object for reuse.
