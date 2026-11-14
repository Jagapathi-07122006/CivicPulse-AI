# Explainability

## Decision

CivicPulse AI computes a deterministic weather-screening indicator from the maximum forecast hourly precipitation probability, maximum forecast hourly precipitation amount, and maximum forecast wind gust over the requested forecast window. The score is a rule-based screening signal, not a trained model, calibrated probability, official hazard category, or casualty prediction.

The calculation is fully documented in `src/civicpulse/analyzer.py`: precipitation probability contributes up to 40 points, forecast precipitation amount contributes up to 40 points, and wind gust contributes up to 20 points. The resulting 0–100 score is labelled Low, Moderate, Elevated, or High using fixed thresholds. Missing variables are not imputed; the report records which components were unavailable and the score is computed only when the required inputs exist.

## Inputs

The agent accepts a place name and retrieves coordinates using Open-Meteo Geocoding. It then retrieves current and hourly forecast variables from the Open-Meteo Forecast API and queries nearby mapped healthcare and emergency-service features from OpenStreetMap Overpass when that optional source is available.

Each successful source response is accompanied by a retrieval timestamp, provider name, query details, and source URL. OpenStreetMap feature counts describe mapped objects returned within the selected radius only; they do not establish facility operating status, bed capacity, staff availability, suitability, or completeness.

## Limitations

The agent does not ingest official government disaster alerts, live road closures, verified population exposure, hospital capacity, shelter occupancy, or emergency-resource inventories in this initial version. Forecast models can change, geocoding may resolve an ambiguous place, Overpass may be unavailable, and OpenStreetMap coverage may be incomplete or stale.

The output is not an official warning or an operational instruction. A qualified human must check official local authority information and verify the situation before making decisions; in an emergency, follow government and emergency-service directions.
