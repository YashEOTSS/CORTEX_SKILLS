---
id: visualization-readiness
name: visualization-readiness
title: Visualization Readiness
summary: Assess whether a CSV, GeoJSON, or Snowflake table is ready for visualization and auto-generate an interactive map or chart.
description: |
  Assess whether a CSV file, GeoJSON file, or Snowflake table is ready for
  visualization (maps, charts, dashboards). Use for ALL requests involving:
  map readiness, geospatial validation, chart recommendation, visualization
  assessment, data profiling for Tableau or BI tools, check if data can be
  plotted, lat/long validation, GeoJSON validation, GeoJSON readiness, polygon
  rendering, choropleth readiness, sankey readiness, heat map readiness,
  time-series readiness. Invoke this skill before the user spends time building
  a dashboard.
authors: Steffi Prithus-Anthraj
status: draft
categories:
  - analytics
  - geospatial
  - visualization
tools:
  - Read
  - Write
  - Bash
  - snowflake_sql_execute
  - open_browser
prompt: Assess town_dim table for visualization readiness
language: en
---

# Visualization Readiness

## Overview

Assess whether a dataset can support a visualization before the user builds it in Tableau or another BI tool. Supports CSV files, GeoJSON files (FeatureCollection, single Feature, or bare geometry), and Snowflake tables. Prioritize map readiness first, then fall back to the best-fit chart type when geospatial rendering is weak or unavailable.

## Setup

1. **Load** `references/visualization_rules.md` for scoring heuristics

## Workflow

### Step 1: Identify Data Source

**Goal:** Determine whether the user has a CSV, GeoJSON, or Snowflake table. Infer this from the user's message — do NOT ask unless the message is completely ambiguous.

**Actions:**

1. **Detect** the data source from the user's message:
   - File path ending in `.csv` -> CSV
   - File path ending in `.geojson` or `.json` -> GeoJSON
   - Table name (with or without database/schema qualifiers) -> Snowflake table
   - If only a table name without schema: search for it using `SHOW TABLES LIKE` or check known schemas

2. **Route:**
   - CSV path -> proceed to Step 2A
   - GeoJSON path -> proceed to Step 2A (same script handles both)
   - Snowflake table -> proceed to Step 2B

**Only stop here if:** The user's message contains no identifiable data source whatsoever (no file path, no table name, no dataset reference).

### Step 2A: Profile CSV or GeoJSON

**Goal:** Run the profiling script to detect field types and map readiness.

**Actions:**

1. **Execute** the profiler:
   ```bash
   uv run --project <SKILL_DIR> python <SKILL_DIR>/scripts/profile_csv.py <FILE_PATH>
   ```
   The script auto-detects format by file extension (.csv, .geojson, .json).

2. **Parse** the JSON output:
   - For CSV: field detection, map assessment, and chart recommendation
   - For GeoJSON: geometry type distribution, coordinate validation, property detection, and map recommendation (symbol map, filled map/choropleth, or path/route map)

**Output:** JSON profile with map assessment and chart recommendation.

**Next:** Proceed to Step 3.

### Step 2B: Profile Snowflake Table

**Goal:** Profile a Snowflake table in ONE round-trip (two parallel SQL calls maximum).

**Actions — execute these TWO queries IN PARALLEL (same tool call batch):**

1. **DESCRIBE TABLE** — get column names and types:
   ```sql
   DESCRIBE TABLE <TABLE_NAME>
   ```

2. **Combined profiling query** — get ALL stats in one shot:
   ```sql
   SELECT
     COUNT(*) AS total_rows,
     COUNT(<col1>) AS non_null_col1,
     COUNT(DISTINCT <col1>) AS distinct_col1,
     -- repeat for each column from DESCRIBE...
     -- If GEOGRAPHY/GEOMETRY column exists, add:
     MIN(ST_DIMENSION(GEOGRAPHY)) AS geo_dim,
     MAX(ST_NPOINTS(GEOGRAPHY)) AS max_npoints
   FROM <TABLE_NAME>
   ```

   For tables with many columns, include only the first 8-10 most relevant columns (prioritize: geography, date/time, categorical, numeric).

**CRITICAL: These two queries MUST be issued in the SAME parallel tool call.** Do NOT run them sequentially.

**Output:** Column types + completeness + geometry type — everything needed to score and generate.

**Next:** Proceed DIRECTLY to Step 3 (scoring) and then Step 5 (generation). Do NOT run additional exploratory queries.

### Step 3: Evaluate Readiness

**Goal:** Score the dataset and choose the best visualization type.

**Decision order:**

1. **Check map readiness** (highest priority):
   - GeoJSON with valid geometries -> symbol map (Points), filled map (Polygons), or path map (LineStrings)
   - Valid lat/lon present for most rows -> symbol map or density map
   - Country/state/city/zip fields clean and standardized -> filled map
   - Geographic fields exist but are weak or ambiguous -> flag issues

2. **If map score < 40, evaluate alternatives:**
   - Time-series: date + numeric measure
   - Bar chart: categorical + numeric measure
   - Sankey: source + target + value
   - Heat map: two axes + intensity measure

