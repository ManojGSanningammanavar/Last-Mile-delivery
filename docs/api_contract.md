# API Contract

## Health
- `GET /health`

## Process Orders
- `POST /orders/process`
- Request:
```json
{
  "orders": [
    {
      "order_id": "ORD001",
      "order_datetime": "2026-03-18 10:30:00",
      "address_raw": "Near temple 3rd cross BTM Layout Bengaluru",
      "city": "Bengaluru",
      "pincode": "560076",
      "past_failures": 1,
      "distance_km": 5.4,
      "time_slot": "evening",
      "area_risk_score": 0.3
    }
  ]
}
```

## Predict Failure
- `POST /predict/failure`

## Route Optimize
- `POST /route/optimize`

## Counterfactual
- `POST /counterfactual/simulate`
