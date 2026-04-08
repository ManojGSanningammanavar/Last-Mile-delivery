# Architecture

## Flow
1. Input raw order data
2. Parse and normalize address
3. Compute address confidence
4. Geocode area and validate coordinates
5. Build ML features
6. Predict delivery failure probability
7. Optimize route sequence
8. Recommend operational action and counterfactual best option

## Modules
- Address: `src/address`
- Geo: `src/geo`
- Routing: `src/routing`
- ML: `src/ml`
- Place Memory Graph: `src/place_graph`
- API: `src/api`
- Frontend: `frontend`
