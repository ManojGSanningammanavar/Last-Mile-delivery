from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.ml.features import FEATURE_CATEGORICAL, FEATURE_NUMERIC, build_feature_frame
from src.utils.io import write_csv

try:
    from xgboost import XGBClassifier  # type: ignore
except Exception:  # pragma: no cover
    XGBClassifier = None


def train_model(orders_path: str, area_risk_path: str, model_path: str, preprocessor_path: str, metadata_path: str) -> dict:
    orders_df = pd.read_csv(orders_path)
    area_risk_df = pd.read_csv(area_risk_path)
    features_df = build_feature_frame(orders_df, area_risk_df)

    feature_cols_num = FEATURE_NUMERIC
    feature_cols_cat = FEATURE_CATEGORICAL

    x = features_df[feature_cols_num + feature_cols_cat]
    y = features_df["label_failed"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=42, stratify=y
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), feature_cols_num),
            ("cat", OneHotEncoder(handle_unknown="ignore"), feature_cols_cat),
        ]
    )

    negative = int((y_train == 0).sum())
    positive = int((y_train == 1).sum())
    scale_pos_weight = float(negative / max(positive, 1))

    model_name = "random_forest"
    if XGBClassifier is not None:
        model = XGBClassifier(
            n_estimators=220,
            max_depth=6,
            learning_rate=0.08,
            subsample=0.9,
            colsample_bytree=0.85,
            objective="binary:logistic",
            eval_metric="logloss",
            scale_pos_weight=scale_pos_weight,
            random_state=42,
        )
        model_name = "xgboost"
    else:
        model = RandomForestClassifier(
            n_estimators=300,
            max_depth=14,
            min_samples_leaf=2,
            class_weight="balanced_subsample",
            random_state=42,
        )

    pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
    pipeline.fit(x_train, y_train)

    pred = pipeline.predict(x_test)
    prob = pipeline.predict_proba(x_test)[:, 1]

    metrics = {
        "model_name": model_name,
        "rows": int(len(features_df)),
        "f1": round(float(f1_score(y_test, pred)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, prob)), 4),
        "report": classification_report(y_test, pred),
        "feature_numeric": feature_cols_num,
        "feature_categorical": feature_cols_cat,
        "scale_pos_weight": round(scale_pos_weight, 4),
    }

    feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()
    estimator = pipeline.named_steps["model"]
    if hasattr(estimator, "feature_importances_"):
        importance = estimator.feature_importances_
        ranked = sorted(
            (
                {
                    "feature": str(name),
                    "importance": round(float(score), 6),
                }
                for name, score in zip(feature_names, importance)
            ),
            key=lambda item: item["importance"],
            reverse=True,
        )
        metrics["top_feature_importance"] = ranked[:12]

    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path)
    joblib.dump(preprocessor, preprocessor_path)

    with Path(metadata_path).open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)

    write_csv(features_df, "data/processed/features_train.csv")
    write_csv(features_df, "data/processed/orders_clean.csv")
    return metrics
