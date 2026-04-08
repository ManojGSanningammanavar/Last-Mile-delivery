# File-by-File Guide

This document explains what each project file does and how modules connect.

## Root Files

### `README.md`
- Project overview, quick start, endpoints, and validation checklist.

### `requirements.txt`
- Python dependencies for API, ML, routing, and tests.

### `.env.example`
- Environment variable template for app name and DB path.

### `.gitignore`
- Ignores virtual env, model binaries, caches, and local artifacts.

## Config

### `configs/config.yaml`
- Central settings for thresholds and feature flags.
- Used by settings loader to keep constants out of code.

## Data

### `data/raw/orders_raw.csv`
- Training and demo source data with order/address/failure labels.

### `data/raw/area_risk.csv`
- Area-level risk priors used in feature engineering.

### `data/raw/weather_sample.csv`
- Weather risk sample used for post-model probability adjustment.

### `data/processed/orders_clean.csv`
- Processed seed copy of raw orders.

### `data/processed/features_train.csv`
- Final model training matrix saved by training pipeline.

### `data/processed/place_graph.json`
- Persistent place-memory graph state for repeat-location behavior.

### `data/processed/app.db`
- SQLite app storage for order/prediction records.

## Models

### `models/failure_model.pkl`
- Trained classifier for delivery failure probability.

### `models/preprocessor.pkl`
- Saved preprocessing pipeline for inference consistency.

### `models/metadata.json`
- Feature list and evaluation metadata for reproducibility.

## Frontend

### `frontend/index.html`
- Single-page dashboard UI and user input panel.

### `frontend/styles.css`
- Custom visual system (colors, typography, responsive layout, animations).

### `frontend/app.js`
- Client logic to submit JSON orders and render API output.

## Scripts

### `scripts/seed_data.py`
- Seeds processed data from raw dataset.

### `scripts/train_model.py`
- Runs model training and saves artifacts.

### `scripts/run_api.py`
- Starts FastAPI app via Uvicorn.

### `scripts/run_demo.py`
- Runs one sample order through full pipeline and prints JSON output.

## Source Package (`src`)

### `src/main.py`
- FastAPI app entrypoint, CORS, router registration, static dashboard mount.

### `src/settings.py`
- Loads typed runtime settings from env and config.

### `src/address/normalizer.py`
- Text normalization rules for noisy address strings.

### `src/address/parser.py`
- Extracts structured address fields: area, landmark, pincode.

### `src/address/confidence.py`
- Computes address confidence score from parse completeness.

### `src/geo/cache.py`
- Static lookup cache mapping known areas to lat/lon coordinates.

### `src/geo/geocoder.py`
- Deterministic geocoder with area-based and city-centroid fallback.

### `src/geo/validator.py`
- Validates geocode reliability and returns warning flags.

### `src/routing/graph_builder.py`
- Utility functions for route graph distance matrix construction.

### `src/routing/optimizer.py`
- Nearest-neighbor route optimizer over delivery nodes.

### `src/routing/eta.py`
- ETA estimation helper from route distance.

### `src/weather/provider.py`
- Loads weather table and fetches slot-level weather score.

### `src/weather/risk.py`
- Adjusts base model probability with weather risk.

### `src/place_graph/place_node.py`
- Place node schema for memory graph representation.

### `src/place_graph/matcher.py`
- Matches incoming order to known place nodes using text/geo similarity.

### `src/place_graph/updater.py`
- Updates place memory with new delivery outcomes.

### `src/place_graph/recommender.py`
- Recommends operational action from place history and risk label.

### `src/counterfactual/simulator.py`
- Simulates what-if interventions and expected risk deltas.

### `src/ml/features.py`
- Feature-building utilities for train/inference alignment.

### `src/ml/train.py`
- Trains model, saves preprocessor/model, writes metadata.

### `src/ml/evaluate.py`
- Computes evaluation metrics for model monitoring.

### `src/ml/predict.py`
- Inference helper returning failure probability and risk labels.

### `src/ml/explain.py`
- Lightweight explanation function for top risk contributors.

### `src/pipeline/run_training_pipeline.py`
- End-to-end training orchestration from raw files.

### `src/pipeline/run_pipeline.py`
- Full online processing pipeline: parse -> geo -> predict -> recommend -> route.

### `src/api/schemas.py`
- Request body contracts for API endpoints.

### `src/api/routes_health.py`
- Health probe endpoint.

### `src/api/routes_orders.py`
- Main processing endpoint using full pipeline.

### `src/api/routes_predict.py`
- Standalone risk prediction endpoint with derived feature enrichment.

### `src/api/routes_route_optimize.py`
- Standalone route optimization endpoint with geo-quality notes.

### `src/api/routes_route.py`
- Counterfactual simulation endpoint.

### `src/db/database.py`
- DB connection and session helpers.

### `src/db/models.py`
- SQLite table models and initialization.

### `src/db/repository.py`
- Data-access layer for writing/reading pipeline results.

### `src/utils/io.py`
- Shared JSON/CSV file helpers.

### `src/utils/logger.py`
- Logging configuration helpers.

### `src/utils/datetime_utils.py`
- Date formatting/parsing utility helpers.

### `src/utils/geo_utils.py`
- Distance utility helpers used by routing logic.

## Tests

### `tests/test_address_parser.py`
- Verifies area/landmark/pincode extraction behavior.

### `tests/test_geo_validator.py`
- Verifies geo confidence and warning generation.

### `tests/test_route_optimizer.py`
- Verifies route ordering and distance output consistency.

### `tests/test_ml_predict.py`
- Trains temporary model and validates inference output columns.

### `tests/test_place_graph_matcher.py`
- Verifies place-node matching logic.

### `tests/test_pipeline_smoke.py`
- Smoke test for full pipeline contract shape.

## Additional Docs

### `docs/architecture.md`
- Architecture and component interaction notes.

### `docs/api_contract.md`
- Endpoint request/response samples.

### `docs/dataset_schema.md`
- Dataset column definitions and expected types.

### `docs/experiment_log.md`
- Model training/evaluation observations.

### `docs/viva_questions.md`
- Interview and project-viva preparation.

## CI

### `.github/workflows/ci.yml`
- GitHub Actions workflow that runs tests on push and pull request.
