# Viva Questions

1. Why this project?
- Last-mile delivery is the most failure-prone and expensive segment in logistics.
- This project predicts failure before dispatch and recommends actions to reduce cost.

2. What algorithms are used?
- NLP style parsing for noisy addresses and confidence scoring.
- Graph heuristic for route optimization (nearest-neighbor).
- ML classifier (XGBoost/RandomForest fallback) for failure prediction.

3. What is unique in your project?
- Self-healing place memory graph plus counterfactual and action engine.
- The system gives decision-ready recommendations, not just probability.

4. How did you measure success?
- F1 and ROC-AUC for model quality.
- Failure rate before vs after intervention.
- Route distance before vs after optimization.

5. Why ML here instead of fixed rules?
- Rules miss multi-factor interactions (distance, time slot, area pattern, address quality).
- ML estimates risk continuously so operations team can prioritize interventions.

6. What business impact did you demonstrate?
- Example demo outcome: projected failure reduction from ~28% to ~17%.
- This translates to fewer reattempts, less fuel waste, and better customer SLA.

7. What are current limitations?
- Synthetic dataset and deterministic geocoder fallback in academic setup.
- Real-time traffic and live geocoding API integration can improve production readiness.

8. Future enhancements?
- Online learning from new delivery outcomes.
- Reinforcement-based dispatch policy for dynamic route re-planning.
- Regional model variants for city-level behavior differences.
