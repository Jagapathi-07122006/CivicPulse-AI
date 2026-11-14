from civicpulse.analyzer import calculate_screening
from civicpulse.schemas import WeatherSnapshot, SourceRecord

def weather(hourly):
    return WeatherSnapshot(
        current={},
        hourly=hourly,
        units={},
        source=SourceRecord(provider="test-vector", url="not-a-live-source", status="test-only")
    )

def test_screening_caps_all_components_at_100():
    score, label, components, maxima = calculate_screening(weather({
        "precipitation_probability": [100],
        "precipitation": [100],
        "wind_gusts_10m": [200],
    }))
    assert score == 100
    assert label == "High screening signal"
    assert sum(v for v in components.values() if v is not None) == 100

def test_screening_missing_all_inputs_is_not_calculated():
    score, label, components, maxima = calculate_screening(weather({}))
    assert score is None
    assert label == "Insufficient data"

def test_screening_ignores_non_numeric_values():
    score, label, components, maxima = calculate_screening(weather({
        "precipitation_probability": [None, "missing"],
        "precipitation": [0],
        "wind_gusts_10m": [0],
    }))
    assert score == 0
    assert components["precipitation_probability_points"] is None

def test_threshold_labels():
    # Explicit mathematical vectors verify the documented score thresholds.
    vectors = [
        (24, {"precipitation_probability": [60], "precipitation": [0], "wind_gusts_10m": [0]}, "Low screening signal"),
        (25, {"precipitation_probability": [62.5], "precipitation": [0], "wind_gusts_10m": [0]}, "Moderate screening signal"),
        (50, {"precipitation_probability": [100], "precipitation": [0], "wind_gusts_10m": [20]}, "Elevated screening signal"),
        (75, {"precipitation_probability": [100], "precipitation": [8.75], "wind_gusts_10m": [0]}, "High screening signal"),
    ]
    for expected_score, hourly, expected_label in vectors:
        score, label, _, _ = calculate_screening(weather(hourly))
        assert score == expected_score
        assert label == expected_label