3. **Score using the weighted formula** from `references/visualization_rules.md`:
   - Field availability: 30%
   - Field quality and validity: 30%
   - Coverage and completeness: 20%
   - Visualization specificity: 20%

### Step 4: Present Report

**Goal:** Deliver a structured readiness assessment.

**Output format:**

```
# Visualization Readiness Report

## Verdict
- Best visualization: [recommendation]
- Readiness score: [0-100]
- Confidence: [low/medium/high]

## Why This Fits
- [evidence 1]
- [evidence 2]

## Issues Found
- [problem 1]
- [problem 2]

## Other Viable Options
- [secondary option with score]

## Next Steps
- [what to clean or verify before building the dashboard]
```

**Do not stop here.** Proceed immediately to Step 5 to generate the visualization.

### Step 5: Generate Visualization

**Goal:** Automatically create the recommended visualization. Execute the entire pipeline without asking the user any questions — make all decisions autonomously using best-practice defaults.

**CRITICAL RULES — No User Prompts, No External Scripts:**
- NEVER ask the user for permission, confirmation, or preferences during visualization generation
- NEVER warn about file sizes, complexity, or performance — just handle it silently
- NEVER present options like "shall I simplify?" or "which approach?" — pick the best one and execute
- If something fails (e.g., self-intersection error), silently try the next best approach
- The user experience must be: provide a table name → get a visualization. Nothing in between.
- **NEVER use Bash or Python scripts** to generate maps. The system will prompt users for permission to run scripts, which ruins the seamless experience. Instead:
  - Read the cached JSONL query result directly using the Read tool
  - Parse the GeoJSON from the result inline (line 1 of the JSONL file is the JSON array; element[0] is the GeoJSON string)
  - Build the complete HTML string in-memory and write it directly using the Write tool
  - This avoids ALL permission prompts since Read and Write are silent operations

**Routing by recommendation:**

#### If recommendation is a MAP (symbol map, filled map, choropleth, path map):

1. **Query** the geographic data with automatic optimization:
   - If GEOGRAPHY column exists:
     - ALWAYS use `ST_SIMPLIFY(GEOGRAPHY, <tolerance>)` directly on the GEOGRAPHY type (meters). Never use `TO_GEOMETRY()` — it causes self-intersection validation errors.
     - Choose tolerance automatically based on row count:
       - < 50 features: 50 meters
       - 50–500 features: 200 meters
       - 500–2000 features: 500 meters
       - > 2000 features: 1000 meters
     - Use `ST_ASGEOJSON(ST_SIMPLIFY(GEOGRAPHY, <tolerance>))` to export
   - If lat/lon columns exist: query coordinates plus label/measure fields (LIMIT 2000 if table is large)
   - If GeoJSON file: use the file directly (if >5MB, sample features)

2. **Build the GeoJSON FeatureCollection query:**
   ```sql
   SELECT OBJECT_CONSTRUCT(
     'type', 'FeatureCollection',
     'features', ARRAY_AGG(
       OBJECT_CONSTRUCT(
         'type', 'Feature',
         'properties', OBJECT_CONSTRUCT('<label_col>', <label_col>, ...),
         'geometry', PARSE_JSON(CAST(ST_ASGEOJSON(ST_SIMPLIFY(GEOGRAPHY, <tolerance>)) AS VARCHAR))
       )
     )
   )::VARCHAR AS geojson_fc
   FROM <table>
   ```

3. **If the query fails** (self-intersection, unsupported type, etc.):
   - First fallback: increase tolerance (double it)
   - Second fallback: use `ST_ASGEOJSON(GEOGRAPHY)` without simplification, then sample rows with LIMIT
   - Third fallback: extract centroids with `ST_CENTROID` for a point map instead
   - Never ask the user — just try the next approach silently

4. **Generate an interactive HTML map in ONE step** (NO Python script, NO intermediate files):
   - Use a SINGLE PowerShell command that:
     a. Reads the cached JSONL result file
     b. Extracts the GeoJSON string (line index 1, parsed from JSON array)
     c. Reads the appropriate HTML template from `references/choropleth_template.html` or `references/symbol_map_template.html`
     d. Replaces `{{GEOJSON_DATA}}`, `{{TITLE}}`, and `{{FEATURE_COUNT}}` placeholders
     e. Writes the final .html file
   - Then open the map in the browser using open_browser
   - This is exactly 2 tool calls: one PowerShell + one open_browser

5. **If result GeoJSON exceeds 10MB after simplification:**
   - Silently increase simplification tolerance and re-query
   - If still too large, LIMIT to 1000 features with a note in the report

#### If recommendation is a TIME-SERIES chart:

1. **Query** aggregated time-series data. Auto-select period:
   - Date range < 90 days: group by DAY
   - Date range 90 days–2 years: group by WEEK
   - Date range 2–10 years: group by MONTH
   - Date range > 10 years: group by YEAR
   ```sql
   SELECT DATE_TRUNC('<period>', <date_column>) AS period, COUNT(*) AS count
   FROM <table> GROUP BY period ORDER BY period
   ```

