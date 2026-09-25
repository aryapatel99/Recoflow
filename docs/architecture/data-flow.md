# RecoFlow Data Flow

## 1. Overview

RecoFlow contains two primary data flows:

1. Historical machine-learning data flow
2. Live application event flow

These flows eventually contribute to the recommendation system.

---

## 2. Historical Data Flow

```text
Amazon Reviews 2023
        ↓
Raw Dataset
        ↓
Validation
        ↓
Cleaning
        ↓
Filtering
        ↓
Interaction Preparation
        ↓
Feature Engineering
        ↓
ML Training
        ↓
Evaluation
        ↓
Recommendation Models