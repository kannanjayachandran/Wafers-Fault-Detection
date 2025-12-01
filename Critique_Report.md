# Technical Audit Report — Wafer Fault Detection System

> Project Status: ARCHIVED
> Codebase: https://github.com/kannanjayachandran/Wafers-Fault-Detection
> Overall Assessment: Fundamentally Unsuitable for Production
> Primary Risk Driver: Dataset does not contain stable or reliable fault signal
> Author: Kannan Jayachandran

## Executive Summary

| Category                |      Score | Severity    | Comment                                             |
| ----------------------- | ---------: | ----------- | --------------------------------------------------- |
| Statistical Methodology | **10/100** | 🔴 Critical | Leakage + metric misuse                             |
| Data Quality & Signal   | **15/100** | 🔴 Critical | Training and test contain different fault semantics |
| Software Engineering    | **50/100** | 🟠 Major    | Monolithic, hard-coded, no testing                  |
| MLOps Practices         | **20/100** | 🔴 Critical | No versioning, no monitoring                        |
| Business Viability      |  **5/100** | 🔴 Critical | Can produce false sense of safety                   |

**Conclusion**: The old system was abandoned due to scientifically invalid results and insufficient signal to support ML automation.

## Root Cause Discovery

Recent deeper analysis on revealed that:

1. The Dataset Does Not Support High-Recall Classification (unrecoverable class overlap, majority of faults are statistically indistinguishable from normal wafers)

**Result**: No model architecture (GBM, SVM, AE) could learn generalizable fault signatures

2. Dataset Possibly Damaged by Anonymization or Process Shift

| Indicator                             | Observation                                  |
| ------------------------------------- | -------------------------------------------- |
| High dimensionality                   | 590+ sensors reduced to ~120 usable           |
| Missing values                        | 75%+ features contain gaps                   |
| Feature drift                         | PCA shows no consistent fault clustering     |
| Train ↔ Test mismatch                 | Good separation in CV, collapse in test      |
| Faults mixed in low-risk score region | AE unable to distinguish faults as anomalies |

**Meaning**: Model failure is not due to modeling mistakes — but missing/erased signal.

3. Research literature on SECOM confirms:
    -  Extreme difficulty → multiple peer-reviewed papers report ROC-AUC ≤ 0.70
    - Even anomaly detection fails to recover masked faults
    - Popular papers online often contain data leakage and metric misuse (even those published in reputed sites)

## Critical Technical Failures in Legacy Codebase

Even if the dataset were better, the system design was not production-safe:

- Metric Mixing — Invalid Model Selection Logic (Comparing accuracy with ROC-AUC across clusters → nonsense math) selecting model that never saw faults to be selected as "best"

- Hard-Label AUC — Random Performance Scores `roc_auc_score()` applied to 0/1 predictions → collapses to ≈0.50 → makes model comparisons random chance

- Clustering Split — Faults Lost in Clusters; K-Means split reduced faults per fold to 0–1, destroying any learning signal

## Overall Impact and Business Risk

If deployed:

| Failure Mode     | Consequence                                    |
| ---------------- | ---------------------------------------------- |
| Fault escapes    | Defective wafers shipped → catastrophic cost   |
| False alarms     | Yield loss → multi-million dollar scrap events |
| Undetected drift | Model silently useless in weeks                |

> **False sense of security** is worse than having no model.

This system increases operational risk rather than reducing it.

## Why the Project Was Terminated

After considerable amount of remediation and scientific validation, I reached a professional conclusion:

- Modeling best practices applied
- Leakage eliminated
- Multi-tier fault architecture attempted
- Anomaly detection evaluated
- Explainability planned
- Underlying data cannot support automated decisioning

Any attempt to continue would lead to misleading performance and unsafe deployment.

## End of Report
