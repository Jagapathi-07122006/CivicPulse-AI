from .schemas import Place, WeatherSnapshot, InfrastructureSummary, AnalysisResult

def _max_numeric(values) -> float | None:
    if not isinstance(values, list):
        return None
    valid = [float(v) for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)]
    return max(valid) if valid else None

def calculate_screening(weather: WeatherSnapshot):
    hourly = weather.hourly
    probability = _max_numeric(hourly.get("precipitation_probability"))
    precipitation = _max_numeric(hourly.get("precipitation"))
    gust = _max_numeric(hourly.get("wind_gusts_10m"))

    # Transparent heuristic points. These are not fitted or calibrated model coefficients.
    p_points = None if probability is None else min(40.0, max(0.0, probability) * 0.4)
    r_points = None if precipitation is None else min(40.0, max(0.0, precipitation) * 4.0)
    w_points = None if gust is None else min(20.0, max(0.0, gust) * 0.5)

    available = [v for v in (p_points, r_points, w_points) if v is not None]
    score = None if not available else round(sum(available))
    components = {
        "precipitation_probability_points": None if p_points is None else round(p_points, 2),
        "precipitation_amount_points": None if r_points is None else round(r_points, 2),
        "wind_gust_points": None if w_points is None else round(w_points, 2),
    }
    if score is None:
        label = "Insufficient data"
    elif score < 25:
        label = "Low screening signal"
    elif score < 50:
        label = "Moderate screening signal"
    elif score < 75:
        label = "Elevated screening signal"
    else:
        label = "High screening signal"
    return score, label, components, {
        "max_precipitation_probability_percent": probability,
        "max_hourly_precipitation_mm": precipitation,
        "max_wind_gust_kmh": gust,
    }

def build_analysis(place: Place, geocoding_source, weather: WeatherSnapshot,
                   infrastructure: InfrastructureSummary) -> AnalysisResult:
    score, label, components, maxima = calculate_screening(weather)
    explanation = [
        f"Maximum forecast precipitation probability: {maxima['max_precipitation_probability_percent']}%.",
        f"Maximum forecast hourly precipitation: {maxima['max_hourly_precipitation_mm']} mm.",
        f"Maximum forecast wind gust: {maxima['max_wind_gust_kmh']} km/h.",
        "The score sums capped heuristic contributions: probability (0–40), precipitation (0–40), and gust (0–20).",
        "Mapped infrastructure counts are contextual only and are not included in the weather screening score.",
    ]
    return AnalysisResult(place=place, geocoding_source=geocoding_source, weather=weather, infrastructure=infrastructure,
                          screening_score=score, screening_label=label,
                          components=components, explanation=explanation)
