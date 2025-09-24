from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="scene-service")

class AnalyzeRequest(BaseModel):
    images: list[str]

class AnalyzeResponse(BaseModel):
    scene_graph_uri: str

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    return AnalyzeResponse(scene_graph_uri="gs://impossible-tower-data/scene_graphs/dummy.json")
