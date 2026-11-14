from .schemas import AnalysisResult

def render_markdown(result: AnalysisResult) -> str:
    place = result.place
    lines = [
        f"# CivicPulse AI — Preliminary Screening Brief",
        "",
        f"**Place resolved by provider:** {place.name}, {place.admin1 or 'Administrative region not supplied'}, {place.country or 'Country not supplied'}",
        f"**Coordinates:** {place.latitude}, {place.longitude}",
        f"**Generated at (UTC):** {result.generated_at}",
        f"**Screening result:** {result.screening_label} — {result.screening_score if result.screening_score is not None else 'not calculated'}/100",
        "",
        "## Geocoding evidence",
        f"- Provider: {result.geocoding_source.provider}",
        f"- Retrieved at: {result.geocoding_source.retrieved_at}",
        f"- Source endpoint: {result.geocoding_source.url}",
        f"- Query detail: {result.geocoding_source.detail}",
        "",
        "## Weather evidence",
        f"- Provider: {result.weather.source.provider}",
        f"- Retrieved at: {result.weather.source.retrieved_at}",
        f"- Source endpoint: {result.weather.source.url}",
        f"- Current observations returned: `{result.weather.current}`",
        f"- Screening components: `{result.components}`",
        "",
        "## Nearby mapped infrastructure",
        f"- Provider: {result.infrastructure.source.provider}",
        f"- Retrieved at: {result.infrastructure.source.retrieved_at}",
        f"- Query status: {result.infrastructure.source.status}",
        f"- Search radius: {result.infrastructure.radius_m} metres",
        f"- Counts: `{result.infrastructure.counts}`",
        f"- Interpretation: {result.infrastructure.note}",
        "",
        "## Decision explanation",
    ]
    lines.extend(f"- {item}" for item in result.explanation)
    lines += [
        "",
        "## Limitations and required human review",
        "- This is a rule-based weather screening signal, not a validated probability, official warning, or prediction of disaster impacts.",
        "- It does not include official alerts, population exposure, road closures, facility capacity, shelter occupancy, or resource availability.",
        "- Forecasts and mapped data may be incomplete, delayed, or revised.",
        "- A human reviewer must check official local authority information before any operational decision.",
        "",
        "## Attribution",
        "- Weather: Open-Meteo (https://open-meteo.com/).",
        "- Map data: © OpenStreetMap contributors (https://www.openstreetmap.org/copyright).",
    ]
    return "\n".join(lines) + "\n"
