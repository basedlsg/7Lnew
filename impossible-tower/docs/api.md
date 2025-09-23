# API Reference

**Service base URLs**
- Checker: https://impossible-tower-checker-612990030705.us-central1.run.app
- Demo: https://impossible-tower-demo-612990030705.us-central1.run.app


## Checker Service

### `POST /check`

Validate a symbolic program against a scene graph using Z3 constraints.

- **Request body:**

```json
{
  "program": {
    "assumptions": ["contact(A,B)", "on(A,B)", "com_within_support(A)"]
  },
  "scene_graph": {},
  "constraints": {}
}
```

- **Response:**

```json
{
  "pass": false,
  "violations": [
    {"rule": "com_support", "object": "block_3"}
  ],
  "counterexample": {
    "block_3": {
      "com_proj": [0.2, -0.1],
      "support_poly": [[-0.1,-0.1],[0.1,-0.1],[0.1,0.1],[-0.1,0.1]]
    }
  }
}
```

- **Errors:**
  - `400` for invalid payloads
  - `422` if Z3 cannot solve due to malformed constraints

## Demo Service

### `GET /healthz`

Health probe returning service status.

### `POST /analyze`

Run the full inference + checking loop on a set of images.

- **Request body:**

```json
{
  "images": ["gs://bucket/scene123/cam_00.png", "gs://bucket/scene123/cam_03.png"],
  "question": "Is this stack physically possible?"
}
```

- **Response:**

```json
{
  "possible": false,
  "program": {"assumptions": [], "claims": []},
  "proof": {
    "pass": false,
    "violations": [{"rule": "support_contact", "object": "block_5"}]
  },
  "explanation": "COM of top block is outside the base support polygon."
}
```

- **Errors:**
  - `502` if the model call fails
  - `500` for unexpected exceptions (with structured error payload)

## Authentication

- Internal services rely on environment variables for API keys.
- For production Cloud Run deployments, configure IAM-based authentication.

## Logging

All services emit JSON logs with trace IDs, request IDs, and latency metrics. See `src/demo/app.py` and `src/checker/service.py` for logging hooks.
