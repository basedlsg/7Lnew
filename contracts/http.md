# HTTP Contracts (Draft)

## scene-service
POST /analyze
- body:
```json
{ "images": ["gs://bucket/path/img.png"] }
```
- response:
```json
{ "scene_graph_uri": "gs://bucket/scene_graphs/example.json" }
```

## vertex-proxy
POST /infer
- body:
```json
{ "prompt": "string", "images": ["gs://..."], "response_schema": {} }
```
- response:
```json
{ "content": "{\\"assumptions\\":[...],\\"claims\\":[...]}" }
```

## z3-checker
POST /check
- body:
```json
{ "program": {"assumptions":[],"claims":[]}, "scene_graph_uri": "gs://..." }
```
- response:
```json
{ "result": "sat", "rationale": "string" }
```
