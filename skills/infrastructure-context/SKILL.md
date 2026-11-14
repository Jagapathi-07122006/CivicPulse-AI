---
name: infrastructure-context
description: Retrieve a bounded contextual count of nearby mapped emergency and healthcare features.
---

# Infrastructure context

1. Query a limited radius around the resolved coordinates using OpenStreetMap Overpass.
2. Count mapped hospitals, clinics/doctors, fire stations, and ambulance stations separately.
3. Deduplicate returned OSM elements by type and ID.
4. Record query radius, provider, retrieval time, and failures.
5. State clearly that mapped objects do not prove capacity, availability, completeness, or suitability.
6. Do not perform bulk regional extraction from public Overpass instances.
