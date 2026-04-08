# B.Tech Minor Project Weekly Progress Report (5 Weeks)

## Project Information
- Department: CSE-CORE
- Semester: VI
- Project Title: Smart Last-Mile Delivery Intelligence System
- Guide Name: ______________________
- Team Members (Name - USN):
  - Member 1: ______________________
  - Member 2: ______________________
  - Member 3: ______________________
  - Member 4: ______________________

---

## Week 1 Report
- Week No: 1
- From: ______________
- To: ______________

### Work Carried Out by Team (Bullet Points)
- Finalized project problem statement and objectives for failed-delivery reduction.
- Completed architecture planning for address intelligence, ML prediction, routing, and monitoring layers.
- Prepared initial repository structure and module-wise folder organization.
- Defined API contract, dataset schema, and implementation plan documents.
- Set up Python environment, dependency list, and project execution scripts.

### Individual Contribution by Student
| Student | Work Carried Out |
|---|---|
| Member 1 | Project architecture design, module decomposition, technical planning |
| Member 2 | API contract drafting, schema planning, endpoint structure definition |
| Member 3 | Repository setup, dependency management, configuration setup |
| Member 4 | Documentation baseline (architecture, dataset schema, planning notes) |

### Work Planned for Following Week
- Generate and clean training data.
- Build address parsing and geo-validation pipeline.
- Implement first stable prediction workflow.

### Major Bottlenecks (If Any)
- Requirement consolidation across multiple modules.
- Alignment of data fields across ML and API layers.

---

## Week 2 Report
- Week No: 2
- From: ______________
- To: ______________

### Work Carried Out by Team (Bullet Points)
- Generated synthetic order dataset with realistic noise and failure patterns.
- Implemented address parser, address confidence scoring, and normalization utilities.
- Implemented geocoding with cache + validation checks (pincode and city-bound validation).
- Built feature-engineering pipeline for model-ready numeric and categorical features.
- Added preprocessing outputs for training reproducibility.

### Individual Contribution by Student
| Student | Work Carried Out |
|---|---|
| Member 1 | Address parsing and confidence computation modules |
| Member 2 | Geocoder integration, cache logic, and validation layer |
| Member 3 | Feature engineering pipeline and transformed dataset outputs |
| Member 4 | Data generation script and schema consistency checks |

### Work Planned for Following Week
- Train baseline and improved ML models.
- Add prediction endpoint and persistence.
- Build route optimization API integration.

### Major Bottlenecks (If Any)
- Handling inconsistent raw address formats.
- Geocoding reliability for partial/ambiguous address text.

---

## Week 3 Report
- Week No: 3
- From: ______________
- To: ______________

### Work Carried Out by Team (Bullet Points)
- Implemented model training pipeline with metadata and artifact export.
- Added inference pipeline for risk probability and risk label assignment.
- Developed FastAPI endpoints for health, prediction, order processing, and route optimization.
- Added SQLite storage for prediction monitoring statistics.
- Integrated core recommendation engine for dispatch actions.

### Individual Contribution by Student
| Student | Work Carried Out |
|---|---|
| Member 1 | Model training pipeline, feature importance, metadata outputs |
| Member 2 | Prediction endpoint and failure-risk response integration |
| Member 3 | Database schema/migrations and monitoring repository logic |
| Member 4 | Route optimization API and response payload structuring |

### Work Planned for Following Week
- Add advanced analytics (uncertainty, causal policy, digital twin).
- Integrate frontend dashboard with backend APIs.
- Improve error handling and API security controls.

### Major Bottlenecks (If Any)
- Model calibration and confidence consistency.
- Synchronizing output schema between backend and frontend.

---

## Week 4 Report
- Week No: 4
- From: ______________
- To: ______________

### Work Carried Out by Team (Bullet Points)
- Implemented conformal uncertainty layer with uncertainty bands and calibration summary.
- Added causal action ranking and intervention uplift estimation module.
- Implemented digital twin simulation for dispatch what-if analysis.
- Built frontend command-center UI with dashboard, map, KPI cards, and advanced result tables.
- Added monitoring endpoint integration and periodic frontend refresh.

### Individual Contribution by Student
| Student | Work Carried Out |
|---|---|
| Member 1 | Conformal uncertainty module and uncertainty API integration |
| Member 2 | Causal uplift policy module and action recommendation enrichment |
| Member 3 | Digital twin simulator and timeline summary outputs |
| Member 4 | Frontend dashboard implementation and API data visualization |

### Work Planned for Following Week
- Complete test coverage and regression checks.
- Finalize documentation and demo flow.
- Prepare submission-ready reports and presentation material.

### Major Bottlenecks (If Any)
- Tuning uncertainty ranges for better interpretability.
- Coordinating advanced outputs across multiple endpoint responses.

---

## Week 5 Report
- Week No: 5
- From: ______________
- To: ______________

### Work Carried Out by Team (Bullet Points)
- Completed end-to-end testing and API endpoint validation.
- Added auth/rate-limit behavior checks and standardized error envelope handling.
- Finalized docs: architecture, API contract, dataset schema, experiment log, demo script.
- Ran full pipeline: seed data, train model, execute tests, run API, validate dashboard.
- Prepared final project audit and completion summary artifacts.

### Individual Contribution by Student
| Student | Work Carried Out |
|---|---|
| Member 1 | Test execution, bug fixes, and endpoint stability validation |
| Member 2 | Security controls validation (auth/rate-limit) and error handling review |
| Member 3 | Final documentation and experiment/result consolidation |
| Member 4 | Demo workflow preparation, UI validation, and final packaging |

### Work Planned for Following Week
- Viva preparation and faculty review updates.
- Minor UI/content refinements based on review feedback.

### Major Bottlenecks (If Any)
- Time management for parallel testing + documentation finalization.
- Last-mile formatting and report standardization for submission.

---

## Submission Notes
- Replace placeholder fields (Guide Name, Team Names/USN, From-To dates) before submission.
- Keep weekly points concise in the physical report exactly as per institute format.
- Use this document as the master source for all 5 weekly entries.
