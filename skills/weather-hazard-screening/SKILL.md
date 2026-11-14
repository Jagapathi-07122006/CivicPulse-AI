---
name: weather-hazard-screening
description: Retrieve and explain public weather forecast indicators for a user-specified place.
---

# Weather hazard screening

1. Resolve the user-provided place using Open-Meteo Geocoding.
2. Show the resolved name and coordinates.
3. Retrieve current and hourly forecast data from Open-Meteo.
4. Validate that hourly timestamps and requested variables are present.
5. Apply the documented deterministic screening calculation.
6. Report missing variables and source timestamps.
7. Never label the score as an official warning or validated probability.