2. **Render** using `visualize_data` with `type: "line_chart"`. Limit to 500 data points max (aggregate further if needed).

#### If recommendation is a BAR CHART:

1. **Query** the top N categories (N = min(15, distinct_count)):
   ```sql
   SELECT <category>, SUM(<measure>) AS total
   FROM <table> GROUP BY <category> ORDER BY total DESC LIMIT 15
   ```

2. **Render** using `visualize_data` with `type: "bar_chart"`. Use `seriesKey` for grouped bars when a natural grouping field exists.

#### If recommendation is a STACKED BAR CHART:

1. **Query** with both category and series dimensions (limit categories to 10, series to 6).
2. **Render** using `visualize_data` with `type: "stacked_bar_chart"` and `seriesKey`.

#### If recommendation is a SCATTER PLOT:

1. **Query** the two numeric axes plus optional color grouping (LIMIT 500 rows if table is large).
2. **Render** using `visualize_data` with `type: "scatter_chart"`.

#### If recommendation is a PIE CHART:

1. **Query** proportional breakdown (max 8 categories; group remaining into "Other").
2. **Render** using `visualize_data` with `type: "pie_chart"`.

**After rendering:** Present the report (from Step 4) below the visualization. Mention the user can request a different chart type or deeper analysis.

## Tools

### Script: profile_csv.py

**Description**: Profiles a CSV or GeoJSON file for visualization readiness. Detects geospatial, temporal, and categorical fields; scores map readiness; recommends the best chart type.

**Usage:**
```bash
uv run --project <SKILL_DIR> python <SKILL_DIR>/scripts/profile_csv.py <FILE_PATH> [--rows N]
```

**Arguments:**
- `file_path` (positional, required): Path to CSV (.csv) or GeoJSON (.geojson, .json) file
- `--rows`: Maximum rows/features to sample (default: 500)

**Output (CSV):** JSON with `format`, `rows_sampled`, `columns`, `field_detection`, `map_assessment`, and `best_non_map_chart`.

**Output (GeoJSON):** JSON with `format`, `feature_count`, `features_sampled`, `property_detection`, `map_assessment` (including `geometry_types` and `recommendation`), and `best_non_map_chart`.

**When to use:** For any CSV or GeoJSON file the user wants to assess.
**When NOT to use:** For Snowflake tables (profile inline using SQL queries instead — never shell out to Python for Snowflake table workflows).

## Stopping Points

- After Step 1 ONLY if the data source cannot be inferred from the user's message at all
- After Step 5 visualization delivery — the user may request a different chart type or deeper analysis

**Important:** If the user's message contains a table name, file path, or any identifiable data source, skip Step 1 entirely and proceed directly to profiling. Never ask "which table?" when the user already named it.

## Performance Rules — Minimize Round-Trips

The ENTIRE workflow for a Snowflake table MUST complete in **4 tool calls maximum**:

| Call | Action | Tools |
|------|--------|-------|
| 1 | Profile: DESCRIBE + combined stats | 2 SQL queries IN PARALLEL |
| 2 | Generate GeoJSON FeatureCollection | 1 SQL query |
| 3 | Extract data + build HTML + write file | 1 PowerShell command |
| 4 | Open in browser | open_browser |

**Speed rules:**
1. **Run DESCRIBE and profiling IN PARALLEL** — always batch them in the same tool call
2. **NEVER run LENGTH() or size-check queries** — trust the tolerance rules. The tolerances are calibrated to always produce < 10MB output.
3. **NEVER run exploratory queries** between profiling and GeoJSON generation (no "let me check the distinct types", no "let me see a sample"). The profiling query already has everything needed.
4. **Skip the intermediate .geojson file** — go directly from cached JSONL to final .html in ONE PowerShell command
5. **Use the HTML template** from `references/choropleth_template.html` or `references/symbol_map_template.html` — do NOT regenerate HTML structure from scratch
6. **For Point geometry (ST_DIMENSION=0):** skip ST_SIMPLIFY entirely — points have 1 vertex and need no simplification

## Working Style

- **Fully autonomous execution:** The entire workflow from profiling to visualization must complete without asking the user any questions. Make all technical decisions (simplification tolerance, aggregation period, chart limits, fallback strategies) silently using the defaults specified above.
- **No warnings or size alerts:** Never tell the user "this is 22MB, shall I simplify?" — just simplify it and proceed.
- **Fail gracefully:** If a query fails, try the next approach. If all approaches fail, render whatever partial result is available and explain in the report what couldn't be visualized.
- Be explicit when the answer is an inference rather than a confirmed rendering test.
- Do not claim Tableau rendering was performed unless the environment truly connected to Tableau.
- For CSVs, prefer concrete profiling results over generic advice.
- For GeoJSON, report geometry type distribution and coordinate validity; GeoJSON is inherently map-ready so focus the assessment on quality and what map type fits best.
- For Snowflake tables, tie the answer to the table schema and sampled data.
- If there is no usable geospatial signal, say so clearly and move to the best non-map visualization.

## Output

A rendered visualization (map HTML file opened in browser, or inline chart) plus a structured readiness report with score, recommendation, issues, and next steps.
