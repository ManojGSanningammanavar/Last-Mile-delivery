# Smart Last-Mile Delivery Intelligence System

A full-stack project that reduces failed deliveries using:
- Address parsing and confidence scoring
- Geo-coordinate validation
- Route optimization
- Delivery failure risk prediction with boosted-tree modeling
- Self-healing place memory graph (unique module)
- Counterfactual suggestions for operational actions
- Business impact metrics (before vs after)

## Architecture

Raw Orders -> Address NLP -> Geocode Validation -> Feature Engineering ->
Failure Prediction + Route Optimization + Action Recommendation -> API/UI

## Key Modules
- `src/address`: parse and normalize messy addresses
- `src/geo`: geocoding utilities and validation checks
- `src/routing`: graph and heuristic route optimization
- `src/ml`: model training, evaluation, and inference
- `src/place_graph`: memory graph for repeated place intelligence
- `src/weather`: weather-aware risk adjustment
- `src/counterfactual`: what-if analysis engine
- `src/metrics`: business impact evaluator
- `src/recommendation`: smart action engine
- `src/simulation`: before-vs-after impact simulation
- `src/api`: FastAPI endpoints
- `frontend`: map and chart enabled command center UI

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/seed_data.py
python scripts/train_model.py
python scripts/run_api.py
```

`seed_data.py` now generates a realistic noisy synthetic dataset (6000 rows) with missing/wrong pincodes and random delivery failures.

Open: `http://127.0.0.1:8000` for API and `http://127.0.0.1:8000/app` for dashboard.

## Demo Endpoints
- `GET /health`
- `POST /orders/process`
- `POST /predict/failure`
- `POST /route/optimize`
- `POST /counterfactual/simulate`

## Completion Checklist

Run this sequence to verify end-to-end completeness:

```bash
python scripts/seed_data.py
python scripts/train_model.py
python -m pytest -q
python scripts/run_api.py
```

Then verify:
- API health: `http://127.0.0.1:8000/health`
- Interactive docs: `http://127.0.0.1:8000/docs`
- Dashboard: `http://127.0.0.1:8000/app`

## Detailed Documentation
- File-by-file implementation guide: `docs/file_by_file_guide.md`
- Architecture notes: `docs/architecture.md`
- API contract: `docs/api_contract.md`
- Dataset schema: `docs/dataset_schema.md`
- Experiment log: `docs/experiment_log.md`
- Viva prep: `docs/viva_questions.md`

## Expected Outcome
- Better address quality detection
- Improved route efficiency
- Early risk detection for failed deliveries
- Actionable interventions before dispatch
- Quantified impact: failure rate and route distance improvements
