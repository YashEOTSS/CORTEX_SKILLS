#!/usr/bin/env python3
"""Profile a CSV or GeoJSON file for visualization readiness.

Reads a data file, infers likely geospatial and charting fields, and prints a
JSON summary that can guide a readiness assessment.

Supported formats:
- CSV (.csv): Infers columns by name and data type
- GeoJSON (.geojson, .json): Validates geometry and inspects properties
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

LAT_NAMES = {"lat", "latitude", "y"}
LON_NAMES = {"lon", "lng", "long", "longitude", "x"}
GEO_HINTS = {"city", "state", "province", "region", "country", "zip", "postal", "postcode", "county"}
DATE_HINTS = {"date", "time", "timestamp", "created_at", "updated_at", "day", "month", "year"}
FLOW_HINTS = {"source", "from", "origin", "target", "to", "destination", "node"}

VALID_GEOJSON_TYPES = {"Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon", "GeometryCollection"}


def _normalize(name: str) -> str:
    return name.strip().lower().replace(" ", "_")


# ---------------------------------------------------------------------------
# CSV profiling (existing logic)
# ---------------------------------------------------------------------------

def _find_columns(df: pd.DataFrame) -> Dict[str, List[str]]:
    cols = list(df.columns)
    normalized = {_normalize(c): c for c in cols}

    lat = [original for norm, original in normalized.items() if norm in LAT_NAMES]
    lon = [original for norm, original in normalized.items() if norm in LON_NAMES]
    geo = [original for norm, original in normalized.items() if any(h in norm for h in GEO_HINTS)]
    date = [original for norm, original in normalized.items() if any(h in norm for h in DATE_HINTS)]
    flow = [original for norm, original in normalized.items() if any(h in norm for h in FLOW_HINTS)]
    numeric = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
    categorical = [c for c in cols if not pd.api.types.is_numeric_dtype(df[c])]

    return {
        "latitude_candidates": lat,
        "longitude_candidates": lon,
        "geo_candidates": geo,
        "date_candidates": date,
        "flow_candidates": flow,
        "numeric_columns": numeric,
        "categorical_columns": categorical,
    }


def _null_rate(s: pd.Series) -> float:
    return float(s.isna().mean()) if len(s) else math.nan


def _score_map(df: pd.DataFrame, cols: Dict[str, List[str]]) -> Dict[str, Any]:
    issues: List[str] = []
    score = 0

    lat_col = cols["latitude_candidates"][0] if cols["latitude_candidates"] else None
    lon_col = cols["longitude_candidates"][0] if cols["longitude_candidates"] else None
    geo_col = cols["geo_candidates"][0] if cols["geo_candidates"] else None

    if lat_col and lon_col:
        score += 50
        lat = pd.to_numeric(df[lat_col], errors="coerce")
        lon = pd.to_numeric(df[lon_col], errors="coerce")
        valid = lat.between(-90, 90) & lon.between(-180, 180)
        score += 20 if valid.mean() >= 0.9 else 8 if valid.mean() >= 0.7 else 0
        if valid.mean() < 0.9:
            issues.append("some coordinates fall outside valid latitude/longitude ranges")
        if lat.isna().mean() > 0.1 or lon.isna().mean() > 0.1:
            issues.append("latitude or longitude has noticeable null coverage")
    elif geo_col:
        score += 25
        if geo_col.lower() in {"country", "state", "province", "region", "zip", "postal", "postcode"}:
            score += 20
        else:
            issues.append("geographic text fields exist but are not clearly standardized")
    else:
        issues.append("no clear geographic fields detected")

    if len(df) > 0:
        score += 10 if len(df) >= 10 else 5
    if df.select_dtypes(include="number").shape[1] > 0:
        score += 5

    return {
        "score": min(score, 100),
        "issues": issues,
        "recommendation": (
            "symbol map" if lat_col and lon_col else "filled map" if geo_col else "not recommended"
        ),
    }


def _best_chart(df: pd.DataFrame, cols: Dict[str, List[str]]) -> Dict[str, Any]:
    if cols["date_candidates"] and cols["numeric_columns"]:
        return {"best": "time-series chart", "reason": "date-like field plus numeric measure"}
    if cols["categorical_columns"] and cols["numeric_columns"]:
        return {"best": "bar chart", "reason": "categorical dimension plus numeric measure"}
    if len(cols["flow_candidates"]) >= 2 and cols["numeric_columns"]:
        return {"best": "sankey diagram", "reason": "source-target style flow fields and value measure"}
    if len(cols["numeric_columns"]) >= 2:
        return {"best": "heat map", "reason": "multiple numeric measures can support intensity patterns"}
    return {"best": "bar chart", "reason": "default comparison chart when clearer structure is missing"}


def _profile_csv(path: Path, max_rows: int) -> Dict[str, Any]:
    df = pd.read_csv(path, nrows=max_rows)
    cols = _find_columns(df)
    map_result = _score_map(df, cols)
    chart_result = _best_chart(df, cols)

    return {
        "format": "csv",
        "rows_sampled": int(len(df)),
        "columns": list(df.columns),
        "field_detection": cols,
        "map_assessment": map_result,
        "best_non_map_chart": chart_result,
    }


# ---------------------------------------------------------------------------
# GeoJSON profiling
# ---------------------------------------------------------------------------

def _extract_coords_flat(geometry: Dict[str, Any]) -> List[List[float]]:
    """Recursively extract all [lon, lat] coordinate pairs from a geometry."""
    coords: List[List[float]] = []
    geom_type = geometry.get("type", "")
    raw_coords = geometry.get("coordinates")

    if geom_type == "Point" and raw_coords:
        coords.append(raw_coords[:2])
    elif geom_type == "MultiPoint" and raw_coords:
        coords.extend(c[:2] for c in raw_coords)
    elif geom_type == "LineString" and raw_coords:
        coords.extend(c[:2] for c in raw_coords)
    elif geom_type == "MultiLineString" and raw_coords:
        for line in raw_coords:
            coords.extend(c[:2] for c in line)
    elif geom_type == "Polygon" and raw_coords:
        for ring in raw_coords:
            coords.extend(c[:2] for c in ring)
    elif geom_type == "MultiPolygon" and raw_coords:
        for polygon in raw_coords:
            for ring in polygon:
                coords.extend(c[:2] for c in ring)
    elif geom_type == "GeometryCollection":
        for g in geometry.get("geometries", []):
            coords.extend(_extract_coords_flat(g))

    return coords


def _score_geojson(data: Dict[str, Any], max_features: int) -> Dict[str, Any]:
    """Score a GeoJSON FeatureCollection for map readiness."""
    issues: List[str] = []

    features = data.get("features", [])
    if not features:
        return {
            "score": 0,
            "issues": ["GeoJSON contains no features"],
            "recommendation": "not recommended",
            "geometry_types": [],
            "feature_count": 0,
        }

    sampled = features[:max_features]
    geometry_types: Dict[str, int] = {}
    null_geometry_count = 0
    all_coords: List[List[float]] = []

    for feature in sampled:
        geom = feature.get("geometry")
        if geom is None:
            null_geometry_count += 1
            continue
        gtype = geom.get("type", "Unknown")
        geometry_types[gtype] = geometry_types.get(gtype, 0) + 1
        all_coords.extend(_extract_coords_flat(geom))

    total_sampled = len(sampled)
    score = 0

    # Geometry presence (features have geometry at all)
    geom_coverage = (total_sampled - null_geometry_count) / total_sampled if total_sampled else 0
    if geom_coverage >= 0.9:
        score += 40
    elif geom_coverage >= 0.7:
        score += 25
        issues.append(f"{null_geometry_count} features have null geometry")
    else:
        score += 10
        issues.append(f"high null geometry rate: {null_geometry_count}/{total_sampled} features lack geometry")

    # Valid geometry types
    invalid_types = [t for t in geometry_types if t not in VALID_GEOJSON_TYPES]
    if not invalid_types:
        score += 15
    else:
        issues.append(f"unrecognized geometry types: {invalid_types}")

    # Coordinate validity (GeoJSON uses [longitude, latitude] order)
    if all_coords:
        valid_count = sum(
            1 for lon, lat in all_coords
            if -180 <= lon <= 180 and -90 <= lat <= 90
        )
        validity_rate = valid_count / len(all_coords)
        if validity_rate >= 0.95:
            score += 25
        elif validity_rate >= 0.8:
            score += 15
            issues.append("some coordinates fall outside valid ranges")
        else:
            score += 5
            issues.append(f"coordinate validity is low ({validity_rate:.0%} valid)")
    else:
        issues.append("no extractable coordinates found in geometries")

    # Feature count bonus
    if total_sampled >= 10:
        score += 10
    elif total_sampled >= 3:
        score += 5

    # Properties bonus (has attributes beyond geometry)
    sample_props = sampled[0].get("properties") if sampled else None
    if sample_props and len(sample_props) > 0:
        score += 10

    # Determine best map type
    dominant_type = max(geometry_types, key=geometry_types.get) if geometry_types else None
    if dominant_type in {"Point", "MultiPoint"}:
        recommendation = "symbol map"
    elif dominant_type in {"Polygon", "MultiPolygon"}:
        recommendation = "filled map (choropleth)"
    elif dominant_type in {"LineString", "MultiLineString"}:
        recommendation = "path/route map"
    else:
        recommendation = "symbol map"

    return {
        "score": min(score, 100),
        "issues": issues,
        "recommendation": recommendation,
        "geometry_types": geometry_types,
        "feature_count": len(features),
        "features_sampled": total_sampled,
    }


def _detect_properties(features: List[Dict[str, Any]], max_features: int) -> Dict[str, List[str]]:
    """Detect property field types from GeoJSON features for non-map chart assessment."""
    sampled = features[:max_features]
    all_keys: Dict[str, set] = {}

    for feature in sampled:
        props = feature.get("properties") or {}
        for key, val in props.items():
            if key not in all_keys:
                all_keys[key] = set()
            all_keys[key].add(type(val).__name__)

    numeric_props = [k for k, types in all_keys.items() if types <= {"int", "float", "NoneType"}]
    categorical_props = [k for k, types in all_keys.items() if "str" in types]
    date_props = [k for k in all_keys if any(h in _normalize(k) for h in DATE_HINTS)]
    flow_props = [k for k in all_keys if any(h in _normalize(k) for h in FLOW_HINTS)]

    return {
        "all_property_keys": list(all_keys.keys()),
        "numeric_properties": numeric_props,
        "categorical_properties": categorical_props,
        "date_properties": date_props,
        "flow_properties": flow_props,
    }


def _best_chart_geojson(prop_detection: Dict[str, List[str]]) -> Dict[str, Any]:
    """Recommend the best non-map chart from GeoJSON properties."""
    if prop_detection["date_properties"] and prop_detection["numeric_properties"]:
        return {"best": "time-series chart", "reason": "date-like property plus numeric measure in features"}
    if prop_detection["categorical_properties"] and prop_detection["numeric_properties"]:
        return {"best": "bar chart", "reason": "categorical property plus numeric measure in features"}
    if len(prop_detection["flow_properties"]) >= 2 and prop_detection["numeric_properties"]:
        return {"best": "sankey diagram", "reason": "flow-style properties with numeric value"}
    if len(prop_detection["numeric_properties"]) >= 2:
        return {"best": "heat map", "reason": "multiple numeric properties can support intensity patterns"}
    return {"best": "bar chart", "reason": "default when clearer structure is missing in properties"}


def _profile_geojson(path: Path, max_features: int) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Handle both FeatureCollection and single Feature
    if data.get("type") == "Feature":
        data = {"type": "FeatureCollection", "features": [data]}
    elif data.get("type") in VALID_GEOJSON_TYPES:
        data = {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": data, "properties": {}}]}

    map_result = _score_geojson(data, max_features)
    features = data.get("features", [])
    prop_detection = _detect_properties(features, max_features)
    chart_result = _best_chart_geojson(prop_detection)

    return {
        "format": "geojson",
        "feature_count": len(features),
        "features_sampled": min(len(features), max_features),
        "property_detection": prop_detection,
        "map_assessment": map_result,
        "best_non_map_chart": chart_result,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Profile a CSV or GeoJSON file for visualization readiness."
    )
    parser.add_argument("file_path", type=Path, help="Path to CSV or GeoJSON file")
    parser.add_argument("--rows", type=int, default=500, help="Max rows/features to sample")
    args = parser.parse_args()

    path = args.file_path
    suffix = path.suffix.lower()

    if suffix == ".csv":
        output = _profile_csv(path, args.rows)
    elif suffix in {".geojson", ".json"}:
        output = _profile_geojson(path, args.rows)
    else:
        print(json.dumps({"error": f"Unsupported file format: {suffix}. Supported: .csv, .geojson, .json"}))
        return 1

    print(json.dumps(output, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
