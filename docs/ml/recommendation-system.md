# RecoFlow Recommendation System

## 1. Overview

RecoFlow is an event-driven personalized recommendation and ranking platform.

The recommendation system is designed to combine multiple recommendation strategies rather than depending on a single algorithm.

The initial strategies are:

- Popularity-based recommendation
- Content-based recommendation
- Collaborative filtering
- Hybrid recommendation

The system separates:

```text
Candidate Generation
        ↓
Candidate Filtering
        ↓
Ranking
        ↓
Top-K Recommendations