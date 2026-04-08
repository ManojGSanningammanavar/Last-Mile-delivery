# Experiment Log

## Baseline
- Model: Logistic Regression
- Features: address_confidence, geo_confidence, past_failures, distance_km, area_risk_score, time_slot, city

## Metrics Template
- F1: 
- ROC-AUC: 
- Notes: 

## Improvement Ideas
- Try RandomForestClassifier
- Calibrate threshold for high-risk precision
- Add interaction feature: address_confidence * geo_confidence
