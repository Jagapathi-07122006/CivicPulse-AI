from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def test_manifest_references_existing_skill_and_tool_files():
    manifest = yaml.safe_load((ROOT / "agent.yaml").read_text())
    assert manifest["spec_version"] == "0.1.0"
    assert manifest["name"] == "civicpulse-ai"
    assert set(manifest["tools"]) == {p.stem for p in (ROOT / "tools").glob("*.yaml")}
    assert set(manifest["skills"]) == {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}

def test_event_explainability_headings_and_two_sentences():
    text = (ROOT / "EXPLAINABILITY.md").read_text()
    for heading in ("## Decision", "## Inputs", "## Limits"):
        assert heading in text
        section = text.split(heading, 1)[1].split("\n## ", 1)[0]
        sentences = [s for s in section.replace("\n", " ").split(".") if len(s.strip()) > 15]
        assert len(sentences) >= 2

def test_maker_checker_are_separate_lines():
    duties = (ROOT / "DUTIES.md").read_text()
    assert "- **Maker" in duties
    assert "- **Checker" in duties
    assert all(not ("Maker" in line and "Checker" in line) for line in duties.splitlines())
    agents = (ROOT / "AGENTS.md").read_text()
    assert all(not ("Maker" in line and "Checker" in line) for line in agents.splitlines())
