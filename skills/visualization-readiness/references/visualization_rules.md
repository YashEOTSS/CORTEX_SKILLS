# Visualization Rules

Use these heuristics when scoring readiness.

## Scoring

- 90-100: very strong fit, clean and complete data, map or chart should be straightforward
- 70-89: strong fit with minor cleanup needed
- 40-69: partial fit, usable but needs validation or transformation
- 0-39: weak fit, visualization is likely misleading or unsupported

## Suggested Score Inputs

- Field availability: 30%
- Field quality and validity: 30%
- Coverage and completeness: 20%
- Visualization specificity: 20%

## Geospatial Validation Checklist

- Latitude between -90 and 90
- Longitude between -180 and 180
- Geography fields align with intended region
- Null rate is low enough to support plotting
- Duplicates are understood and expected
- Text geography values are not overly ambiguous

## Non-Map Decision Cues

- Time-series: date or timestamp exists and measure varies over time
- Bar chart: categorical comparison is clear
- Sankey: source and target fields both exist
- Heat map: two meaningful axes plus intensity field exist
