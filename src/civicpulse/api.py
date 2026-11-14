from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .agent import CivicPulseAgent
from .collectors import DataSourceError

app = FastAPI(title="CivicPulse AI", version="0.1.0",
              description="Evidence-linked preliminary weather screening; not an emergency authority.")
agent = CivicPulseAgent()

class AnalyzeRequest(BaseModel):
    place: str = Field(min_length=2, max_length=160)
    radius_m: int = Field(default=5000, ge=500, le=10000)
    forecast_days: int = Field(default=2, ge=1, le=7)

@app.get("/health")
async def health():
    return {"status": "ok", "agent": "civicpulse-ai", "mode": "live-public-data"}

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        result, report = await agent.analyze_report(request.place, request.radius_m, request.forecast_days)
        return {"result": result.model_dump(), "report_markdown": report}
    except (DataSourceError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Upstream or processing failure: {type(exc).__name__}: {exc}")
