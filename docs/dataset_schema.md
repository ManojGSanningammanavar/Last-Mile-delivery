# Dataset Schema

## orders_raw.csv
- order_id: Unique order identifier
- order_datetime: Timestamp of order
- address_raw: Customer-provided free-text address
- city: City name
- pincode: Postal code
- customer_id: Customer identifier
- past_failures: Historical failed deliveries count
- distance_km: Warehouse-to-order distance estimate
- time_slot: morning/afternoon/evening/night
- delivery_status: delivered/failed
- failure_reason: failure category

## area_risk.csv
- area: canonical area
- area_risk_score: 0 to 1 risk score
- avg_failure_rate: historical area failure rate

## weather_sample.csv
- date
- time_slot
- city
- rainfall_mm
- temperature_c
- weather_risk_score
