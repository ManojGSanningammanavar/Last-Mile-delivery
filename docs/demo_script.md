# Demo Script (Placement-Ready)

## Goal
Show how the system prevents failed deliveries before dispatch.

## 1. Problem Framing
- Last-mile failures increase cost due to bad addresses and weak dispatch decisions.
- Manual process reacts after failure; this system predicts and prevents.

## 2. Input Noisy Order
Use this sample in dashboard input:
- address_raw: Near temple 3rd cross BTM Layout Bengaluru
- pincode: blank or wrong (optional to show risk increase)

## 3. Explain Processing Stages
- Address parser extracts area and landmark and computes confidence.
- Geo validation checks coordinate reliability.
- ML predicts failure probability.
- Action engine recommends intervention.
- Route optimizer generates dispatch sequence.

## 4. Show Risk + Explainability
Narrate output:
- Failure Risk: HIGH (example)
- Top reasons: low address confidence, long distance, historical failures
- Recommended action: call_customer_before_dispatch

## 5. Show Before vs After Impact
Present impact panel:
- Failure rate before intervention: around 28%
- Failure rate after intervention: around 17%
- Improvement: around 39%

## 6. Route Impact
Use map and route chart:
- Naive route distance vs optimized route distance
- ETA and stop sequence

## 7. One-Line Close
- The system is not just predictive; it is preventive and operationally actionable.
